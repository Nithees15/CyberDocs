<!-- SPDX-License-Identifier: GPL-3.0-or-later | Copyright (C) 2026 Nithees Narendra S -->
# TODO — Cybersecurity-Mastery

_Generated 2026-08-13. Hands-on-first model: keep growing runnable labs, not prose._

## Done

- [x] Interactive lesson layout (~75% hands-on): stepper w/ Run/Copy, live terminal, quizzes, progress
- [x] Dark black/grey + terminal-green web-app UI (callouts, cards, tabs, badges, big Prev/Next)
- [x] Lab Runner backend (labserver/) — real execution in a Kali container, localhost + token guarded
- [x] Per-track lab environments + downloadable docker compose in labs/environments/
- [x] Labs pillar: hands-on campaign + 6 cross-topic boss labs
- [x] 13 lessons with fully authored, runnable walkthroughs; MCQ quizzes on flagships
- [x] All 293 lessons + reference + projects + cheatsheets generated, zero broken links

## Next — grow the hands-on coverage

- [ ] Author `PRACTICE[slug]` walkthroughs + `QUIZZES[slug]` for the remaining lessons (add to `_meta/labdata.py`). Priority: web, offensive, blue-team, cloud, identity.
- [ ] Add part environments for the remaining sections in `_meta/partlabs.py` (crypto, secure-dev, wireless, compliance).
- [ ] Add more boss labs (mobile, ICS/OT, wifi) in `_meta/bosslabs.py`.
- [ ] Lab Runner: optional streaming (SSE) + a persistent-shell PTY mode; vendor xterm.js for a richer terminal.
- [ ] Expand cheatsheet command tables (`_meta/cheatdata.py`).

## Authored practice labs so far

- active-directory-attacks, buffer-overflow, command-injection, csrf, idor, jwt, memory-forensics, privilege-escalation, scanning, sql-injection, threat-hunting, xss, yara

## How to resume

1. Add a `PRACTICE[slug]` entry in `_meta/labdata.py` (walkthrough/challenges/detect/skills).
2. Add a part environment in `_meta/partlabs.py` for any uncovered section.
3. `python _meta/generate.py` (idempotent, validates links) then `python _meta/build_site.py`.
4. Deep theory (kept short) lives in `_meta/deepdata.py`; boss labs in `_meta/bosslabs.py`.
