<!-- SPDX-License-Identifier: GPL-3.0-or-later | Copyright (C) 2026 Nithees Narendra S -->
# Changelog

All notable changes to Cybersecurity-Mastery are recorded here. This project follows a breadth-first, then recursively-deepen model.

## [0.3.0] — 2026-08-13 — Interactive learning app

### Changed

- **Rebuilt every chapter into an interactive W3Schools/GeeksforGeeks-style LESSON** (~75% hands-on / ~25% theory): short Overview → interactive Hands-On Practice → compact Reference.
- **New web-app UI:** dark **black/grey + terminal-green** theme (no blue), colored callouts, cards, a **stepper** walkthrough with **▸ Run** / **📋 Copy** on every command, a **Live Terminal**, instant **quizzes**, per-lesson/track **progress** (saved in-browser), big Prev/Next, active-scroll TOC.
- Nav restructured into **Tracks** (the 16 domains) with per-track progress bars and a home dashboard.
### Added

- **Lab Runner** (`labserver/`, pure Python stdlib): a localhost-only, token-guarded backend that runs each command **inside a Kali container** (`docker exec`) so the site's Run buttons and terminal execute for real. Graceful **📋 Copy** fallback when it isn't running.
- Downloadable per-track `docker compose` environments in `labs/environments/`; **▸ Start lab** brings them up.
- Interactive MCQ quizzes for the flagship lessons; `cf-step`/`cf-quiz`/`cf-lab`/`cf-terminal` component protocol in the Markdown→HTML build.

## [0.2.0] — 2026-08-13 — Hands-on-first refactor

### Changed

- **Flipped every chapter to hands-on-first:** short **Concept** (necessary theory only, kept tight) → a large **Hands-On Practice** block → a compact **Reference**. Roughly half of each page is doing.
- Hands-On Practice = lab environment + guided walkthrough (command → expected output → why) + *Try it yourself* challenges (hints + solutions) + *Detect & defend* + a skills check.
- Theme is now **monochrome black & grey** (no blue), light and dark.
### Added

- **Per-part lab environments:** a one-time `docker compose` / CyberForge setup at the top of each section README that provisions that whole part's targets (9 sections).
- **Labs pillar** (`labs/`): a hands-on campaign that orders every lab by track, plus 6 cross-topic **boss labs** (full kill-chains: web→root, breach→Domain Admin, purple-team detection, network pivot, malware IR, SSRF→cloud takeover).
- 13 chapters with fully authored, runnable walkthroughs against bWAPP/DVWA/Juice-Shop/Metasploitable/GOAD/LocalStack.

## [0.1.0] — 2026-08-13

### Added

- Initial breadth-first generation of the entire repository from a data-driven generator.
- 293 Manual chapters across 16 sections, each with the full document template (theory → labs → framework mappings → further reading).
- 89 tool reference pages and 12 learning-platform roadmaps.
- 100 graded projects and 28 cheatsheets (13 filled with full command references).
- 16 flagship chapters hand-authored to expert depth (SQLi, XSS, SSRF, buffer overflow, TLS, Kerberos, AD attacks, ATT&CK, incident response, DNS).
- 10 curated CyberForge + Kali hands-on labs; every practical chapter carries a lab.
- Curated framework references (ATT&CK/OWASP/CWE/CAPEC/CVE/NIST/RFC) with cross-cutting indexes.
- Self-contained, serverless offline web UI (Unity-documentation style) with search and Mermaid.
- Resumable build: progress.json, TODO.md, and a single-point lab-platform integration.

### Notes

- Non-flagship chapters are structurally complete with real references and labs; prose is enriched recursively. See TODO.md for the deepening queue.
