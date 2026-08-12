<!-- SPDX-License-Identifier: GPL-3.0-or-later | Copyright (C) 2026 Nithees Narendra S -->
[Home](../../README.md) › [Labs](../README.md) › **Boss Lab 2 — Assumed Breach to Domain Admin**

# Boss Lab 2 — Assumed Breach to Domain Admin

> Assume-breach: you start with one low-privileged domain user's credentials. Reach Domain Admin and prove domain persistence.

| | |
| --- | --- |
| **Difficulty** | Advanced |
| **Est. time** | ~6 hours |
| **Tracks** | Identity, Offensive |

## Environment

GOAD (recommended) or the Identity part environment (Samba AD-DC for the basics).

> Everything is local and isolated. This is a capstone: it assumes you've worked the related chapters below.

## Objectives (capture the flags)

- [ ] service account password
- [ ] krbtgt hash
- [ ] Golden Ticket admin access

## Stages

_Work them in order. Each stage has a hint — try hard before opening it._

### Stage 1 — Enumerate

Collect the AD graph and identify high-value targets and paths.

<details><summary>Hint</summary>

BloodHound 'shortest path to Domain Admins'.

</details>

### Stage 2 — Harvest credentials

Kerberoast/AS-REP roast and crack a service account.

<details><summary>Hint</summary>

impacket-GetUserSPNs + hashcat -m 13100.

</details>

### Stage 3 — Walk the path

Abuse an ACL edge (GenericAll/WriteDACL/ForceChangePassword) to control a privileged principal.

<details><summary>Hint</summary>

Follow BloodHound's edges literally; each has a documented abuse.

</details>

### Stage 4 — Domain compromise

DCSync the krbtgt hash and forge a Golden Ticket.

<details><summary>Hint</summary>

impacket-secretsdump then impacket-ticketer.

</details>

### Stage 5 — Detect your own attack

Re-run the chain while capturing 4768/4769/4662 and write detections.

<details><summary>Hint</summary>

This is the purple-team half — map every step to an event ID.

</details>

## Debrief

Rank your steps by how detectable they were. Which AD hardening (gMSA, AES-only, tiering, LAPS) would have broken the path earliest?

## Chapters this draws on

- [Enumeration](../../manual/06-offensive-security/enumeration.md)
- [Active Directory Attacks](../../manual/06-offensive-security/active-directory-attacks.md)
- [Kerberos](../../manual/01-networking/kerberos.md)
- [Lateral Movement](../../manual/06-offensive-security/lateral-movement.md)
- [Credential Access](../../manual/06-offensive-security/credential-access.md)

[← Back to the Labs campaign](../README.md)

