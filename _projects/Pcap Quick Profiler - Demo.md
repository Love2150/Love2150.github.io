# PCAP Quick Profiler — Demo

[▶ Open the live demo report][(tools/Pcap-profiler/out/demo_small_20251110-145852.html)](https://github.com/Love2150/security-tools/blob/main/tools/Pcap-profiler/out/demo_small_20251112-101830.html).

![PCAP Report – Demo](https://love2150.github.io/assets/images/pcap_demo.png)

**Goal.** Rapid triage of PCAPs focusing on DNS/TLS/HTTP, with simple beacon detection and a dark-mode HTML report.

**Dataset.** Small filtered slice (≈250 packets, ~194 KB) from an existing capture.

**Method (how it works).**
- Filters to DNS/TLS/HTTP for speed, parses via TShark JSON.
- Extracts TLS SNI/JA3 and HTTP metadata; tallies top IPs/ports.
- Beacon heuristic: low-variance inter-arrival times score higher.
- Optional allowlist (SNI/JA3) suppresses known-benign noise.

**Findings (demo).**
- No beacon suspects surfaced.
- HTTP/PKI endpoints consistent with Windows/Let’s Encrypt OCSP/CRL lookups.
- UA `Microsoft-CryptoAPI/10.0` indicates certificate validation activity.

**Limitations.**
- Encrypted payloads; resumed TLS may lack SNI; thresholds may need tuning.

**What’s next.**
- Config file for thresholds/allowlist; “rare SNI/JA3” panel; non-zero exit when suspects found (CI-friendly).
