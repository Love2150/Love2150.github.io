#!/usr/bin/env python3
"""
Medium RSS -> Jekyll Markdown importer
- Fetches your Medium RSS feed
- Converts items to Markdown with front matter
- Saves new posts under _posts/YYYY-MM-DD-slug.md (idempotent)
Usage:
  python scripts/medium_to_jekyll.py --feed FEED_URL --out _posts --author "Your Name"
"""
import argparse, os, re, sys, time
from datetime import datetime
import feedparser
import requests
from markdownify import markdownify as md
from slugify import slugify
import pytz

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

def to_md(html: str) -> str:
    return md(html or "", heading_style="ATX", strip=['span'])

def first_sentence(text: str) -> str:
    text = re.sub(r"\s+", " ", text).strip()
    m = re.search(r"(.{40,200}?\.)\s", text)
    return m.group(1) if m else text[:200]

def yq(s: str) -> str:
    """Escape double quotes for YAML double-quoted strings."""
    return (s or "").replace('"', r'\"')

def write_post(out_dir: str, author: str, entry) -> str:
    title = (entry.get('title') or 'Untitled').strip()

    # Date (prefer published -> updated -> now)
    dt = None
    for key in ('published_parsed', 'updated_parsed'):
        if entry.get(key):
            dt = datetime.fromtimestamp(time.mktime(entry.get(key)))
            break
    if dt is None:
        dt = datetime.utcnow()

    tz = pytz.timezone('America/Chicago')
    dt_local = tz.localize(dt.replace(tzinfo=None)) if dt.tzinfo is None else dt.astimezone(tz)
    date_str = dt_local.strftime('%Y-%m-%d')

    slug = slugify(title) or f"post-{int(dt.timestamp())}"
    filename = f"{date_str}-{slug}.md"
    path = os.path.join(out_dir, filename)
    if os.path.exists(path):
        return path

    # Content HTML
    if entry.get('content'):
        content_html = entry.content[0].get('value', '')
    else:
        content_html = entry.get('summary', '') or entry.get('description', '')

    body_md = to_md(content_html).strip()

    tags = []
    for tag in (entry.get('tags') or []):
        term = tag.get('term')
        if term:
            tags.append(str(term).strip())

    canonical = (entry.get('link') or '').strip()
    excerpt = first_sentence(re.sub(r"\n+", " ", body_md))

    esc_title = yq(title)
    esc_author = yq(author)
    esc_canonical = yq(canonical)
    fm = [
        '---',
        'layout: post',
        f'title: "{esc_title}"',
        f'date: {dt_local.strftime("%Y-%m-%d %H:%M:%S %z")}',
        f'author: "{esc_author}"',
        f'medium_canonical: "{esc_canonical}"',
    ]
    if tags:
        fm_tags = ", ".join([f'"{yq(t)}"' for t in tags])
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
    print(f"Processed {len(feed.entries)} entries. New files may be under {args.out}.")

if __name__ == '__main__':
    main()
