<!-- SPDX-License-Identifier: GPL-3.0-or-later | Copyright (C) 2026 Nithees Narendra S -->
# CWE Index

> Weaknesses referenced across the repository. See the [CWE chapter](../manual/14-threat-intelligence/cwe.md) for the taxonomy.

| CWE | Weakness | Chapters |
| --- | --- | --- |
| [CWE-22](https://cwe.mitre.org/data/definitions/22.html) | Improper Limitation of a Pathname (Path Traversal) | [Directory Traversal](../manual/04-vulnerabilities/directory-traversal.md) |
| [CWE-73](https://cwe.mitre.org/data/definitions/73.html) | External Control of File Name or Path | [Local File Inclusion](../manual/04-vulnerabilities/lfi.md) |
| [CWE-77](https://cwe.mitre.org/data/definitions/77.html) | Command Injection | [OS Command Injection](../manual/04-vulnerabilities/command-injection.md) |
| [CWE-78](https://cwe.mitre.org/data/definitions/78.html) | OS Command Injection | [Remote Code Execution](../manual/04-vulnerabilities/rce.md), [OS Command Injection](../manual/04-vulnerabilities/command-injection.md) |
| [CWE-79](https://cwe.mitre.org/data/definitions/79.html) | Improper Neutralization of Input During Web Page Generation | [Cross-Site Scripting](../manual/04-vulnerabilities/xss.md) |
| [CWE-79](https://cwe.mitre.org/data/definitions/79.html) | XSS | [OWASP Top 10](../manual/03-web-security/owasp-top-10.md), [DOM-Based XSS](../manual/04-vulnerabilities/dom-xss.md), [Stored XSS](../manual/04-vulnerabilities/stored-xss.md) |
| [CWE-89](https://cwe.mitre.org/data/definitions/89.html) | SQL Injection | [OWASP Top 10](../manual/03-web-security/owasp-top-10.md), [SQL Injection](../manual/04-vulnerabilities/sql-injection.md), [Blind SQL Injection](../manual/04-vulnerabilities/blind-sql-injection.md) |
| [CWE-90](https://cwe.mitre.org/data/definitions/90.html) | LDAP Injection | [LDAP](../manual/01-networking/ldap.md) |
| [CWE-94](https://cwe.mitre.org/data/definitions/94.html) | Code Injection | [Remote Code Execution](../manual/04-vulnerabilities/rce.md), [Server-Side Template Injection](../manual/04-vulnerabilities/template-injection.md) |
| [CWE-98](https://cwe.mitre.org/data/definitions/98.html) | Improper Control of Filename for Include/Require in PHP | [Remote File Inclusion](../manual/04-vulnerabilities/rfi.md) |
| [CWE-98](https://cwe.mitre.org/data/definitions/98.html) | PHP Remote File Inclusion | [Local File Inclusion](../manual/04-vulnerabilities/lfi.md) |
| [CWE-120](https://cwe.mitre.org/data/definitions/120.html) | Buffer Copy without Checking Size | [Buffer Overflows](../manual/04-vulnerabilities/buffer-overflow.md) |
| [CWE-121](https://cwe.mitre.org/data/definitions/121.html) | Stack-based Buffer Overflow | [Stack-Based Overflows](../manual/04-vulnerabilities/stack-overflow.md) |
| [CWE-122](https://cwe.mitre.org/data/definitions/122.html) | Heap-based Buffer Overflow | [Heap-Based Overflows](../manual/04-vulnerabilities/heap-overflow.md) |
| [CWE-134](https://cwe.mitre.org/data/definitions/134.html) | Use of Externally-Controlled Format String | [Format String Vulnerabilities](../manual/04-vulnerabilities/format-strings.md) |
| [CWE-190](https://cwe.mitre.org/data/definitions/190.html) | Integer Overflow or Wraparound | [Integer Overflows](../manual/04-vulnerabilities/integer-overflow.md) |
| [CWE-191](https://cwe.mitre.org/data/definitions/191.html) | Integer Underflow | [Integer Overflows](../manual/04-vulnerabilities/integer-overflow.md) |
| [CWE-208](https://cwe.mitre.org/data/definitions/208.html) | Observable Timing Discrepancy | [Applied Cryptanalysis](../manual/02-cryptography/cryptanalysis.md) |
| [CWE-256](https://cwe.mitre.org/data/definitions/256.html) | Plaintext Storage of a Password | [Password Hashing and Storage](../manual/02-cryptography/password-storage.md) |
| [CWE-284](https://cwe.mitre.org/data/definitions/284.html) | Improper Access Control | [Insecure Direct Object References](../manual/04-vulnerabilities/idor.md) |
| [CWE-287](https://cwe.mitre.org/data/definitions/287.html) | Improper Authentication | [OWASP Top 10](../manual/03-web-security/owasp-top-10.md) |
| [CWE-295](https://cwe.mitre.org/data/definitions/295.html) | Improper Certificate Validation | [X.509 Certificates](../manual/02-cryptography/certificates.md) |
| [CWE-321](https://cwe.mitre.org/data/definitions/321.html) | Use of Hard-coded Cryptographic Key | [JSON Web Tokens](../manual/03-web-security/jwt.md) |
| [CWE-326](https://cwe.mitre.org/data/definitions/326.html) | Inadequate Encryption Strength | [TLS](../manual/01-networking/tls.md) |
| [CWE-327](https://cwe.mitre.org/data/definitions/327.html) | Use of a Broken or Risky Cryptographic Algorithm | [TLS](../manual/01-networking/tls.md), [AES](../manual/02-cryptography/aes.md) |
| [CWE-328](https://cwe.mitre.org/data/definitions/328.html) | Use of Weak Hash | [Hash Functions](../manual/02-cryptography/hashes.md) |
| [CWE-329](https://cwe.mitre.org/data/definitions/329.html) | Not Using a Random IV with CBC | [AES](../manual/02-cryptography/aes.md) |
| [CWE-347](https://cwe.mitre.org/data/definitions/347.html) | Improper Verification of Cryptographic Signature | [HMAC](../manual/02-cryptography/hmac.md), [Applied Cryptanalysis](../manual/02-cryptography/cryptanalysis.md), [JSON Web Tokens](../manual/03-web-security/jwt.md), [SAML](../manual/03-web-security/saml.md) |
| [CWE-350](https://cwe.mitre.org/data/definitions/350.html) | Reliance on Reverse DNS Resolution | [DNS](../manual/01-networking/dns.md) |
| [CWE-352](https://cwe.mitre.org/data/definitions/352.html) | CSRF | [OWASP Top 10](../manual/03-web-security/owasp-top-10.md), [OAuth 2.0 and 2.1](../manual/03-web-security/oauth.md) |
| [CWE-352](https://cwe.mitre.org/data/definitions/352.html) | Cross-Site Request Forgery | [Cross-Site Request Forgery](../manual/04-vulnerabilities/csrf.md) |
| [CWE-362](https://cwe.mitre.org/data/definitions/362.html) | Race Condition | [Race Conditions](../manual/04-vulnerabilities/race-conditions.md) |
| [CWE-367](https://cwe.mitre.org/data/definitions/367.html) | TOCTOU Race Condition | [Race Conditions](../manual/04-vulnerabilities/race-conditions.md) |
| [CWE-416](https://cwe.mitre.org/data/definitions/416.html) | Use After Free | [Heap-Based Overflows](../manual/04-vulnerabilities/heap-overflow.md), [Memory Corruption](../manual/04-vulnerabilities/memory-corruption.md) |
| [CWE-444](https://cwe.mitre.org/data/definitions/444.html) | HTTP Request/Response Smuggling | [HTTP Request Smuggling](../manual/03-web-security/request-smuggling.md) |
| [CWE-476](https://cwe.mitre.org/data/definitions/476.html) | NULL Pointer Dereference | [Memory Corruption](../manual/04-vulnerabilities/memory-corruption.md) |
| [CWE-502](https://cwe.mitre.org/data/definitions/502.html) | Deserialization of Untrusted Data | [Insecure Deserialization](../manual/04-vulnerabilities/insecure-deserialization.md) |
| [CWE-564](https://cwe.mitre.org/data/definitions/564.html) | Hibernate Injection | [SQL Injection](../manual/04-vulnerabilities/sql-injection.md) |
| [CWE-601](https://cwe.mitre.org/data/definitions/601.html) | Open Redirect | [OAuth 2.0 and 2.1](../manual/03-web-security/oauth.md) |
| [CWE-611](https://cwe.mitre.org/data/definitions/611.html) | Improper Restriction of XML External Entity Reference | [XML External Entity Injection](../manual/04-vulnerabilities/xxe.md) |
| [CWE-614](https://cwe.mitre.org/data/definitions/614.html) | Sensitive Cookie Without Secure | [Cookies](../manual/03-web-security/cookies.md) |
| [CWE-639](https://cwe.mitre.org/data/definitions/639.html) | Authorization Bypass Through User-Controlled Key | [Insecure Direct Object References](../manual/04-vulnerabilities/idor.md) |
| [CWE-759](https://cwe.mitre.org/data/definitions/759.html) | Use of a One-Way Hash without a Salt | [Hash Functions](../manual/02-cryptography/hashes.md) |
| [CWE-780](https://cwe.mitre.org/data/definitions/780.html) | Use of RSA Without OAEP | [RSA](../manual/02-cryptography/rsa.md) |
| [CWE-787](https://cwe.mitre.org/data/definitions/787.html) | Out-of-bounds Write | [Buffer Overflows](../manual/04-vulnerabilities/buffer-overflow.md), [Stack-Based Overflows](../manual/04-vulnerabilities/stack-overflow.md), [Memory Corruption](../manual/04-vulnerabilities/memory-corruption.md), [Exploit Development](../manual/06-offensive-security/exploit-development.md) |
| [CWE-829](https://cwe.mitre.org/data/definitions/829.html) | Inclusion of Functionality from Untrusted Control Sphere | [Dependency and Supply Chain Vulnerabilities](../manual/04-vulnerabilities/supply-chain-vulnerabilities.md) |
| [CWE-916](https://cwe.mitre.org/data/definitions/916.html) | Use of Password Hash With Insufficient Computational Effort | [Password Hashing and Storage](../manual/02-cryptography/password-storage.md) |
| [CWE-918](https://cwe.mitre.org/data/definitions/918.html) | SSRF | [OWASP Top 10](../manual/03-web-security/owasp-top-10.md) |
| [CWE-918](https://cwe.mitre.org/data/definitions/918.html) | Server-Side Request Forgery | [Server-Side Request Forgery](../manual/04-vulnerabilities/ssrf.md) |
| [CWE-942](https://cwe.mitre.org/data/definitions/942.html) | Permissive Cross-domain Policy with Untrusted Domains | [CORS](../manual/03-web-security/cors.md) |
| [CWE-1004](https://cwe.mitre.org/data/definitions/1004.html) | Sensitive Cookie Without HttpOnly | [Cookies](../manual/03-web-security/cookies.md) |
| [CWE-1021](https://cwe.mitre.org/data/definitions/1021.html) | Improper Restriction of Rendered UI Layers (Clickjacking) | [Content Security Policy](../manual/03-web-security/csp.md) |
| [CWE-1336](https://cwe.mitre.org/data/definitions/1336.html) | Server-Side Template Injection | [Server-Side Template Injection](../manual/04-vulnerabilities/template-injection.md) |
| [CWE-1357](https://cwe.mitre.org/data/definitions/1357.html) | Reliance on Insufficiently Trustworthy Component | [Dependency and Supply Chain Vulnerabilities](../manual/04-vulnerabilities/supply-chain-vulnerabilities.md) |
| [CWE-1391](https://cwe.mitre.org/data/definitions/1391.html) | Use of Weak Credentials | [SSH](../manual/01-networking/ssh.md) |

[← Repository home](../README.md)
