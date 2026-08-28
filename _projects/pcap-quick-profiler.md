---
layout: project
title: "PCAP Quick Profiler"
permalink: /projects/pcap-quick-profiler/
image: /assets/images/pcap_demo.png
summary: "Windows-friendly PCAP triage: top IPs/ports, HTTP/TLS metadata (SNI/JA3), beacon heuristic, and HTML report."
tags: [dfir, networking, windows, python]
status: "Working demo"
featured: true
last_reviewed: 2026-08-28
role: "Tool developer and analyst"
tools: [Python, PCAP, DNS, HTTP, TLS, JA3, HTML]
outcome: "Publishes an HTML triage report with protocol mix, top IPs and ports, HTTP and TLS metadata, and beacon suspects."
repo: "https://github.com/Love2150/security-tools/tree/main/tools/Pcap-profiler"
demo: "/reports/pcap-profiler/demo_report.html"
weight: 10
description: "Fast PCAP triage with DNS/TLS/HTTP focus, beacon detection, allowlist, and dark-mode HTML output."
---

## Overview
PCAP Quick Profiler turns raw captures into fast, readable triage: protocol mix, top IPs/ports, HTTP/TLS metadata (SNI/JA3), and an experimental beaconing score.

---

## ▶ Live Demo
<p class="meta">
  <a href="{{ '/reports/pcap-profiler/demo_report.html' | relative_url }}" target="_blank" rel="noopener">
    Open full report ↗
  </a>
</p>

{% include pcap-demo-iframe.html %}

---

## What it shows
- Protocol hierarchy & bytes by protocol  
- Top IPs/ports  
- HTTP hosts, URLs, User-Agents, content-types  
- TLS SNI/versions/ciphers/JA3  
- Beacon suspects (score, hits, avg interval)

