<!-- SPDX-License-Identifier: GPL-3.0-or-later | Copyright (C) 2026 Nithees Narendra S -->
[Home](../README.md) › [Cheatsheets](README.md) › **Wireshark/tshark Filter Cheatsheet**

# Wireshark/tshark Filter Cheatsheet

> Display and capture filters for fast triage. Printable: use your browser's *Print → Save as PDF*.

_Domain: Networking · Last updated 2026-08-13_

## Quick reference

This cheatsheet is a fast recall aid, not a tutorial — learn the concepts in the Manual, then keep this beside you while you work.

## Capture filters (BPF — set before capture)
| Filter | Matches |
| --- | --- |
| `host 10.0.0.5` | To/from a host |
| `net 10.0.0.0/24` | A subnet |
| `port 443` | A port |
| `tcp port 80 or tcp port 443` | Web traffic |
| `not arp and not stp` | Drop noise |

## Display filters (after capture)
| Filter | Matches |
| --- | --- |
| `ip.addr == 10.0.0.5` | Host either direction |
| `tcp.port == 22` | SSH |
| `http.request.method == "POST"` | POSTs |
| `http.response.code == 200` | 200 OK |
| `dns.qry.name contains "exfil"` | Suspicious DNS |
| `tcp.flags.syn==1 && tcp.flags.ack==0` | SYN scan probes |
| `tls.handshake.type == 1` | ClientHello |
| `frame contains "password"` | Bytes match |
| `tcp.analysis.retransmission` | Retransmits |

## Workflow
Right-click a packet → **Follow → TCP/HTTP Stream** to reassemble a conversation.
**Statistics → Conversations / Protocol Hierarchy** for a top-down view.
`tshark -r cap.pcap -Y 'http.request' -T fields -e ip.dst -e http.host -e http.request.uri`

## Related

- [All cheatsheets](README.md)
- [Tools reference](../reference/tools/README.md)
- [Repository home](../README.md)

