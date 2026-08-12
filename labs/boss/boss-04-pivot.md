<!-- SPDX-License-Identifier: GPL-3.0-or-later | Copyright (C) 2026 Nithees Narendra S -->
[Home](../../README.md) › [Labs](../README.md) › **Boss Lab 4 — Pivot Across Segmented Networks**

# Boss Lab 4 — Pivot Across Segmented Networks

> Only the DMZ host is reachable. Compromise it, then pivot to reach a target on the isolated `secure` segment that you cannot route to directly.

| | |
| --- | --- |
| **Difficulty** | Advanced |
| **Est. time** | ~4 hours |
| **Tracks** | Networking, Offensive |

## Environment

A three-network range: your `labnet`, an internal `dmz`, and a `secure` segment only reachable through a dual-homed host (compose with three networks).

> Everything is local and isolated. This is a capstone: it assumes you've worked the related chapters below.

## Objectives (capture the flags)

- [ ] DMZ host foothold
- [ ] internal network map
- [ ] secure-segment flag

## Stages

_Work them in order. Each stage has a hint — try hard before opening it._

### Stage 1 — Breach the DMZ

Compromise the internet-facing host.

<details><summary>Hint</summary>

Standard recon → exploit.

</details>

### Stage 2 — Discover the second network

From the DMZ host, find the interface/route into `secure`.

<details><summary>Hint</summary>

`ip a`, `ip r`, and ARP/ping sweeps from the pivot host.

</details>

### Stage 3 — Tunnel

Stand up a pivot (chisel/ssh -D/ligolo) so your Kali tools reach `secure`.

<details><summary>Hint</summary>

proxychains + a SOCKS proxy through the DMZ host.

</details>

### Stage 4 — Reach the crown jewel

Scan and exploit the `secure`-segment target through the tunnel.

<details><summary>Hint</summary>

Point nmap/exploits at the internal IP via proxychains.

</details>

### Stage 5 — Map the segmentation

Document exactly which firewall rule allowed the pivot.

<details><summary>Hint</summary>

The fix is usually one egress/segmentation rule on the dual-homed host.

</details>

## Debrief

Which segmentation or egress control would have stopped the pivot? Why is 'NAT' not a security boundary here?

## Chapters this draws on

- [Scanning](../../manual/06-offensive-security/scanning.md)
- [Exploitation](../../manual/06-offensive-security/exploitation.md)
- [Lateral Movement](../../manual/06-offensive-security/lateral-movement.md)
- [Firewalls](../../manual/01-networking/firewalls.md)
- [NAT](../../manual/01-networking/nat.md)

[← Back to the Labs campaign](../README.md)

