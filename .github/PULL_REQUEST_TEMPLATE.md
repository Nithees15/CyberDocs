<!-- SPDX-License-Identifier: GPL-3.0-or-later -->
## What this changes

Briefly describe the change and why.

## Which module did you edit?

<!-- Everything is generated from _meta/ — edit the data/templates, not the generated pages. -->
- [ ] `_meta/topics_*.py` (add/rename lessons, tools, projects, cheatsheets)
- [ ] `_meta/refdata.py` (references)
- [ ] `_meta/labdata.py` (`PRACTICE` walkthroughs / `QUIZZES`)
- [ ] `_meta/deepdata.py` (short authored theory)
- [ ] `_meta/partlabs.py` / `bosslabs.py` (environments / boss labs)
- [ ] `_meta/lab_platform.py` / `generate.py` / `build_site.py` (rendering / site)
- [ ] `labserver/` (Lab Runner)
- [ ] Other:

## Checklist

- [ ] I edited the **data/templates in `_meta/`**, not the generated pages.
- [ ] `python _meta/generate.py` prints **"Link check: OK"** (no broken links).
- [ ] `python _meta/build_site.py` builds without errors.
- [ ] Any hands-on content targets **local, isolated, intentionally-vulnerable** labs only, and offensive
      techniques are paired with detection/defence.
- [ ] New source files carry the GPL header; files are UTF-8 with LF newlines.
- [ ] I agree my contribution is licensed under **GPL-3.0-or-later**.
