// scripts/fetch-feeds.mjs (hardened)
import fs from "node:fs/promises";
import path from "node:path";
import { createRequire } from "node:module";
const require = createRequire(import.meta.url);

async function getRssParser() {
  // Try CJS require first (most reliable on Actions), then ESM dynamic import
  try {
    const Parser = require("rss-parser");
    return Parser?.default ? Parser.default : Parser;
  } catch (e1) {
    try {
      const mod = await import("rss-parser");
      return mod.default ?? mod;
    } catch (e2) {
      console.error("Failed to load rss-parser via CJS and ESM.");
      console.error("CJS error:", e1?.message);
      console.error("ESM error:", e2?.message);
      return null;
    }
  }
}

const FEEDS = [
  "https://isc.sans.edu/rssfeed.xml",
  "https://www.ncsc.gov.uk/api/1/services/v1/all-rss-feed.xml",
  "https://krebsonsecurity.com/feed/"
];

const KEYWORDS = [
  "best practice","guidance","how to","mitigation",
  "hardening","secure","detection","playbook","tip","recommendation"
];

const MAX_ITEMS   = 50;
const PER_FEED_TO = 8000; // ms
const OUTFILE     = path.join("assets", "tips.json");

const tidy = (s="") => s.replace(/<[^>]+>/g,"").replace(/\s+/g," ").trim();

function filterAndShape(feedTitle, items) {
  return (items || []).map(it => {
    const title = tidy(it.title || "");
    const summary = tidy(it.contentSnippet || it.content || it["content:encoded"] || it.summary || "");
    const link = (it.link || "").trim();
    const date = new Date(it.isoDate || it.pubDate || Date.now());
    return { title, summary, link, date: date.toISOString(), source: feedTitle };
  }).filter(it => {
    const hay = (it.title + " " + it.summary).toLowerCase();
    return KEYWORDS.some(k => hay.includes(k));
  });
}

function dedupeSort(items) {
  const seen = new Set();
  const unique = [];
  for (const it of items) {
    const key = it.link || it.title;
    if (!key || seen.has(key)) continue;
    seen.add(key);
    unique.push(it);
  }
  unique.sort((a, b) => new Date(b.date) - new Date(a.date));
  return unique.slice(0, MAX_ITEMS);
}

async function parseWithTimeout(parser, url) {
  const ctrl = new AbortController();
  const tm = setTimeout(() => ctrl.abort(), PER_FEED_TO);
  try {
    // rss-parser doesn’t accept AbortController; this is a soft timeout guard.
    // If it hangs, we’ll continue after PER_FEED_TO.
    const res = await Promise.race([
      parser.parseURL(url),
      new Promise((_, rej) => setTimeout(() => rej(new Error("timeout")), PER_FEED_TO + 200))
    ]);
    return res;
  } finally {
    clearTimeout(tm);
  }
}

async function main() {
  const Parser = await getRssParser();
  const all = [];

  if (!Parser) {
    console.warn("rss-parser unavailable; writing fallback tips.json.");
  } else {
    const parser = new Parser({ headers: { "user-agent": "Love2150-TipsBot/1.0" } });

    for (const url of FEEDS) {
      try {
        const feed = await parseWithTimeout(parser, url);
        const title = tidy(feed?.title || new URL(url).hostname);
        const shaped = filterAndShape(title, feed?.items || []);
        all.push(...shaped);
      } catch (e) {
        console.error("Feed error:", url, e?.message || e);
      }
    }
  }

  let items = dedupeSort(all);

  // Fallback if filtering produced nothing
  if (items.length === 0) {
    items = [{
      title: "Enable MFA and auto-updates on all critical accounts",
      summary: "For email, GitHub, cloud consoles, password managers, and banking—use multi-factor authentication and keep automatic updates on to block common attacks.",
      link: "https://www.cisa.gov/secure-our-world",
      date: new Date().toISOString(),
      source: "Baseline Tip"
    }];
  }

  const payload = { updated_at: new Date().toISOString(), items };

  await fs.mkdir(path.dirname(OUTFILE), { recursive: true });
  await fs.writeFile(OUTFILE, JSON.stringify(payload, null, 2), "utf8");
  console.log(`Wrote ${items.length} tips -> ${OUTFILE}`);

  // Always exit successfully so Actions doesn’t fail the job
  process.exitCode = 0;
}

main().catch(err => {
  console.error("Unexpected error:", err);
  // Even if something catastrophic happens, write a minimal JSON so the site keeps working
  const payload = {
    updated_at: new Date().toISOString(),
    items: [{
      title: "Use a password manager with MFA",
      summary: "Strong, unique passwords + MFA stop the majority of account takeovers.",
      link: "https://www.cisa.gov/secure-our-world",
      date: new Date().toISOString(),
      source: "Baseline Tip"
    }]
  };
  fs.mkdir(path.dirname(OUTFILE), { recursive: true })
    .then(() => fs.writeFile(OUTFILE, JSON.stringify(payload, null, 2), "utf8"))
    .then(() => { process.exitCode = 0; })
    .catch(() => { process.exitCode = 0; });
});
