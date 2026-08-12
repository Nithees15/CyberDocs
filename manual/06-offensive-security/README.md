<!-- SPDX-License-Identifier: GPL-3.0-or-later | Copyright (C) 2026 Nithees Narendra S -->
# Offensive Security — Track

The attacker's methodology end to end, structured on the cyber kill chain and MITRE ATT&CK. Every technique is paired with a lawful, local lab.

<div class="track-progress"><div class="progress" data-track-progress data-lessons="06-offensive-security/offensive-methodology.html,06-offensive-security/recon.html,06-offensive-security/osint.html,06-offensive-security/enumeration.html,06-offensive-security/scanning.html,06-offensive-security/vulnerability-assessment.html,06-offensive-security/exploitation.html,06-offensive-security/password-attacks.html,06-offensive-security/persistence.html,06-offensive-security/privilege-escalation.html,06-offensive-security/lateral-movement.html,06-offensive-security/defense-evasion.html,06-offensive-security/credential-access.html,06-offensive-security/command-and-control.html,06-offensive-security/exfiltration.html,06-offensive-security/post-exploitation.html,06-offensive-security/active-directory-attacks.html,06-offensive-security/wireless-attacks.html,06-offensive-security/social-engineering.html,06-offensive-security/red-team.html,06-offensive-security/opsec.html,06-offensive-security/ctf.html,06-offensive-security/bug-bounty.html,06-offensive-security/exploit-development.html"><i></i></div><div class="tp-label" style="color:var(--muted);font-size:13px;margin-top:6px">Your progress in this track</div></div>

**Set up the lab environment below once, then work the lessons — each one is hands-on-first.**

## Lab Environment

_Set up once, then use it for every chapter in the **Offensive Security** part. Everything runs locally and isolated — you never touch a system you don't own._

A mini attack range: a vulnerable Linux host to own, a web target to breach, and (optionally) an Active Directory forest for the domain-attack chapters.

**What you get**

| Target | How to reach it |
| --- | --- |
| `metasploitable` | boot-to-root Linux target (recon → exploit → loot) |
| `dvwa / juice-shop` | web foothold targets |
| `AD forest (optional)` | GOAD or a Windows Server eval VM for AD chapters — see notes |

**Provision it** — save this as `docker-compose.yml` and run `docker compose up -d` (or import the equivalent spec into CyberForge):

```yaml
# offsec-lab/docker-compose.yml  —  Offensive part environment
services:
  target-linux:
    image: tleemcjr/metasploitable2
    networks: [labnet]
    command: /bin/sh -c "/etc/rc.local; tail -f /dev/null"
  target-web:
    image: vulnerables/web-dvwa
    ports: ["8082:80"]
    networks: [labnet]

networks:
  labnet:
    driver: bridge
    internal: true
```

**Attacker box.** Kali on `labnet` runs the full kill chain: `nmap`/`nuclei` (recon), `metasploit`/manual exploits, then local privesc enumeration (`linpeas`). For AD, use `netexec`, `bloodhound`, `impacket`, `kerbrute`.

**Verify it works**

- `nmap -sV target-linux` from a Kali container attached to labnet lists exploitable services.

**Notes**

- **Active Directory:** containers can't host a real DC well. For AD chapters, provision **GOAD** (github.com/Orange-Cyberdefense/GOAD) or a Windows Server evaluation VM in VirtualBox/VMware on an isolated host-only network. A Samba AD-DC container covers Kerberos/LDAP basics only.

**Teardown.** `docker compose down` stops it; add `-v` to also drop volumes. Snapshot before big changes so you can revert.

> **Safety.** Keep intentionally-vulnerable targets on an isolated/`internal` network. Never expose them to the internet or attack anything outside this lab.


## Lessons

