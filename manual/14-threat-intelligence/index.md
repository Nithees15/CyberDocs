<!-- SPDX-License-Identifier: GPL-3.0-or-later | Copyright (C) 2026 Nithees Narendra S -->
# Threat Intelligence and Frameworks — Track

The shared vocabularies, catalogues and scoring systems that connect every other domain.

<div class="track-progress"><div class="progress" data-track-progress data-lessons="14-threat-intelligence/cti-fundamentals.html,14-threat-intelligence/mitre-attack.html,14-threat-intelligence/attack-navigator.html,14-threat-intelligence/d3fend.html,14-threat-intelligence/capec.html,14-threat-intelligence/cwe.html,14-threat-intelligence/cve.html,14-threat-intelligence/cvss.html,14-threat-intelligence/epss.html,14-threat-intelligence/kev.html,14-threat-intelligence/osint-intelligence.html,14-threat-intelligence/ioc-ioa.html,14-threat-intelligence/ttp-analysis.html,14-threat-intelligence/diamond-model.html,14-threat-intelligence/threat-intel-platforms.html,14-threat-intelligence/attribution.html"><i></i></div><div class="tp-label" style="color:var(--muted);font-size:13px;margin-top:6px">Your progress in this track</div></div>

**Set up the lab environment below once, then work the lessons — each one is hands-on-first.**

## Lab Environment

_Set up once, then use it for every chapter in the **Threat Intelligence and Frameworks** part. Everything runs locally and isolated — you never touch a system you don't own._

This part is mostly conceptual and tool-driven — no dedicated vulnerable targets are needed. Work from Kali (or any Linux box) and the tools called out in each chapter.

**What you get**

| Target | How to reach it |
| --- | --- |
| `Kali / local shell` | everything you need is a terminal and the tools named per chapter |

**Provision it** — save this as `docker-compose.yml` and run `docker compose up -d` (or import the equivalent spec into CyberForge):

```yaml
# Optional scratch box for trying commands in isolation:
services:
  scratch:
    image: kalilinux/kali-rolling        # or debian:stable-slim
    container_name: scratch
    command: sleep infinity
    networks: [labnet]
networks:
  labnet: { driver: bridge, internal: true }
```

**Attacker box.** Run the chapter's commands directly on Kali, or in the disposable `scratch` container to keep your main system clean.

**Verify it works**

- `docker exec -it scratch bash` gives an isolated shell.

**Teardown.** `docker compose down` stops it; add `-v` to also drop volumes. Snapshot before big changes so you can revert.

> **Safety.** Keep intentionally-vulnerable targets on an isolated/`internal` network. Never expose them to the internet or attack anything outside this lab.


## Lessons

| # | Lesson | Difficulty | Hands-on | What you'll do |
| --- | --- | --- | --- | --- |
| 1 | [Cyber Threat Intelligence Fundamentals](cti-fundamentals.md) | 🟢 Beginner | ~48m | The intel lifecycle, requirements, collection, analysis and dissemination. |
| 2 | [MITRE ATT&CK](mitre-attack.md) | 🟡 Intermediate | ~72m | Tactics, techniques, sub-techniques, matrices, and using ATT&CK to drive detection. |
| 3 | [ATT&CK Navigator](attack-navigator.md) | 🟡 Intermediate | ~30m | Building layers, heatmaps, coverage mapping and gap analysis. |
| 4 | [MITRE D3FEND and Engage](d3fend.md) | 🟡 Intermediate | ~30m | Countermeasure knowledge graph, mapping defences and adversary engagement. |
| 5 | [CAPEC](capec.md) | 🟡 Intermediate | ~36m | Attack pattern catalogue, relationships to CWE and using CAPEC in threat models. |
| 6 | [CWE](cwe.md) | 🟡 Intermediate | ~36m | Weakness taxonomy, views, relationships and mapping findings correctly. |
| 7 | [CVE](cve.md) | 🟢 Beginner | ~30m | Identifiers, the CNA ecosystem, records, and using CVEs responsibly. |
| 8 | [CVSS](cvss.md) | 🟢 Beginner | ~36m | Base/temporal/environmental metrics, v3.1 vs v4.0 and scoring pitfalls. |
| 9 | [EPSS](epss.md) | 🟢 Beginner | ~30m | Exploit prediction scoring, interpretation and combining EPSS with CVSS and KEV. |
| 10 | [CISA KEV and Prioritisation](kev.md) | 🟢 Beginner | ~30m | Known-exploited-vulnerability catalogue and risk-based patch prioritisation. |
| 11 | [OSINT for Intelligence](osint-intelligence.md) | 🟡 Intermediate | ~48m | Collection tradecraft, verification, source reliability and analytic bias. |
| 12 | [Indicators: IOC and IOA](ioc-ioa.md) | 🟡 Intermediate | ~36m | Atomic/computed/behavioural indicators, the pyramid of pain and indicator decay. |
| 13 | [TTP Analysis](ttp-analysis.md) | 🟠 Advanced | ~48m | Behaviour-centric analysis, ATT&CK mapping and building adversary profiles. |
| 14 | [The Diamond Model and Kill Chains](diamond-model.md) | 🟡 Intermediate | ~36m | Adversary/infrastructure/capability/victim, kill chains and unified frameworks. |
| 15 | [Threat Intelligence Platforms and Sharing](threat-intel-platforms.md) | 🟡 Intermediate | ~36m | MISP, STIX/TAXII, TLP, feeds and operationalising shared intelligence. |
| 16 | [Attribution](attribution.md) | 🟠 Advanced | ~36m | Evidence, confidence, false flags and the limits of attribution. |

**16 lessons.**

[← Repository home](../../README.md) · [Full contents](../../SUMMARY.md) · [Labs campaign](../../labs/README.md)
