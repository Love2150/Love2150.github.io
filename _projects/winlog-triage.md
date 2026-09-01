---
layout: project
title: "Windows Log Triage"
permalink: /projects/winlog-triage/
image: /assets/images/wintriage_demo.png
summary: "Installable EVTX/Sysmon triage with parser-completeness metadata, validated IOCs, lightweight rules, and protected reports."
tags: [dfir, windows, sysmon, evtx, python, secure-development]
status: "Tested portfolio tool"
featured: true
last_reviewed: 2026-09-01
role: "Tool developer and security analyst"
tools: [Python, EVTX, Sysmon, PowerShell, Jinja2, HTML, JSON, CSV]
outcome: "Produces escaped HTML and machine-readable reports while exposing records read, records skipped, parse errors, and parser backend."
outcome_label: "Verified result"
weight: 8
repo: "https://github.com/Love2150/security-tools/tree/main/tools/winlog-triage"
demo: "/reports/wintriage/demo_report.html"
description: "Defensive Windows event-log triage with safe path handling, parsing-completeness metadata, validated indicators, and portable reports."
---

## Executive summary

Windows Log Triage processes EVTX and Sysmon evidence into normalized events, IOC candidates, lightweight behavior leads, process/network summaries, and portable reports.

The tool makes incomplete analysis visible. Its JSON result records the parser backend, records read, records skipped, and parse-error count. Rules are triage heuristics rather than full Sigma coverage or detection verdicts.

## Security engineering work

- Split reading, normalization, IOC extraction, rules, analysis, reporting, and CLI behavior into focused modules.
- Passes EVTX paths to PowerShell through an environment variable and uses `-LiteralPath` instead of interpolating paths into commands.
- Surfaces PowerShell subprocess failures.
- Imports `xmltodict` independently from `python-evtx` so fallback behavior is explicit.
- Validates IPv4 candidates with Python's `ipaddress` module.
- Rejects non-positive `--max-per-file` values.
- Escapes attacker-controlled evidence in HTML and applies restrictive browser protections.
- Labels intentionally limited processing through completeness metadata rather than silently presenting partial results as complete.

## Measured validation

A clean-wheel run against sanitized EVTX data recorded:

| Metric | Result |
| --- | ---: |
| Records read | 5 |
| Records skipped | 0 |
| Parse errors | 0 |

Repository CI builds and installs the package, exercises `winlog-triage` and `python -m winlog_triage`, runs the complete test suite across supported Python versions, and feeds the stable aggregate quality gate.

## Sanitized demonstration

<div class="meta" style="margin:.5rem 0 1rem;display:flex;gap:.5rem;flex-wrap:wrap">
  <a class="pill" href="{{ '/reports/wintriage/demo_report.html' | relative_url }}" target="_blank" rel="noopener">Open sanitized demonstration report ↗</a>
  <a class="pill" href="{{ page.repo }}" target="_blank" rel="noopener">Repository ↗</a>
</div>

<iframe class="embedded-report-preview"
  title="Sanitized Windows Log Triage demonstration"
  src="{{ '/reports/wintriage/demo_report.html' | relative_url }}?v={{ site.time | date: '%s' }}"
  width="100%" height="760"
  style="border:1px solid #e2e8f0;border-radius:12px">
</iframe>

## Outputs and limitations

- JSON: complete machine-readable summary and parsing metadata
- CSV: representative normalized event rows
- HTML: escaped summary and evidence fields with restrictive browser protections

Reports may contain sensitive usernames, hostnames, command lines, paths, and indicators. Do not execute commands or browse extracted indicators. Preserve original EVTX evidence separately.

## Evidence

- [Canonical package](https://github.com/Love2150/security-tools/tree/main/tools/winlog-triage)
- [Architecture and trust boundaries](https://github.com/Love2150/security-tools/blob/main/docs/ARCHITECTURE.md)
- [Portfolio case studies](https://github.com/Love2150/security-tools/blob/main/docs/PORTFOLIO.md)
- [Packaging and hardening pull request](https://github.com/Love2150/security-tools/pull/4)
