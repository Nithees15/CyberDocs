<!-- SPDX-License-Identifier: GPL-3.0-or-later | Copyright (C) 2026 Nithees Narendra S -->
# Contributing to Cybersecurity-Mastery

Thanks for helping build this. A few things make contributing here different from a normal docs repo, so
please skim this first.

## The golden rule: everything is generated

**Do not hand-edit the generated pages** (`manual/`, `reference/`, `projects/`, `cheatsheets/`, `labs/`,
`site/`, `README.md`, `SUMMARY.md`, `progress.json`, …). They are produced from the data modules in
[`_meta/`](_meta/README.md) and will be overwritten. Edit the data, then regenerate:

```bash
python _meta/generate.py     # renders all Markdown; validates that there are no broken links
python _meta/build_site.py   # rebuilds the interactive site in ./site
```

`generate.py` must print **"Link check: OK"** — a PR that breaks a link will fail CI.

## Where to make changes

| To… | Edit | 
| --- | --- |
| Add/rename a lesson, tool, project or cheatsheet | `_meta/topics_core.py` / `topics_ext.py` / `topics_tools.py` |
| Add references (ATT&CK/OWASP/CWE/CAPEC/CVE/RFC, books, papers) | `_meta/refdata.py` (`REFS[slug]`) |
| Add a fully authored hands-on walkthrough | `_meta/labdata.py` (`PRACTICE[slug]`) — steps are `(goal, command, expected_output, why)` |
| Add an interactive quiz | `_meta/labdata.py` (`QUIZZES[slug]`) |
| Add short authored theory | `_meta/deepdata.py` (`DEEP[slug]`) — keep it tight; this is a *hands-on* course |
| Add/adjust a track's lab environment | `_meta/partlabs.py` (`PART_LABS[section_id]`) |
| Add a cross-topic boss lab | `_meta/bosslabs.py` (`BOSS`) |
| Fill a cheatsheet | `_meta/cheatdata.py` (`CHEATS[slug]`) |
| Change how any of the above renders | `_meta/lab_platform.py` (labs), `_meta/generate.py` (pages), `_meta/build_site.py` (site/UI) |

The site's interactive components come from custom fenced blocks (`cf-step`, `cf-quiz`, `cf-lab`,
`cf-terminal`) that `build_site.py` renders — you normally emit these from `lab_platform.py`, not by hand.

## Content ground rules

- **Hands-on first.** Theory stays short and clear; the centre of gravity of every lesson is doing.
- **Lawful and local.** Every lab must target local, isolated, intentionally-vulnerable environments. Never
  add anything that instructs attacking systems the reader does not own or is not authorised to test. Teach
  offensive techniques **alongside their detection and defence**.
- **No dead links, no duplication.** Link only to slugs that exist; the generator enforces this.
- **Accuracy.** Prefer primary sources (RFCs, vendor docs, MITRE) and real CVE/incident references.

## Coding conventions

- Python 3.8+, standard library only for `labserver/` (no third-party deps there).
- Files are UTF-8 with `\n` newlines. **Never** rewrite `_meta/*.py` with PowerShell `Set-Content` — it
  mangles non-ASCII and adds a BOM.
- Keep `labserver/server.py` console output **ASCII-only** (Windows cp1252 consoles crash on `→`/emoji).
- New source files should carry the GPL header (see any existing `_meta/*.py`).

## Submitting

1. Fork, branch, make your change in the `_meta/` data/templates.
2. Run `python _meta/generate.py && python _meta/build_site.py` and confirm the link check passes.
3. Open a PR describing what you added and which module you edited. By contributing you agree your
   contribution is licensed under **GPL-3.0-or-later** (see [LICENSE](LICENSE)).

Please also read the [Code of Conduct](CODE_OF_CONDUCT.md) and [Security policy](SECURITY.md).
