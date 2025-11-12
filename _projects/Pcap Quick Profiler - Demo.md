<iframe src="/reports/pcap-profiler/demo_report.html"
        width="100%" height="760"
        style="border:1px solid #e2e8f0;border-radius:12px"></iframe>

# PCAP Quick Profiler — Demo

**Goal.** Rapid triage of PCAPs focusing on DNS/TLS/HTTP, with simple beacon detection and a dark-mode HTML report.

**Dataset.** Small filtered slice (250 packets, ~194 KB) from an existing capture.

**Method (how it works).**
- Filters to DNS/TLS/HTTP for speed, parses via TShark JSON.
- Extracts TLS SNI/JA3 and HTTP metadata; tallies top IPs/ports.
- Beacon heuristic: low-variance inter-arrival times score higher.
- Optional allowlist (SNI/JA3) suppresses known-benign noise.

**Findings (demo).**
- No beacon suspects surfaced.
- HTTP and PKI endpoints consistent with Windows/Let’s Encrypt OCSP/CRL lookups.
- User-Agent `Microsoft-CryptoAPI/10.0` indicates certificate validation activity.

**Limitations.**
- Encrypted payloads; resumed TLS may lack SNI; thresholds may need tuning.

**What’s next.**
- Config file for thresholds/allowlist; “rare SNI/JA3” panel; non-zero exit when suspects found (CI-friendly).
