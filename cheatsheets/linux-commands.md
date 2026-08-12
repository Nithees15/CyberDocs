<!-- SPDX-License-Identifier: GPL-3.0-or-later | Copyright (C) 2026 Nithees Narendra S -->
[Home](../README.md) › [Cheatsheets](README.md) › **Linux Command-Line Cheatsheet**

# Linux Command-Line Cheatsheet

> Everyday and security-relevant Linux commands in one printable page. Printable: use your browser's *Print → Save as PDF*.

_Domain: Foundations · Last updated 2026-08-13_

## Quick reference

This cheatsheet is a fast recall aid, not a tutorial — learn the concepts in the Manual, then keep this beside you while you work.

## Navigation & files
| Command | Purpose |
| --- | --- |
| `pwd` / `cd -` | Print working dir / jump to previous dir |
| `ls -la` | Long listing incl. hidden & permissions |
| `find / -name '*.conf' 2>/dev/null` | Find files, suppress errors |
| `find / -perm -4000 2>/dev/null` | Find SUID binaries (privesc triage) |
| `grep -rn "password" .` | Recursive search with line numbers |
| `stat file` | Timestamps, inode, permissions |
| `du -sh *` / `df -h` | Dir sizes / filesystem usage |

## Permissions & ownership
| Command | Purpose |
| --- | --- |
| `chmod 640 file` | rw-r----- |
| `chown user:group file` | Set owner/group |
| `umask` | Default permission mask |
| `getcap -r / 2>/dev/null` | Find file capabilities |

## Processes, services, network
| Command | Purpose |
| --- | --- |
| `ps aux --sort=-%mem` | Processes by memory |
| `top` / `htop` | Live process view |
| `systemctl status svc` | Service state |
| `ss -tulpn` | Listening TCP/UDP sockets + PIDs |
| `lsof -i :443` | What holds a port |
| `ip a` / `ip r` | Addresses / routes |

## Users & auth (triage)
| Command | Purpose |
| --- | --- |
| `id` / `whoami` / `groups` | Current identity |
| `sudo -l` | What you can run as root (privesc) |
| `cat /etc/passwd` / `/etc/group` | Accounts / groups |
| `last` / `w` | Login history / who is on |

## Text processing
`cut -d: -f1 /etc/passwd` · `awk -F: '{print $1}' file` · `sed 's/old/new/g' file` ·
`sort | uniq -c | sort -rn` · `tr -d '\r'` · `jq '.'`

## Related

- [All cheatsheets](README.md)
- [Tools reference](../reference/tools/README.md)
- [Repository home](../README.md)

