<!-- SPDX-License-Identifier: GPL-3.0-or-later | Copyright (C) 2026 Nithees Narendra S -->
# Networking — Track

Protocol-by-protocol internals, on the wire. Every attack and every detection eventually reduces to bytes crossing a link.

<div class="track-progress"><div class="progress" data-track-progress data-lessons="01-networking/osi-model.html,01-networking/tcp-ip.html,01-networking/routing.html,01-networking/switching.html,01-networking/arp.html,01-networking/dhcp.html,01-networking/dns.html,01-networking/icmp.html,01-networking/http.html,01-networking/https.html,01-networking/tls.html,01-networking/ssh.html,01-networking/smtp.html,01-networking/ftp.html,01-networking/smb.html,01-networking/ldap.html,01-networking/kerberos.html,01-networking/bgp.html,01-networking/ipv6.html,01-networking/nat.html,01-networking/firewalls.html,01-networking/vpn.html,01-networking/load-balancers.html,01-networking/packet-analysis.html,01-networking/protocol-internals.html"><i></i></div><div class="tp-label" style="color:var(--muted);font-size:13px;margin-top:6px">Your progress in this track</div></div>

**Set up the lab environment below once, then work the lessons — each one is hands-on-first.**

## Lab Environment

_Set up once, then use it for every chapter in the **Networking** part. Everything runs locally and isolated — you never touch a system you don't own._

A small network range: a multi-service Linux target plus a packet-capture point, so you can scan, sniff and dissect real traffic.

**What you get**

| Target | How to reach it |
| --- | --- |
| `metasploitable` | Many open services (FTP/SSH/Telnet/SMB/HTTP/MySQL) — the scan & enumerate target |
| `Kali (you)` | Attacker + capture host (tcpdump/wireshark/tshark/nmap) |

**Provision it** — save this as `docker-compose.yml` and run `docker compose up -d` (or import the equivalent spec into CyberForge):

```yaml
# net-lab/docker-compose.yml  —  Networking part environment
services:
  metasploitable:
    image: tleemcjr/metasploitable2
    container_name: net-target
    networks: [labnet]
    # intentionally vulnerable services; keep it OFF any routed network
    command: /bin/sh -c "/etc/rc.local; tail -f /dev/null"

networks:
  labnet:
    driver: bridge
    internal: true          # no route to host/internet — fail closed
```

**Attacker box.** Your Kali box is the attacker. Put it on the same `labnet` network (`docker network connect labnet kali`) or use the published host ports. All targets are on an **internal, isolated** network by default — they cannot reach the internet or your host, which is exactly what we want.

**Verify it works**

- `docker compose up -d` then `docker network inspect labnet` shows the target's IP.
- From Kali on labnet: `nmap -sn <subnet>` finds the target; `nmap -sV <ip>` lists services.

**Notes**

- Metasploitable 2 is deliberately vulnerable — never expose it on a routed network.

**Teardown.** `docker compose down` stops it; add `-v` to also drop volumes. Snapshot before big changes so you can revert.

> **Safety.** Keep intentionally-vulnerable targets on an isolated/`internal` network. Never expose them to the internet or attack anything outside this lab.


## Lessons

