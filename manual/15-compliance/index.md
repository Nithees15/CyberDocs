<!-- SPDX-License-Identifier: GPL-3.0-or-later | Copyright (C) 2026 Nithees Narendra S -->
# Governance, Risk and Compliance — Track

The frameworks, laws and risk methods that turn security work into an accountable program.

<div class="track-progress"><div class="progress" data-track-progress data-lessons="15-compliance/grc-fundamentals.html,15-compliance/risk-management.html,15-compliance/nist-csf.html,15-compliance/nist-800-53.html,15-compliance/nist-800-171.html,15-compliance/nist-rmf.html,15-compliance/iso-27001.html,15-compliance/pci-dss.html,15-compliance/soc2.html,15-compliance/gdpr.html,15-compliance/hipaa.html,15-compliance/privacy-engineering.html,15-compliance/security-policy.html,15-compliance/audit-assurance.html,15-compliance/security-awareness.html,15-compliance/business-continuity.html"><i></i></div><div class="tp-label" style="color:var(--muted);font-size:13px;margin-top:6px">Your progress in this track</div></div>

**Set up the lab environment below once, then work the lessons — each one is hands-on-first.**

## Lab Environment

_Set up once, then use it for every chapter in the **Governance, Risk and Compliance** part. Everything runs locally and isolated — you never touch a system you don't own._

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
| 1 | [GRC Fundamentals](grc-fundamentals.md) | 🟢 Beginner | ~48m | Governance, risk management, compliance, the CIA triad and control types. |
| 2 | [Risk Management](risk-management.md) | 🟡 Intermediate | ~60m | Risk identification, qualitative/quantitative analysis, FAIR, treatment and acceptance. |
| 3 | [NIST Cybersecurity Framework](nist-csf.md) | 🟢 Beginner | ~36m | Govern/Identify/Protect/Detect/Respond/Recover, tiers, profiles and CSF 2.0. |
| 4 | [NIST SP 800-53](nist-800-53.md) | 🟡 Intermediate | ~48m | Control families, baselines, tailoring and using 800-53 as a control catalogue. |
| 5 | [NIST SP 800-171 and CMMC](nist-800-171.md) | 🟡 Intermediate | ~36m | Protecting CUI, control mapping and the CMMC assessment model. |
| 6 | [NIST Risk Management Framework](nist-rmf.md) | 🟡 Intermediate | ~36m | Categorise, select, implement, assess, authorise, monitor and ATO. |
| 7 | [ISO/IEC 27001 and 27002](iso-27001.md) | 🟡 Intermediate | ~48m | ISMS, Annex A controls, Statement of Applicability and certification. |
| 8 | [PCI DSS](pci-dss.md) | 🟡 Intermediate | ~48m | Cardholder data environment, the twelve requirements, scoping and v4.0 changes. |
| 9 | [SOC 2](soc2.md) | 🟡 Intermediate | ~36m | Trust services criteria, Type I vs II, evidence and the audit process. |
| 10 | [GDPR](gdpr.md) | 🟢 Beginner | ~36m | Lawful bases, data-subject rights, breach notification and privacy by design. |
| 11 | [HIPAA](hipaa.md) | 🟢 Beginner | ~36m | Privacy and Security Rules, safeguards, PHI and breach handling. |
| 12 | [Privacy Engineering](privacy-engineering.md) | 🟡 Intermediate | ~36m | Data minimisation, PETs, DPIAs and building privacy into systems. |
| 13 | [Security Policy and Standards](security-policy.md) | 🟢 Beginner | ~36m | Policy hierarchy, writing enforceable standards and exception handling. |
| 14 | [Audit and Assurance](audit-assurance.md) | 🟡 Intermediate | ~36m | Control testing, evidence, sampling, findings and continuous compliance. |
| 15 | [Security Awareness and Culture](security-awareness.md) | 🟢 Beginner | ~30m | Behaviour change, phishing simulation ethics and measuring program impact. |
| 16 | [Business Continuity and Disaster Recovery](business-continuity.md) | 🟡 Intermediate | ~36m | BIA, RTO/RPO, backup strategy, resilience and testing recovery plans. |

**16 lessons.**

[← Repository home](../../README.md) · [Full contents](../../SUMMARY.md) · [Labs campaign](../../labs/README.md)
