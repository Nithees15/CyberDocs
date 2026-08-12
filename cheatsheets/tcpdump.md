<!-- SPDX-License-Identifier: GPL-3.0-or-later | Copyright (C) 2026 Nithees Narendra S -->
[Home](../README.md) › [Cheatsheets](README.md) › **tcpdump Cheatsheet**

# tcpdump Cheatsheet

> BPF expressions and capture recipes. Printable: use your browser's *Print → Save as PDF*.

_Domain: Networking · Last updated 2026-08-13_

## Quick reference

This cheatsheet is a fast recall aid, not a tutorial — learn the concepts in the Manual, then keep this beside you while you work.

## Essentials
| Command | Purpose |
| --- | --- |
| `tcpdump -D` | List interfaces |
| `tcpdump -i eth0` | Capture on interface |
| `tcpdump -i eth0 -w out.pcap` | Write to file |
| `tcpdump -r out.pcap` | Read a file |
| `tcpdump -nn` | No name/port resolution |
| `tcpdump -A` / `-X` | ASCII / hex+ASCII payload |
| `tcpdump -c 100` | Stop after N packets |
| `tcpdump -s 0` | Full packet (snaplen) |

## Filters (BPF)
```
tcpdump -i eth0 host 10.0.0.5
tcpdump -i eth0 net 10.0.0.0/24
tcpdump -i eth0 tcp port 443
tcpdump -i eth0 'tcp[tcpflags] & tcp-syn != 0'     # SYNs
tcpdump -i eth0 'port 53'                          # DNS
tcpdump -i eth0 'icmp'                             # pings
tcpdump -i eth0 src 10.0.0.5 and dst port 80
```
Combine with `and` / `or` / `not`. Rotate files: `-G 3600 -w cap-%F-%H.pcap`.

## Related

- [All cheatsheets](README.md)
- [Tools reference](../reference/tools/README.md)
- [Repository home](../README.md)