| # | Lesson | Difficulty | Hands-on | What you'll do |
| --- | --- | --- | --- | --- |
| 1 | [The OSI Model](osi-model.md) | 🟢 Beginner | ~30m | Seven-layer reference model, what each layer really owns and how to use it as a triage tool. |
| 2 | [TCP/IP](tcp-ip.md) | 🟢 Beginner | ~48m | The DoD model, IP datagrams, TCP state machine, UDP, ports, MTU and fragmentation. |
| 3 | [Routing](routing.md) | 🟡 Intermediate | ~48m | Longest-prefix match, static vs dynamic routing, RIP/OSPF/EIGRP and route-based attacks. |
| 4 | [Switching](switching.md) | 🟡 Intermediate | ~36m | MAC learning, VLANs, trunking, STP and layer-2 attacks such as VLAN hopping and STP takeover. |
| 5 | [ARP](arp.md) | 🟢 Beginner | ~30m | Address resolution, the ARP cache, gratuitous ARP and the mechanics of ARP spoofing. |
| 6 | [DHCP](dhcp.md) | 🟢 Beginner | ~30m | DORA exchange, options, relays, rogue servers, starvation attacks and DHCP snooping. |
| 7 | [DNS](dns.md) | 🟡 Intermediate | ~60m | Resolution flow, record types, zone transfers, DNSSEC, DoH/DoT, tunnelling and cache poisoning. |
| 8 | [ICMP](icmp.md) | 🟢 Beginner | ~30m | Message types, path MTU discovery, traceroute mechanics and ICMP covert channels. |
| 9 | [HTTP](http.md) | 🟢 Beginner | ~48m | Request/response grammar, methods, status codes, headers, HTTP/1.1 vs /2 vs /3 framing. |
| 10 | [HTTPS](https.md) | 🟡 Intermediate | ~30m | HTTP over TLS, SNI, ALPN, HSTS, mixed content and interception proxies. |
| 11 | [TLS](tls.md) | 🟠 Advanced | ~72m | Handshake internals for TLS 1.2 and 1.3, cipher suites, session resumption and downgrade attacks. |
| 12 | [SSH](ssh.md) | 🟡 Intermediate | ~48m | Transport, auth and connection layers, host keys, agent forwarding, tunnels and key hygiene. |
| 13 | [SMTP and Email Transport](smtp.md) | 🟡 Intermediate | ~48m | Envelope vs headers, relaying, SPF, DKIM, DMARC, MTA-STS and spoofing mechanics. |
| 14 | [FTP and File Transfer](ftp.md) | 🟢 Beginner | ~30m | Active vs passive mode, control/data channels, anonymous access, FTPS and SFTP contrasted. |
| 15 | [SMB](smb.md) | 🟡 Intermediate | ~60m | Dialects, session setup, signing, shares, named pipes and the protocol behind lateral movement. |
| 16 | [LDAP](ldap.md) | 🟡 Intermediate | ~48m | Directory model, DNs, filters, binds, LDAPS/StartTLS, injection and enumeration. |
| 17 | [Kerberos](kerberos.md) | 🟠 Advanced | ~84m | AS-REQ through TGS-REP, tickets, PACs, delegation and the full family of ticket attacks. |
| 18 | [BGP](bgp.md) | 🟠 Advanced | ~60m | Path-vector routing, ASNs, peering, route leaks, prefix hijacking, RPKI and internet-scale outages. |
| 19 | [IPv6](ipv6.md) | 🟡 Intermediate | ~48m | Addressing, SLAAC, NDP, extension headers, transition mechanisms and IPv6-only attack paths. |
| 20 | [NAT](nat.md) | 🟢 Beginner | ~30m | SNAT, DNAT, PAT, hairpinning, NAT traversal, STUN/TURN and why NAT is not a firewall. |
| 21 | [Firewalls](firewalls.md) | 🟡 Intermediate | ~60m | Packet filtering, stateful inspection, NGFW, WAF, nftables/pf rulesets and evasion techniques. |
| 22 | [VPN](vpn.md) | 🟡 Intermediate | ~60m | IPsec, WireGuard, OpenVPN, SSL VPNs, split tunnelling and VPN appliance CVEs. |
| 23 | [Load Balancers and Proxies](load-balancers.md) | 🟡 Intermediate | ~48m | L4/L7 balancing, health checks, X-Forwarded-For trust, TLS termination and request smuggling. |
| 24 | [Packet Analysis](packet-analysis.md) | 🟡 Intermediate | ~72m | Capture, filter, follow and interpret traffic with tcpdump, Wireshark and tshark. |
| 25 | [Protocol Internals and Reverse Engineering](protocol-internals.md) | 🟠 Advanced | ~72m | Dissecting undocumented and binary protocols, building dissectors and fuzzing parsers. |

**25 lessons.**

[← Repository home](../../README.md) · [Full contents](../../SUMMARY.md) · [Labs campaign](../../labs/README.md)
