---
layout: post
title: "AS-Rep Challenge(LetsDefend)"
date: 2025-11-26 20:04:11 -0600
author: "Brandon Love"
medium_canonical: "https://medium.com/@brandonlove2150/as-rep-challenge-letsdefend-cf1dee11b6a5?source=rss-024d132ba4b7------2"
tags: ["letsdefend-writeup", "letsdefendio", "blueteamlabs", "cybersecurity"]
---
> Originally published on Medium: https://medium.com/@brandonlove2150/as-rep-challenge-letsdefend-cf1dee11b6a5?source=rss-024d132ba4b7------2

Today, I took on another challenge from LetsDefend.

<!--more-->

Today, I took on another challenge from LetsDefend. The challenge was simple: analyze the AS-REP attack. This was a great challenge to get more practice reading Windows Security logs, filtering out noisy traffic, and identifying malicious activity.

### Background

A network security team received alerts from a Domain Controller (DC) indicating that a user was making unusual requests for Kerberos tickets, which is not typical for their role. Given that this behavior aligns with potential reconnaissance or lateral movement within the network, the security team escalated the issue to a senior investigator. The investigator has been tasked with analyzing the provided DC and workstation logs to trace the attacker’s movements, determine the source of the anomaly, and understand how the attacker gained access and what actions they might have taken inside the network.

