<!-- SPDX-License-Identifier: GPL-3.0-or-later | Copyright (C) 2026 Nithees Narendra S -->
[Home](../README.md) › [Cheatsheets](README.md) › **Networking and Ports Cheatsheet**

# Networking and Ports Cheatsheet

> Common ports, protocol flags, subnetting and quick references. Printable: use your browser's *Print → Save as PDF*.

_Domain: Networking · Last updated 2026-08-13_

## Quick reference

This cheatsheet is a fast recall aid, not a tutorial — learn the concepts in the Manual, then keep this beside you while you work.

## Common ports
| Port | Service | Port | Service |
| --- | --- | --- | --- |
| 20/21 | FTP | 143/993 | IMAP/IMAPS |
| 22 | SSH | 161/162 | SNMP |
| 23 | Telnet | 389/636 | LDAP/LDAPS |
| 25/587 | SMTP | 443 | HTTPS |
| 53 | DNS | 445 | SMB |
| 67/68 | DHCP | 3306 | MySQL |
| 69 | TFTP | 3389 | RDP |
| 80 | HTTP | 5432 | PostgreSQL |
| 88 | Kerberos | 5985/5986 | WinRM |
| 110/995 | POP3/POP3S | 6379 | Redis |
| 123 | NTP | 8080 | HTTP-alt |

## TCP flags & handshake
`SYN → SYN/ACK → ACK` (open). `FIN/ACK` (close). `RST` (reset). Half-open SYN scan never completes the ACK.

## Subnetting quick table
| CIDR | Mask | Hosts |
| --- | --- | --- |
| /24 | 255.255.255.0 | 254 |
| /25 | 255.255.255.128 | 126 |
| /26 | 255.255.255.192 | 62 |
| /27 | 255.255.255.224 | 30 |
| /28 | 255.255.255.240 | 14 |
| /30 | 255.255.255.252 | 2 |

## Private ranges (RFC 1918)
`10.0.0.0/8` · `172.16.0.0/12` · `192.168.0.0/16` · link-local `169.254.0.0/16` · loopback `127.0.0.0/8`

## Related

- [All cheatsheets](README.md)
- [Tools reference](../reference/tools/README.md)
- [Repository home](../README.md)