| # | Lesson | Difficulty | Hands-on | What you'll do |
| --- | --- | --- | --- | --- |
| 1 | [Offensive Security Methodology](offensive-methodology.md) | 🟢 Beginner | ~36m | Kill chain, ATT&CK, PTES and how engagements, scoping and rules of engagement are structured. |
| 2 | [Reconnaissance](recon.md) | 🟢 Beginner | ~60m | Passive and active information gathering, footprinting and building a target model. |
| 3 | [OSINT](osint.md) | 🟢 Beginner | ~60m | People, infrastructure and metadata discovery from open sources with a clean audit trail. |
| 4 | [Enumeration](enumeration.md) | 🟡 Intermediate | ~72m | Service, user, share and application enumeration that turns access into a foothold plan. |
| 5 | [Scanning](scanning.md) | 🟢 Beginner | ~60m | Host discovery, port and service scanning, versioning and safe scan tuning. |
| 6 | [Vulnerability Assessment](vulnerability-assessment.md) | 🟡 Intermediate | ~48m | Scanner selection, validation, false-positive triage and risk-based prioritisation. |
| 7 | [Exploitation](exploitation.md) | 🟠 Advanced | ~84m | Turning a vulnerability into reliable access, payload selection and staging in a lab. |
| 8 | [Password Attacks](password-attacks.md) | 🟡 Intermediate | ~60m | Guessing, spraying, cracking, and coercion, plus defensive lockout and detection. |
| 9 | [Persistence](persistence.md) | 🟠 Advanced | ~72m | Maintaining access across reboots on Linux and Windows and the telemetry it generates. |
| 10 | [Privilege Escalation](privilege-escalation.md) | 🟠 Advanced | ~84m | Local escalation on Linux and Windows through misconfiguration, tokens and kernel bugs. |
| 11 | [Lateral Movement](lateral-movement.md) | 🟠 Advanced | ~72m | Moving between hosts with remote execution, pivoting and relayed credentials. |
| 12 | [Defense Evasion](defense-evasion.md) | 🟠 Advanced | ~72m | Bypassing controls, obfuscation, and living-off-the-land, with the detections they trip. |
| 13 | [Credential Access](credential-access.md) | 🟠 Advanced | ~72m | Dumping, sniffing and forging credentials across the OS and directory services. |
| 14 | [Command and Control](command-and-control.md) | 🟠 Advanced | ~60m | C2 architecture, channels, redirectors, malleable profiles and beacon detection. |
| 15 | [Exfiltration](exfiltration.md) | 🟠 Advanced | ~48m | Staging, compression, encryption and covert channels, plus DLP and egress detection. |
| 16 | [Post-Exploitation](post-exploitation.md) | 🟠 Advanced | ~72m | Situational awareness, data collection, objective completion and cleanup discipline. |
| 17 | [Active Directory Attacks](active-directory-attacks.md) | 🔴 Expert | ~108m | Kerberoasting, delegation abuse, ACL attacks, DCSync and full domain-compromise chains. |
| 18 | [Wireless Attacks](wireless-attacks.md) | 🟠 Advanced | ~60m | Capturing handshakes, evil twins and PMKID attacks against a lab access point. |
| 19 | [Social Engineering](social-engineering.md) | 🟡 Intermediate | ~48m | Pretexting, phishing infrastructure, payload delivery and human-layer defences. |
| 20 | [Red Teaming](red-team.md) | 🔴 Expert | ~84m | Objective-based adversary emulation, infrastructure, OPSEC and reporting. |
| 21 | [Operational Security](opsec.md) | 🟠 Advanced | ~48m | Attribution management, infrastructure hygiene and separating tooling from identity. |
| 22 | [Capture The Flag](ctf.md) | 🟢 Beginner | ~60m | Categories, methodology, tooling and a structured path from first blood to expert. |
| 23 | [Bug Bounty](bug-bounty.md) | 🟡 Intermediate | ~60m | Program selection, scope, recon automation, reporting and building a repeatable pipeline. |
| 24 | [Exploit Development](exploit-development.md) | 🔴 Expert | ~108m | From crash to control: fuzzing, triage, primitive building and mitigation bypass. |

**24 lessons.**

[← Repository home](../../README.md) · [Full contents](../../SUMMARY.md) · [Labs campaign](../../labs/README.md)
