---
layout: null
title: "PCAP Quick Profiler"
date: 2025-10-10 09:00:00 -0600
image: "/assets/images/pcap_demo.png"   # <-- new screenshot
summary: "Windows-friendly PCAP triage: protocols, top IPs/ports, HTTP/TLS metadata, and auto reports."
tags: [dfir, networking, windows, python]
repo: "https://github.com/Love2150/security-tools/tree/main/tools/Pcap-profiler"
demo_url: "/reports/pcap-profiler/demo_report.html"   # <-- path to the HTML you copied into the site
weight: 10
---

## 🧠 PCAP Quick Profiler
Automated network traffic triage for `.pcap` / `.pcapng` using Python + PyShark (TShark). Get instant summaries…

<!-- Live demo embed -->
<iframe
  src="{{ page.demo_url | relative_url }}"
  width="100%" height="760"
  style="border:1px solid #e2e8f0;border-radius:12px">
</iframe>

### 🔍 Overview
Built on Wireshark’s TShark…
