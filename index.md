<!-- SPDX-License-Identifier: GPL-3.0-or-later | Copyright (C) 2026 Nithees Narendra S -->
# Cybersecurity-Mastery

<p align="center"><em>Learn security by <strong>doing</strong> it — an offline, interactive, hands-on learning app that turns 293 lessons across 16 tracks into runnable labs, not walls of text.</em></p>

<p align="center">
  <a href="LICENSE"><img alt="License: GPL v3" src="https://img.shields.io/badge/license-GPLv3-2ea043.svg"></a>
  <a href="https://github.com/Nithees15/CyberDocs/actions/workflows/build.yml"><img alt="Build" src="https://github.com/Nithees15/CyberDocs/actions/workflows/build.yml/badge.svg"></a>
  <a href="https://nithees15.github.io/CyberDocs/"><img alt="Live site" src="https://img.shields.io/badge/live-GitHub%20Pages-2ea043"></a>
  <img alt="293 lessons" src="https://img.shields.io/badge/lessons-293-2ea043">
  <img alt="~75% hands-on" src="https://img.shields.io/badge/hands--on-~75%25-2ea043">
  <img alt="Works offline" src="https://img.shields.io/badge/works-offline-2ea043">
</p>

**Cybersecurity-Mastery** is a self-contained security learning app you run on your own machine. Instead of *reading about* attacks and defences, you **perform** them: each lesson opens with a short, plain-English **Overview**, then hands you a full **lab** — provision an isolated target, follow a step-by-step walkthrough where **every command has a Run and a Copy button**, watch the real output, take an instant quiz, and finish with a *detect-and-defend* debrief. Theory is about a quarter of each page; the rest is doing.

**▶ Live site:** <https://nithees15.github.io/CyberDocs/> &nbsp;·&nbsp; **Run locally:** `python _meta/build_site.py`, then open `site/index.html`.

> **16 tracks · 293 lessons · 6 boss labs · 89 tool guides · 100 projects · 28 cheatsheets · GPL-3.0.**

---

## Why it's different

- **Hands-on first (~75/25).** The centre of gravity of every lesson is a lab, not prose — short theory, then you build.
- **The commands actually run.** With the optional **Lab Runner** (`labserver/`), **▸ Run** and the **Live Terminal** execute each command *inside an isolated Kali container* (`docker exec`) — never on your host. No backend running? Everything still works via **📋 Copy**.
- **Everything is local and isolated.** Targets are intentionally-vulnerable apps — bWAPP, DVWA, OWASP Juice Shop, Metasploitable, GOAD, LocalStack — on fail-closed networks. Nothing here touches systems you don't own.
- **Structured like a course.** 16 tracks, a one-command lab environment per track, saved progress and quizzes, and cross-topic **boss labs** — full kill-chains that chain many lessons together.
- **One source of truth.** The entire site is produced by a small, data-driven generator in [`_meta/`](_meta/README.md): no dead links, no duplication, fully reproducible.

## Quick start

**1. Open the app.** No server, no build tools, works offline:

```bash
git clone https://github.com/Nithees15/CyberDocs.git
# then open site/index.html in your browser  (or run: python _meta/build_site.py to rebuild it)
```

Prefer to read on GitHub? Start from [SUMMARY.md](SUMMARY.md) or jump straight into a track below.

**2. Run commands for real (optional).** Start the Lab Runner, then connect the site to it:

```bash
python labserver/server.py     # binds to 127.0.0.1 and prints a one-time session token
```

In any lesson, click **Connect lab runner** in the Live Terminal card and paste the token — now **▸ Run** executes inside your Kali container, and **▸ Start lab** brings up that track's targets (compose files live in [`labs/environments/`](labs/environments/)). Everything stays on isolated, fail-closed networks. See [labserver/README.md](labserver/README.md).

**3. Follow the campaign.** [labs/README.md](labs/README.md) orders every lab by track and caps each with a cross-topic **boss lab** — a full kill-chain that combines many lessons.

## Tracks

