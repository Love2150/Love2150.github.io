```md
---
title: "AS-REP Roasting Investigation Report (LetsDefend)"
layout: post
categories: [SOC, Incident-Response, Active-Directory]
tags: [Kerberos, AS-REP, Windows-Event-Logs, Blue-Team, LetsDefend]
---

## Incident Report — AS-REP Roasting (Lab Write-Up)

> **Note:** This report is based on a controlled lab dataset from LetsDefend and is intended for educational/portfolio purposes.

---

## Case Summary

- **Incident Type:** Kerberos AS-REP Roasting / Credential Access  
- **Severity:** High (credential theft can lead to domain compromise)  
- **Primary Finding:** A Kerberos ticket request associated with user **Corrado** used **RC4 encryption (0x17)** from an internal host **192.168.110.129**, followed by a successful network logon and basic host discovery activity (**whoami.exe**).

---

## Key Evidence Observed

### Domain Controller (DC) — `Security.evtx`

**Event ID 4768** (Kerberos TGT requested)

- **Time (UTC/local as provided):** 2024-10-05 14:42:44  
- **User:** Corrado  
- **User SID:** S-1-5-21-3079141193-1468241477-2901848075-1108  
- **Ticket Encryption Type:** `0x17 (RC4)`  
- **Service:** `krbtgt` (service SID ends in `-502`)  
- **Source IP/Port:** `192.168.110.129:49684`

### Workstation/User Logs (Corrado folder)

**Event ID 4624** (Successful logon)

- **Time:** 2024-10-05 14:48:58  
- **Logon Type:** 3 (Network)  
- **Source Address:** `192.168.110.129` (source port observed)

### Prefetch (Command Execution Indicator)

- **Artifact:** `whoami.exe` execution (Prefetch metadata)  
- **Time:** 2024-10-05 ~15:01:28  
- **Interpretation:** Post-access discovery behavior consistent with validating current user context after credential misuse.

---

## Timeline (Condensed)

1. **14:42:44** — Kerberos **4768** ticket request for Corrado using **RC4 (0x17)** from `192.168.110.129`  
2. **14:48:58** — **4624** successful **network logon** correlated to the same source host  
3. **~15:01:28** — Prefetch artifact indicates **whoami.exe** execution shortly after access

---

## Assessment & Likely Attack Flow (Lab Interpretation)

- The activity aligns with conditions commonly associated with **AS-REP Roasting**, which often involves targeting accounts that can be requested in a way that enables **offline password guessing**.
- The use of `0x17 (RC4)` is noteworthy because it can indicate **legacy encryption usage** and is frequently treated as suspicious in many modern environments.
- Following the authentication activity, a successful logon and **basic discovery** (e.g., `whoami`) suggests the actor validated access and began initial exploration.

---

## Indicators of Compromise (IOCs)

- **Source IP:** `192.168.110.129`  
- **Account Targeted:** `Corrado`  
- **Kerberos Artifact:** `TicketEncryptionType = 0x17 (RC4)`  
- **Execution Evidence:** `whoami.exe` (Prefetch)

---

## MITRE ATT&CK Mapping (Practical)

- **T1558.004** — Steal or Forge Kerberos Tickets: AS-REP Roasting  
- **T1078** — Valid Accounts (if credentials were successfully used)  
- **Discovery (general)** — post-logon discovery behavior consistent with environment/user enumeration

---

## Recommended Response Actions

### Immediate Containment / Investigation

- Investigate the source host `192.168.110.129` (EDR triage, process/network review, persistence checks).
- Reset credentials for the affected account (**Corrado**) and review authentication events around the incident window.
- Hunt for potential follow-on activity in Windows logs:
  - **4769** (Kerberos service ticket requests)
  - **4672** (special privileges assigned)
  - **4688** (process creation, if enabled)
  - **4648** (explicit credential usage)

### Hardening

- Audit accounts for **Kerberos pre-authentication configuration** and remove exceptions unless explicitly required.
- Reduce/disable RC4 where feasible and prefer **AES** in Kerberos and account settings.
- Enforce stronger password policy for at-risk accounts (especially service/privileged users).

---

## Detection Ideas (Quick Wins)

- Alert when: **EventID = 4768** AND **TicketEncryptionType = 0x17**
- Correlate suspicious 4768 activity with:
  - **4624** (Logon Type 3) from the same source host shortly after
  - Discovery commands and administrative tooling executed soon after logon (via **4688** or EDR telemetry)

Example correlation logic (plain English):

> Identify hosts making Kerberos requests with legacy encryption indicators, then verify whether they successfully authenticate and perform discovery actions soon after.

---

## Final Conclusion

Based on the lab evidence, the sequence is consistent with **AS-REP Roasting-style activity** progressing into **successful access** and **early discovery**. The priority response is to **contain the source host**, **secure the affected account**, and **validate there was no lateral movement or escalation**.
```
