<!-- SPDX-License-Identifier: GPL-3.0-or-later | Copyright (C) 2026 Nithees Narendra S -->
# Digital Forensics and Incident Response — Track

Evidence-driven investigation across memory, disk, network and cloud, kept forensically sound.

<div class="track-progress"><div class="progress" data-track-progress data-lessons="13-digital-forensics/dfir-fundamentals.html,13-digital-forensics/memory-forensics-deep.html,13-digital-forensics/disk-forensics-deep.html,13-digital-forensics/browser-forensics.html,13-digital-forensics/cloud-forensics.html,13-digital-forensics/email-forensics.html,13-digital-forensics/log-forensics.html,13-digital-forensics/timeline-analysis.html,13-digital-forensics/mobile-forensics.html,13-digital-forensics/anti-forensics.html,13-digital-forensics/malware-forensics.html,13-digital-forensics/forensic-reporting.html"><i></i></div><div class="tp-label" style="color:var(--muted);font-size:13px;margin-top:6px">Your progress in this track</div></div>

**Set up the lab environment below once, then work the lessons — each one is hands-on-first.**

## Lab Environment

_Set up once, then use it for every chapter in the **Digital Forensics and Incident Response** part. Everything runs locally and isolated — you never touch a system you don't own._

A forensics workbench with the analysis tools pre-installed. Bring your own disk/memory images (CyberDefenders and public DFIR datasets are ideal, and safe).

**What you get**

| Target | How to reach it |
| --- | --- |
| `dfir-box` | Volatility 3, Sleuth Kit/Autopsy, plaso, RegRipper, Chainsaw |

**Provision it** — save this as `docker-compose.yml` and run `docker compose up -d` (or import the equivalent spec into CyberForge):

```yaml
# dfir-lab/docker-compose.yml  —  Forensics part environment
services:
  dfir-box:
    image: sk4la/plaso                    # plaso + timeline tooling; or build a custom SIFT-like image
    container_name: dfir-box
    command: sleep infinity
    volumes:
      - ./evidence:/evidence:ro           # drop disk/memory images here (read-only)
    networks: [labnet]

networks:
  labnet:
    driver: bridge
    internal: true
```

**Attacker box.** You're the investigator. Work inside `dfir-box` over the read-only `/evidence` mount: `vol -f mem.raw windows.pslist`, `log2timeline.py`, `mmls`/`fls` (Sleuth Kit). Keep originals read-only and work on copies/hashes.

**Verify it works**

- `docker exec -it dfir-box vol -h` runs Volatility 3.
- Your image appears under `/evidence` inside the container.

**Notes**

- Use public, shareable DFIR datasets (CyberDefenders, DFIR CTFs). Never process real case evidence in a teaching lab.

**Teardown.** `docker compose down` stops it; add `-v` to also drop volumes. Snapshot before big changes so you can revert.

> **Safety.** Keep intentionally-vulnerable targets on an isolated/`internal` network. Never expose them to the internet or attack anything outside this lab.


## Lessons

| # | Lesson | Difficulty | Hands-on | What you'll do |
| --- | --- | --- | --- | --- |
| 1 | [DFIR Fundamentals](dfir-fundamentals.md) | 🟢 Beginner | ~48m | Forensic principles, order of volatility, chain of custody and legal admissibility. |
| 2 | [Memory Forensics in Depth](memory-forensics-deep.md) | 🟠 Advanced | ~84m | Acquisition, structures, plugins, rootkit hunting and reconstructing execution. |
| 3 | [Disk Forensics in Depth](disk-forensics-deep.md) | 🟠 Advanced | ~84m | NTFS/ext4/APFS internals, journaling, carving, and building a super timeline. |
| 4 | [Browser Forensics](browser-forensics.md) | 🟡 Intermediate | ~48m | History, cache, cookies, storage, downloads and reconstructing user activity. |
| 5 | [Cloud Forensics](cloud-forensics.md) | 🟠 Advanced | ~60m | Log-centric investigation, API-based acquisition and the limits of cloud evidence. |
| 6 | [Email Forensics](email-forensics.md) | 🟡 Intermediate | ~36m | Header analysis, transport reconstruction, mailbox artefacts and BEC investigation. |
| 7 | [Log Forensics](log-forensics.md) | 🟡 Intermediate | ~48m | Windows event logs, Linux logs, correlation and detecting anti-forensics. |
| 8 | [Timeline Analysis](timeline-analysis.md) | 🟠 Advanced | ~60m | Super timelines with plaso, pivoting, anchor events and narrative reconstruction. |
| 9 | [Mobile Forensics](mobile-forensics.md) | 🟠 Advanced | ~60m | Acquisition tiers, app data, secure enclaves and the constraints of modern devices. |
| 10 | [Anti-Forensics](anti-forensics.md) | 🟠 Advanced | ~36m | Timestomping, log clearing, wiping, and how investigators detect tampering. |
| 11 | [Malware-Focused Forensics](malware-forensics.md) | 🟠 Advanced | ~48m | Finding, extracting and triaging malicious artefacts during an investigation. |
| 12 | [Forensic Reporting](forensic-reporting.md) | 🟡 Intermediate | ~36m | Findings documentation, defensibility, expert-witness basics and executive summaries. |

**12 lessons.**

[← Repository home](../../README.md) · [Full contents](../../SUMMARY.md) · [Labs campaign](../../labs/README.md)
