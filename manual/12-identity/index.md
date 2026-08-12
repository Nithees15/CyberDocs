<!-- SPDX-License-Identifier: GPL-3.0-or-later | Copyright (C) 2026 Nithees Narendra S -->
# Identity and Access — Track

The directory, authentication and federation systems that attackers target to own everything.

<div class="track-progress"><div class="progress" data-track-progress data-lessons="12-identity/identity-fundamentals.html,12-identity/active-directory.html,12-identity/azure-ad.html,12-identity/ldap-identity.html,12-identity/kerberos-identity.html,12-identity/ntlm.html,12-identity/sso.html,12-identity/mfa.html,12-identity/passwordless.html,12-identity/pam.html,12-identity/identity-governance.html"><i></i></div><div class="tp-label" style="color:var(--muted);font-size:13px;margin-top:6px">Your progress in this track</div></div>

**Set up the lab environment below once, then work the lessons — each one is hands-on-first.**

## Lab Environment

_Set up once, then use it for every chapter in the **Identity and Access** part. Everything runs locally and isolated — you never touch a system you don't own._

An identity lab. Samba AD-DC gives you Kerberos, LDAP and NTLM to attack; for full Windows AD attack paths, provision GOAD.

**What you get**

| Target | How to reach it |
| --- | --- |
| `samba-ad` | LDAP/Kerberos/SMB directory services to enumerate and attack |
| `GOAD (optional)` | full multi-DC Windows forest for realistic AD attacks |

**Provision it** — save this as `docker-compose.yml` and run `docker compose up -d` (or import the equivalent spec into CyberForge):

```yaml
# id-lab/docker-compose.yml  —  Identity part environment
services:
  samba-ad:
    image: nowsci/samba-domain            # or diladele/samba-ad-dc
    environment:
      - DOMAIN=LAB.LOCAL
      - DOMAINPASS=Passw0rd!Passw0rd!
      - HOSTIP=172.20.0.10
    networks:
      labnet: { ipv4_address: 172.20.0.10 }
    cap_add: ["SYS_ADMIN"]

networks:
  labnet:
    driver: bridge
    ipam: { config: [{ subnet: 172.20.0.0/24 }] }
```

**Attacker box.** `netexec ldap/smb`, `kerbrute`, `impacket-*`, `bloodhound-python` from Kali. Samba covers enumeration, Kerberoasting basics and LDAP; GOAD covers delegation, ACL abuse and DCSync faithfully.

**Verify it works**

- `netexec smb 172.20.0.10` shows the domain and hostname.
- `ldapsearch -x -H ldap://172.20.0.10 -b 'dc=lab,dc=local'` returns the base DN.

**Notes**

- **GOAD** (github.com/Orange-Cyberdefense/GOAD) is the recommended full AD lab; it provisions Windows VMs via Vagrant on an isolated network.

**Teardown.** `docker compose down` stops it; add `-v` to also drop volumes. Snapshot before big changes so you can revert.

> **Safety.** Keep intentionally-vulnerable targets on an isolated/`internal` network. Never expose them to the internet or attack anything outside this lab.


## Lessons

| # | Lesson | Difficulty | Hands-on | What you'll do |
| --- | --- | --- | --- | --- |
| 1 | [Identity Fundamentals](identity-fundamentals.md) | 🟢 Beginner | ~48m | Identification, authentication, authorization, accounting and identity lifecycle. |
| 2 | [Active Directory](active-directory.md) | 🟠 Advanced | ~96m | Forests, domains, trusts, GPOs, the schema and the objects attackers pivot through. |
| 3 | [Entra ID (Azure AD)](azure-ad.md) | 🟠 Advanced | ~72m | Tenants, conditional access, app registrations, tokens and cloud-identity attacks. |
| 4 | [LDAP as an Identity Store](ldap-identity.md) | 🟡 Intermediate | ~36m | Schema, binds, group membership and query-driven enumeration. |
| 5 | [Kerberos in Depth](kerberos-identity.md) | 🔴 Expert | ~84m | Tickets, PAC, S4U delegation, encryption types and the full ticket-attack catalogue. |
| 6 | [NTLM](ntlm.md) | 🟠 Advanced | ~60m | Challenge/response, pass-the-hash, relay, coercion and why NTLM persists. |
| 7 | [Single Sign-On](sso.md) | 🟡 Intermediate | ~48m | Federation patterns, SAML/OIDC trade-offs, session risks and IdP compromise impact. |
| 8 | [Multi-Factor Authentication](mfa.md) | 🟡 Intermediate | ~48m | Factors, TOTP/push/WebAuthn, MFA fatigue, bypasses and phishing-resistant design. |
| 9 | [Passwordless and FIDO2](passwordless.md) | 🟡 Intermediate | ~36m | WebAuthn ceremonies, passkeys, attestation and enterprise rollout. |
| 10 | [Privileged Access Management](pam.md) | 🟠 Advanced | ~48m | Tiering, just-in-time access, vaulting, session recording and break-glass. |
| 11 | [Identity Governance](identity-governance.md) | 🟡 Intermediate | ~36m | Joiner/mover/leaver, access reviews, entitlement creep and least privilege at scale. |

**11 lessons.**

[← Repository home](../../README.md) · [Full contents](../../SUMMARY.md) · [Labs campaign](../../labs/README.md)
