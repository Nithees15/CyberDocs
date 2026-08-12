<!-- SPDX-License-Identifier: GPL-3.0-or-later | Copyright (C) 2026 Nithees Narendra S -->
# Platforms — Track

Security architecture, attack surface and hardening for each major platform family.

<div class="track-progress"><div class="progress" data-track-progress data-lessons="05-platforms/linux-security.html,05-platforms/windows-security.html,05-platforms/macos-security.html,05-platforms/android-security.html,05-platforms/ios-security.html,05-platforms/embedded-security.html,05-platforms/iot-security.html,05-platforms/ics-security.html,05-platforms/scada-security.html,05-platforms/cloud-platform-security.html,05-platforms/container-security.html,05-platforms/kubernetes-security.html,05-platforms/serverless-security.html,05-platforms/virtualization-security.html,05-platforms/mainframe-security.html"><i></i></div><div class="tp-label" style="color:var(--muted);font-size:13px;margin-top:6px">Your progress in this track</div></div>

**Set up the lab environment below once, then work the lessons — each one is hands-on-first.**

## Lab Environment

_Set up once, then use it for every chapter in the **Platforms** part. Everything runs locally and isolated — you never touch a system you don't own._

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
| 1 | [Linux Security](linux-security.md) | 🟡 Intermediate | ~84m | DAC, capabilities, SELinux/AppArmor, namespaces, auditd and privilege-escalation surface. |
| 2 | [Windows Security](windows-security.md) | 🟡 Intermediate | ~96m | Tokens, integrity levels, UAC, LSASS, WDAC, Credential Guard and event-log telemetry. |
| 3 | [macOS Security](macos-security.md) | 🟠 Advanced | ~60m | SIP, TCC, Gatekeeper, notarisation, XPC, keychain and macOS persistence locations. |
| 4 | [Android Security](android-security.md) | 🟠 Advanced | ~72m | Sandbox model, permissions, APK internals, root detection and mobile testing methodology. |
| 5 | [iOS Security](ios-security.md) | 🟠 Advanced | ~72m | Secure Boot chain, Data Protection, entitlements, jailbreak impact and IPA analysis. |
| 6 | [Embedded Systems Security](embedded-security.md) | 🟠 Advanced | ~72m | Firmware extraction, UART/JTAG, bootloaders, secure boot and hardware attack surface. |
| 7 | [IoT Security](iot-security.md) | 🟠 Advanced | ~72m | Device lifecycle, cloud/companion apps, MQTT/CoAP, update integrity and IoT botnet history. |
| 8 | [ICS Security](ics-security.md) | 🟠 Advanced | ~72m | Process control, PLCs, safety instrumented systems and the Purdue reference architecture. |
| 9 | [SCADA Security](scada-security.md) | 🟠 Advanced | ~60m | Modbus, DNP3, S7comm, historian exposure and monitoring OT networks passively. |
| 10 | [Cloud Platform Security](cloud-platform-security.md) | 🟡 Intermediate | ~72m | Control vs data plane, metadata services, tenancy and cross-account trust failures. |
| 11 | [Container Security](container-security.md) | 🟠 Advanced | ~72m | Image provenance, runtime isolation, seccomp/AppArmor, escapes and admission control. |
| 12 | [Kubernetes Security](kubernetes-security.md) | 🟠 Advanced | ~96m | RBAC, service accounts, network policy, admission control, etcd exposure and attack paths. |
| 13 | [Serverless Security](serverless-security.md) | 🟡 Intermediate | ~48m | Event-driven trust, function IAM, cold-start telemetry gaps and dependency risk. |
| 14 | [Virtualization Security](virtualization-security.md) | 🟠 Advanced | ~48m | Hypervisor attack surface, VM escapes, nested virtualization and lab isolation design. |
| 15 | [Mainframe Security](mainframe-security.md) | 🔴 Expert | ~48m | z/OS, RACF, TSO/JCL, and why legacy transaction processing still matters to attackers. |

**15 lessons.**

[← Repository home](../../README.md) · [Full contents](../../SUMMARY.md) · [Labs campaign](../../labs/README.md)
