<!-- SPDX-License-Identifier: GPL-3.0-or-later | Copyright (C) 2026 Nithees Narendra S -->
# Secure Development — Track

Building security into the software lifecycle: modelling threats, writing safe code and automating verification in the pipeline.

<div class="track-progress"><div class="progress" data-track-progress data-lessons="09-secure-development/secure-sdlc.html,09-secure-development/threat-modeling.html,09-secure-development/secure-coding.html,09-secure-development/devsecops.html,09-secure-development/sast.html,09-secure-development/dast.html,09-secure-development/iast.html,09-secure-development/secrets-management.html,09-secure-development/cicd-security.html,09-secure-development/dependency-security.html,09-secure-development/supply-chain-security.html,09-secure-development/sbom.html,09-secure-development/api-secure-design.html,09-secure-development/secure-defaults.html,09-secure-development/code-review-security.html"><i></i></div><div class="tp-label" style="color:var(--muted);font-size:13px;margin-top:6px">Your progress in this track</div></div>

**Set up the lab environment below once, then work the lessons — each one is hands-on-first.**

## Lab Environment

_Set up once, then use it for every chapter in the **Secure Development** part. Everything runs locally and isolated — you never touch a system you don't own._

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
| 1 | [Secure SDLC](secure-sdlc.md) | 🟢 Beginner | ~48m | Shifting left, security activities per phase, gates and maturity models (BSIMM/SAMM). |
| 2 | [Threat Modeling](threat-modeling.md) | 🟡 Intermediate | ~60m | STRIDE, attack trees, data-flow diagrams, PASTA and turning models into requirements. |
| 3 | [Secure Coding](secure-coding.md) | 🟡 Intermediate | ~72m | Input validation, output encoding, safe APIs and language-specific pitfalls. |
| 4 | [DevSecOps](devsecops.md) | 🟡 Intermediate | ~60m | Pipeline security, policy as code, guardrails and measuring program effectiveness. |
| 5 | [Static Application Security Testing](sast.md) | 🟡 Intermediate | ~48m | How SAST works, taint analysis, rule tuning, triage and CI integration. |
| 6 | [Dynamic Application Security Testing](dast.md) | 🟡 Intermediate | ~48m | Crawling, active scanning, authenticated scans and pipeline gating. |
| 7 | [Interactive Application Security Testing](iast.md) | 🟡 Intermediate | ~36m | Instrumentation, runtime coverage, and the trade-offs versus SAST and DAST. |
| 8 | [Secrets Management](secrets-management.md) | 🟡 Intermediate | ~48m | Vaulting, dynamic secrets, rotation, detection of leaks and preventing hardcoded keys. |
| 9 | [CI/CD Security](cicd-security.md) | 🟠 Advanced | ~60m | Runner isolation, poisoned pipeline execution, artefact integrity and OIDC federation. |
| 10 | [Dependency Security](dependency-security.md) | 🟡 Intermediate | ~48m | SCA, transitive risk, lockfiles, pinning and vulnerability triage for third-party code. |
| 11 | [Software Supply Chain Security](supply-chain-security.md) | 🟠 Advanced | ~60m | SLSA, provenance, signing with Sigstore, build integrity and threat scenarios. |
| 12 | [Software Bill of Materials](sbom.md) | 🟡 Intermediate | ~36m | SPDX and CycloneDX, generation, consumption, VEX and continuous monitoring. |
| 13 | [Secure API Design](api-secure-design.md) | 🟡 Intermediate | ~48m | AuthN/AuthZ patterns, input contracts, rate limiting and secure defaults. |
| 14 | [Secure Defaults and Hardening](secure-defaults.md) | 🟡 Intermediate | ~36m | Least privilege, fail-safe design, configuration baselines and secure-by-design principles. |
| 15 | [Security Code Review](code-review-security.md) | 🟠 Advanced | ~60m | Manual review methodology, sink hunting, diff review and reviewer tooling. |

**15 lessons.**

[← Repository home](../../README.md) · [Full contents](../../SUMMARY.md) · [Labs campaign](../../labs/README.md)
