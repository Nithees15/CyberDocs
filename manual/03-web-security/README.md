<!-- SPDX-License-Identifier: GPL-3.0-or-later | Copyright (C) 2026 Nithees Narendra S -->
# Web Security — Track

How the web platform works, how its trust boundaries are drawn, and where they leak.

<div class="track-progress"><div class="progress" data-track-progress data-lessons="03-web-security/web-architecture.html,03-web-security/http-protocol.html,03-web-security/cookies.html,03-web-security/sessions.html,03-web-security/authentication.html,03-web-security/authorization.html,03-web-security/jwt.html,03-web-security/oauth.html,03-web-security/openid-connect.html,03-web-security/saml.html,03-web-security/owasp-top-10.html,03-web-security/api-security.html,03-web-security/graphql.html,03-web-security/websockets.html,03-web-security/cors.html,03-web-security/csp.html,03-web-security/browser-security-model.html,03-web-security/file-upload-security.html,03-web-security/client-side-security.html,03-web-security/web-cache-security.html,03-web-security/request-smuggling.html"><i></i></div><div class="tp-label" style="color:var(--muted);font-size:13px;margin-top:6px">Your progress in this track</div></div>

**Set up the lab environment below once, then work the lessons — each one is hands-on-first.**

## Lab Environment

_Set up once, then use it for every chapter in the **Web Security** part. Everything runs locally and isolated — you never touch a system you don't own._

Four classic vulnerable web apps on one isolated network. Point Burp/ZAP and your browser at any of them; every web-security and vulnerability chapter uses one of these.

**What you get**

| Target | How to reach it |
| --- | --- |
| `bWAPP` | http://localhost:8081  — 100+ web bugs, best for targeted practice |
| `DVWA` | http://localhost:8082  — adjustable security levels |
| `Juice Shop` | http://localhost:8083 — modern SPA, full OWASP Top 10 |
| `WebGoat` | http://localhost:8084 — guided lessons |

**Provision it** — save this as `docker-compose.yml` and run `docker compose up -d` (or import the equivalent spec into CyberForge):

```yaml
# web-lab/docker-compose.yml  —  Web Security part environment
services:
  bwapp:
    image: raesene/bwapp
    ports: ["8081:80"]
    networks: [labnet]
  dvwa:
    image: vulnerables/web-dvwa
    ports: ["8082:80"]
    networks: [labnet]
  juice-shop:
    image: bkimminich/juice-shop
    ports: ["8083:3000"]
    networks: [labnet]
  webgoat:
    image: webgoat/webgoat
    ports: ["8084:8080"]
    networks: [labnet]

networks:
  labnet:
    driver: bridge
    # routed here so your browser/Burp on the host can reach the apps;
    # for a jeopardy-style setup put the attacker box on labnet and set internal: true
```

**Attacker box.** Drive these from your browser through **Burp Suite** or **OWASP ZAP** as an intercepting proxy. `sqlmap`, `ffuf`, `nikto`, `wpscan` and friends all run from Kali against the published ports.

**Verify it works**

- `docker compose up -d` then browse to http://localhost:8081 (bWAPP install page) — run its `install.php` once to initialise the database.
- Juice Shop answers on http://localhost:8083 immediately.

**Notes**

- First bWAPP run: visit `/install.php` to create the DB. DVWA: log in `admin/password`, click 'Create/Reset Database', then set the security level per exercise.

**Teardown.** `docker compose down` stops it; add `-v` to also drop volumes. Snapshot before big changes so you can revert.

> **Safety.** Keep intentionally-vulnerable targets on an isolated/`internal` network. Never expose them to the internet or attack anything outside this lab.


## Lessons

