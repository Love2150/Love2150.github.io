Below are two files to add to your repo to automatically import ALL Medium posts into `_posts/` and show the newest three on the homepage.

---

## 1) `.github/workflows/medium-sync.yml`

```yaml
name: Medium → Jekyll sync

on:
  workflow_dispatch:
  schedule:
    - cron: '17 */6 * * *'  # every 6 hours at :17

permissions:
  contents: write  # allow committing back to the repo

jobs:
  sync:
    runs-on: ubuntu-latest
    steps:
      - name: Checkout
        uses: actions/checkout@v4
        with:
          fetch-depth: 0

      - name: Set up Python
        uses: actions/setup-python@v5
        with:
          python-version: '3.x'

      - name: Install deps
        run: |
          python -m pip install --upgrade pip
          pip install feedparser markdownify python-slugify requests pytz

      - name: Run importer
        run: |
          python scripts/medium_to_jekyll.py \
            --feed "https://medium.com/feed/@brandonlove2150" \
            --out "_posts" \
            --author "Brandon Love"

      - name: Commit & push if changed
        run: |
          git config user.name "github-actions[bot]"
          git config user.email "41898282+github-actions[bot]@users.noreply.github.com"
          git add _posts
          git commit -m "chore: sync Medium posts" || echo "No changes to commit"
          git push
```

---

## 2) `scripts/medium_to_jekyll.py`

```python
#!/usr/bin/env python3
"""
Medium RSS → Jekyll Markdown importer
- Fetches your Medium RSS feed
- Converts items to Markdown with front matter
- Saves new posts under _posts/YYYY-MM-DD-slug.md (idempotent)

Usage:
  python scripts/medium_to_jekyll.py --feed FEED_URL --out _posts --author "Your Name"
"""
import argparse
import os
import re
import sys
import time
from datetime import datetime

import feedparser  # RSS/Atom parser
import requests
from markdownify import markdownify as md
from slugify import slugify
import pytz

def fetch(url: str) -> str:
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
    # Convert HTML → Markdown; keep code blocks and images reasonably intact
    return md(html or "", heading_style="ATX", strip=['span'])

def first_sentence(text: str) -> str:
    text = re.sub(r"\s+", " ", text).strip()
    m = re.search(r"(.{40,200}?\.)\s", text)
    return m.group(1) if m else text[:200]

def write_post(out_dir: str, author: str, entry) -> str:
    # Title
    title = entry.get('title', 'Untitled').strip()

    # Date
    # Prefer published date; fall back to updated or now
    dt = None
    for key in ('published_parsed', 'updated_parsed'):
        if getattr(entry, key, None):
            dt = datetime.fromtimestamp(time.mktime(getattr(entry, key)))
            break
    if dt is None:
        dt = datetime.utcnow()
    # Normalize to America/Chicago for deterministic file names
    tz = pytz.timezone('America/Chicago')
    dt_local = tz.localize(dt.replace(tzinfo=None)) if dt.tzinfo is None else dt.astimezone(tz)

    date_str = dt_local.strftime('%Y-%m-%d')

    # Slug
    slug = slugify(title) or f"post-{int(dt.timestamp())}"

    # Filename
    filename = f"{date_str}-{slug}.md"
    path = os.path.join(out_dir, filename)

    if os.path.exists(path):
        return path  # already imported

    # Content HTML
    content_html = ''
    # Medium feeds may expose content via 'content', 'summary', or 'description'
    if 'content' in entry and entry.content:
        content_html = entry.content[0].get('value', '')
    else:
        content_html = entry.get('summary', '') or entry.get('description', '')

    # Convert to Markdown
    body_md = to_md(content_html).strip()

    # Categories/Tags
    tags = []
    for tag in entry.get('tags', []) or []:
        term = tag.get('term')
        if term:
            tags.append(str(term).strip())

    # Canonical link
    canonical = entry.get('link', '').strip()

    # Excerpt
    excerpt = first_sentence(re.sub(r"\n+", " ", body_md))

    # Front matter
    front_matter = [
        '---',
        'layout: post',
        f'title: "{title.replace("\"", "\\\"")}"',
        f'date: {dt_local.strftime("%Y-%m-%d %H:%M:%S %z")}',
        f'author: "{author}"',
        f'medium_canonical: "{canonical}"',
    ]
    if tags:
        fm_tags = ", ".join([f'"{t.replace("\"", "\\\"")}"' for t in tags])
        front_matter.append(f'tags: [{fm_tags}]')
    front_matter.append('---\n')

    # Compose file
    # Add a canonical notice and a read‑more marker after the intro
    content = (
        "\n".join(front_matter)
        + f"> Originally published on Medium: {canonical}\n\n"
        + excerpt + "\n\n<!--more-->\n\n"
        + body_md
        + "\n"
    )

    os.makedirs(out_dir, exist_ok=True)
    with open(path, 'w', encoding='utf-8') as f:
        f.write(content)
    return path


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--feed', required=True, help='Medium RSS/Atom feed URL (e.g., https://medium.com/feed/@username)')
    ap.add_argument('--out', default='_posts', help='Output folder for Jekyll posts')
    ap.add_argument('--author', default='Author', help='Default author name')
    args = ap.parse_args()

    xml = fetch(args.feed)
    feed = feedparser.parse(xml)

    if not feed.entries:
        print('No entries in feed — check the URL or visibility.', file=sys.stderr)
        sys.exit(0)

    created = 0
    for e in feed.entries:
        p = write_post(args.out, args.author, e)
        if p:
            created += 1
    print(f"Processed {len(feed.entries)} entries. New/updated files may be created under {args.out}.")

if __name__ == '__main__':
    main()
```

---

### How this works

* The workflow runs every 6 hours (and on manual dispatch), fetches your Medium RSS, converts posts to Markdown, and commits any new ones into `_posts/`.
* Your homepage still shows the latest 3 Medium posts via the widget; the **imported Markdown posts** will appear in your Jekyll Blog section and Archive page.

### Setup steps

1. Create folders and files:

   * `.github/workflows/medium-sync.yml`
   * `scripts/medium_to_jekyll.py` (make sure the `scripts/` folder exists)
2. Commit & push to `main`.
3. Go to **Actions** tab → run **“Medium → Jekyll sync”** with **Run workflow** (first-run priming).
4. Confirm new files appear in `_posts/`.

> No secrets needed — it uses the built-in `GITHUB_TOKEN` to commit.

### Optional tweaks

* Change the schedule: edit the `cron` line.
* Add categories per post: extend the script to map Medium tags to `categories:` too.
* Keep only the 3 newest in `_posts/`: we can add a retention rule if you prefer.
