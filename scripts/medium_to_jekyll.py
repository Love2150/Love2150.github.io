#!/usr/bin/env python3
"""
Medium RSS -> Jekyll Markdown importer
- Fetches your Medium RSS feed
- Converts items to Markdown with front matter
- Saves new posts under _posts/YYYY-MM-DD-slug.md (idempotent)
Usage:
  python scripts/medium_to_jekyll.py --feed FEED_URL --out _posts --author "Your Name"
"""
import argparse
import calendar
import hashlib
import json
import os
import re
import sys
from datetime import datetime, timezone
from pathlib import Path

import feedparser
import pytz
import requests
from bs4 import BeautifulSoup
from markdownify import markdownify as md
from slugify import slugify


def fetch(url: str) -> str:
    # Medium sometimes blocks default bots; use browsery headers.
    headers = {
        "User-Agent": ("Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                       "AppleWebKit/537.36 (KHTML, like Gecko) "
                       "Chrome/120.0.0.0 Safari/537.36"),
        "Accept": "application/rss+xml, application/xml;q=0.9, */*;q=0.8",
        "Accept-Language": "en-US,en;q=0.9",
        "Connection": "close",
    }
    r = requests.get(url, headers=headers, timeout=30)
    r.raise_for_status()
    return r.text

def to_md(html: str, fallback_alt: str = "Article evidence image") -> str:
    soup = BeautifulSoup(html or "", "html.parser")
    for image in list(soup.find_all("img")):
        source = image.get("src", "")
        if "medium.com/_/stat" in source.lower():
            image.decompose()
            continue
        if image.get("alt", "").strip():
            continue
        figure = image.find_parent("figure")
        caption = figure.find("figcaption") if figure else None
        if not caption and figure:
            candidate = figure.find_next_sibling()
            candidate_text = candidate.get_text(" ", strip=True) if candidate else ""
            if candidate_text.lower().startswith("caption:"):
                caption = candidate
        image["alt"] = caption.get_text(" ", strip=True).removeprefix("Caption:").strip(" “\"") if caption else fallback_alt
    return md(str(soup), heading_style="ATX", strip=['span'])

def first_sentence(text: str) -> str:
    text = re.sub(r"\s+", " ", text).strip()
    match = re.match(r"^(.{40,200}?[.!?])(?:\s|$)", text)
    if match:
        return match.group(1)
    if len(text) <= 200:
        return text
    shortened = text[:197].rsplit(" ", 1)[0]
    return f"{shortened}..."


def summary_from_markdown(markdown: str) -> str:
    for block in re.split(r"\n\s*\n", markdown):
        candidate = re.sub(r"\s+", " ", block).strip()
        if not candidate or candidate.startswith(("#", "!", ">", "```")):
            continue
        candidate = re.sub(r"\[([^\]]+)\]\([^)]+\)", r"\1", candidate)
        candidate = re.sub(r"[*_`]", "", candidate)
        if len(candidate) >= 40:
            return first_sentence(candidate)
    return first_sentence(re.sub(r"[#*_`]", "", markdown))


def yq(s: str) -> str:
    """Serialize a string as a YAML-compatible JSON scalar."""
    return json.dumps(s or "", ensure_ascii=False)

def write_post(out_dir: str, author: str, entry) -> str | None:
    title = (entry.get('title') or 'Untitled').strip()

    # Feedparser exposes UTC struct_time values.
    dt = None
    for key in ('published_parsed', 'updated_parsed'):
        if entry.get(key):
            timestamp = calendar.timegm(entry.get(key))
            dt = datetime.fromtimestamp(timestamp, tz=timezone.utc)
            break
    if dt is None:
        dt = datetime.now(timezone.utc)

    tz = pytz.timezone('America/Chicago')
    dt_local = dt.astimezone(tz)
    date_str = dt_local.strftime('%Y-%m-%d')

    canonical = (entry.get('link') or '').strip()
    slug = slugify(title) or f"post-{int(dt.timestamp())}"
    filename = f"{date_str}-{slug}.md"
    path = os.path.join(out_dir, filename)
    if os.path.exists(path):
        existing = Path(path).read_text(encoding="utf-8")
        if not canonical or f"medium_canonical: {yq(canonical)}" in existing:
            return None
        suffix = hashlib.sha256(canonical.encode("utf-8")).hexdigest()[:10]
        path = os.path.join(out_dir, f"{date_str}-{slug}-{suffix}.md")
        if os.path.exists(path):
            existing = Path(path).read_text(encoding="utf-8")
            if f"medium_canonical: {yq(canonical)}" in existing:
                return None
            raise RuntimeError(f"Post filename collision: {path}")

    # Content HTML
    if entry.get('content'):
        content_html = entry.content[0].get('value', '')
    else:
        content_html = entry.get('summary', '') or entry.get('description', '')

    body_md = to_md(content_html, f"{title} evidence image").strip()

    tags = []
    for tag in (entry.get('tags') or []):
        term = tag.get('term')
        if term:
            tags.append(str(term).strip())

    excerpt = summary_from_markdown(body_md)

    fm = [
        '---',
        'layout: post',
        f'title: {yq(title)}',
        f'date: {dt_local.strftime("%Y-%m-%d %H:%M:%S %z")}',
        f'author: {yq(author)}',
        f'summary: {yq(excerpt)}',
        f'medium_canonical: {yq(canonical)}',
        f'canonical_url: {yq(canonical)}',
    ]
    if tags:
        fm_tags = ", ".join(yq(tag) for tag in tags)
        fm.append(f'tags: [{fm_tags}]')
    fm.append('---\n')

    content = (
        "\n".join(fm)
        + (f"> Originally published on Medium: {canonical}\n\n" if canonical else "")
        + excerpt + "\n\n<!--more-->\n\n"
        + body_md + "\n"
    )

    os.makedirs(out_dir, exist_ok=True)
    with open(path, 'w', encoding='utf-8') as f:
        f.write(content)
    return path

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--feed', required=True)
    ap.add_argument('--out', default='_posts')
    ap.add_argument('--author', default='Author')
    args = ap.parse_args()

    xml = fetch(args.feed)
    feed = feedparser.parse(xml)
    print(f"Feed title: {feed.feed.get('title','n/a')}")
    print(f"Entries found: {len(feed.entries)}")

    if not feed.entries:
        print('No entries in feed — check the URL or visibility.', file=sys.stderr)
        sys.exit(0)

    created = 0
    os.makedirs(args.out, exist_ok=True)
    for e in feed.entries:
        p = write_post(args.out, args.author, e)
        if p:
            created += 1
    print(f"Processed {len(feed.entries)} entries. Created {created} new post(s).")

if __name__ == '__main__':
    main()
