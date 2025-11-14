---
layout: page
title: "Windows Log Triage"
permalink: /projects/winlog-triage/
image: /assets/images/wintriage_demo.png
summary: "EVTX + Sysmon → Sigma-like hits, IOCs, and a dark-mode HTML report."
tags: [dfir, windows, sysmon, sigma, evtx]
weight: 8
repo: https://github.com/Love2150/security-tools/tree/main/tools/winlog-triage
---

## Overview
Fast Windows log triage for analysts. Ingests **EVTX + Sysmon**, extracts **IOCs**, flags **Sigma-like patterns** (EncodedCommand, mshta/regsvr32/rundll32/certutil, etc.), and generates a **shareable HTML** report (dark mode) + JSON/CSV artifacts.

<div class="meta" style="margin:.5rem 0 1rem;display:flex;gap:.5rem;flex-wrap:wrap">
  <a class="pill" href="{{ '/reports/wintriage/demo_report.html' | relative_url }}" target="_blank" rel="noopener">Open full report ↗</a>
  <a class="pill" href="{{ page.repo }}" target="_blank" rel="noopener">Repo →</a>
</div>

## Live Demo (embedded)
<iframe
  title="Windows Log Triage demo"
  src="{{ '/reports/wintriage/demo_report.html' | relative_url }}?v={{ site.time | date: '%s' }}"
  width="100%" height="760"
  style="border:1px solid #e2e8f0;border-radius:12px">
</iframe>

## Features
- Normalize **Security**, **Sysmon (EID 1/3/… )**, **PowerShell/Operational**
- **Sigma-like quick hits** with ATT&CK hints
- **IOC extraction:** URLs, domains, IPv4, hashes, emails
- **Network by process** (from Sysmon EID 3)
- **Dark-mode report** + **JSON** + **CSV**

## How to Run (local)
```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt

# Place EVTX under .\samples\
#   Security.evtx
#   Sysmon.evtx
#   PowerShell-Operational.evtx (optional)
python .\wintriage.py .\samples --outdir .\out --max-per-file 5000
start .\out
Quick EVTX export
powershell
Copy code
# Run PowerShell as Administrator
New-Item -ItemType Directory -Path C:\Logs -Force | Out-Null
wevtutil epl Security C:\Logs\Security.evtx /ow:true
wevtutil epl Microsoft-Windows-Sysmon/Operational C:\Logs\Sysmon.evtx /ow:true
wevtutil epl Microsoft-Windows-PowerShell/Operational C:\Logs\PowerShell-Operational.evtx /ow:true

Artifacts Produced
Writes to out/:

wintriage-*.html — shareable report (used in the live demo above)

wintriage-*.json — machine-readable summary

wintriage-*.csv — sample rows (ts/provider/eid/image/cmd)

Roadmap
ATT&CK mini heatmap

Optional pySigma integration

VT/AbuseIPDB enrichment toggles

Case bundle export (HTML + JSON + matched rules)


