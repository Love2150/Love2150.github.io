---
layout: page
title: "eval_unpacker — JavaScript De-obfuscation Toolkit"
permalink: /projects/eval_unpacker/
image: /assets/images/eval-unpacker-hero.jpg
summary: "Detects and safely unpacks common JS obfuscators (Packer, base64 chains, array-join loaders), extracts IOCs, and beautifies output."
tags: [reverse-engineering, javascript, malware-analysis, dfir, python]
repo: "https://github.com/Love2150/security-tools/tree/main/tools/eval_unpacker"
weight: 5
description: "A Python-based static de-obfuscation tool that detects Dean Edwards Packer (eval(function(p,a,c,k,e,d){…})), layered base64, escaped Unicode/hex, atob wrappers, and array-join loaders. Produces beautified code + extracted IOCs for rapid triage."
---

## What is it?
`eval_unpacker` is a **static JavaScript de-obfuscation** tool for analysts. It **does not execute** attacker code. Instead, it detects common packers, repeatedly **decodes layers** (base64/hex/`%uXXXX`/`\xNN`/`\uNNNN`/`unescape`/`atob`), reconstructs array-join loaders, and finally **beautifies** the result and **extracts IOCs** (domains, URLs, IPs, hashes, emails).

- No `eval`/VM runtime — safe pattern/AST-assisted approach  
- Layered decoding until stable (or max passes)  
- One-shot triage: readable output + IOCs + JSON summary

---

## What it detects/unpacks
- **Dean Edwards Packer**: `eval(function(p,a,c,k,e,d){…})`
- **Layered encodings**: base64 → hex → `%uXXXX`/`\xNN`/`\uNNNN` → `unescape`/`atob`
- **Array-join loaders**: `['h','t','t','p'].join('')`, chunk rebuild patterns
- **String spreading/noise**: split/concat and replace-maps that rebuild payloads
- **Heuristics**:
  - JSFuck indicators (`!+[]` etc.)
  - anti-debug snippets (`Function('debugger')`)
  - suspicious endpoints (`/gate.php`, `/admin/`)

> Focuses on mainstream, automatable obfuscations common in loaders/web skimmers. Complex custom VMs typically require sandboxing.

---

## Quick start
```powershell
# 1) Create & activate venv (Windows PowerShell)
python -m venv .venv
.\.venv\Scripts\Activate.ps1

# 2) Install deps
python -m pip install -U jsbeautifier chardet

# 3) Run on a file or folder
python eval_unpacker.py .\samples\packed.js --out .\out
````

---

## CLI usage

```text
usage: eval_unpacker.py [-h] [--out OUTDIR] [--max-passes N] [--beautify {on,off}]
                        [--json JSON_OUT] [--txt TXT_OUT] [--ioc IOC_OUT]
                        target_path

positional arguments:
  target_path           File or directory of .js/.txt/.html to analyze

options:
  -h, --help            show this help message and exit
  --out OUTDIR          Output directory (default: ./out)
  --max-passes N        Max decode passes (default: 6)
  --beautify {on,off}   Beautify final JS (default: on)
  --json JSON_OUT       Write machine-readable result summary
  --txt TXT_OUT         Write human-readable summary
  --ioc IOC_OUT         Write extracted IOCs (text)
```

---

## Output (example)

**Console summary**

```
[eval_unpacker] target: samples\packed.js
  • Detected: Packer, base64 chain (2 layers), %uXXXX escapes
  • Passes: 4 → stabilized
  • IOCs: 3 domains, 2 URLs, 1 IPv4
  • Output:
      - out\packed.decoded.js
      - out\packed.ioc.txt
      - out\packed.summary.json
```

**IOC file (`*.ioc.txt`)**

```
domains:
  - cdn-stat-assets.com
  - update-checker.net
urls:
  - https://cdn-stat-assets.com/g/loader.js
  - http://update-checker.net/ping.php
ipv4:
  - 185.199.110.153
```

---

## How it works (high-level)

1. **Sniff** obfuscation signatures (regex + token checks).
2. **Unpack** in passes: Packer → base64/hex → escape normalization → `atob/unescape` → array-join rebuild.
3. **Beautify** final JavaScript (`jsbeautifier`, or `prettier` if you add it).
4. **Extract IOCs** (domains/URLs/IPs/emails/hashes), de-dupe and sort.
5. **Report** to console + write decoded JS, IOC list, and JSON summary.

---

## Why analysts like it

* **Fast triage** — answer “what is this?” in seconds
* **Repeatable** — deterministic output, ideal for case notes/PRs
* **Readable** — beautified code for code-review/YARA/Sigma drafting
* **Portable** — pure-Python, works offline

---

## Limitations

* Custom VM protectors and runtime-keyed decryptors won’t fully de-virtualize.
* Heavy anti-analysis (WASM VMs, canvas/audio crypto) needs sandboxing.
* Encrypted blobs (RC4/AES) are flagged but not always decrypted without keys.

---

## Roadmap

* Extra array-mangling/AST rebuild patterns
* Optional `prettier` backend (auto-detect if Node is present)
* Skimmer family signatures (magecart-style)
* SARIF/JSONL export for CI pipelines

---

## Links

* **Repo:** <{{ page.repo }}>
* **Related project:** PCAP Quick Profiler → {{ '/projects/pcap-quick-profiler/' | relative_url }}

---

## Notes for this site

* The header image path is `/assets/images/eval_unpacker.png`.
  Add a screenshot or diagram at that path to show a hero image.

```
```
