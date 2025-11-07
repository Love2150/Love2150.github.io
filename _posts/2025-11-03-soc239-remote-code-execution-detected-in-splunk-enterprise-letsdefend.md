---
layout: post
title: "SOC239 — Remote Code Execution Detected in Splunk Enterprise (LetsDefend)"
date: 2025-11-03 20:57:02 -0600
author: "Brandon Love"
medium_canonical: "https://medium.com/@brandonlove2150/soc239-remote-code-execution-detected-in-splunk-enterprise-letsdefend-34b36bd92fff?source=rss-024d132ba4b7------2"
tags: ["lets-defend", "cybersecurity", "letsdefendio"]
---
> Originally published on Medium: https://medium.com/@brandonlove2150/soc239-remote-code-execution-detected-in-splunk-enterprise-letsdefend-34b36bd92fff?source=rss-024d132ba4b7------2

cdn-images-1.medium.com/max/937/1*VaQMHSrRmbiixTw8d1dIjg.png) SOC Alert ### Walkthrough Today, I completed another alert from LetsDefend regarding a Remote Code Execution Detected in Splunk Enterprise.

<!--more-->

### SOC239 — Remote Code Execution Detected in Splunk Enterprise (LetsDefend)

![](https://cdn-images-1.medium.com/max/937/1*VaQMHSrRmbiixTw8d1dIjg.png)

SOC Alert

### Walkthrough

Today, I completed another alert from LetsDefend regarding a Remote Code Execution Detected in Splunk Enterprise. After reviewing this alert, I searched the Log Management system using the source IP address *180.101.88.240* and found that the IP address had contacted our internal Host with the hostname Splunk Enterprise, which has the IP address *172.16.20.13*. It requested *http://18.219.80.54:8000/en-US/splunkd/\_\_upload/indexing/preview?output\_mode=json&props.NO\_BINARY\_CHECK=1&input.path=shell.xsl.*

![](https://cdn-images-1.medium.com/max/1024/1*zNnFrb7C1UhM-m125HDgig.png)

Log Management

![](https://cdn-images-1.medium.com/max/1024/1*5bpKY57ncF5UShGtkKCCbw.png)

Source Logs

This is only the first half of the investigation, though. We need to search for the endpoint IP address *172.16.20.13.* Examining the exact time as recorded in our log, we can see that the same request was made on this end and was successful. Immediately after this, we can see that a new username and password have been created, as shown in the image above.

To confirm that everything matches up, I reviewed the Endpoint Security tab of the Host. Examining these logs, we can see that a user was added, and the whoami, groups, useradd, and passwd commands were executed on the host.

![](https://cdn-images-1.medium.com/max/1024/1*_zBPu5jMLOrA6U80Th8hRw.png)

Endpoint Security

After collecting all this evidence, it’s time to search the source IP address on [VirusTotal](https://www.virustotal.com/gui/ip-address/180.101.88.240) to see if we can gather any additional information.

![](https://cdn-images-1.medium.com/max/1024/1*K4Jx2ePEIIWCnVPkewuh9Q.png)

VirusTotal

As you can see, the IP address is flagged as malicious. We can now answer the playbook question, having gathered all the necessary information.

![](https://cdn-images-1.medium.com/max/1024/1*FLKLxyguocHmD6X9Jc9nTg.png)

Playbook pt 1

![](https://cdn-images-1.medium.com/max/1024/1*eNy-Izx-yy1kJmpaMhLrDw.png)

Playbook pt 2

### Analyst Notes

On November 21, 2023, at 12:24 p.m., an alert was triggered for a remote code execution detected in Splunk Enterprise.

The Source IP address is 180.101.88.240, and it targeted 172.16.20.13, trying to request this URL <http://18.219.80.54:8000/en-US/splunkd/__upload/indexing/preview?output_mode=json&props.NO_BINARY_CHECK=1&input.path=shell.xsl>.

This vulnerability aligns with CVE-2023–46214, Which Involves Remote code execution (RCE) in Splunk Enterprise due to insecure XML Parsing.

The attacker was able to log in and create a new account on the Splunk Enterprise host.

I recommend containment for the host. Change the passwords and delete the new user account created. Updating and patching to the latest version available is highly essential. Recommend continuing to monitor this host for further activity and escalating to Tier 2.

![](https://cdn-images-1.medium.com/max/1024/1*BSfDTFYi71n1JlENIjDoXQ.png)

Completion

### Summary

The attacker gained access to the Splunk Enterprise-hosted endpoint using the XML injection method. They were able to create a new user and password. The recommendation is to reset all passwords, delete the newly created user, block the source IP address, contain the endpoint, update and patch to the latest version, and continue to monitor for suspicious behavior coming from Spluck Enterprise.

![](https://medium.com/_/stat?event=post.clientViewed&referrerSource=full_rss&postId=34b36bd92fff)
