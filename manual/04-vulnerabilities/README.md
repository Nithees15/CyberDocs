<!-- SPDX-License-Identifier: GPL-3.0-or-later | Copyright (C) 2026 Nithees Narendra S -->
# Vulnerabilities — Track

Bug classes from first principles: root cause, exploitation, detection and durable fixes. Each chapter maps to CWE, CAPEC, OWASP and real CVEs.

<div class="track-progress"><div class="progress" data-track-progress data-lessons="04-vulnerabilities/vulnerability-taxonomy.html,04-vulnerabilities/sql-injection.html,04-vulnerabilities/blind-sql-injection.html,04-vulnerabilities/nosql-injection.html,04-vulnerabilities/xss.html,04-vulnerabilities/stored-xss.html,04-vulnerabilities/dom-xss.html,04-vulnerabilities/csrf.html,04-vulnerabilities/ssrf.html,04-vulnerabilities/rce.html,04-vulnerabilities/lfi.html,04-vulnerabilities/rfi.html,04-vulnerabilities/directory-traversal.html,04-vulnerabilities/xxe.html,04-vulnerabilities/command-injection.html,04-vulnerabilities/template-injection.html,04-vulnerabilities/insecure-deserialization.html,04-vulnerabilities/idor.html,04-vulnerabilities/race-conditions.html,04-vulnerabilities/memory-corruption.html,04-vulnerabilities/buffer-overflow.html,04-vulnerabilities/stack-overflow.html,04-vulnerabilities/heap-overflow.html,04-vulnerabilities/integer-overflow.html,04-vulnerabilities/format-strings.html,04-vulnerabilities/authentication-bypass.html,04-vulnerabilities/business-logic.html,04-vulnerabilities/privilege-escalation-concepts.html,04-vulnerabilities/cwe-top-25.html,04-vulnerabilities/supply-chain-vulnerabilities.html"><i></i></div><div class="tp-label" style="color:var(--muted);font-size:13px;margin-top:6px">Your progress in this track</div></div>

**Set up the lab environment below once, then work the lessons — each one is hands-on-first.**

## Lab Environment

_Set up once, then use it for every chapter in the **Vulnerabilities** part. Everything runs locally and isolated — you never touch a system you don't own._

Reuses the Web Security apps for injection/logic bugs, and adds a disposable build box for the memory-corruption chapters (compile and exploit vulnerable C locally).

**What you get**

| Target | How to reach it |
| --- | --- |
| `bWAPP / DVWA / Juice Shop` | the web bug targets (see the Web Security part environment) |
| `pwn-box` | Ubuntu build/debug container for buffer/heap/format-string labs |

**Provision it** — save this as `docker-compose.yml` and run `docker compose up -d` (or import the equivalent spec into CyberForge):

```yaml
# vuln-lab/docker-compose.yml  —  Vulnerabilities part environment
services:
  bwapp:
    image: raesene/bwapp
    ports: ["8081:80"]
    networks: [labnet]
  dvwa:
    image: vulnerables/web-dvwa
    ports: ["8082:80"]
    networks: [labnet]
  pwn-box:
    image: ubuntu:22.04
    container_name: pwn-box
    cap_add: ["SYS_PTRACE"]          # allow gdb inside the container
    security_opt: ["seccomp=unconfined"]
    command: sleep infinity
    networks: [labnet]

networks:
  labnet:
    driver: bridge
```

**Attacker box.** Web bugs: Burp/ZAP + Kali web tooling. Memory corruption: work *inside* `pwn-box` (`docker exec -it pwn-box bash`), install `build-essential gdb python3-pip`, add `pwntools`/`pwndbg`, and compile targets with mitigations toggled.

**Verify it works**

- `docker exec -it pwn-box bash` gives a root shell in the build box.
- `gcc --version` after installing build-essential; `gdb ./vuln` works with SYS_PTRACE.

**Notes**

- `pwn-box` grants SYS_PTRACE and unconfined seccomp *for debugging only* — keep it on the isolated network.

**Teardown.** `docker compose down` stops it; add `-v` to also drop volumes. Snapshot before big changes so you can revert.

> **Safety.** Keep intentionally-vulnerable targets on an isolated/`internal` network. Never expose them to the internet or attack anything outside this lab.


## Lessons

