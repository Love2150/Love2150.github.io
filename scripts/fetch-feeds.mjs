// scripts/fetch-feeds.mjs
import fs from "node:fs/promises";
import path from "node:path";
import Parser from "rss-parser";

const FEEDS = [
  "https://isc.sans.edu/rssfeed.xml",
  "https://www.ncsc.gov.uk/api/1/services/v1/all-rss-feed.xml",
  "https://krebsonsecurity.com/feed/"
  // You can add more; keep it focused/high-signal
];

const KEYWORDS = [
  "best practice","guidance","how to","mitigation",
  "hardening","secure","detection","playbook","tip","recommendation"
];

const MAX_ITEMS = 50;   // limit for JSON size on the site
const OUTFILE = path.join("assets", "tips.json");

const tidy = (s="") => s.replace(/<[^>]+>/g,"").replace(/\s+/g," ").trim();

const parser = new Parser({
  timeout: 8000, // ms per feed
  headers: { "user-agent": "Love2150-TipsBot/1.0" }
});

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
    if (key && !seen.has(key)) {
      seen.add(key);
      unique.push(it);
    }
  }
  unique.sort((a, b) => new Date(b.date) - new Date(a.date));
  return unique.slice(0, MAX_ITEMS);
}

async function main() {
  const all = [];
  for (const url of FEEDS) {
    try {
      const feed = await parser.parseURL(url);
      const title = tidy(feed.title || new URL(url).hostname);
      const shaped = filterAndShape(title, feed.items);
      all.push(...shaped);
    } catch (e) {
      console.error("Feed error:", url, e.message);
    }
  }

  // fallback: if keyword filter too strict, keep latest from all feeds
  let items = dedupeSort(all);
  if (items.length === 0) {
    console.warn("Keyword filter yielded 0; falling back to latest entries from all feeds.");
    const fallbackAll = [];
    for (const url of FEEDS) {
      try {
        const feed = await parser.parseURL(url);
        const title = tidy(feed.title || new URL(url).hostname);
        fallbackAll.push(...(feed.items || []).map(it => ({
          title: tidy(it.title || ""),
          summary: tidy(it.contentSnippet || it.content || it["content:encoded"] || it.summary || ""),
          link: (it.link || "").trim(),
          date: new Date(it.isoDate || it.pubDate || Date.now()).toISOString(),
          source: title
        })));
      } catch {}
    }
    items = dedupeSort(fallbackAll);
  }

  const payload = {
    updated_at: new Date().toISOString(),
    items
  };

  await fs.mkdir(path.dirname(OUTFILE), { recursive: true });
  await fs.writeFile(OUTFILE, JSON.stringify(payload, null, 2), "utf8");
  console.log(`Wrote ${items.length} tips -> ${OUTFILE}`);
}

main().catch(err => {
  console.error(err);
  process.exit(1);
});
