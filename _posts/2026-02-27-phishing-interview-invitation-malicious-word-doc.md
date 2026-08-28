---
layout: post
title: "Phishing “Interview Invitation” — Malicious Word Doc."
date: 2026-02-27 23:22:42 -0600
author: "Brandon Love"
medium_canonical: "https://medium.com/@brandonlove2150/phishing-interview-invitation-malicious-word-doc-b35d2a30f100?source=rss-024d132ba4b7------2"
canonical_url: "https://medium.com/@brandonlove2150/phishing-interview-invitation-malicious-word-doc-b35d2a30f100?source=rss-024d132ba4b7------2"
tags: ["cybersecurity", "lets-defend"]
---
> Originally published on Medium: https://medium.com/@brandonlove2150/phishing-interview-invitation-malicious-word-doc-b35d2a30f100?source=rss-024d132ba4b7------2

## Phishing “Interview Invitation” — Malicious Word Doc.

<!--more-->

## Phishing “Interview Invitation” — Malicious Word Doc. — MSDT Activity (Follina Signals) — Payload Staging

Even in 2026, one of the most effective attack paths is still the simplest:

**a convincing email + a document attachment.**

In this lab-based investigation (LetsDefend + VirusTotal + ANY.RUN), I traced a suspicious “interview invitation” email that delivered a malicious Word document. Endpoint and network telemetry aligned with behavior commonly associated with CVE-2022–30190 (“Follina”/MSDT abuse) and with follow-on payload staging.

#### Initial Access: The Email That Started It

**Sender:** radiosputnik@ria.ru

**To:** jonas@letsdefend.io

**Subject:** Invitation for an interview

**Date:** Jun 02, 2022 — 01:51 PM

This is a classic social engineering theme: urgency + opportunity (“interview”) to entice the user to open an attachment.

#### Host & Environment

• Endpoint: 172.16.17.39 (Windows 10, 64-bit)

• User: admin

• Telemetry Sources: LetsDefend (Endpoint + Log Mgmt), VirusTotal, ANY.RUN

#### What Made This Alert High Severity

1)VirusTotal: Strong malicious consensus on the document

The document was flagged heavily on VirusTotal:

• sample.doc

• SHA-256: 4a24048f81afbe9fb62e7a6a49adbd1faf41f266b5f9feecdceb567aec096784

• Detections: 47/66

• Tags/labels included w97m, calls-wmi, cve-2022–30190, and legacy exploit references (ex: CVE-2017–0199)

