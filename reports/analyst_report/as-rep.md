---
layout: report
title: "AS-REP - Kerberos Authentication Investigation"
description: "Analyst Write-Up · AS-REP Attack
image: /assets/images/as-rep.png
tags: [DFIR, Windows-Event-Logs, Active-Directory, Kerberos]
weight: 09
---

# AS-REP — Kerberos Authentication Investigation

Analyst Write-Up · LetsDefend Kerberos AS-REP Roasting Timeline

AS-REP Challenge — LetsDefend  
Kerberos AS-REP Roasting · DFIR / Incident Response Report

* * *

## 1) Executive Summary

On **Oct 5, 2024**, suspicious Kerberos authentication activity was identified involving user **Corrado**.
A Kerberos ticket request using **RC4 (0x17)** was observed from an internal host (**192.168.110.129**),
followed by a successful network logon and basic post-access discovery activity (**whoami.exe**).

* * *

## 2) Incident Details

| Field | Description |
|---|---|
| Report Type | Kerberos Authentication / AS-REP Roasting (Lab) |
| Analyst | Brandon Love |
| Date/Time Detected | 2024-10-05 14:42:44 |
| Severity | High |
| Category | Credential Access / Authentication Abuse |
| Detection Source | Windows Security Logs (DC + Workstation) |
| Systems Affected | Domain Controller (Security.evtx), Corrado Workstation Logs |
| Users Involved | Corrado |
| Business Impact | Lab / Training Dataset |

* * *

## 3) Timeline of Events

| Time | Event |
|---|---|
| 2024-10-05 14:42:44 | DC Security log shows Kerberos ticket request (Event ID **4768**) for **Corrado** using **RC4 (0x17)** from **192.168.110.129:49684** |
| 2024-10-05 14:48:58 | Workstation Security log shows successful logon (Event ID **4624**, Logon Type **3**) linked to **192.168.110.129** |
| 2024-10-05 ~15:01:28 | Prefetch indicates **whoami.exe** execution (post-access validation / discovery) |

* * *

## 4) Technical Analysis

### DC Evidence (Security.evtx)

- **Event ID:** 4768 (TGT requested)
- **Time:** 2024-10-05 14:42:44
- **User:** Corrado
- **User SID:** S-1-5-21-3079141193-1468241477-2901848075-1108
- **Ticket Encryption Type:** `0x17 (RC4)`
- **Service:** `krbtgt` (Service SID ends in `-502`)
- **Source:** `192.168.110.129:49684`

### Workstation Evidence (Corrado Security Log)

- **Event ID:** 4624 (Successful logon)
- **Time:** 2024-10-05 14:48:58
- **Logon Type:** `3 (Network)`
- **Source Address:** `192.168.110.129`

### Host Artifact Evidence (Prefetch)

- **Executable:** `whoami.exe`
- **Approx Time:** 2024-10-05 ~15:01:28
- **Meaning:** Quick “validate access” behavior commonly seen after credential abuse.

### MITRE ATT&CK (Reference)

- **T1558.004** — Steal or Forge Kerberos Tickets: AS-REP Roasting  
- **T1078** — Valid Accounts (if credentials were used)  
- **Discovery** — Post-logon validation/discovery behavior

* * *

## 5) Containment & Eradication (Checked = Completed)

- [ ] Isolate suspected source host (192.168.110.129)
- [ ] Reset impacted user credentials (Corrado)
- [ ] Collect additional telemetry (EDR, process execution, network connections)
- [ ] Review for follow-on activity (4769, 4672, 4688, 4648)
- [ ] Validate no persistence mechanisms present

* * *

## 6) Recovery & Verification

- [ ] Confirm host is clean (AV/EDR scan)
- [ ] Restore access after validation
- [ ] Monitor authentication activity for reoccurrence
- [ ] Document lessons learned / update detections

* * *

## 7) Root Cause

> Activity consistent with **AS-REP-roasting-style authentication abuse** in a lab dataset: a Kerberos ticket request associated with legacy/weak encryption indicators (RC4 / 0x17), followed by successful access and basic discovery.

* * *

## 8) Recommendations

- Audit AD accounts that do not require Kerberos pre-authentication and remove unnecessary exceptions.
- Reduce/disable RC4 where feasible and prioritize AES-compatible configuration.
- Strengthen passwords for at-risk accounts (service/privileged) and monitor for abnormal ticket requests.

* * *

## 9) Indicators of Compromise (IOCs)

| Type | Value | Description |
|---|---|---|
| IP | 192.168.110.129 | Source host initiating suspicious Kerberos activity |
| Account | Corrado | Targeted user account |
| Kerberos | Event ID 4768 + TicketEncryptionType 0x17 | Suspicious ticket request with RC4 indicator |
| Host Artifact | whoami.exe | Post-access validation/discovery |

* * *

## 10) Appendices (Evidence)

- DC Security.evtx excerpts (Event ID 4768)
- Workstation Security.evtx excerpts (Event ID 4624)
- Prefetch metadata for `whoami.exe`
- Screenshots from investigation notes (if applicable)
