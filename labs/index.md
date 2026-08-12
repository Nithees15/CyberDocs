<!-- SPDX-License-Identifier: GPL-3.0-or-later | Copyright (C) 2026 Nithees Narendra S -->
# Labs — the Hands-On Campaign

> This repository is **hands-on first**. Every Manual chapter already ends in a full **Hands-On Practice** block. This campaign strings those labs into an ordered, beginner→expert path per track, and adds cross-topic **boss labs** — full kill-chains that combine many chapters.

## How to run the campaign

1. Pick a track below and **set up its part lab environment once** (link next to the track).
2. Work each chapter's *Hands-On Practice* in order — walkthrough, then the *Try it yourself* challenges.
3. Finish the track with its **boss lab** to prove you can chain the techniques end to end.
4. Everything is local and isolated. Never attack systems you don't own.

## Tracks

### Networking

Environment: [set up the Networking environment](../manual/01-networking/README.md#lab-environment)

1. [Scanning](../manual/06-offensive-security/scanning.md#hands-on-practice) — 🟢 Beginner
   - 🏁 **Capstone:** [Boss Lab 1 — Web App to Root](boss/boss-01-web-to-root.md)
   - 🏁 **Capstone:** [Boss Lab 4 — Pivot Across Segmented Networks](boss/boss-04-pivot.md)

### Web Security

Environment: [set up the Web Security environment](../manual/03-web-security/README.md#lab-environment)

1. [Insecure Direct Object References](../manual/04-vulnerabilities/idor.md#hands-on-practice) — 🟢 Beginner
1. [Cross-Site Request Forgery](../manual/04-vulnerabilities/csrf.md#hands-on-practice) — 🟡 Intermediate
1. [OS Command Injection](../manual/04-vulnerabilities/command-injection.md#hands-on-practice) — 🟡 Intermediate
1. [JSON Web Tokens](../manual/03-web-security/jwt.md#hands-on-practice) — 🟡 Intermediate
1. [SQL Injection](../manual/04-vulnerabilities/sql-injection.md#hands-on-practice) — 🟡 Intermediate
1. [Cross-Site Scripting](../manual/04-vulnerabilities/xss.md#hands-on-practice) — 🟡 Intermediate
   - 🏁 **Capstone:** [Boss Lab 1 — Web App to Root](boss/boss-01-web-to-root.md)

### Vulnerabilities

Environment: [set up the Vulnerabilities environment](../manual/04-vulnerabilities/README.md#lab-environment)

1. [Buffer Overflows](../manual/04-vulnerabilities/buffer-overflow.md#hands-on-practice) — 🟠 Advanced

### Offensive Security

Environment: [set up the Offensive Security environment](../manual/06-offensive-security/README.md#lab-environment)

1. [Privilege Escalation](../manual/06-offensive-security/privilege-escalation.md#hands-on-practice) — 🟠 Advanced
   - 🏁 **Capstone:** [Boss Lab 1 — Web App to Root](boss/boss-01-web-to-root.md)

### Defensive Security

Environment: [set up the Defensive Security environment](../manual/07-defensive-security/README.md#lab-environment)

1. [Threat Hunting](../manual/07-defensive-security/threat-hunting.md#hands-on-practice) — 🟠 Advanced
   - 🏁 **Capstone:** [Boss Lab 3 — Purple Team: Detect the Whole Chain](boss/boss-03-purple-killchain.md)

### Malware Analysis

Environment: [set up the Malware Analysis environment](../manual/08-malware/README.md#lab-environment)

1. [YARA](../manual/07-defensive-security/yara.md#hands-on-practice) — 🟡 Intermediate
   - 🏁 **Capstone:** [Boss Lab 5 — Incident: Triage a Compromised Host](boss/boss-05-malware-ir.md)

### Identity and Access

Environment: [set up the Identity and Access environment](../manual/12-identity/README.md#lab-environment)

1. [Active Directory Attacks](../manual/06-offensive-security/active-directory-attacks.md#hands-on-practice) — 🔴 Expert
   - 🏁 **Capstone:** [Boss Lab 2 — Assumed Breach to Domain Admin](boss/boss-02-domain-domination.md)

### Digital Forensics and Incident Response

Environment: [set up the Digital Forensics and Incident Response environment](../manual/13-digital-forensics/README.md#lab-environment)

1. [Memory Forensics](../manual/07-defensive-security/memory-forensics.md#hands-on-practice) — 🟠 Advanced
   - 🏁 **Capstone:** [Boss Lab 5 — Incident: Triage a Compromised Host](boss/boss-05-malware-ir.md)

## Boss Labs (cross-topic capstones)

| Lab | Difficulty | Tracks | Time |
| --- | --- | --- | --- |
| [Boss Lab 1 — Web App to Root](boss/boss-01-web-to-root.md) | Intermediate | Web, Offensive | ~4h |
| [Boss Lab 2 — Assumed Breach to Domain Admin](boss/boss-02-domain-domination.md) | Advanced | Identity, Offensive | ~6h |
| [Boss Lab 3 — Purple Team: Detect the Whole Chain](boss/boss-03-purple-killchain.md) | Advanced | Defensive, Purple | ~5h |
| [Boss Lab 4 — Pivot Across Segmented Networks](boss/boss-04-pivot.md) | Advanced | Networking, Offensive | ~4h |
| [Boss Lab 5 — Incident: Triage a Compromised Host](boss/boss-05-malware-ir.md) | Advanced | Forensics, Malware, Defensive | ~5h |
| [Boss Lab 6 — SSRF to Cloud Account Takeover](boss/boss-06-cloud-breach.md) | Advanced | Cloud, Web | ~4h |

## Every chapter is a lab

The tracks above feature the labs with fully authored walkthroughs. **Every** Manual chapter — all of them — has a Hands-On Practice block with a guided walkthrough, challenges and a detect-and-defend section. Browse the [Manual](../manual/00-foundations/README.md) and jump to any chapter's practice.

[← Repository home](../README.md) · [Full contents](../SUMMARY.md)
