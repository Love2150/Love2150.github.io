---
layout: null
title: "PCAP Quick Profiler"
date: 2025-10-10 09:00:00 -0600
image: "/assets/images/Pcap-profiler.png"
summary: "Windows-friendly PCAP triage: protocols, top IPs/ports, HTTP/TLS metadata, and auto reports."
tags: [dfir, networking, windows, python]
repo: "https://github.com/Love2150/security-tools/tree/main/tools/Pcap-profiler"
weight: 10
---

## 🧠 PCAP Quick Profiler
Automated network traffic triage for `.pcap` / `.pcapng` using Python + PyShark (TShark). Get instant summaries (protocols, top IPs/ports, HTTP/TLS metadata, and throughput) and save JSON/CSV reports.

### 🔍 Overview
Built on Wireshark’s TShark, this tool turns raw captures into structured, readable insights for analysts, SOC teams, and threat hunters.

### ⚙️ Key Features
- **Protocol Summary:** TCP/UDP/HTTP/DNS/SMB/TLS…
- **IP & Port Analysis:** Top src/dst IPs and ports
- **HTTP & TLS Insight:** Hosts, User-Agents, URLs, content-types, JA3, SNI
- **Performance Metrics:** Packets, bytes, duration, avg throughput
- **Auto Reports:** JSON + CSV to `reports/pcap-profiler/`

### 🧰 Tech
Python 3.11+, PyShark (TShark), asyncio, JSON/CSV

### 📊 Example Output
Packets: 2,011
Bytes: 116,672
Start: 2010-07-04T15:24:16Z
End: 2010-07-04T15:24:39Z
Duration: 23.09s Avg throughput: 4.9 KB/s

🖧 Protocols:

TCP (2011)

🌍 Top Source IPs:

172.16.0.8 (1994)

64.13.134.52 (17)

🔢 Top Destination Ports:

36050 (16), 443 (2), 3306 (2)

markdown
Copy code

### 🧩 Advanced
- Custom **decode-as** (e.g. `tcp.port==36050,http`)
- JSON **config profiles**
- Timestamp normalization for legacy PCAPs
- Windows-friendly event-loop handling

### 📈 Real-World Uses
| Use Case | Benefit |
|---|---|
| Incident Response | Quickly spot compromised hosts/flows |
| Threat Hunting | Surface C2 beacons or anomalies |
| SOC Triage | Fast pre-Wireshark summary |
| Malware Analysis | Trace exfil/beaconing patterns |

### 🔗 Links
- 🔧 **Repo:** <https://github.com/Love2150/security-tools/tree/main/tools/Pcap-profiler>
- 🧑‍💻 **Let’sDefend:** <https://app.letsdefend.io/user/shinyhunter>
- 💼 **LinkedIn:** <https://www.linkedin.com/in/brandon-love-85b247261>