| # | Lesson | Difficulty | Hands-on | What you'll do |
| --- | --- | --- | --- | --- |
| 1 | [Web Application Architecture](web-architecture.md) | 🟢 Beginner | ~36m | Clients, servers, reverse proxies, APIs, SPAs, rendering models and where controls belong. |
| 2 | [HTTP for Security Testing](http-protocol.md) | 🟢 Beginner | ~48m | Method semantics, header trust, caching, redirects, parsers and desync-prone constructs. |
| 3 | [Cookies](cookies.md) | 🟢 Beginner | ~36m | Attributes, scope, SameSite, prefixes, partitioning and cookie tossing/injection. |
| 4 | [Session Management](sessions.md) | 🟡 Intermediate | ~48m | Session identifiers, fixation, invalidation, server vs stateless sessions and concurrency. |
| 5 | [Web Authentication](authentication.md) | 🟡 Intermediate | ~60m | Password flows, MFA, WebAuthn/passkeys, magic links, rate limiting and account recovery abuse. |
| 6 | [Authorization](authorization.md) | 🟡 Intermediate | ~60m | RBAC, ABAC, ReBAC, policy engines, multi-tenancy and the roots of broken access control. |
| 7 | [JSON Web Tokens](jwt.md) | 🟡 Intermediate | ~48m | JWS/JWE structure, alg confusion, kid injection, claims validation and revocation strategy. |
| 8 | [OAuth 2.0 and 2.1](oauth.md) | 🟠 Advanced | ~72m | Grant types, PKCE, redirect URI validation, token leakage and confused-deputy attacks. |
| 9 | [OpenID Connect](openid-connect.md) | 🟠 Advanced | ~48m | ID tokens, discovery, nonce/state, hybrid flow risks and identity-provider mix-up attacks. |
| 10 | [SAML](saml.md) | 🟠 Advanced | ~60m | Assertions, bindings, signature wrapping, XSW attacks and canonicalisation pitfalls. |
| 11 | [OWASP Top 10](owasp-top-10.md) | 🟢 Beginner | ~60m | The 2021 categories mapped to concrete bug classes, tests and remediations. |
| 12 | [API Security](api-security.md) | 🟡 Intermediate | ~72m | REST design flaws, OWASP API Top 10, mass assignment, BOLA/BFLA and gateway controls. |
| 13 | [GraphQL Security](graphql.md) | 🟠 Advanced | ~48m | Introspection, query depth/complexity abuse, batching attacks and resolver-level authorization. |
| 14 | [WebSockets](websockets.md) | 🟡 Intermediate | ~36m | Upgrade handshake, origin checks, CSWSH, message-level authorization and proxying. |
| 15 | [CORS](cors.md) | 🟡 Intermediate | ~36m | Preflights, credentialed requests, reflected origins, null origin and misconfiguration impact. |
| 16 | [Content Security Policy](csp.md) | 🟠 Advanced | ~48m | Directives, nonces, strict-dynamic, common bypasses and rollout with report-only. |
| 17 | [Browser Security Model](browser-security-model.md) | 🟡 Intermediate | ~60m | Same-origin policy, site isolation, sandboxing, storage partitioning and security headers. |
| 18 | [File Upload Security](file-upload-security.md) | 🟡 Intermediate | ~36m | Content-type and extension validation, path handling, image parsers and storage isolation. |
| 19 | [Client-Side Security](client-side-security.md) | 🟠 Advanced | ~60m | DOM clobbering, prototype pollution, postMessage, clickjacking and supply-chain scripts. |
| 20 | [Web Cache Poisoning and Deception](web-cache-security.md) | 🟠 Advanced | ~48m | Cache keys, unkeyed input, poisoning primitives, deception and CDN-level defences. |
| 21 | [HTTP Request Smuggling](request-smuggling.md) | 🔴 Expert | ~60m | CL.TE, TE.CL, TE.TE, H2 downgrade desync, discovery methodology and exploitation impact. |

**21 lessons.**

[← Repository home](../../README.md) · [Full contents](../../SUMMARY.md) · [Labs campaign](../../labs/README.md)
