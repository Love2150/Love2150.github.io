---
title: "AS-REP Roasting Investigation Report (LetsDefend)"
layout: page
permalink: /reports/analyst_report/as-rep.html
---

<div class="card report-hero">
  <h1 class="report-title">AS-REP Roasting Investigation Report</h1>
  <p class="report-subtitle">Windows Security Log Triage • Kerberos Authentication Analysis • Timeline Correlation</p>

  <div class="report-meta">
    <span class="chip">LetsDefend Lab</span>
    <span class="chip">Active Directory</span>
    <span class="chip">Kerberos</span>
    <span class="chip">Incident Triage</span>
  </div>

  <div class="callout info">
    <strong>Portfolio note:</strong> This report is based on a controlled LetsDefend dataset for educational purposes.
  </div>
</div>

<div class="card report-section">
  ## Case Summary

  **Incident Type:** Kerberos AS-REP Roasting / Credential Access  
  **Severity:** High (credential theft can lead to domain compromise)  
  **Primary Finding:** A Kerberos TGT request for user **Corrado** used **RC4 encryption (0x17)** from a suspicious internal host **192.168.110.129**, followed by a successful network logon and post-access discovery (**whoami.exe**).
</div>

<div class="card report-section">
  ## Key Evidence Observed

  ### Domain Controller (DC) — Security.evtx
  - **Event ID:** 4768 (TGT requested)  
  - **Time:** 2024-10-05 14:42:44  
  - **User:** Corrado  
  - **User SID:** S-1-5-21-3079141193-1468241477-2901848075-1108  
  - **Ticket Encryption Type:** **0x17 (RC4)**  
  - **Service:** krbtgt (Service SID ends in **-502**)  
  - **Source IP/Port:** **192.168.110.129:49684**

  ### Workstation/User Logs (Corrado folder)
  - **Event ID:** 4624 (Successful logon)  
  - **Time:** 2024-10-05 14:48:58  
  - **Logon Type:** 3 (Network)  
  - **Source Address:** **192.168.110.129**

  ### Prefetch (Command Execution Indicator)
  - **Artifact:** whoami.exe  
  - **Time:** 2024-10-05 ~15:01:28  
  - **Interpretation:** Post-access validation/discovery behavior commonly observed after credential misuse.
</div>

<div class="card report-section">
  ## Timeline (Condensed)

  <div class="timeline">
    <div class="timeline-item">
      <div class="timeline-time">2024-10-05 14:42:44</div>
      <div class="timeline-body"><strong>4768</strong> Kerberos TGT request for <strong>Corrado</strong> using <code>RC4 (0x17)</code> from <code>192.168.110.129:49684</code>.</div>
    </div>

    <div class="timeline-item">
      <div class="timeline-time">2024-10-05 14:48:58</div>
      <div class="timeline-body"><strong>4624</strong> Successful logon (<code>Logon Type 3</code>) correlated to <code>192.168.110.129</code>.</div>
    </div>

    <div class="timeline-item">
      <div class="timeline-time">2024-10-05 ~15:01:28</div>
      <div class="timeline-body">Prefetch indicates <code>whoami.exe</code> execution (post-access discovery/validation).</div>
    </div>
  </div>
</div>

<div class="card report-section">
  ## Assessment & Likely Attack Flow

  - Activity aligns with **AS-REP Roasting-style** credential access patterns (lab scenario).
  - **RC4 (0x17)** is a notable legacy/weak encryption indicator often treated as suspicious in modern environments.
  - Successful logon + quick discovery suggests the actor validated access and began initial exploration.
</div>

<div class="card report-section">
  ## Indicators of Compromise (IOCs)

  <div class="ioc-list">
    <div class="ioc-row"><span>Source IP</span><code>192.168.110.129</code></div>
    <div class="ioc-row"><span>Targeted User</span><code>Corrado</code></div>
    <div class="ioc-row"><span>Kerberos Signal</span><code>EventID 4768 + TicketEncryptionType 0x17 (RC4)</code></div>
    <div class="ioc-row"><span>Execution Evidence</span><code>whoami.exe</code></div>
  </div>
</div>

<div class="card report-section">
  ## MITRE ATT&CK Mapping (Practical)

  - **T1558.004** — Steal or Forge Kerberos Tickets: AS-REP Roasting  
  - **T1078** — Valid Accounts (if credentials were used)  
  - **Discovery** — Post-logon validation/discovery behavior
</div>

<div class="card report-section">
  ## Recommended Response Actions

  ### Immediate containment
  - Investigate / isolate host **192.168.110.129** (EDR triage, running processes, network connections, persistence).
  - Reset credentials for **Corrado** and review recent authentication activity.
  - Hunt for follow-on activity: **4769**, **4672**, **4688**, **4648**.

  ### Hardening
  - Audit AD for accounts that do not require Kerberos pre-authentication and remediate unnecessary exceptions.
  - Reduce/disable RC4 where feasible; prioritize **AES**.
  - Enforce strong password policy for service/privileged accounts and monitor anomalies.
</div>

<div class="report-actions">
  <a class="btn" href="/reports/analyst_report/">← Back to Analyst Reports</a>
  <a class="btn btn-ghost" href="/">Home</a>
</div>
