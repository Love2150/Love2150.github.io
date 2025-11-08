---
layout: post
title: "Cobalt Strike: Triage to Timeline"
date: 2025-11-07 10:30:00 -0600
image: /assets/images/cobalt-strike-hero.jpg   # ← this is option 4
tags: [DFIR, PCAP, ATT&CK]
---


I walked through a network forensics scenario involving Cobalt Strike beacons and HTTP/S traffic. <!--more-->

**Highlights**
- Quick protocol hierarchy to focus scope
- File carving with NetworkMiner
- Initial beacon patterns and IOCs

### Indicators
- UA: `curl/7.88.1`
- Paths: `/server-info.action` → `setupadministrator.action` → `finishsetup.action`
- Infra: 43.130.1.222

### Notes
- Map findings to ATT&CK (C2 over HTTP/S, discovery, exfil paths)
- Add Sigma/YARA stubs for detection follow-up
