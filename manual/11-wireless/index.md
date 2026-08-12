<!-- SPDX-License-Identifier: GPL-3.0-or-later | Copyright (C) 2026 Nithees Narendra S -->
# Wireless and RF Security — Track

Security of radio-based protocols from Wi-Fi to cellular, tested against lab hardware only.

<div class="track-progress"><div class="progress" data-track-progress data-lessons="11-wireless/rf-fundamentals.html,11-wireless/wifi.html,11-wireless/bluetooth.html,11-wireless/rfid.html,11-wireless/nfc.html,11-wireless/zigbee.html,11-wireless/lora.html,11-wireless/cellular.html,11-wireless/sdr.html,11-wireless/gps.html"><i></i></div><div class="tp-label" style="color:var(--muted);font-size:13px;margin-top:6px">Your progress in this track</div></div>

**Set up the lab environment below once, then work the lessons — each one is hands-on-first.**

## Lab Environment

_Set up once, then use it for every chapter in the **Wireless and RF Security** part. Everything runs locally and isolated — you never touch a system you don't own._

This part is mostly conceptual and tool-driven — no dedicated vulnerable targets are needed. Work from Kali (or any Linux box) and the tools called out in each chapter.

**What you get**

| Target | How to reach it |
| --- | --- |
| `Kali / local shell` | everything you need is a terminal and the tools named per chapter |

**Provision it** — save this as `docker-compose.yml` and run `docker compose up -d` (or import the equivalent spec into CyberForge):

```yaml
# Optional scratch box for trying commands in isolation:
services:
  scratch:
    image: kalilinux/kali-rolling        # or debian:stable-slim
    container_name: scratch
    command: sleep infinity
    networks: [labnet]
networks:
  labnet: { driver: bridge, internal: true }
```

**Attacker box.** Run the chapter's commands directly on Kali, or in the disposable `scratch` container to keep your main system clean.

**Verify it works**

- `docker exec -it scratch bash` gives an isolated shell.

**Teardown.** `docker compose down` stops it; add `-v` to also drop volumes. Snapshot before big changes so you can revert.

> **Safety.** Keep intentionally-vulnerable targets on an isolated/`internal` network. Never expose them to the internet or attack anything outside this lab.


## Lessons

| # | Lesson | Difficulty | Hands-on | What you'll do |
| --- | --- | --- | --- | --- |
| 1 | [RF and Wireless Fundamentals](rf-fundamentals.md) | 🟢 Beginner | ~48m | Spectrum, modulation, antennas, SDR basics and the shared-medium threat model. |
| 2 | [Wi-Fi Security](wifi.md) | 🟡 Intermediate | ~84m | 802.11 frames, WEP/WPA/WPA2/WPA3, 4-way handshake, PMKID and enterprise EAP. |
| 3 | [Bluetooth and BLE Security](bluetooth.md) | 🟡 Intermediate | ~60m | Pairing, GATT, BLE sniffing, spoofing and vulnerabilities like KNOB and BlueBorne. |
| 4 | [RFID Security](rfid.md) | 🟡 Intermediate | ~48m | LF/HF tags, MIFARE, cloning, relay attacks and access-control bypass in a lab. |
| 5 | [NFC Security](nfc.md) | 🟡 Intermediate | ~36m | NDEF, card emulation, relay and replay, and mobile-wallet threat models. |
| 6 | [Zigbee and 802.15.4](zigbee.md) | 🟠 Advanced | ~48m | Mesh networking, key provisioning, sniffing and smart-home attack surface. |
| 7 | [LoRa and LoRaWAN](lora.md) | 🟠 Advanced | ~48m | Long-range IoT, join procedures, key management and replay/jamming risks. |
| 8 | [Cellular Security (4G/5G)](cellular.md) | 🟠 Advanced | ~60m | Air interface, IMSI catchers, roaming/SS7 risks and the 5G security architecture. |
| 9 | [Software Defined Radio](sdr.md) | 🟠 Advanced | ~60m | GNU Radio, capture/replay, signal identification and lawful experimentation. |
| 10 | [GPS and GNSS Security](gps.md) | 🟠 Advanced | ~36m | Positioning basics, spoofing, jamming and resilient-timing considerations. |

**10 lessons.**

[← Repository home](../../README.md) · [Full contents](../../SUMMARY.md) · [Labs campaign](../../labs/README.md)
