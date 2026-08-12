<!-- SPDX-License-Identifier: GPL-3.0-or-later | Copyright (C) 2026 Nithees Narendra S -->
[Home](../../README.md) › [Tools](README.md) › **radare2**

# radare2

> Command-line reverse-engineering framework for analysis and patching.

| | |
| --- | --- |
| **Category** | Reverse Engineering |
| **Difficulty** | 🔴 Expert |
| **Estimated time to proficiency** | ~12 hours |
| **Availability** | Present in `kali-linux-everything`; also installable standalone |
| **Last updated** | 2026-08-13 |

## Purpose

radare2 is used for: Command-line reverse-engineering framework for analysis and patching. Know precisely what problem it solves so you reach for it at the right moment and not out of habit.

## Architecture

Understand how radare2 is put together — its major components, where it keeps state, and how it talks to targets or data. That model is what lets you predict its behaviour and its blind spots.

## Installation

On Kali it is already present. Standalone: use the distribution package or the official release. Verify with `--version` and confirm you are running a current build, since security tools change quickly.

## Configuration

Note the config file locations, profiles, and any API keys or wordlists radare2 depends on. Keep configuration in version control so runs are reproducible.

## Core Commands & Arguments

Learn the ten flags you will use daily before the hundred you will not. The cheatsheet in this repo lists them; below, focus on the arguments that change *behaviour* (scope, intensity, output) rather than cosmetics.

## Examples

Work the examples against the labs in this repository, never against systems you do not own. Start minimal, read the output critically, then add options one at a time.

## Workflows

radare2 is rarely used alone. Learn where it sits in a chain — what feeds it and what consumes its output — so it becomes one stage of a repeatable pipeline.

## Detection

Everything radare2 does is observable to a defender. Learn its network and host signatures so you can both operate deliberately and, on the blue team, detect its use.

## Limitations

Know what radare2 does *not* do and where it produces false positives or negatives. A tool trusted beyond its limits is a liability.

## Alternatives

Keep one or two alternatives in mind for when radare2 is blocked, unavailable, or the wrong fit — diversity of tooling is resilience.

## Automation & Integration

Prefer machine-readable output (JSON/XML/CSV) and wire radare2 into scripts, CI, or your notes so results are captured, diffable and repeatable.

## Troubleshooting

When radare2 misbehaves, check scope and permissions first, then connectivity, then the tool. Read its verbose/debug output before searching the web.

## See also

- Cheatsheets: [browse the printable cheatsheets](../../cheatsheets/README.md)
- [All tools](README.md) · [Repository home](../../README.md)

---

_Tool reference · Reverse Engineering · 🔴 Expert · Last updated 2026-08-13._
