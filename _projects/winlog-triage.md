
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
Fast Windows log triage for analysts. Ingests **EVTX + Sysmon**, extracts **IOCs**, flags **Sigma-like patterns** (PowerShell EncodedCommand, mshta/regsvr32/rundll32/certutil, etc.), and generates a **shareable HTML** report (dark-mode) + JSON/CSV artifacts.

<div class="meta" style="margin:.5rem 0 1rem">
  <a class="pill" href="{{ '/reports/wintriage/demo_report.html' | relative_url }}" target="_blank" rel="noopener">Open full report ↗</a>
  {% if page.repo %}<a class="pill" href="{{ page.repo }}" target="_blank" rel="noopener">Repo →</a>{% endif %}
</div>

## ▶ Live Demo (embedded)
<iframe
  title="Windows Log Triage demo"
  src="{{ '/reports/wintriage/demo_report.html' | relative_url }}?v={{ site.time | date: '%s' }}"
  width="100%" height="760"
  style="border:1px solid #e2e8f0;border-radius:12px">
</iframe>

## ✨ Features
- **Normalize Windows logs** (Security, Sysmon, PowerShell/Operational)
- **Sigma-like quick hits** with ATT&CK technique tags
- **IOC extraction**: URLs, domains, IPv4, hashes, emails
- **Network by process** (from Sysmon Event ID 3)
- **Suspicious command lines** (LOLBins, base64 blobs)
- **Dark-mode report** + **JSON** + **CSV**

## 📦 How to Run (local)
```powershell
# Create a venv and install deps
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt

# Put your EVTX files under .\samples\
#   Security.evtx
#   Sysmon.evtx    (export of Microsoft-Windows-Sysmon/Operational)
#   PowerShell-Operational.evtx (optional)
python .\wintriage.py .\samples --outdir .\out --max-per-file 5000

# Open the generated HTML
start .\out

Exporting EVTX quickly
# Run PowerShell as Administrator
New-Item -ItemType Directory -Path C:\Logs -Force | Out-Null
wevtutil epl Security C:\Logs\Security.evtx /ow:true
wevtutil epl Microsoft-Windows-Sysmon/Operational C:\Logs\Sysmon.evtx /ow:true
wevtutil epl Microsoft-Windows-PowerShell/Operational C:\Logs\PowerShell-Operational.evtx /ow:true

🔎 What the Report Shows

Case Summary: events, time range, top providers

Top Processes/Parents with counts

Network by Process: process → ip:port tallies

Sigma-like Rule Hits: rule name, ATT&CK technique, timestamp, cmdline

Suspicious Cmdlines: LOLBins, long base64, download cradles

IOCs: deduped domains, URLs, IPs, hashes, emails

Sample Events: first 25 rows for quick eyeballing

📂 Artifacts Produced

When you run the tool, it writes to out/:

wintriage-*.html — the shareable report (used for the live demo above)

wintriage-*.json — machine-readable summary

wintriage-*.csv — sample rows (ts/provider/eid/image/cmd)

Upload the HTML to your site at:

/reports/wintriage/demo_report.html

🧪 Sample Data & Notes

If you don’t have Sysmon yet, install it on a VM and generate some benign activity (browser, PowerShell usage), then export logs with wevtutil.

Avoid sharing sensitive logs publicly. Sanitize/redact first.

🗺️ Roadmap

ATT&CK mini heatmap

pySigma optional integration with a curated ruleset

Enrichment toggles (VT/AbuseIPDB) via environment variables

Case bundle export (HTML + JSON + matched rules)
> If you want a repo link to show under the overview buttons, add `repo:` to the front matter, e.g.  
> `repo: https://github.com/Love2150/security-tools/tree/main/tools/winlog-triage`

---
