---
layout: post
title: "SOC227 — Microsoft SharePoint Server Elevation of Privilege"
date: 2025-11-13 17:17:39 -0600
author: "Brandon Love"
medium_canonical: "https://medium.com/@brandonlove2150/soc227-microsoft-sharepoint-server-elevation-of-privilege-054803829e80?source=rss-024d132ba4b7------2"
tags: ["cybersecurity", "lets-defend", "blueteamlabs", "letsdefendio"]
---
> Originally published on Medium: https://medium.com/@brandonlove2150/soc227-microsoft-sharepoint-server-elevation-of-privilege-054803829e80?source=rss-024d132ba4b7------2

OC227 — Microsoft SharePoint Server Elevation of Privilege #### (LetsDefend) Walkthrough Today, I started another LetsDefend practice SOC alert for a Microsoft SharePoint Server elevation of privilege.

<!--more-->

### SOC227 — Microsoft SharePoint Server Elevation of Privilege

#### (LetsDefend) Walkthrough

Today, I started another LetsDefend practice SOC alert for a Microsoft SharePoint Server elevation of privilege. This is a possible CVE-2023–29357 Exploitation.

### Background

CVE-2023–29357 is a Microsoft SharePoint Server Privilege Escalation Vulnerability. This is caused by an unspecified vulnerability that allows an attacker to use spoofed JWT authentication tokens for a network attack. The attack bypasses authentication, enabling the attacker to gain administrator [privileges](https://www.cisa.gov/known-exploited-vulnerabilities-catalog?field_cve=CVE-2023-29357).

### Walkthrough

![](https://cdn-images-1.medium.com/proxy/1*sCX_w5BTZ-w0TdLs-1Zs6g.png)

Alert

To investigate this alert, I searched the logs for 172.16.17.233, the Host, and 39.91.166.222, the source IP address. I found there were three attempts to react to the /.api/web/siteusers with the User-Agent being python-requests/2.28.1. This indicates an automated attack using a Python script. 2 of the attempts were successful, with the HTTPS code being 200.

![](https://cdn-images-1.medium.com/max/1024/1*b_0uHKeHpUgEH0_UnjOYnw.png)

Logs

### Playbook

![](https://cdn-images-1.medium.com/max/838/1*XvjFPzbTDFuRV3_telTDQA.png)

Question 1

To determine if this is malicious traffic, we need to obtain the Source IP address of *39.91.166.222* and run it through the built-in threat monitoring page and VirusTotal.

![](https://cdn-images-1.medium.com/max/846/1*tdMktxin7gQJd-uK1U6BJw.png)

Results

Threat Intel and VirusTotal have reconfirmed that this IP address is malicious. BitDefender and G-Data have this marked as phishing.

![](https://cdn-images-1.medium.com/max/583/1*atJSGPxR2TvIGbUqTvPVvg.png)

Question 2 & 3

The CVE–2023–29357 utilizes a JSON Web Token (JWT) to bypass signature validation. With this information, we know the attack vector is *other*. Looking at the email traffic, there is no mention of a planned test.

![](https://cdn-images-1.medium.com/max/583/1*_AQT1eJBUefbFnX12qin8w.png)

Question 4

Referring back to the logs that we reviewed, we know that the traffic was from the internet to the company network.

![](https://cdn-images-1.medium.com/max/591/1*U_BbHnXKtaP3jwIXK9Mn5w.png)

Question 5

We know that the attack was successful because of the HTTP response code of 200. Since the attack was successful, we also need to contain this server. Looking at the server as well, we know that this was a CVE-2003–29357 attack because the OS is a Windows Server 2019.

![](https://cdn-images-1.medium.com/max/677/1*3PShIlrmUBCsWPQTUwMexw.png)

Question 6

Due to the attack's success, it needs to be escalated to the next tier.

![](https://cdn-images-1.medium.com/max/672/1*KRXheBE3DjUdYdQ_kWhtMw.png)

Artifacts

These are the artifacts that were found in the logs.

### Analyst Notes

On October 6, 2023, at 8:05 p.m., an alert triggered by Microsoft SharePoint Server Elevation of Privilege (CVE-2023–29357) was detected.

The Hostname affected was MS-SharePointServer with the IP Address of 172.16.17.233.

The source IP Address is 39.91.166.22. VirusTotal has this flagged as malicious, with Bitdefender and G-Data marking it as phishing.

The URL “GET /\_api/web/siteusers HTTP/1.1” 200 1453 “-” “python-requests/2.28.1” was successful with the HTTPS code of 200, and there was another request for the current user that was also successful.

I have contained the endpoint, and I recommend escalating to Tier 2. I found no other systems affected.

![](https://medium.com/_/stat?event=post.clientViewed&referrerSource=full_rss&postId=054803829e80)
