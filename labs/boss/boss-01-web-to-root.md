<!-- SPDX-License-Identifier: GPL-3.0-or-later | Copyright (C) 2026 Nithees Narendra S -->
[Home](../../README.md) › [Labs](../README.md) › **Boss Lab 1 — Web App to Root**

# Boss Lab 1 — Web App to Root

> You have a single in-scope web application and nothing else. Get a shell on the server and escalate to root, capturing a flag at each stage.

| | |
| --- | --- |
| **Difficulty** | Intermediate |
| **Est. time** | ~4 hours |
| **Tracks** | Web, Offensive |

## Environment

Use the Web Security + Offensive part environments (a vulnerable web app on `labnet`, Kali as attacker).

> Everything is local and isolated. This is a capstone: it assumes you've worked the related chapters below.

## Objectives (capture the flags)

- [ ] flag1 (web root)
- [ ] flag2 (group-readable file)
- [ ] root.txt

## Stages

_Work them in order. Each stage has a hint — try hard before opening it._

### Stage 1 — Recon

Map the app: pages, parameters, tech stack. Find every input that reaches the server.

<details><summary>Hint</summary>

httpx + a directory brute-force (ffuf/gobuster) reveal hidden endpoints.

</details>

### Stage 2 — Foothold

Exploit a web vulnerability (SQLi, command injection, or file upload) to reach code execution. Capture flag 1 from the web root.

<details><summary>Hint</summary>

Chain the injection to a reverse shell; keep the exact payload in your notes.

</details>

### Stage 3 — Situational awareness

As the web user, enumerate the host: users, services, sudo, SUID, cron.

<details><summary>Hint</summary>

linpeas, then verify by hand. Flag 2 is readable by a specific group.

</details>

### Stage 4 — Privilege escalation

Escalate to root via a misconfiguration. Capture the root flag.

<details><summary>Hint</summary>

GTFOBins for the sudo/SUID binary you found.

</details>

### Stage 5 — Report

Write it up: the chain, each finding mapped to CWE/ATT&CK, and the one fix per stage that would have broken it.

<details><summary>Hint</summary>

A defender should be able to close any single link and stop you.

</details>

## Debrief

Which single control at each stage would have stopped the chain? Now build the detection for your foothold (web-server process spawning a shell) and your privesc (SUID/sudo abuse).

## Chapters this draws on

- [Scanning](../../manual/06-offensive-security/scanning.md)
- [SQL Injection](../../manual/04-vulnerabilities/sql-injection.md)
- [OS Command Injection](../../manual/04-vulnerabilities/command-injection.md)
- [Remote Code Execution](../../manual/04-vulnerabilities/rce.md)
- [Privilege Escalation](../../manual/06-offensive-security/privilege-escalation.md)

[← Back to the Labs campaign](../README.md)

