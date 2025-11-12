---
layout: page
title: "PCAP Quick Profiler"
permalink: /projects/pcap-quick-profiler/
image: /assets/images/pcap_demo.png
summary: "Windows-friendly PCAP triage: protocols, top IPs/ports, HTTP/TLS metadata (SNI/JA3), beacon heuristic, and HTML report."
tags: [dfir, networking, windows, python]
repo: "https://github.com/Love2150/security-tools/tree/main/tools/Pcap-profiler"
demo: "/reports/pcap-profiler/demo_report.html"
weight: 10
description: "Fast PCAP triage with DNS/TLS/HTTP focus, beacon detection, allowlist, and dark-mode HTML output."
---

## 🧠 Overview
PCAP Quick Profiler turns raw captures into fast, readable triage: protocol mix, top IPs/ports, HTTP/TLS metadata (SNI/JA3), and an experimental beaconing score. Exports JSON/CSV/HTML (dark-mode), with an allowlist to suppress known-benign SNI/JA3.

- **Tech:** Python, PyShark (TShark), asyncio  
- **Focus:** DNS/TLS/HTTP for speed & signal  
- **Extras:** Allowlist, beacon heuristic, HTML report

---

## ▶ Live Demo
<p class="meta">
  <a href="{{ '/reports/pcap-profiler/demo_report.html' | relative_url }}" target="_blank" rel="noopener">Open full report ↗</a>
</p>

<iframe
  title="PCAP demo report"
  src="{{ '/reports/pcap-profiler/demo_report.html' | relative_url }}?v={{ site.time | date: '%s' }}"
  width="100%"
  height="760"
  style="border:1px solid #e2e8f0;border-radius:12px">
</iframe>

---

## 📈 What it shows
- Protocol hierarchy & bytes by protocol  
- Top source/destination IPs and destination ports  
- HTTP hosts, URLs, User-Agents, content-types  
- TLS SNI, versions, ciphers, and JA3 hashes  
- Beacon suspects (score, hits, average interval)

> **Allowlist:** Place `enrichment/allowlist.json` next to the script to hide known-good SNI/JA3 in results.

---

## 🔗 Links
- **Repo:** <{{ page.repo }}>
- **Raw report:** <{{ page.demo | relative_url }}>
- **Homepage:** <{{ '/' | relative_url }}>
