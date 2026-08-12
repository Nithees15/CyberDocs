<!-- SPDX-License-Identifier: GPL-3.0-or-later | Copyright (C) 2026 Nithees Narendra S -->
[Home](../README.md) › [Cheatsheets](README.md) › **Nmap Cheatsheet**

# Nmap Cheatsheet

> Scan types, timing, NSE and output options at a glance. Printable: use your browser's *Print → Save as PDF*.

_Domain: Networking · Last updated 2026-08-13_

## Quick reference

This cheatsheet is a fast recall aid, not a tutorial — learn the concepts in the Manual, then keep this beside you while you work.

## Host discovery
| Command | Purpose |
| --- | --- |
| `nmap -sn 10.0.0.0/24` | Ping sweep (no port scan) |
| `nmap -Pn host` | Skip discovery, treat as up |
| `nmap -PS22,80,443 host` | TCP SYN discovery on ports |

## Port scanning
| Command | Purpose |
| --- | --- |
| `nmap -sS host` | SYN (half-open) scan — default as root |
| `nmap -sT host` | TCP connect (no root) |
| `nmap -sU host` | UDP scan (slow) |
| `nmap -p-` | All 65535 TCP ports |
| `nmap -p 80,443,8080` | Specific ports |
| `nmap -F` | Fast (top 100) |
| `nmap --top-ports 1000` | Top N ports |

## Service, OS, scripts
| Command | Purpose |
| --- | --- |
| `nmap -sV host` | Version detection |
| `nmap -O host` | OS detection |
| `nmap -A host` | Aggressive: -sV -O -sC --traceroute |
| `nmap -sC host` | Default safe NSE scripts |
| `nmap --script vuln host` | Vuln category scripts |
| `nmap --script "http-*" host` | Category glob |

## Timing & output
| Flag | Purpose |
| --- | --- |
| `-T0..-T5` | paranoid → insane (stealth ↔ speed) |
| `--min-rate/--max-rate` | Packets per second control |
| `-oA base` | Save normal + XML + grepable |
| `-v` / `-d` | Verbose / debug |
| `--reason` | Why a port is in its state |

> Scan only hosts you own or are authorised to test. A `-T4 -p-` full scan is loud; an IDS sees the SYN sweep.

## Related

- [All cheatsheets](README.md)
- [Tools reference](../reference/tools/README.md)
- [Repository home](../README.md)

