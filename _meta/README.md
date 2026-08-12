# `_meta/` — the repository generator

Everything in the repository outside this `_meta/` folder is **generated**. To change content, edit the
data/templates here and re-run the generator. This keeps ~600 pages consistent, cross-linked and free of dead
links.

## Pipeline

```
_meta/topics_core.py   ─┐
_meta/topics_ext.py     ├─ topic manifest (source of truth: sections, chapters, tools, projects, cheatsheets)
_meta/topics_tools.py  ─┘
_meta/refdata.py        ── curated references (ATT&CK/OWASP/CWE/CAPEC/CVE/RFC/NIST/books/papers) + curated labs
_meta/deepdata.py       ── hand-authored, expert-depth prose for flagship chapters (DEEP[slug])
_meta/cheatdata.py      ── real command references for key cheatsheets (CHEATS[slug])
_meta/lab_platform.py   ── THE single integration point for lab environments (CyberForge + Kali)
        │
        ▼
_meta/generate.py       ── renders all Markdown (Manual, Reference, Projects, Cheatsheets, indexes, root files)
_meta/build_site.py     ── renders the offline Unity-style web UI into ./site
```

## Commands

```bash
python _meta/generate.py     # (re)generate all Markdown — idempotent, validates links
python _meta/build_site.py   # (re)build the offline web UI in ./site
```

`generate.py` prints a link-check result; it must say "OK (no broken internal .md links)".

## How to extend

- **Add a chapter/tool/project/cheatsheet** → add a tuple to the relevant manifest in `topics_*.py`.
- **Add references to a chapter** → add a `REFS[slug]` entry in `refdata.py`.
- **Add a hands-on lab to a chapter** → add a `LABS[slug]` entry in `refdata.py` (rendered by `lab_platform`).
- **Deepen a chapter to expert prose** → add a `DEEP[slug]` entry in `deepdata.py` (overrides templated
  sections; keys: theory, history, internal, terminology, extra, realworld, mistakes, bestpractices, case).
- **Fill a cheatsheet** → add a `CHEATS[slug]` entry in `cheatdata.py`.
- **Retarget every lab to a different platform** → edit `lab_platform.py` only.

## Design rules

- **No dead links.** Content links only to slugs that exist; `validate_links()` fails the build otherwise.
- **Idempotent.** Re-running never duplicates; generated files are overwritten in place.
- **UTF-8, `\n` newlines.** Never rewrite these `.py` files with PowerShell `Set-Content` — it re-encodes
  non-ASCII (emoji, arrows) into mojibake and adds a BOM. Use an editor that preserves UTF-8 without BOM.
- **Resumable.** `progress.json` + `TODO.md` (repo root) track status; `deepdata.py`/`cheatdata.py` grow the
  authored coverage over successive passes without touching structure.

## Not generated (safe to hand-edit)

`LICENSE`, `CONTRIBUTING.md`, `CODE_OF_CONDUCT.md`, `SECURITY.md`, `.gitattributes`, `.gitignore`, `book.toml`,
`.github/`, `_suggestions/`, `labserver/`, and this file. Everything else is output.

## Licensing

The project is **GPL-3.0-or-later** (see `../LICENSE`). Source files in `_meta/` and `labserver/` carry a GPL
header; `generate.py`/`build_site.py` stamp an `SPDX-License-Identifier` line onto every generated `.md`,
`.yml` and `.html`. Keep the header on any new source file.
