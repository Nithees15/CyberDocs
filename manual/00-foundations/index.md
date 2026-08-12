<!-- SPDX-License-Identifier: GPL-3.0-or-later | Copyright (C) 2026 Nithees Narendra S -->
# Foundations — Track

The computer science, systems and programming groundwork every security discipline is built on. Start here if anything below feels shaky.

<div class="track-progress"><div class="progress" data-track-progress data-lessons="00-foundations/computer-science.html,00-foundations/programming.html,00-foundations/algorithms.html,00-foundations/data-structures.html,00-foundations/discrete-mathematics.html,00-foundations/computer-architecture.html,00-foundations/operating-systems.html,00-foundations/networking-primer.html,00-foundations/databases.html,00-foundations/virtualization.html,00-foundations/containers.html,00-foundations/cloud.html,00-foundations/linux.html,00-foundations/windows.html,00-foundations/powershell.html,00-foundations/bash.html,00-foundations/python.html,00-foundations/c.html,00-foundations/cpp.html,00-foundations/rust.html,00-foundations/go.html,00-foundations/javascript.html,00-foundations/assembly.html,00-foundations/git.html,00-foundations/github.html"><i></i></div><div class="tp-label" style="color:var(--muted);font-size:13px;margin-top:6px">Your progress in this track</div></div>

**Set up the lab environment below once, then work the lessons — each one is hands-on-first.**

## Lab Environment

_Set up once, then use it for every chapter in the **Foundations** part. Everything runs locally and isolated — you never touch a system you don't own._

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
| 1 | [Computer Science Fundamentals](computer-science.md) | 🟢 Beginner | ~36m | Computation, abstraction, complexity and the models that underpin every security tool. |
| 2 | [Programming Fundamentals](programming.md) | 🟢 Beginner | ~60m | Variables, control flow, functions, types and memory as they matter to security work. |
| 3 | [Algorithms](algorithms.md) | 🟡 Intermediate | ~72m | Sorting, searching, graph traversal and the complexity analysis behind scanner and cracker design. |
| 4 | [Data Structures](data-structures.md) | 🟡 Intermediate | ~72m | Arrays, lists, trees, hash tables and tries, plus how their layout creates memory-safety bugs. |
| 5 | [Discrete Mathematics](discrete-mathematics.md) | 🟡 Intermediate | ~60m | Logic, sets, combinatorics, number theory and probability, the mathematical base of cryptography. |
| 6 | [Computer Architecture](computer-architecture.md) | 🟡 Intermediate | ~72m | CPU pipelines, registers, cache, MMU and privilege rings, the substrate exploits actually target. |
| 7 | [Operating Systems](operating-systems.md) | 🟡 Intermediate | ~84m | Processes, threads, scheduling, virtual memory, syscalls and the kernel/user boundary. |
| 8 | [Networking Primer](networking-primer.md) | 🟢 Beginner | ~48m | A fast, practical on-ramp to packets, addressing and protocol layering before the deep dive. |
| 9 | [Databases](databases.md) | 🟡 Intermediate | ~60m | Relational and NoSQL engines, SQL semantics, transactions and where injection actually happens. |
| 10 | [Virtualization](virtualization.md) | 🟡 Intermediate | ~48m | Hypervisor types, hardware-assisted virtualization, snapshots and lab isolation guarantees. |
| 11 | [Containers](containers.md) | 🟡 Intermediate | ~48m | Namespaces, cgroups, union filesystems and why a container is not a security boundary by default. |
| 12 | [Cloud Computing](cloud.md) | 🟡 Intermediate | ~48m | Service models, the shared responsibility model, regions, tenancy and cloud control planes. |
| 13 | [Linux](linux.md) | 🟢 Beginner | ~84m | Filesystem hierarchy, permissions, processes, systemd, package management and the shell. |
| 14 | [Windows](windows.md) | 🟢 Beginner | ~84m | NT architecture, registry, services, tokens, SIDs, ACLs and the Windows API surface. |
| 15 | [PowerShell](powershell.md) | 🟡 Intermediate | ~60m | Objects in the pipeline, remoting, execution policy, logging and offensive/defensive tradecraft. |
| 16 | [Bash and POSIX Shell](bash.md) | 🟢 Beginner | ~48m | Redirection, pipelines, quoting, job control and safe scripting patterns for security automation. |
| 17 | [Python](python.md) | 🟢 Beginner | ~96m | The default language of security tooling: sockets, requests, parsing, automation and packaging. |
| 18 | [C](c.md) | 🟠 Advanced | ~96m | Pointers, manual memory management and undefined behaviour, the source of most memory-corruption CVEs. |
| 19 | [C++](cpp.md) | 🟠 Advanced | ~84m | Objects, vtables, RAII, templates and the exploitation surface unique to C++ binaries. |
| 20 | [Rust](rust.md) | 🟠 Advanced | ~84m | Ownership, borrowing and lifetimes as a compile-time defence against memory-safety vulnerabilities. |
| 21 | [Go](go.md) | 🟡 Intermediate | ~72m | Goroutines, channels, static binaries and why Go dominates modern offensive and cloud tooling. |
| 22 | [JavaScript](javascript.md) | 🟡 Intermediate | ~72m | The event loop, prototypes, the DOM and the execution context that XSS lives inside. |
| 23 | [Assembly Language](assembly.md) | 🟠 Advanced | ~108m | x86-64 and ARM64 instruction sets, calling conventions and stack frames for reversing and exploitation. |
| 24 | [Git](git.md) | 🟢 Beginner | ~36m | Objects, refs, branching, history rewriting and how secrets leak through commit history. |
| 25 | [GitHub and Forge Security](github.md) | 🟢 Beginner | ~30m | Pull requests, Actions, tokens, branch protection and the supply-chain risks of a shared forge. |

**25 lessons.**

[← Repository home](../../README.md) · [Full contents](../../SUMMARY.md) · [Labs campaign](../../labs/README.md)
