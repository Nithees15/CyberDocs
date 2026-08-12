<!-- SPDX-License-Identifier: GPL-3.0-or-later | Copyright (C) 2026 Nithees Narendra S -->
[Home](../README.md) › [Cheatsheets](README.md) › **Web Testing Cheatsheet**

# Web Testing Cheatsheet

> Payloads, encodings and checklists for the OWASP Top 10. Printable: use your browser's *Print → Save as PDF*.

_Domain: Web Security · Last updated 2026-08-13_

## Quick reference

This cheatsheet is a fast recall aid, not a tutorial — learn the concepts in the Manual, then keep this beside you while you work.

## Methodology (per endpoint)
1. **Map** — spider, note every parameter, header, cookie, and hidden field.
2. **Auth/Session** — test login, logout, reset, MFA; check cookie flags and session fixation.
3. **Access control** — swap IDs (IDOR), force-browse admin paths, change roles (BOLA/BFLA).
4. **Injection** — SQLi, NoSQLi, command, SSTI, XXE, LDAP — one payload class at a time.
5. **Client-side** — XSS (all contexts), CSRF, CORS, clickjacking, open redirect.
6. **Business logic** — quantity/price tampering, workflow skipping, race conditions.
7. **Config** — headers (CSP/HSTS), verbose errors, exposed files (`/.git`, backups).

## Fast checks
```bash
whatweb http://TARGET
ffuf -u http://TARGET/FUZZ -w wordlist.txt -mc 200,301,302,403
nikto -h http://TARGET
nuclei -u http://TARGET
```

## Header hygiene to verify
`Content-Security-Policy` · `Strict-Transport-Security` · `X-Content-Type-Options: nosniff` ·
`X-Frame-Options` / frame-ancestors · `Set-Cookie: HttpOnly; Secure; SameSite`.

See the [SQLi](sqli-payloads.md) and [XSS](xss-payloads.md) payload cheatsheets for injection strings.

## Related

- [All cheatsheets](README.md)
- [Tools reference](../reference/tools/README.md)
- [Repository home](../README.md)

