<!-- SPDX-License-Identifier: GPL-3.0-or-later | Copyright (C) 2026 Nithees Narendra S -->
[Home](../README.md) › [Cheatsheets](README.md) › **Hashcat and John Cheatsheet**

# Hashcat and John Cheatsheet

> Modes, masks, rules and common hash formats. Printable: use your browser's *Print → Save as PDF*.

_Domain: Cryptography · Last updated 2026-08-13_

## Quick reference

This cheatsheet is a fast recall aid, not a tutorial — learn the concepts in the Manual, then keep this beside you while you work.

## Attack modes
| Mode | Meaning |
| --- | --- |
| `-a 0` | Straight (wordlist) |
| `-a 1` | Combination (two lists) |
| `-a 3` | Brute-force / mask |
| `-a 6` | Wordlist + mask |
| `-a 7` | Mask + wordlist |

## Common hash types (`-m`)
| `-m` | Hash |
| --- | --- |
| 0 | MD5 |
| 100 | SHA1 |
| 1400 | SHA-256 |
| 1800 | sha512crypt ($6$) |
| 3200 | bcrypt ($2*$) |
| 1000 | NTLM |
| 5600 | NetNTLMv2 |
| 13100 | Kerberoast (TGS-REP) |
| 18200 | AS-REP |
| 22000 | WPA-PBKDF2 (PMKID/handshake) |

## Recipes
```bash
hashcat -m 1000 hashes.txt rockyou.txt                     # NTLM + wordlist
hashcat -m 0 hashes.txt rockyou.txt -r rules/best64.rule   # with rules
hashcat -m 3200 hash.txt -a 3 ?l?l?l?l?l?d?d               # bcrypt mask
hashcat -m 22000 hs.hc22000 wordlist.txt                   # WPA
hashcat --show -m 1000 hashes.txt                          # show cracked
```
Mask charsets: `?l` a-z · `?u` A-Z · `?d` 0-9 · `?s` symbols · `?a` all · `?b` 0x00-0xff.

## John equivalent
`john --format=NT --wordlist=rockyou.txt hashes.txt` · `john --show hashes.txt`

## Related

- [All cheatsheets](README.md)
- [Tools reference](../reference/tools/README.md)
- [Repository home](../README.md)

