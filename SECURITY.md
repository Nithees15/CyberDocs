<!-- SPDX-License-Identifier: GPL-3.0-or-later | Copyright (C) 2026 Nithees Narendra S -->
# Security Policy

This repository has two security dimensions: (1) it is a **teaching project full of dual-use offensive
techniques**, and (2) it ships a small **command-execution backend** (`labserver/`). Please read both parts.

## 1. Intended, lawful use

Cybersecurity-Mastery is for **education and defence**. All offensive material is taught alongside its
detection and remediation, and every lab targets **local, isolated, intentionally-vulnerable environments**
(bWAPP, DVWA, Juice Shop, Metasploitable, GOAD, LocalStack, and the like).

**Only use these techniques against systems you own or have explicit written authorisation to test.**
Unauthorised access to computer systems is illegal in most jurisdictions. You are solely responsible for how
you use this material. The authors and contributors accept no liability for misuse.

## 2. The Lab Runner (`labserver/`) — powerful by design

The optional Lab Runner executes commands so the site's **Run** buttons work. Its safety rests on constraints
you must not weaken:

- It **binds to `127.0.0.1` only** — never expose it to a LAN or the internet.
- `/run` and `/lab/*` require the **session token** printed at startup.
- It executes **only via `docker exec` into a designated container** — never on your host.

Run it only for your own local, authorised lab. See [labserver/README.md](labserver/README.md).

## 3. Reporting a vulnerability in the tooling

If you find a security issue in the **project's own code** (e.g. a way to make the Lab Runner execute outside
its container, bypass the token, or a path traversal in the generator/site), please report it **privately**:

- Preferred: open a **GitHub Security Advisory** ("Report a vulnerability") on this repository, or
- Send a private message to the maintainer, **Nithees Narendra S**, via GitHub.

Please include steps to reproduce and the impact. Do **not** open a public issue for an unpatched
vulnerability. We aim to acknowledge reports within a few days and to credit reporters who wish to be named.

## Supported versions

This is an actively developed educational project; fixes land on the default branch. There is no long-term
support branch — please track `main`.
