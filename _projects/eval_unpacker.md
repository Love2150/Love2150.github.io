---
title: "eval-unpacker (JS packer unpacker)"
tags: ["python", "reverse-engineering", "malware-analysis"]
image: "/assets/images/eval-unpacker-hero.png"   # optional screenshot
repo: "https://github.com/Love2150/eval-unpacker"
description: "CLI tool to unpack JavaScript packed via eval(function(p,a,c,k,e,d)...) with safe two-pass token replacement, optional beautify, and recursive mode."
---

**Highlights**
- Detects and unpacks obfuscated JS packer payloads
- Optional `--beautify` (jsbeautifier)
- Recursive unpacking for nested wrappers
