---
layout: project
title: "PCAP Quick Profiler"
permalink: /projects/pcap-quick-profiler/
image: /assets/images/pcap_demo.png
summary: "Installable PCAP triage with complete-capture statistics, HTTP/TLS evidence, CSP-protected reports, and public-unicast-filtered VirusTotal enrichment."
tags: [dfir, networking, python, tshark, secure-development]
status: "Tested portfolio tool"
featured: true
last_reviewed: 2026-09-01
role: "Tool developer and security analyst"
tools: [Python, TShark, PyShark, PCAP, HTTP, TLS, JA3, VirusTotal]
outcome: "Produces JSON, CSV, text, and CSP-protected HTML; complete-capture totals were independently validated and installed entry points are exercised by Repository CI."
repo: "https://github.com/Love2150/security-tools/tree/main/tools/pcap-profiler"
demo: "/reports/pcap-profiler/demo_report.html"
weight: 10
description: "Secure first-pass PCAP profiling with complete-capture statistics, focused HTTP/TLS analysis, and optional public-unicast IP enrichment."
---

## Executive summary

PCAP Quick Profiler converts packet captures into a fast first-pass analyst view: complete packet/byte totals, protocol mix, top endpoints and ports, HTTP/TLS observations, JA3 values, and heuristic beacon leads.

It is a triage tool, not a maliciousness verdict. Encrypted payloads are not decrypted, heuristic findings require validation, and generated reports can contain sensitive or attacker-controlled evidence.

## Security and correctness work

- Escapes attacker-controlled report fields and applies restrictive Content Security Policy protection.
- Reports complete-capture packet and byte totals instead of presenting a focused protocol subset as the whole capture.
- Consolidates execution under one canonical installable package.
- Exercises `pcap-profiler`, `pcap-profiler-vt`, and `python -m pcap_quick_profiler` from built wheels.
- Restricts VirusTotal enrichment to validated, globally routable unicast IPv4/IPv6 values.
- Rejects private, reserved, multicast, ULA, and malformed candidates both at report extraction and immediately before requests.
- Keeps `VT_API_KEY` in the environment and never writes it into reports.

## Measured validation

- A historical sample was independently confirmed with TShark at 13 packets and 1,590 bytes.
- Repository CI generates a deterministic one-packet, 60-byte fixture with source `10.1.1.1`, destination `10.2.2.2`, and UDP destination port `53`.
- The expanded verifier checks packet count, byte count, source, destination, and port.
- Package builds, clean-installed entry points, dependency auditing, secret scanning, and supported Python versions are enforced by Repository CI.

## Demonstration

<p class="meta">
  <a href="{{ '/reports/pcap-profiler/demo_report.html' | relative_url }}" target="_blank" rel="noopener">Open sanitized demonstration report ↗</a>
</p>

{% include pcap-demo-iframe.html %}

## Outputs

- JSON machine-readable summary
- CSV endpoint and port counts
- Human-readable text summary
- Escaped, CSP-protected HTML report
- Optional VirusTotal JSON and Markdown enrichment reports

## Evidence

- [Canonical package](https://github.com/Love2150/security-tools/tree/main/tools/pcap-profiler)
- [Architecture and trust boundaries](https://github.com/Love2150/security-tools/blob/main/docs/ARCHITECTURE.md)
- [Portfolio case studies](https://github.com/Love2150/security-tools/blob/main/docs/PORTFOLIO.md)
- [Phase 1 security remediation](https://github.com/Love2150/security-tools/pull/1)
- [Phase 2 package consolidation](https://github.com/Love2150/security-tools/pull/2)
- [Phase 8 outbound-data hardening](https://github.com/Love2150/security-tools/pull/9)
