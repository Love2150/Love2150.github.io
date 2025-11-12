---
layout: page
title: "Windows Log Triage"
permalink: /projects/winlog-triage/
image: /assets/images/wintriage_demo.png
summary: "EVTX + Sysmon → Sigma-like hits, IOCs, and a dark-mode HTML report."
tags: [dfir, windows, sysmon, sigma, evtx]
weight: 8
---

## 🧠 Overview
Fast Windows log triage for analysts. Ingests **EVTX + Sysmon**, extracts **IOCs**, flags **Sigma-like** patterns (PowerShell EncodedCommand, mshta/regsvr32/rundll32/certutil, etc.), and generates a **shareable HTML** report.

## ▶ Live Demo
<p class="meta">
  <a href="{{ '/reports/wintriage/demo_report.html' | relative_url }}" target="_blank" rel="noopener">Open full report ↗</a>
</p>

<iframe
  title="Windows Log Triage demo"
  src="{{ '/reports/wintriage/demo_report.html' | relative_url }}?v={{ site.time | date: '%s' }}"
  width="100%" height="760"
  style="border:1px solid #e2e8f0;border-radius:12px">
</iframe>

## 📈 Sections shown
Top processes/parents · Net by process · Sigma-like hits · Suspicious cmdlines · IOC lists · Sample events
