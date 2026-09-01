---
layout: project
title: "Security Tools Engineering Portfolio"
permalink: /projects/security-tools-engineering/
summary: "A phased security-engineering program covering hostile-input handling, analytical correctness, Python packaging, evidence provenance, CI/CD, and release governance."
tags: [security-engineering, dfir, python, secure-development, ci-cd]
status: "Eight phases passed separate fail-closed review"
featured: false
last_reviewed: 2026-09-01
role: "Security engineer, tool developer, and analyst"
tools: [Python, Pytest, Ruff, TShark, GitHub Actions, Gitleaks, pip-audit, Mermaid]
outcome: "Hardened three defensive tools through nine reviewable pull requests, 79 automated tests, clean-install package checks, and a stable aggregate CI result suitable for branch protection."
repo: "https://github.com/Love2150/security-tools"
weight: 4
description: "Security engineering case studies spanning PCAP, EVTX, packed JavaScript, hostile-input testing, package assurance, evidence governance, and CI/CD."
---

## Executive summary

This repository began as three useful analyst scripts and was developed into a tested, installable, and governed defensive-security portfolio. Eight engineering phases plus the documentation foundation were delivered through nine pull requests, so each security, correctness, packaging, and CI decision remains reviewable.

The tools remain triage aids rather than detection verdicts. Inputs and resulting report fields are treated as attacker influenced, and findings require validation against original evidence.

## Security engineering highlights

- Escaped attacker-controlled PCAP and EVTX report fields and added restrictive Content Security Policy protection.
- Corrected full-capture packet and byte totals against independent TShark measurements.
- Consolidated duplicate code into canonical installable packages and exercised built wheels in clean environments.
- Added parser-completeness metadata so skipped EVTX records and parse errors are visible to analysts.
- Bounded Eval Unpacker input, tokens, replacements, recursion, intermediate data, and output growth without executing reconstructed JavaScript.
- Removed 57 generated report/output files and seven PCAP/EVTX samples without established redistribution permission.
- Added provenance requirements for retained evidence: origin, creator, permission, SHA-256, expected indicators, and sanitization status.
- Added Repository CI across supported Python versions, builds, installed entry points, TShark integration, dependency auditing, secret scanning, and a stable aggregate gate.
- Added governance, private vulnerability reporting, MIT licensing, and a fail-closed release procedure.

## VirusTotal egress hardening

Independent portfolio review exposed a VirusTotal disclosure path: Python's `ipaddress.is_global` can include multicast addresses. The final implementation accepts only globally routable unicast IPv4/IPv6 candidates and rejects private, reserved, multicast, ULA, and malformed values both when profiler JSON is loaded and immediately before network requests.

Regression tests include IPv4 multicast, IPv6 multicast, private, ULA, reserved, malformed, and public-unicast cases and prove rejected candidates never reach the VirusTotal request function.

## Measured verification

| Control | Verified result |
| --- | --- |
| Complete repository suite | 79 tests passed |
| Eval Unpacker core coverage | 91% |
| Supported Python range | 3.9 boundary plus 3.10–3.13 shared matrix |
| Package assurance | A wheel and source distribution for each of three packages; clean-installed entry-point smokes |
| Network integration | Deterministic one-packet TShark fixture; 60 bytes; UDP destination port 53 |
| Supply-chain controls | Strict dependency audit and secret scanning |
| Documentation assurance | Parsed schemas, live CLI parity, internal links, and rendered Mermaid architecture |
| Independent review | Separate fail-closed AI review plus executable tests; final review passed with no security concerns or blockers |

## Architecture and case studies

- [Portfolio guide and six case studies](https://github.com/Love2150/security-tools/blob/main/docs/PORTFOLIO.md)
- [Architecture and trust boundaries](https://github.com/Love2150/security-tools/blob/main/docs/ARCHITECTURE.md)
- [Security policy](https://github.com/Love2150/security-tools/blob/main/SECURITY.md)
- [Repository CI](https://github.com/Love2150/security-tools/blob/main/.github/workflows/repository-ci.yml)
- [Release procedure](https://github.com/Love2150/security-tools/blob/main/docs/RELEASING.md)

## Phased evidence

| Pull request | Focus |
| --- | --- |
| [#1](https://github.com/Love2150/security-tools/pull/1) | Report injection and analytical correctness |
| [#2](https://github.com/Love2150/security-tools/pull/2) | Canonical PCAP package |
| [#3](https://github.com/Love2150/security-tools/pull/3) | Documentation foundation |
| [#4](https://github.com/Love2150/security-tools/pull/4) | Windows Log Triage packaging and hardening |
| [#5](https://github.com/Love2150/security-tools/pull/5) | Eval Unpacker hostile-input controls |
| [#6](https://github.com/Love2150/security-tools/pull/6) | Repository hygiene and evidence provenance |
| [#7](https://github.com/Love2150/security-tools/pull/7) | Repository-wide quality gates |
| [#8](https://github.com/Love2150/security-tools/pull/8) | Governance and release readiness |
| [#9](https://github.com/Love2150/security-tools/pull/9) | Employer presentation and VirusTotal disclosure hardening |

## Skills demonstrated

Threat modeling, defensive parsing, secure report generation, analytical validation, test-driven remediation, Python packaging, CI/CD security, evidence governance, release engineering, technical writing, and independent review.
