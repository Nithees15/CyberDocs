<!-- SPDX-License-Identifier: GPL-3.0-or-later | Copyright (C) 2026 Nithees Narendra S -->
# Defensive Security — Track

Building, running and improving the blue team: telemetry, detection, response and hunting.

<div class="track-progress"><div class="progress" data-track-progress data-lessons="07-defensive-security/defensive-methodology.html,07-defensive-security/soc.html,07-defensive-security/siem.html,07-defensive-security/ids.html,07-defensive-security/ips.html,07-defensive-security/edr.html,07-defensive-security/xdr.html,07-defensive-security/threat-hunting.html,07-defensive-security/threat-intelligence.html,07-defensive-security/incident-response.html,07-defensive-security/detection-engineering.html,07-defensive-security/log-analysis.html,07-defensive-security/digital-forensics-intro.html,07-defensive-security/memory-forensics.html,07-defensive-security/disk-forensics.html,07-defensive-security/email-analysis.html,07-defensive-security/network-forensics.html,07-defensive-security/yara.html,07-defensive-security/sigma.html,07-defensive-security/purple-teaming.html,07-defensive-security/security-monitoring.html,07-defensive-security/vulnerability-management.html"><i></i></div><div class="tp-label" style="color:var(--muted);font-size:13px;margin-top:6px">Your progress in this track</div></div>

**Set up the lab environment below once, then work the lessons — each one is hands-on-first.**

## Lab Environment

_Set up once, then use it for every chapter in the **Defensive Security** part. Everything runs locally and isolated — you never touch a system you don't own._

A blue-team stack: ship logs into a SIEM, generate attacker telemetry, and write detections. Wazuh gives you agent telemetry, rules and a dashboard in one container set.

**What you get**

| Target | How to reach it |
| --- | --- |
| `Wazuh dashboard` | https://localhost:5601 (or :443) — SIEM/XDR UI, rules, alerts |
| `victim host + agent` | generates the telemetry you hunt over |

**Provision it** — save this as `docker-compose.yml` and run `docker compose up -d` (or import the equivalent spec into CyberForge):

```yaml
# blue-lab/docker-compose.yml  —  Defensive part environment
# Wazuh ships an official single-node compose. Pull it and bring it up:
#   git clone https://github.com/wazuh/wazuh-docker -b v4.x
#   cd wazuh-docker/single-node && docker compose up -d
# Then add a target that generates events:
services:
  victim:
    image: ubuntu:22.04
    container_name: blue-victim
    command: sleep infinity
    networks: [labnet]
  # (install the Wazuh agent in 'victim', or run Sysmon on a Windows VM,
  #  then run Atomic Red Team tests to generate detections.)

networks:
  labnet:
    driver: bridge
```

**Attacker box.** Generate telemetry with **Atomic Red Team** (`Invoke-AtomicTest`) or manual technique execution on the victim, then hunt in Wazuh/Kibana and author **Sigma** rules. **Zeek**/**Suricata** on a span port give you network detections.

**Verify it works**

- Wazuh dashboard loads and the agent on `victim` reports as active.
- An Atomic test (e.g. T1059) produces a matching alert.

**Notes**

- Wazuh single-node needs ~4 GB RAM. ELK (Elasticsearch+Kibana+Filebeat) is an alternative stack if you prefer raw log hunting.

**Teardown.** `docker compose down` stops it; add `-v` to also drop volumes. Snapshot before big changes so you can revert.

> **Safety.** Keep intentionally-vulnerable targets on an isolated/`internal` network. Never expose them to the internet or attack anything outside this lab.


## Lessons

| # | Lesson | Difficulty | Hands-on | What you'll do |
| --- | --- | --- | --- | --- |
| 1 | [Defensive Security Methodology](defensive-methodology.md) | 🟢 Beginner | ~36m | Defence in depth, the SOC operating model, detection maturity and the OODA loop. |
| 2 | [Security Operations Center](soc.md) | 🟢 Beginner | ~60m | Tiers, roles, runbooks, metrics, shift handover and alert-fatigue management. |
| 3 | [SIEM](siem.md) | 🟡 Intermediate | ~72m | Log pipelines, normalisation, correlation, use-case development and content tuning. |
| 4 | [Intrusion Detection Systems](ids.md) | 🟡 Intermediate | ~48m | Signature vs anomaly detection, sensor placement, tuning and evasion awareness. |
| 5 | [Intrusion Prevention Systems](ips.md) | 🟡 Intermediate | ~36m | Inline enforcement, fail-open/closed, false-positive risk and change control. |
| 6 | [Endpoint Detection and Response](edr.md) | 🟠 Advanced | ~72m | Sensor telemetry, behavioural detection, response actions and tamper resistance. |
| 7 | [Extended Detection and Response](xdr.md) | 🟡 Intermediate | ~36m | Cross-domain correlation, data fabric design and the promise and limits of XDR. |
| 8 | [Threat Hunting](threat-hunting.md) | 🟠 Advanced | ~72m | Hypothesis-driven hunts, the pyramid of pain, MITRE-aligned queries and hunt reporting. |
| 9 | [Threat Intelligence](threat-intelligence.md) | 🟡 Intermediate | ~60m | Intel lifecycle, strategic/operational/tactical intel, feeds and the diamond model. |
| 10 | [Incident Response](incident-response.md) | 🟠 Advanced | ~84m | PICERL lifecycle, containment strategy, evidence handling and post-incident review. |
| 11 | [Detection Engineering](detection-engineering.md) | 🟠 Advanced | ~84m | Detection as code, the detection lifecycle, testing, and reducing false positives. |
| 12 | [Log Analysis](log-analysis.md) | 🟡 Intermediate | ~60m | Sources, parsing, enrichment, and pivoting across logs to reconstruct activity. |
| 13 | [Digital Forensics Fundamentals](digital-forensics-intro.md) | 🟡 Intermediate | ~60m | Order of volatility, chain of custody, imaging and forensic soundness. |
| 14 | [Memory Forensics](memory-forensics.md) | 🟠 Advanced | ~72m | Acquisition, Volatility 3 workflows, process/handle analysis and malware in RAM. |
| 15 | [Disk Forensics](disk-forensics.md) | 🟠 Advanced | ~72m | File systems, deleted-file recovery, timelines, artefacts and carving. |
| 16 | [Email Analysis](email-analysis.md) | 🟡 Intermediate | ~36m | Header forensics, authentication results, phishing triage and attachment handling. |
| 17 | [Network Forensics](network-forensics.md) | 🟠 Advanced | ~60m | Full-packet and flow analysis, protocol reconstruction and beacon detection. |
| 18 | [YARA](yara.md) | 🟡 Intermediate | ~48m | Rule syntax, strings and conditions, performance, and building a maintainable ruleset. |
| 19 | [Sigma](sigma.md) | 🟡 Intermediate | ~48m | Generic detection rules, the taxonomy, backends and converting to SIEM queries. |
| 20 | [Purple Teaming](purple-teaming.md) | 🟠 Advanced | ~48m | Adversary emulation with Atomic Red Team, detection validation and feedback loops. |
| 21 | [Security Monitoring Architecture](security-monitoring.md) | 🟡 Intermediate | ~48m | Visibility mapping, log source coverage, retention and the MITRE DeTT&CT approach. |
| 22 | [Vulnerability Management](vulnerability-management.md) | 🟡 Intermediate | ~60m | Asset inventory, scanning cadence, risk scoring, SLAs and remediation workflows. |

**22 lessons.**

[← Repository home](../../README.md) · [Full contents](../../SUMMARY.md) · [Labs campaign](../../labs/README.md)