> AS-REP Attack: I have already covered what an AS-REP attack is in this walkthrough of a [GoldenTicket](https://medium.com/@brandonlove2150/golden-ticket-walkthrough-d47dd458994d).

![](https://cdn-images-1.medium.com/max/1024/1*6LSK97w5K5c1-JNe4EaLOw.png)

Filter Log

Opening the ChallengeFile, there are two folders we need to look at: one for the username Corrado and one titled DC. This is the folder to explore first to answer the challenge questions. Once the security log is opened, to reduce traffic, filter the events by **EventID 4678**, which corresponds to Kerberos ticket requests.

![](https://cdn-images-1.medium.com/max/605/1*yIr2TQ9eOwW2CsrXHDrybw.png)

Search Events by 0x17

Knowing that it is a suspicious Kerberos ticket, search for the RC4 encryption algorithm **0x17**; this should point to the needed ticket.

![](https://cdn-images-1.medium.com/max/1024/1*Dp0zlKZ5B9YHAW8H5G9_JA.png)

Filtered Log

Looking at the image above, the time that the Kerberos ticket request was made, the user account affected, the SID associated with the user account, the type of encryption used, and the IP and port number that were used to request the ticket.

> 2024–10–05 14:42:44  
> -Corrado  
> -S-1–5–21–3079141193–1468241477–2901848075–1108  
> -RC4  
> -192.168.110.129:49684

![](https://cdn-images-1.medium.com/max/1024/1*jGhA8ZtCTy2hf-ugOEFIIQ.png)

Corrado Security Log

The next step is to search the Corrado Folder and open the Security file to view these events, as the Corrado account was compromised. Once the log is filtered by **EventID 4624** (corresponding to logon), and the IP address *192.168.110.129* is searched for, the first successful logon time will be displayed.

![](https://cdn-images-1.medium.com/max/1024/1*5Xia3QJPTPfvYx6H1o9crA.png)

1st time logon

> -2024–10–05 14:48:58

The final logs to look at are the prefetch file. Once the date is filtered by time, comparing the commands run at the time the attacker accessed the account shows the first command used. Since I could not get the Zimmerman tools to analyze the *whoami* command successfully, I examined the properties and added or subtracted 2 seconds from the time the file was modified to find the correct answer.

![](https://cdn-images-1.medium.com/max/1024/1*7QGgnwwbrVaYL7j_o0GOAA.png)

prefetch file

> whoami

> 2024–10–05 15:01:28

![](https://cdn-images-1.medium.com/max/978/1*fSO53OVgZxDIH8e5mPEQTQ.png)

Completion Badge

### Case Summary

**Incident Type:** Kerberos AS-REP Roasting / Credential Access  
 **Severity:** High (credential theft can lead to domain compromise)  
 **Primary Finding:** A Kerberos TGT request for user **Corrado** used **RC4 encryption (0x17)** from a suspicious internal host, **192.168.110.129**, followed by a successful network logon and host reconnaissance (**whoami.exe**).

### Key Evidence Observed

**Domain Controller (DC) — Security.evtx**

* **Event ID 4768** (TGT requested)
* **Time:** 2024–10–05 14:42:44
* **User:** Corrado
* **User SID:** S-1–5–21–3079141193–1468241477–2901848075–1108
* **Ticket Encryption Type:** **0x17 (RC4)**
* **Service:** krbtgt (**Service SID ends in -502**)
* **Source IP/Port:** **192.168.110.129:49684**

**Workstation/User Logs (Corrado folder)**

* **Event ID 4624** (Successful logon)
* **Time:** 2024–10–05 14:48:58
* **Logon Type:** 3 (Network)
* **Source Address:** **192.168.110.129** (port observed in logs)

**Prefetch (Command Execution Indicator)**

* **whoami.exe** execution observed via Prefetch metadata
* **Time:** 2024–10–05 ~15:01:28
* **Interpretation:** Post-access discovery / “validate my access” behavior commonly seen after credential abuse.

### Timeline (Condensed)

1. **14:42:44** — Suspicious **4768** TGT request for Corrado using **RC4 (0x17)** from **192.168.110.129**
2. **14:48:58–4624** successful **network logon** connected to the same source IP
3. **~15:01:28** — **whoami.exe** evidence in Prefetch suggests attacker discovery activity

### Assessment & Likely Attack Flow

* The attacker likely targeted an account with **Kerberos pre-authentication disabled** (or otherwise misconfigured), enabling an **AS-REP roast**.
* **RC4 (0x17)** is a major red flag in modern environments and is commonly associated with techniques used to obtain crackable material for offline password guessing.
* After obtaining or leveraging credentials, the attacker established a **network logon** and performed a fundamental discovery (**whoami**) to confirm their privileges and context.

### Indicators of Compromise (IOCs)

* **Source IP:** 192.168.110.129
* **Targeted User:** Corrado
* **Suspicious Kerberos Artifact:** Ticket Encryption Type 0x17 (RC4)
* **Suspicious Process Evidence:** whoami.exe (Prefetch)

### MITRE ATT&CK Mapping (Practical)

* **T1558.004 — Steal or Forge Kerberos Tickets: AS-REP Roasting**
* **T1078 — Valid Accounts** (if credentials were successfully used)
* **T1087 / T1033 / T1082 (Discovery family)** (whoami aligns with basic discovery behavior)

### Recommended Response Actions

**Immediate containment**

* Isolate/investigate host **192.168.110.129** (EDR triage, running processes, network connections, persistence checks).
* Force password reset for **Corrado** and review recent authentication activity.
* Review for follow-on activity: **4769 (TGS)**, **4672 (Special Privileges)**, **4688 (Process Creation)**, **4648 (Explicit Creds)**, suspicious SMB/RDP/WMI usage.

**Hardening**

* Audit AD for **“Do not require Kerberos preauthentication”** and remediate any accounts that don’t explicitly need it.
* Reduce/disable RC4 where possible; prioritize **AES** in Kerberos policy and account settings.
* Enforce a stronger password policy/length for accounts at risk (especially service and privileged users).

### Detection Ideas (Quick Win Queries)

**Windows Event Viewer / SIEM logic**

* Alert when **EventID=4768** AND **TicketEncryptionType=0x17**
* Correlate 4768 from a source IP with near-term:
* **4624 LogonType=3** from same IP
* Discovery process execution (e.g., whoami, nltest, net, dsquery, quser, ipconfig)

**Example correlation filter (plain English)**

> *“Find internal IPs requesting RC4 Kerberos tickets, then check if they log on successfully and run discovery commands shortly after.”*

### Final Conclusion

This activity is consistent with AS-REP roasting leading into credential misuse, with evidence of successful access and early discovery. The priority is to contain the source host, secure the Corrado account, and validate that no further lateral movement or privilege escalation occurred.

![](https://medium.com/_/stat?event=post.clientViewed&referrerSource=full_rss&postId=cf1dee11b6a5)
