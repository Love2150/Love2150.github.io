
```markdown
# 🚀 Brandon Love — Cybersecurity Portfolio & Blog

[![Built with Jekyll](https://img.shields.io/badge/Built%20with-Jekyll-blueviolet?logo=jekyll&logoColor=white)](https://jekyllrb.com/)
[![Deployed on GitHub Pages](https://img.shields.io/badge/Deployed%20on-GitHub%20Pages-181717?logo=github&logoColor=white)](https://pages.github.com/)
[![Made with HTML, CSS, JS](https://img.shields.io/badge/Frontend-HTML%20%7C%20CSS%20%7C%20JS-orange?logo=html5)](#)
[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)

A responsive, **cybersecurity portfolio and technical blog** built with **Jekyll** and deployed on **GitHub Pages**.  
Designed to highlight my **DFIR projects, blue-team case studies, and detection engineering write-ups** — all with interactive sliders, markdown posts, and modern dark mode styling.

🔗 **Live Site:** [https://love2150.github.io](https://love2150.github.io)

---

## 🧠 Overview

This portfolio serves as both a **personal brand hub** and a **cybersecurity learning showcase**, integrating blog posts, projects, and automation workflows under a clean, lightweight design.

---

## ⚙️ Features

### 🔹 Core Sections
- **Hero:** A short intro and CTAs to explore Projects and Blog.
- **Portfolio Highlights:** DFIR and detection engineering studies.
- **Projects Slider:** Interactive auto-sliding carousel (touch + keyboard-friendly).
- **Latest Blogs:** Displays 3 newest posts from `_posts/` (Markdown-based).
- **Contact:** Professional links and location.

### 🔹 Technical Highlights
- 🎡 Dual sliders (Projects + Blog) with autoplay, touch, and reduced-motion support.
- ⚡ Jekyll-powered with custom `_projects` and `_posts` collections.
- 🔄 Optional Medium RSS → Markdown sync via GitHub Actions.
- 📱 Responsive sticky header with mobile drawer.
- 🔒 Accessible UI with semantic HTML and ARIA roles.

---

## 🗂️ Folder Structure


├── _layouts/
│   └── post.html             # Blog post layout
├── _posts/                   # Markdown blog posts (YYYY-MM-DD-title.md)
├── _projects/                # Project metadata and case studies
├── archive/
│   └── index.html            # Blog archive page
├── scripts/
│   └── medium_to_jekyll.py   # Medium RSS to Markdown converter
├── index.html                # Homepage (portfolio + sliders)
├── medium.html               # Optional Medium feed page
├── _config.yml               # Jekyll config file
└── README.md                 # (this file)


---

## 🧰 Tech Stack

| Component        | Description                                      |
|------------------|--------------------------------------------------|
| **Static Site**  | Jekyll (GitHub Pages native)                    |
| **Language**     | HTML, CSS, JavaScript (Vanilla)                 |
| **Hosting**      | GitHub Pages                                    |
| **Automation**   | GitHub Actions (Medium sync)                    |
| **Versioning**   | Git / GitHub                                    |
| **Design**       | Fluid layout, dark mode, modern typography       |

---

## 🚀 Deployment

### 🖥️ Local Preview
Install Jekyll to test locally:
```bash
gem install bundler jekyll
jekyll serve
````

Then visit: [http://localhost:4000](http://localhost:4000)

### 🌐 GitHub Pages Deployment

1. Push changes to the `main` branch.
2. In **Settings → Pages**, set:

   ```
   Build and Deployment → Source → GitHub Actions (or Main / Root)
   ```
3. GitHub will auto-build and publish to:
   ➜ [https://love2150.github.io](https://love2150.github.io)

---

## 🧩 Adding Content

### ✏️ New Blog Post

Create a file in `_posts/` using:

```
YYYY-MM-DD-title.md
```

Example:

```markdown
---
layout: post
title: "SOC235 — Atlassian Confluence CVE-2023-22515 (LetsDefend)"
tags: [letsdefend, blue-team, cybersecurity]
---
Today, I analyzed an Atlassian Confluence exploitation attempt using PCAP evidence...
```

### 🛠️ New Project

Create a file in `_projects/`:

```markdown
---
title: "PowerShell Deobfuscator"
image: /assets/images/projects/powershell-deobfuscator.jpg
tags: [PowerShell, DFIR, Windows]
summary: "Tool to decode Base64 and Unicode-escaped PowerShell payloads."
repo: "https://github.com/Love2150/powershell-deobfuscator"
demo: "https://love2150.github.io/#featured-projects"
weight: 2
---
```

---

## 🎨 Customization

### Site Info

Edit `_config.yml`:

```yaml
title: "Brandon Love — Portfolio"
url: "https://love2150.github.io"
timezone: America/Chicago
```

### Contact Info

Inside `index.html`:

```html
<li>Email: <a href="mailto:brandonlove2150@icloud.com">brandonlove2150@icloud.com</a></li>
<li>GitHub: <a href="https://github.com/Love2150">github.com/Love2150</a></li>
<li>Location: Killeen, TX</li>
```

### Adjust Slider Speed

In the bottom `<script>`:

```js
interval: 5000 // time in ms
```

---

## 🧑‍💻 Author

**Brandon Love**
Cybersecurity Analyst · DFIR Enthusiast · U.S. Army Veteran

[![LinkedIn](https://img.shields.io/badge/LinkedIn-Connect-blue?logo=linkedin)](https://www.linkedin.com/in/brandon-love-85b247261/)
[![GitHub](https://img.shields.io/badge/GitHub-Love2150-181717?logo=github)](https://github.com/Love2150)
[![Medium](https://img.shields.io/badge/Medium-@brandonlove2150-black?logo=medium)](https://medium.com/@brandonlove2150)
[![LetsDefend](https://img.shields.io/badge/LetsDefend-shinyhunter-2a9d8f)](https://app.letsdefend.io/user/shinyhunter)

---

## 📜 License

MIT License © 2025 Brandon Love
You are free to use, copy, and modify this project — attribution appreciated.

---

## 🌟 Acknowledgments

* [GitHub Pages](https://pages.github.com/) — effortless hosting
* [Jekyll](https://jekyllrb.com/) — the static engine behind the site
* [MediumWidget](https://medium-widget.pixelpoint.io/) — optional integration for live feeds
* Inspiration from security blogs, DFIR labs, and fellow defenders

---

> *“Security isn’t just defense — it’s clarity, curiosity, and continuous learning.”* 🛡️
