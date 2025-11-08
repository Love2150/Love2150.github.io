---
layout: null
title: "Personal Portfolio & Blog (Jekyll + GitHub Pages)"
date: 2025-11-07 10:00:00 -0600
image: /assets/images/Homepage-Overlay.png   # ← add an image to this path
tags: [Jekyll, GitHub Pages, CI/CD, JavaScript, HTML/CSS]
summary: "Responsive portfolio with a Jekyll-powered blog, Medium-to-Markdown autosync, and custom blog/projects sliders."
repo: "https://github.com/Love2150/Love2150.github.io"   # ← your repo URL
demo: "https://love2150.github.io/"                      # ← live site
weight: 1                                               # ← lower = more featured in slider
---

### What I built
A fast, responsive portfolio with:
- **Jekyll** static blog (`_posts/`) and an **auto-import** from Medium via GitHub Actions.
- **Featured sliders** for the newest blog posts and projects (with touch/keyboard + autoplay).
- **Accessible, mobile-first** design with a sticky header and drawer navigation.

### Tech stack
- **Jekyll 3** on **GitHub Pages** (no custom build server)
- **GitHub Actions** to pull Medium RSS → Markdown in `_posts/`
- **Vanilla JS** for the sliders (no deps)
- **Semantic HTML + CSS** with dark/light friendly colors

### Key workflows
- `/.github/workflows/medium-sync.yml` fetches `https://medium.com/feed/@brandonlove2150`,
  converts to Markdown with front-matter, and commits to `_posts/`.

### Highlights
- Clean, zero-dependency sliders (touch, keyboard, and reduced-motion aware).
- Structured collections: `_projects/` with `weight`, `summary`, and `image` front-matter.
- Archive pages: `/projects/` and `/archive/`.

### Next steps
- Add tag filters and search to `/projects/`.
- Add Lighthouse CI in Actions for perf budgets.