| # | Track | Lessons | Focus |
| --- | --- | --- | --- |
| 00 | [Foundations](manual/00-foundations/README.md) | 25 | The computer science, systems and programming groundwork every security discipline is built on. |
| 01 | [Networking](manual/01-networking/README.md) | 25 | Protocol-by-protocol internals, on the wire. |
| 02 | [Cryptography](manual/02-cryptography/README.md) | 18 | Primitives, protocols and the failure modes that turn strong maths into broken systems. |
| 03 | [Web Security](manual/03-web-security/README.md) | 21 | How the web platform works, how its trust boundaries are drawn, and where they leak. |
| 04 | [Vulnerabilities](manual/04-vulnerabilities/README.md) | 30 | Bug classes from first principles: root cause, exploitation, detection and durable fixes. |
| 05 | [Platforms](manual/05-platforms/README.md) | 15 | Security architecture, attack surface and hardening for each major platform family. |
| 06 | [Offensive Security](manual/06-offensive-security/README.md) | 24 | The attacker's methodology end to end, structured on the cyber kill chain and MITRE ATT&CK. |
| 07 | [Defensive Security](manual/07-defensive-security/README.md) | 22 | Building, running and improving the blue team: telemetry, detection, response and hunting. |
| 08 | [Malware Analysis](manual/08-malware/README.md) | 19 | What malware is, how each family behaves, and how to analyse it safely in isolation. |
| 09 | [Secure Development](manual/09-secure-development/README.md) | 15 | Building security into the software lifecycle: modelling threats, writing safe code and automating verification in the pipeline. |
| 10 | [Cloud Security](manual/10-cloud-security/README.md) | 14 | Provider-specific and provider-agnostic security for modern cloud-native systems. |
| 11 | [Wireless and RF Security](manual/11-wireless/README.md) | 10 | Security of radio-based protocols from Wi-Fi to cellular, tested against lab hardware only. |
| 12 | [Identity and Access](manual/12-identity/README.md) | 11 | The directory, authentication and federation systems that attackers target to own everything. |
| 13 | [Digital Forensics and Incident Response](manual/13-digital-forensics/README.md) | 12 | Evidence-driven investigation across memory, disk, network and cloud, kept forensically sound. |
| 14 | [Threat Intelligence and Frameworks](manual/14-threat-intelligence/README.md) | 16 | The shared vocabularies, catalogues and scoring systems that connect every other domain. |
| 15 | [Governance, Risk and Compliance](manual/15-compliance/README.md) | 16 | The frameworks, laws and risk methods that turn security work into an accountable program. |

## Repository layout

```
CyberDocs/
├─ manual/        the 16 tracks and their lessons (the content)
├─ labs/          the campaign, boss labs, and per-track environments/
├─ reference/     tool guides, learning-platform roadmaps, glossary, ATT&CK/CWE/RFC indexes
├─ projects/      graded, hands-on builds
├─ cheatsheets/   printable quick-references
├─ labserver/     the local Lab Runner — live in-browser command execution
├─ _meta/         the data-driven generator  (edit here, then regenerate)
└─ site/          the built app  (generated; open site/index.html)
```

## The Reference

- [Tools](reference/tools/README.md) — every major security tool, documented end to end (89 tools)
- [Learning Platforms](reference/platforms/README.md) — HTB, THM, PortSwigger and more, with beginner→expert roadmaps
- [Projects](projects/README.md) — 100+ graded, hands-on builds
- [Cheatsheets](cheatsheets/README.md) — printable quick references
- [Glossary](reference/glossary.md) · [ATT&CK Index](reference/attack-index.md) · [CWE Index](reference/cwe-index.md) · [RFC Index](reference/rfc-index.md)

## Lab platform & the Lab Runner

Targets are hosted with **CyberForge** and plain `docker compose`; your **Kali Linux** box is the attacker; ready-made vulnerable apps (**bWAPP, DVWA, Juice Shop, Metasploitable, GOAD, LocalStack**) fill in the rest. The optional **Lab Runner** (`labserver/`, pure Python stdlib) is what makes the site's **▸ Run** buttons and **Live Terminal** execute for real — it runs each command *inside a designated Kali container* via `docker exec`, bound to `127.0.0.1`, token-guarded, never on your host. See [labserver/README.md](labserver/README.md). Targets default to *internal*, fail-closed networks.

## How each lesson is built (hands-on first, ~75/25)

Short **Overview** (necessary theory — what it is, how it works, key terms, a diagram) → a large interactive **Hands-On Practice**: a **Lab-setup card** (Start/Stop) · a **stepper** walkthrough (*command → Run/Copy → expected output → why*) · a **Live Terminal** · **Try it yourself** challenges · instant **quizzes** · **Detect & defend** · a skills check → a compact **Reference** (ATT&CK/OWASP/CWE/CAPEC/CVE mappings, reading, related). Progress and quiz results are saved in your browser.

## Status & roadmap

Generated, then recursively deepened. See [progress.json](progress.json), [TODO.md](TODO.md) and [CHANGELOG.md](CHANGELOG.md). Every chapter has a working Hands-On Practice block; flagship chapters carry fully authored walkthroughs and more are added each pass.

## Contributing

Content and code are generated from the data modules in [`_meta/`](_meta/README.md) — edit those and re-run the generator, don't hand-edit generated pages. See [CONTRIBUTING.md](CONTRIBUTING.md) for how to add a lesson, a lab walkthrough, or a track environment, and [CODE_OF_CONDUCT.md](CODE_OF_CONDUCT.md).

## Licence

**GNU General Public License v3.0 or later** — see [LICENSE](LICENSE). Copyright © 2026 **Nithees Narendra S**. You may use, study, share and modify this project under the GPL-3.0; derivative works must also be GPL-3.0. **For any use outside the GPL-3.0 terms** (e.g. proprietary or commercial relicensing), you must obtain **separate written permission from the copyright holder**. `SPDX-License-Identifier: GPL-3.0-or-later`.

## Ethics & safe use

Educational and defensive by design. Everything here is for defending systems and for **authorised** testing of systems you own or have explicit written permission to assess. Offensive techniques are taught alongside their detections and defences, and every lab is local and isolated. The optional **Lab Runner** executes commands only inside a container on an isolated network — never your host. See [SECURITY.md](SECURITY.md). Do not use any of this against systems you do not own or lack authorisation to test.
