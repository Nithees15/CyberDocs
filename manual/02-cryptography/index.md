<!-- SPDX-License-Identifier: GPL-3.0-or-later | Copyright (C) 2026 Nithees Narendra S -->
# Cryptography — Track

Primitives, protocols and the failure modes that turn strong maths into broken systems.

<div class="track-progress"><div class="progress" data-track-progress data-lessons="02-cryptography/cryptography-foundations.html,02-cryptography/symmetric.html,02-cryptography/asymmetric.html,02-cryptography/aes.html,02-cryptography/rsa.html,02-cryptography/ecc.html,02-cryptography/diffie-hellman.html,02-cryptography/hashes.html,02-cryptography/mac.html,02-cryptography/hmac.html,02-cryptography/digital-signatures.html,02-cryptography/certificates.html,02-cryptography/pki.html,02-cryptography/tls-cryptography.html,02-cryptography/password-storage.html,02-cryptography/randomness.html,02-cryptography/post-quantum.html,02-cryptography/cryptanalysis.html"><i></i></div><div class="tp-label" style="color:var(--muted);font-size:13px;margin-top:6px">Your progress in this track</div></div>

**Set up the lab environment below once, then work the lessons — each one is hands-on-first.**

## Lab Environment

_Set up once, then use it for every chapter in the **Cryptography** part. Everything runs locally and isolated — you never touch a system you don't own._

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
| 1 | [Cryptography Foundations](cryptography-foundations.md) | 🟢 Beginner | ~36m | Confidentiality, integrity, authenticity, threat models, Kerckhoffs's principle and entropy. |
| 2 | [Symmetric Cryptography](symmetric.md) | 🟡 Intermediate | ~60m | Block and stream ciphers, modes of operation, padding, IV/nonce handling and AEAD. |
| 3 | [Asymmetric Cryptography](asymmetric.md) | 🟡 Intermediate | ~60m | Trapdoor functions, key pairs, hybrid encryption and the maths behind public-key systems. |
| 4 | [AES](aes.md) | 🟡 Intermediate | ~48m | Rijndael internals, key schedule, rounds, GCM/CBC/CTR modes and practical misuse. |
| 5 | [RSA](rsa.md) | 🟠 Advanced | ~60m | Key generation, padding schemes, common implementation attacks and CTF-style factorisation. |
| 6 | [Elliptic Curve Cryptography](ecc.md) | 🟠 Advanced | ~60m | Curve arithmetic, ECDSA, EdDSA, X25519 and nonce-reuse key recovery. |
| 7 | [Diffie-Hellman](diffie-hellman.md) | 🟡 Intermediate | ~36m | Key agreement, ephemeral vs static, forward secrecy, small-subgroup and Logjam attacks. |
| 8 | [Hash Functions](hashes.md) | 🟢 Beginner | ~36m | Preimage and collision resistance, MD5/SHA families, BLAKE3 and length-extension. |
| 9 | [Message Authentication Codes](mac.md) | 🟡 Intermediate | ~30m | MAC goals, CBC-MAC, CMAC, Poly1305 and encrypt-then-MAC composition rules. |
| 10 | [HMAC](hmac.md) | 🟡 Intermediate | ~30m | Construction, security proof intuition, key sizing and constant-time verification. |
| 11 | [Digital Signatures](digital-signatures.md) | 🟡 Intermediate | ~48m | Signature schemes, non-repudiation, signing vs encryption and signature-verification bypasses. |
| 12 | [X.509 Certificates](certificates.md) | 🟡 Intermediate | ~48m | Fields, extensions, chains, SANs, revocation, CT logs and validation mistakes. |
| 13 | [Public Key Infrastructure](pki.md) | 🟠 Advanced | ~60m | CAs, RAs, trust stores, enrolment, internal PKI design and AD CS abuse paths. |
| 14 | [TLS Cryptography](tls-cryptography.md) | 🟠 Advanced | ~48m | How the primitives compose inside TLS, key schedules, 0-RTT risks and protocol attacks. |
| 15 | [Password Hashing and Storage](password-storage.md) | 🟡 Intermediate | ~36m | bcrypt, scrypt, Argon2, salting, peppering, work factors and credential-stuffing economics. |
| 16 | [Randomness and Key Management](randomness.md) | 🟠 Advanced | ~48m | CSPRNGs, entropy sources, key rotation, HSMs, KMS design and key-compromise recovery. |
| 17 | [Post-Quantum Cryptography](post-quantum.md) | 🟠 Advanced | ~48m | Shor and Grover impact, ML-KEM/ML-DSA, hybrid deployment and harvest-now-decrypt-later. |
| 18 | [Applied Cryptanalysis](cryptanalysis.md) | 🔴 Expert | ~72m | Padding oracles, timing side channels, bit-flipping, nonce reuse and hash-length extension in practice. |

**18 lessons.**

[← Repository home](../../README.md) · [Full contents](../../SUMMARY.md) · [Labs campaign](../../labs/README.md)
