---
layout: post
title: "Upstyle Backdoor (LetsDefend)"
date: 2025-11-05 18:19:42 -0600
author: "Brandon Love"
medium_canonical: "https://medium.com/@brandonlove2150/upstyle-backdoor-letsdefend-7513e41cd145?source=rss-024d132ba4b7------2"
tags: ["letsdefend-writeup", "blue-team", "letsdefendio", "cybersecurity"]
---
> Originally published on Medium: https://medium.com/@brandonlove2150/upstyle-backdoor-letsdefend-7513e41cd145?source=rss-024d132ba4b7------2

Today, I took on another challenge from LetsDefend.

<!--more-->

Today, I took on another challenge from LetsDefend. This challenge focused on exploiting Palo Alto firewalls using CVE–2024–3400 in early 2024. [UPSTYLE](https://attack.mitre.org/software/S1164) is a Python-based backdoor and has only been observed in relation to this exploitation activity, which involved attempted installation on compromised devices by the threat actor UTA0218.

![](https://cdn-images-1.medium.com/max/674/1*IGgTkg9BXPSkt3oYG46NGg.png)

Mitre ATT&CK

This is a breakdown from MITRE of the backdoor attack and its execution process.

### Background

### Upstyle Backdoor

Help us to analyze specifically targeting a backdoor known as UPSTYLE and its relation to CVEs (Common Vulnerabilities and Exposures) that affect Palo Alto Networks’ [products](https://app.letsdefend.io/challenge/upstyle-backdoor).

**File Location:** C:\Users\LetsDefend\Desktop\ChallengeFile\sample.zip

**File Password:** infected

### Walkthrough

The first step in this challenge is to navigate to the ChallengeFile folder and unzip the sample.zip folder to review its contents. The password is infected, like LetsDefend provided.

![](https://cdn-images-1.medium.com/max/1024/1*zjhLGhprtsQUJV43qijnQQ.png)

Challenge File

To find the answers to this challenge, the Python script should be examined using Notepad++.

![](https://cdn-images-1.medium.com/max/1024/1*1ZXjSa4SootDkMipK7UUrA.png)

Python Script

![](https://cdn-images-1.medium.com/max/1024/1*dW5kxmaof2U4zsS9VyFKqA.png)

Python Script 2

### Script Analysis

Let's break down this script by line, question by question.

#### Q1 — def check():

* This function initializes the main malicious behavior.
* It imports modules (os, subprocess, time, threading, etc.) and starts background processes that read, decode, and execute base64 data — effectively allowing the attacker to run arbitrary code hidden in encoded form.
* This is a common trick to **obfuscate the payload** from antivirus or signature-based detection.

#### Q2 — systempth = "/usr/lib/python3.6/site-packages/system.pth"

* The script writes malicious code into this file (system.pth).
* .pth Files in Python site-packages are automatically executed **whenever Python starts**.
* This means **every Python process on the system will load the attacker’s code**, creating **persistent execution** — a stealthy persistence mechanism.

#### Q3 — css\_path = "/var/appweb/..."

* This references a CSS file used by a web portal (likely *GlobalProtect* or a VPN portal).
* The malware **modifies or injects data into a legitimate web resource**, possibly to **plant a web shell** or **embed malicious JavaScript**.
* It abuses this file path to ensure its malicious code runs in the context of a web application.

#### Q4 — os.unlink("/opt/pancfg/mgmt/licenses/PA\_VM\*")

* This line **deletes Palo Alto Networks license files** (used by PAN-OS firewalls or GlobalProtect gateways).
* That could cause **service disruption**, **loss of configuration**, or even **bypass certain restrictions**.
* It’s highly destructive and indicates a targeted attack on **Palo Alto firewall infrastructure**.

#### Q5 — signal.signal(signal.SIGTERM, stop)

* Installs a **signal handler** to rewrite the malicious .pth file if it’s removed or the process is terminated.
* In short, if a defender deletes the infection, it can **recreate itself**.
* This provides **resilience** against cleanup attempts.

#### Q6 — def protect():

* Defines a persistence and self-protection routine.
* Ensures the malicious code remains /usr/lib/python3.6/site-packages/system.pth even if deleted.
* Runs continuously alongsidecheck(), effectively keeping the system infected.

#### Q7 — SHELL\_PATTERN = "img\\(([A-Za-z0-9+/=]+)\\)"

* This regex searches for **base64-encoded commands** hidden in log files (under an img(...) pattern).
* The attacker can hide commands inside **legitimate log lines**, which the script then decodes and executes — a **command-and-control (C2)** channel disguised as log traffic.

#### Q8 — /var/log/pan/sslvpn\_ngx\_error.log

* The script reads this log file — likely from a Palo Alto SSL VPN.
* It scans it for base64-encoded payloads using the pattern above.
* When found, it decodes and executes them — allowing the attacker to send commands via log injection.

### Summary of Script

This is a **persistence + C2 Python backdoor** designed for **network appliances (likely Palo Alto GlobalProtect VPNs)**.  
 It maintains access by embedding itself in Python libraries, reads incoming base64-encoded commands from log files, executes them, and resists removal.

### Summary — Upstyle Backdoor (LetsDefend)

In this LetsDefend challenge, I analyzed the UPSTYLE Python backdoor associated with the exploitation of Palo Alto devices (CVE-2024–3400) and activity attributed to threat actor UTA0218. The delivered sample is a multi-component backdoor that establishes persistent execution by writing to Python’s site-packages (/usr/lib/python3.6/site-packages/system.pth), installs self-protection to restore itself if removed, and provides a stealthy command-and-control (C2) channel by scanning appliance logs (e.g., /var/log/pan/sslvpn\_ngx\_error.log) for img(…) patterns containing base64 payloads. It also tampers with device-specific files (e.g., deleting /opt/pancfg/mgmt/licenses/PA\_VM\*), suggesting targeted disruption of Palo Alto GlobalProtect/PAN-OS environments. The code decodes and executes hidden commands, uses signal handlers to survive termination, and can inject or modify web portal files to persist or conceal activity. Overall, UPSTYLE is a resilient, targeted backdoor that combines persistence, covert command and control (C2) via log injection, and destructive or disruptive actions against firewall/VPN infrastructure.

![](https://medium.com/_/stat?event=post.clientViewed&referrerSource=full_rss&postId=7513e41cd145)
