---
layout: post
title: "SOC246 — Forced Authentication Detected (LetsDefend)"
date: 2025-10-31 19:51:25 -0500
author: "Brandon Love"
medium_canonical: "https://medium.com/@brandonlove2150/soc246-forced-authentication-detected-letsdefend-0747859c4bda?source=rss-024d132ba4b7------2"
tags: ["letsdefend-writeup", "blue-team", "cybersecurity", "letsdefendio"]
---
> Originally published on Medium: https://medium.com/@brandonlove2150/soc246-forced-authentication-detected-letsdefend-0747859c4bda?source=rss-024d132ba4b7------2

### SOC246 — Forced Authentication Detected (LetsDefend) Today, I dove into a Let's LetsDefend SOC Alert that introduced us to Forced Authentication Detected.

<!--more-->

### SOC246 — Forced Authentication Detected (LetsDefend)

Today, I dove into a Let's LetsDefend SOC Alert that introduced us to Forced Authentication Detected. This was another great practical attempt to sharpen my skills in monitoring and investigating SOC Alerts. Follow me through this walkthrough as I analyze the alert, implement controls, and escalate it to a higher tier if necessary.

### Forced Authentication

Adversaries may gather credential material by invoking or forcing a user to automatically provide authentication information through a mechanism that they can intercept and exploit.

The Server Message Block (SMB) protocol is commonly used in Windows networks for authentication and communication between systems for access to resources and file sharing. When a Windows system attempts to connect to an SMB resource, it will automatically try to authenticate and send credential information for the current user to the remote system.[[1]](https://en.wikipedia.org/wiki/Server_Message_Block) This behavior is typical in enterprise environments, allowing users to access network resources without needing to enter credentials.

![](https://cdn-images-1.medium.com/proxy/1*Kfnc8tzN5q52sD9LenNyAA.png)

SOC246 Alert

### Investigation

We will use the playbook provided by LetsDefend and conduct our analysis.

![](https://cdn-images-1.medium.com/max/848/1*hZCN1rY-pX84pBiaPIhyjA.png)

Question 1

We will need to refer back to the alert to identify anything suspicious that triggered it.

![](https://cdn-images-1.medium.com/max/879/1*RisIVRAL2TJq0Nad_1X2Pw.png)

Alert

We can see that the event is being triggered from an outside source within our network. The destination IP address and hostname are also provided for our use. The suspicious aspect of this alert is that multiple post requests were observed from the same IP address to the fixed URL *"/accounts/login"*. We will need to check the source IP address *120.48.36.175* against VirusTotal to see if we receive any malicious hits.

![](https://cdn-images-1.medium.com/proxy/1*Gcg9I1pVUWDoxX_iH3y4UQ.png)

Virus Total

VirusTotal came back with 4/95 security vendors flagging this IP address as malicious. SSH brute-force Attackers were detected on 2023-09-20, according to ArcSight Threat Intelligence. The four vendors that marked this URL as malicious were BitDefender, CyRadar, G-Data, and SOCRadar.

![](https://cdn-images-1.medium.com/max/1024/1*Lnh76H8cU3vwLuuK0bO_ww.png)

Security Vendors’ Analysis

> Now we know the IP that contacted our Host is malicious

![](https://cdn-images-1.medium.com/max/826/1*lwiERrQuskX8ljPKNH8D9A.png)

Question 2

> We seen that the malicious IP was trying to use bruteforce to access the network, we can list this attack type as other.

![](https://cdn-images-1.medium.com/max/806/1*OCTTBD6hsqInWNJxvFUgFQ.png)

Question 3

> Looking in the email traffic there was no reference to a planned test.

![](https://cdn-images-1.medium.com/max/810/1*YuPiqmdg9fJqMUVGhsze9g.png)

Question 4

> Looking at the log we can see that this was an outside Ip address attempting to contact the Company Network.

![](https://cdn-images-1.medium.com/max/805/1*xFsYHSQLMfI8jH080i9lew.png)

Log Entry

![](https://cdn-images-1.medium.com/max/812/1*hOSsPAjM9SKTg7j5snFkbw.png)

Question 5

> Refering back to the logs we can see that the endpoint allowed the event to process.

![](https://cdn-images-1.medium.com/proxy/1*1L1mPIFURN_XJErW8IFxMg.png)

Log Access

![](https://cdn-images-1.medium.com/max/819/1*Svyq8T20J3fvrGStKLanMw.png)

Question 6

> Because of the successful attempt of the bruteforce attack, this alert needs to be escalated to Tier 2 for further action and analysis.

![](https://cdn-images-1.medium.com/max/1024/1*4dHZvAe2QSNZuDQlExAtug.png)

Completion

### Analyst Note

> On December 12, 2023, an alert was issued for a forced authentication detection. The source IP address was 120.48.36.175, and the target IP address was 104.26.15.61, associated with the host WevServer\_Test. The requested URL was   
> <http://test-frontend.letsdefend.io/accounts/login>. During the gathering and investigation process, 22 requests were made from the source IP address, spanning multiple source and destination ports. This was a sample of RAW log capture:   
> The Request URL: <http://test-frontend.letsdefend.io/accounts/login>  
> Request Method: POST  
> Device Action: Permitted  
> User-Agent: Mozilla/5.0 (Windows NT 10.0; rv: 78.0) Gecko/20100101 Firefox/78.0  
> Credentials: Username=mysql&Password=princess  
> These actions were permitted, but the firewall blocked some of the requests.  
> Viewing the source IP in VirusTotal, it is identified as a malicious threat.  
> I recommend this be escalated to Tier 2 analysis.

### Summary

In this investigation, a forced authentication alert revealed repeated unauthorized POST requests to the organization's login endpoint from a malicious external IP (120.48.36.175). Threat intelligence confirmed the source's association with SSH brute-force activity. The logs showed that the endpoint permitted multiple requests before partial blocking occurred. Due to the confirmed malicious behavior and successful connection attempts, the incident was escalated to Tier 2 for deeper forensic analysis and remediation.

![](https://medium.com/_/stat?event=post.clientViewed&referrerSource=full_rss&postId=0747859c4bda)