![](https://cdn-images-1.medium.com/max/1024/1*Ir6VJbJJI3HOlNJJOEbDzA@2x.jpeg)

“VT: sample.doc flagged by 47/66 engines; tags include CVE-2022–30190 (Follina indicators).”

Screenshot: VirusTotal results for sample.doc (47/66 detected)

#### 2) Embedded artifact flagged too (document.xml.rels)

A related embedded artifact also showed strong detections:

• document.xml.rels

• SHA-256: 62f262d180a5a48f89be19369a8425bec596bc6a02ed23100424930791ae3df0

• Detections: 35/62

• Tags included cve-2022–30190, cve-2017–11882, cve-2017–0199, exploit references

![](https://cdn-images-1.medium.com/max/1024/1*N906js_puYtOAT3-9UCiww@2x.jpeg)

“VT: malicious embedded relationship file (document.xml.rels) also heavily flagged.”

Screenshot: VirusTotal results for document.xml.rels (35/62 detected)

#### 3) Network telemetry: outbound HTTPS + suspicious content host

LetsDefend proxy/network logs showed outbound traffic tied to the same activity chain:

• Source: 172.16.17.39

• Destination IP: 141.105.65.149

• Port: 443

• URL: https://www.xmlformats.com/office/word/2022/wordprocessingDrawing/RDF8421.html

![](https://cdn-images-1.medium.com/max/1024/1*zEfYuaIIGCdD8Xb45qZyFA@2x.jpeg)

“Proxy log: host reached xmlformats[.]com path during the investigation window.”

Screenshot: LetsDefend log view showing the URL artifact

![](https://cdn-images-1.medium.com/max/1024/1*OuEXJoaSUuYcet2dEZyk9g@2x.jpeg)

“Event fields: src 172.16.17.39 → dst 141.105.65.149:443 (proxy).”

Screenshot: LetsDefend fields view (source/destination/port/time)

#### 4) Endpoint commands: MSDT involvement + payload staging behavior

This is where the alert becomes especially interesting.

The endpoint command-line history included MSDT activity and follow-on staging behavior using built-in utilities (a common “LOLBin” pattern). Specifically:

• taskkill /f /im msdt.exe (MSDT process termination observed)

• decode/unpack behavior consistent with “extract ➝ decode ➝ expand ➝ execute” workflows (often used to stage payloads)

![](https://cdn-images-1.medium.com/max/1024/1*dIrY4PHkbxygfg95rKT2RA@2x.jpeg)

“Terminal history: suspicious commands executed shortly after the activity.”

Screenshot: LetsDefend Terminal History list view

![](https://cdn-images-1.medium.com/max/1024/1*EFZri-wUYNF0hRcM0yD6rw@2x.jpeg)

“Command-line detail: staging behavior observed (decode/unpack/execution pattern).”

Screenshot: Command line modal (overview)

Why MSDT matters: MSDT is commonly referenced in investigations into Follina-style execution chains, where Office content can spawn unexpected child processes and enable remote template/URL retrieval.

#### Enrichment: VirusTotal IP context

The destination IP wasn’t widely flagged (only 1/93), but the relationships and communicating artifacts still made it important in context.

![](https://cdn-images-1.medium.com/max/1024/1*yasrZ1yEusYxMC2fOcNuRQ@2x.jpeg)

“VT IP context: low detections, but relationships and artifacts still useful for triage.”

Screenshot: VT IP relations / passive DNS context

![](https://cdn-images-1.medium.com/max/1024/1*76Q-g1EKTyz109hTQ0PJ2Q@2x.jpeg)

“Vendor verdicts on the IP: low overall detection does not equal ‘safe’ — context matters.”

Screenshot: VT IP vendor detections list

#### Sandbox View: ANY.RUN supporting telemetry

ANY.RUN also showed related activity in the process/network view (supporting enrichment for the investigation).

![](https://cdn-images-1.medium.com/max/1024/1*Ggv6BylloORJBlTiJZ2lFQ@2x.jpeg)

“ANY.RUN: process/network visibility to support enrichment during triage.”

Screenshot: ANY.RUN process HTTP requests view (WINWORD.EXE context)

#### Key IOCs

**Email**

• radiosputnik@ria.ru → jonas@letsdefend.io

• Subject: “Invitation for an interview.”

• Date: Jun 02, 2022 01:51 PM

**File Hashes**

• sample.doc SHA-256: 4a24048f81afbe9fb62e7a6a49adbd1faf41f266b5f9feecdceb567aec096784

• document.xml.rels SHA-256: 62f262d180a5a48f89be19369a8425bec596bc6a02ed23100424930791ae3df0

**Network**

• IP: 141.105.65.149

• Domain: xmlformats[.]com

• URL: https://www.xmlformats.com/office/word/2022/wordprocessingDrawing/RDF8421.html

#### **Analyst Takeaways**

1. Email context is everything. A believable subject line can still defeat good instincts.

2. Don’t rely on “IP detections” alone. Low VT hits can still be part of a malicious chain.

3. Command-line + network + file reputation together = fast confidence.

4. MSDT visibility is a must-have. Even seeing attempts to terminate it is meaningful during triage.

#### What I’d Do Next

• Isolate endpoint 172.16.17.39

• Delete the email

• Pull full process tree: WINWORD.EXE → child processes

• Search enterprise-wide for:

• the file hashes above

• command-line patterns involving MSDT + decode/unpack behavior

• connections to xmlformats[.]com and the destination IP

• Validate persistence points (scheduled tasks, run keys, WMI subscriptions

![](https://medium.com/_/stat?event=post.clientViewed&referrerSource=full_rss&postId=b35d2a30f100)
