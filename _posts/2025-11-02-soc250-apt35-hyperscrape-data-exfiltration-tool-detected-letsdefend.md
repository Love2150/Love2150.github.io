---
layout: post
title: "SOC250 — APT35 HyperScrape Data Exfiltration Tool Detected (LetsDefend)"
date: 2025-11-02 06:49:03 -0600
author: "Brandon Love"
medium_canonical: "https://medium.com/@brandonlove2150/soc250-apt35-hyperscrape-data-exfiltration-tool-detected-letsdefend-f85d6388111f?source=rss-024d132ba4b7------2"
tags: ["letsdefendio", "cybersecurity", "blue-team", "letsdefend-writeup"]
---
> Originally published on Medium: https://medium.com/@brandonlove2150/soc250-apt35-hyperscrape-data-exfiltration-tool-detected-letsdefend-f85d6388111f?source=rss-024d132ba4b7------2

### SOC250 — APT35 HyperScrape Data Exfiltration Tool Detected (LetsDefend) I just completed another SOC Alert from LetsDefend, and this alert was for HyperScrape Data Ecfiltration Tool Detected.

<!--more-->

### SOC250 — APT35 HyperScrape Data Exfiltration Tool Detected (LetsDefend)

I just completed another SOC Alert from LetsDefend, and this alert was for HyperScrape Data Ecfiltration Tool Detected. This alert provided another opportunity to gain hands-on experience in responding to an alert, completing another playbook, and analyzing logs.

![](https://cdn-images-1.medium.com/max/1024/1*Zf74uDHcpIvb3BJoLCfxUQ.png)

SOC Alert

### WalkThrough

![](https://cdn-images-1.medium.com/proxy/1*4v7-Zv5zvQltm5WwwY1b6A.png)

Start of Playbook

After starting the playbook, I first searched the MD5SUM Hash *cd2ba296828660ecd07a36e8931b851dda0802069ed926b3161745aae9aa6daa.* This hash was flagged as malicious, scoring 51 on VirusTotal.

![](https://cdn-images-1.medium.com/max/1024/1*DFvx0Xlg7QQEcx_hyH2xLQ.png)

VirusTotal

*We can see that ALYac lists it as a Trojan Email Downloader. Examining the history section of the file reveals additional information about it.*

![](https://cdn-images-1.medium.com/max/607/1*l-IzMH5_6wT9TcGeCQK9mw.png)

History

The first log I searched was the log management section on the GUI of LetsDefend. From this log, we can see that at 11:21:48, a file was downloaded using a process called *EmailDownloader.exe,* which was downloaded from *136.243.108.14.* We can confirm that the host was Arthur and the IP address is *172.16.17.72*.

![](https://cdn-images-1.medium.com/max/966/1*PJsyNlWFGCgbPDdxBD_vAw.png)

Log Management

Since we have seen that the process EmailDownloader.exe was run, the next step is to check the emails of *arthur@letsdefend.io*. After checking the emails, there was no traffic. This makes the alert more suspicious; further investigation into the endpoint, *Arthur*, is needed.

![](https://cdn-images-1.medium.com/max/953/1*wborSJvWfihYv9nNAArekg.png)

Endpoint Logs

Two logs were captured around the time of the alert. The first instance occurred at 11:21:37, when the explorer.exe process triggered the emaildownloader.exe process to download the suspicious file. The second process was MpCmdRun.exe, which ran the command SignaturesUpdateService with the -ScheduleJob and -UnmanagedUpdate parameters. This means that the file was able to modify the signatures.

Using all the information that was gathered, these were my answers to the questions in the playbook.

![](https://cdn-images-1.medium.com/max/801/1*rl8aeML-nG6cmO-GH_4B8A.png)

Question 1

![](https://cdn-images-1.medium.com/max/734/1*T0B3eLQCIXwpi5rSdEPV_Q.png)

Question 2

![](https://cdn-images-1.medium.com/max/780/1*qsVtJYEn4vulC3RkBdM8ig.png)

Question 3

![](https://cdn-images-1.medium.com/max/694/1*1jCw1im0mekYVRDlAbZoiQ.png)

Question 4

![](https://cdn-images-1.medium.com/max/720/1*PIlySmZfJ2pCRreQNcgndQ.png)

Question 5

![](https://cdn-images-1.medium.com/max/1024/1*Dyl4SYDDG-CPrKHEZXyyBQ.png)

Containment

![](https://cdn-images-1.medium.com/max/1024/1*pAuk3Guh7-lhzEAMzkgCIA.png)

Completion

### Analyst Notes

> On December 27, 2023, at 11:22 AM, an alert was triggered for Unusual or suspicious behavior linked to a file (cd2ba296828660ecd07a36e8931b851dda0802069ed926b3161745aae9aa6daa).

> After reviewing the hash file, it is identified as malicious by VirusTotal, with a score of 51.

> This file ran an EmailDownloader.exe process; however, upon analyzing the email security, no emails were found to be linked to the host machine or its email address.

> Analyzing the logs, we can see that a file was downloaded at 11:21:48. Examining the Host endpoint (Arthur) in the network logs reveals that several processes were run.

> The first one that triggered the email download was at 11:21:37, and it ran explorer.exe to download the file with EmailDownloader.exe.

> The second process, run at 11:38:10, was MpCmdRun.exe, which executed the command “SignaturesUpdateService -ScheduleJob -UnmanagedUpdate”.

> The host was contained, and no other endpoints were compromised.

> I suggest blocking the attacker’s IP address and resetting the host’s password.

![](https://medium.com/_/stat?event=post.clientViewed&referrerSource=full_rss&postId=f85d6388111f)
