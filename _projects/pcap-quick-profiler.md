---
layout: page
title: PCAP Quick Profiler
permalink: /projects/pcap-quick-profiler/
image: /assets/images/pcap_demo.png
description: "Windows-friendly PCAP triage with DNS/TLS/HTTP focus, beacon detection, and a dark-mode HTML report."
---

## 🧠 Overview
PCAP Quick Profiler turns raw captures into fast, readable triage: protocols, top IPs/ports, HTTP/TLS metadata (SNI/JA3), and an experimental beaconing score. Exports JSON/CSV/HTML (with dark-mode).

- **Tech:** Python, PyShark (TShark), asyncio  
- **Focus:** DNS/TLS/HTTP for speed and signal  
- **Bonus:** Allowlist to suppress known-benign SNI/JA3

## ▶ Live Demo
<p class="meta"><a href="{{ '/reports/pcap-profiler/demo_report.html' | relative_url }}">Open full report ↗</a></p>

<iframe
  src="{{ '/reports/pcap-profiler/demo_report.html' | relative_url }}"
  width="100%" height="760"
  style="border:1px solid #e2e8f0;border-radius:12px">
</iframe>