| # | Lesson | Difficulty | Hands-on | What you'll do |
| --- | --- | --- | --- | --- |
| 1 | [Vulnerability Taxonomy](vulnerability-taxonomy.md) | 🟢 Beginner | ~30m | How CWE, CAPEC, OWASP and ATT&CK relate, and how to classify a finding correctly. |
| 2 | [SQL Injection](sql-injection.md) | 🟡 Intermediate | ~72m | Query context, union and error-based extraction, stacked queries and parameterised defences. |
| 3 | [Blind SQL Injection](blind-sql-injection.md) | 🟠 Advanced | ~60m | Boolean, time-based and out-of-band inference, plus automation and WAF-aware tuning. |
| 4 | [NoSQL Injection](nosql-injection.md) | 🟡 Intermediate | ~36m | Operator injection, type juggling in document stores and server-side JavaScript execution. |
| 5 | [Cross-Site Scripting](xss.md) | 🟡 Intermediate | ~72m | Reflected, stored and DOM sinks, contexts, encoding rules and the modern XSS defence stack. |
| 6 | [Stored XSS](stored-xss.md) | 🟡 Intermediate | ~36m | Persistence paths, admin-panel escalation, sanitiser bypasses and worm behaviour. |
| 7 | [DOM-Based XSS](dom-xss.md) | 🟠 Advanced | ~48m | Source-to-sink dataflow, client-side templating, Trusted Types and DOM Invader workflow. |
| 8 | [Cross-Site Request Forgery](csrf.md) | 🟡 Intermediate | ~48m | State-changing requests, token patterns, SameSite behaviour and CSRF-in-JSON edge cases. |
| 9 | [Server-Side Request Forgery](ssrf.md) | 🟠 Advanced | ~72m | URL parsing, cloud metadata theft, blind SSRF, DNS rebinding and egress-control defences. |
| 10 | [Remote Code Execution](rce.md) | 🟠 Advanced | ~72m | How arbitrary code execution is reached, chained and stabilised, plus containment strategies. |
| 11 | [Local File Inclusion](lfi.md) | 🟡 Intermediate | ~48m | Include semantics, wrappers, log poisoning, session-file abuse and LFI-to-RCE chains. |
| 12 | [Remote File Inclusion](rfi.md) | 🟡 Intermediate | ~30m | Remote include conditions, language configuration and hosting payloads safely in a lab. |
| 13 | [Directory Traversal](directory-traversal.md) | 🟢 Beginner | ~36m | Path canonicalisation, encoding tricks, chroot/jail limits and safe file-access patterns. |
| 14 | [XML External Entity Injection](xxe.md) | 🟠 Advanced | ~48m | DTDs, entity expansion, blind OOB exfiltration, SSRF pivots and parser hardening. |
| 15 | [OS Command Injection](command-injection.md) | 🟡 Intermediate | ~48m | Shell metacharacters, argument injection, blind detection and safe process invocation. |
| 16 | [Server-Side Template Injection](template-injection.md) | 🟠 Advanced | ~60m | Engine fingerprinting, sandbox escapes in Jinja2/Twig/Freemarker and template-to-RCE chains. |
| 17 | [Insecure Deserialization](insecure-deserialization.md) | 🔴 Expert | ~72m | Object graphs, gadget chains in Java/.NET/PHP/Python and format-level mitigations. |
| 18 | [Insecure Direct Object References](idor.md) | 🟢 Beginner | ~36m | Object-level authorization, identifier enumeration, tenant isolation and systematic testing. |
| 19 | [Race Conditions](race-conditions.md) | 🟠 Advanced | ~60m | TOCTOU, limit-overrun, single-packet attacks and locking or idempotency defences. |
| 20 | [Memory Corruption](memory-corruption.md) | 🔴 Expert | ~72m | Memory layout, corruption primitives, exploit mitigations and the modern exploitation pipeline. |
| 21 | [Buffer Overflows](buffer-overflow.md) | 🟠 Advanced | ~72m | Bounds-check failures, overwrite targets, shellcode and mitigation-aware exploitation. |
| 22 | [Stack-Based Overflows](stack-overflow.md) | 🟠 Advanced | ~72m | Saved return addresses, canaries, ASLR/DEP, ROP chains and a full local lab exploit. |
| 23 | [Heap-Based Overflows](heap-overflow.md) | 🔴 Expert | ~84m | Allocator internals, chunk metadata, use-after-free, tcache poisoning and heap grooming. |
| 24 | [Integer Overflows](integer-overflow.md) | 🟠 Advanced | ~48m | Wrap-around, truncation, signedness confusion and the allocation bugs they cause. |
| 25 | [Format String Vulnerabilities](format-strings.md) | 🟠 Advanced | ~48m | Varargs abuse, %n writes, memory disclosure and arbitrary-write exploitation. |
| 26 | [Authentication Bypass](authentication-bypass.md) | 🟡 Intermediate | ~48m | Logic gaps, forced browsing, token forgery, response tampering and 2FA bypass patterns. |
| 27 | [Business Logic Vulnerabilities](business-logic.md) | 🟠 Advanced | ~60m | Workflow abuse, price and quantity manipulation, state machines and non-scannable bugs. |
| 28 | [Privilege Escalation Concepts](privilege-escalation-concepts.md) | 🟡 Intermediate | ~48m | Vertical vs horizontal escalation, trust boundaries and escalation primitives across platforms. |
| 29 | [CWE Top 25 Reference](cwe-top-25.md) | 🟡 Intermediate | ~60m | Every entry in the CWE Top 25 with root cause, example, detection and fix. |
| 30 | [Dependency and Supply Chain Vulnerabilities](supply-chain-vulnerabilities.md) | 🟠 Advanced | ~48m | Typosquatting, dependency confusion, build compromise and reproducible-build defences. |

**30 lessons.**

[← Repository home](../../README.md) · [Full contents](../../SUMMARY.md) · [Labs campaign](../../labs/README.md)
