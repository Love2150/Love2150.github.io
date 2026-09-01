---
layout: project
title: "Eval Unpacker"
permalink: /projects/eval_unpacker/
image: /assets/images/eval-unpacker-hero.jpg
summary: "Bounded reconstruction of classic eval(function(...)) JavaScript packer payloads without executing recovered code."
tags: [reverse-engineering, javascript, malware-analysis, dfir, python, secure-development]
status: "Tested portfolio tool"
featured: false
last_reviewed: 2026-09-01
role: "Tool developer and security analyst"
tools: [Python, Pytest, Coverage, JavaScript analysis, jsbeautifier]
outcome: "Reconstructs the first supported classic packer occurrence with explicit syntax boundaries, resource limits, UTF-8 diagnostics, and 91% core coverage."
repo: "https://github.com/Love2150/security-tools/tree/main/tools/eval-unpacker"
weight: 5
description: "Static reconstruction of a defined classic JavaScript packer family with hostile-input controls and no recovered-code execution."
---

## Executive summary

Eval Unpacker reconstructs the first supported classic `eval(function(p,a,c,k,e,d){...})(...)` packer occurrence without executing JavaScript. With `--recursive`, it follows the first nested supported occurrence at each layer.

This is a source-triage utility, not a sandbox, malware classifier, IOC extractor, or general JavaScript deobfuscation engine. Recovered source may still be malicious and must not be executed on a trusted system.

## Security engineering work

- Added malformed and adversarial tests for nested strings, escaped quotes, empty tokens, base bounds, unsupported syntax, and multiple packer calls.
- Rejects negative numeric conversion inputs.
- Limits input bytes, declared token count, token replacements, recursion depth, intermediate values, output size, and beautification input.
- Documents first-supported-occurrence behavior instead of implying every packed block is processed.
- Replaces invalid UTF-8 bytes visibly, reports the first invalid-byte offset, and never silently discards evidence.
- Provides bounded optional beautification without changing the security boundary.
- Corrected package naming, metadata, URLs, and the canonical README.

## Verification

| Control | Result |
| --- | --- |
| Python compatibility | 3.9–3.13 |
| Focused tests | 35 passed |
| Core coverage | 91% |
| Installed interfaces | `eval-unpack` and `python -m eval_unpacker.cli` |
| Package formats | Wheel and source distribution |
| Execution policy | Reconstructed JavaScript is never executed |

## Usage

```bash
python -m pip install "./tools/eval-unpacker[beautify]"
eval-unpack packed.js --recursive --beautify
cat packed.js | eval-unpack -
```

Successful output is reconstructed UTF-8 JavaScript text on standard output. Diagnostics, decoding warnings, and errors are written to standard error.

## Supported boundary

The parser accepts a quoted payload string, an integer base from 2 through 36, a non-negative token count, and either a split dictionary or literal string array. Other packer families, runtime-keyed decryption, custom virtual machines, and dynamic token expressions are outside scope.

## Evidence

- [Canonical package](https://github.com/Love2150/security-tools/tree/main/tools/eval-unpacker)
- [Architecture and trust boundaries](https://github.com/Love2150/security-tools/blob/main/docs/ARCHITECTURE.md)
- [Portfolio case studies](https://github.com/Love2150/security-tools/blob/main/docs/PORTFOLIO.md)
- [Hostile-input hardening pull request](https://github.com/Love2150/security-tools/pull/5)
