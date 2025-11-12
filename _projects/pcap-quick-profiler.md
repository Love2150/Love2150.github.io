---
layout: page
title: "PCAP Quick Profiler"
image: /assets/images/pcap_demo.png
summary: "Windows-friendly PCAP triage: protocols, top IPs/ports, HTTP/TLS metadata (SNI/JA3), beacon heuristic, and HTML report."
tags: [dfir, networking, windows, python]
repo: "https://github.com/Love2150/security-tools/tree/main/tools/Pcap-profiler"
demo: "/reports/pcap-profiler/demo_report.html"
weight: 10
description: "Fast PCAP triage with DNS/TLS/HTTP focus, beacon detection, allowlist, and dark-mode HTML output."
---

## 🧠 Overview
PCAP Quick Profiler turns raw captures into fast, readable triage…

## ▶ Live Demo
<p class="meta">
  <a href="{{ '/reports/pcap-profiler/demo_report.html' | relative_url }}" target="_blank" rel="noopener">Open full report ↗</a>
</p>

{% include pcap-demo-iframe.html %}

## 📈 What it shows
- Protocol hierarchy & bytes by protocol  
- Top IPs/ports  
- HTTP/TLS metadata (SNI/JA3)  
- Beacon suspects


> **Allowlist:** Place `enrichment/allowlist.json` next to the script to hide known-good SNI/JA3 in results.

---

## 🔗 Links
- **Repo:** <{{ page.repo }}>
- **Raw report:** <{{ page.demo | relative_url }}>
- **Homepage:** <{{ '/' | relative_url }}>


---

## 🔗 Links
- **Repo:** <{{ page.repo }}>
- **Raw report:** <{{ page.demo | relative_url }}>
- **Homepage:** <{{ '/' | relative_url }}>
