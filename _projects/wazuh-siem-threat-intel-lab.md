---
layout: page
title: "Wazuh SIEM + VirusTotal + Action1 Patch Management Lab"
image: /assets/images/F8C556A5-ACB7-4FE1-8417-62B2AEEA9DED.png
permalink: /projects/wazuh-siem-threat-intel-lab/
tags: [siem, wazuh, threat-intelligence, patch-management, soc, blue-team, linux, windows]
---

# Wazuh SIEM Deployment with Threat Intelligence & Patch Automation

## Overview

This project documents the deployment of a full security monitoring and remediation lab using:

- Wazuh (SIEM + HIDS)
- Ubuntu Server (Manager)
- Windows & Linux Endpoints
- VirusTotal (Threat Intelligence Enrichment)
- Action1 (Patch Management)

The lab simulates a real-world SOC lifecycle:

**Detect → Enrich → Remediate → Validate**

---

## 🏗 Architecture Diagram

![Architecture Diagram](/assets/images/F8C556A5-ACB7-4FE1-8417-62B2AEEA9DED.png)

*Figure 1: High-level architecture of Wazuh, endpoints, VirusTotal integration, and Action1 patch workflow.*

---

## Environment

| Component | Role |
|------------|------|
| SIEM | Wazuh |
| Server OS | Ubuntu Server |
| Endpoints | Windows 10/11, Ubuntu Linux |
| Threat Intelligence | VirusTotal API |
| Patch Management | Action1 |

---

## 1️⃣ Wazuh Deployment (Ubuntu)

Installed Wazuh All-in-One:

```bash
- curl -sO https://packages.wazuh.com/4.x/wazuh-install.sh 
- sudo bash wazuh-install.sh -a

📸 Wazuh Dashboard

Figure 2: Wazuh dashboard showing active agents and alert summary.

⸻

2️⃣ Endpoint Onboarding

Windows Agent

msiexec.exe /i wazuh-agent.msi /q WAZUH_MANAGER="<server-ip>"
NET START WazuhSvc

📸 Windows Agent Connected

Figure 3: Windows endpoint successfully registered in Wazuh.

⸻

Linux Agent

sudo dpkg -i wazuh-agent.deb
sudo systemctl enable wazuh-agent
sudo systemctl start wazuh-agent

📸 Linux Agent Connected

Figure 4: Linux endpoint successfully reporting to Wazuh.

⸻

3️⃣ File Integrity Monitoring (FIM)

Monitored download directories:

Windows

C:\Users\*\Downloads

Linux

/home/*/Downloads

📸 FIM Alert Example

Figure 5: File creation event detected in Downloads directory.

⸻

4️⃣ VirusTotal Integration

Configured in:

/var/ossec/etc/ossec.conf

<integration>
  <name>virustotal</name>
  <api_key>YOUR_API_KEY</api_key>
  <group>syscheck</group>
  <alert_format>json</alert_format>
</integration>

Reloaded systemd and restarted manager:

sudo systemctl daemon-reload
sudo systemctl restart wazuh-manager.service

📸 VirusTotal Enriched Alert

Figure 6: Wazuh alert enriched with VirusTotal detection ratio.

⸻

5️⃣ Vulnerability Detection

Enabled vulnerability detection module to identify:
	•	Missing security patches
	•	Outdated software versions
	•	Known CVEs

📸 Vulnerability Dashboard

Figure 7: Detected vulnerabilities mapped to CVEs.

⸻

6️⃣ Patch Management with Action1

Installed Action1 agent on endpoints.

Configured:
	•	Auto-approve critical patches
	•	Scheduled maintenance windows
	•	Controlled reboots
	•	Compliance tracking

📸 Action1 Patch Deployment

Figure 8: Patch deployment and compliance view in Action1.

⸻

🔄 Integrated Security Lifecycle

Phase	Tool	Function
Log Collection	Wazuh	Centralized monitoring
File Detection	Wazuh FIM	Detect new downloads
Threat Enrichment	VirusTotal	Hash reputation lookup
Vulnerability Detection	Wazuh	Identify exposure
Patch Remediation	Action1	Deploy updates
Validation	Wazuh	Confirm compliance


⸻

Skills Demonstrated
	•	SIEM deployment & configuration
	•	Windows & Linux agent management
	•	Threat intelligence integration
	•	Automated malware reputation checks
	•	Vulnerability lifecycle management
	•	Patch governance strategy
	•	SOC workflow design
	•	Blue team operational alignment

⸻

Outcome

Built a defense-in-depth monitoring and remediation lab that mirrors modern enterprise SOC operations and demonstrates practical blue team capabilities including detection engineering, enrichment automation, and structured patch compliance validation.
