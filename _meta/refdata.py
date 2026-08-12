# -*- coding: utf-8 -*-
# Cybersecurity-Mastery - an interactive, offline cybersecurity learning app.
# Copyright (C) 2026 Nithees Narendra S
# SPDX-License-Identifier: GPL-3.0-or-later
#
# This file is part of Cybersecurity-Mastery. It is free software: you can
# redistribute it and/or modify it under the terms of the GNU General Public
# License as published by the Free Software Foundation, either version 3 of the
# License, or (at your option) any later version. There is NO WARRANTY. See the
# LICENSE file for the full text. For use outside the GPL-3.0 terms (e.g.
# proprietary/commercial), contact the copyright holder for a separate licence.

"""Curated reference data keyed by chapter slug.

Everything here is real: CWE/CAPEC/ATT&CK/CVE identifiers, RFC numbers, NIST
publications, canonical books and papers. The generator turns these into linked
"mappings" and "further reading" tables (Unity-docs "all refs" style). Slugs not
present fall back to domain-based defaults built in ``generate.py``.

Deep, hand-authored per-chapter content lives in ``deepdata.py`` and is exposed
here as ``DEEP`` so the generator can override its templated sections.

Value shapes
------------
REFS[slug] = {
    "cwe":   [(id:int, "title"), ...],
    "capec": [(id:int, "title"), ...],
    "attack":["T1190", "T1059.001", ...],
    "owasp": [("A03:2021 Injection", "url-or-empty"), ...],
    "cve":   ["CVE-2021-44228", ...],
    "nist":  [("SP 800-53 Rev.5", "note"), ...],
    "rfc":   [(9110, "HTTP Semantics"), ...],
    "books": [("Title", "Author"), ...],
    "papers":[("Title", "Venue/Year"), ...],
    "docs":  [("Label", "https://..."), ...],
}
LABS[slug] = kwargs for lab_platform.render_lab (minus lab_no/chapter_title/category/difficulty).
"""

try:
    from deepdata import DEEP  # noqa: F401  (per-slug hand-authored deep content)
except Exception:               # pragma: no cover - deep content is optional
    DEEP = {}

# --------------------------------------------------------------------------
# Reusable book shelves per domain
# --------------------------------------------------------------------------
BOOKS = {
    "web": [
        ("The Web Application Hacker's Handbook, 2nd ed.", "Stuttard & Pinto"),
        ("Real-World Bug Hunting", "Peter Yaworski"),
        ("The Tangled Web", "Michal Zalewski"),
        ("Web Security for Developers", "Malcolm McDonald"),
    ],
    "network": [
        ("TCP/IP Illustrated, Vol. 1", "W. Richard Stevens"),
        ("Computer Networking: A Top-Down Approach", "Kurose & Ross"),
        ("Practical Packet Analysis, 3rd ed.", "Chris Sanders"),
    ],
    "crypto": [
        ("Serious Cryptography, 2nd ed.", "Jean-Philippe Aumasson"),
        ("Cryptography Engineering", "Ferguson, Schneier & Kohno"),
        ("Real-World Cryptography", "David Wong"),
    ],
    "offense": [
        ("The Hacker Playbook 3", "Peter Kim"),
        ("Penetration Testing", "Georgia Weidman"),
        ("Red Team Field Manual (RTFM)", "Ben Clark"),
        ("Advanced Penetration Testing", "Wil Allsopp"),
    ],
    "defense": [
        ("Blue Team Handbook", "Don Murdoch"),
        ("The Practice of Network Security Monitoring", "Richard Bejtlich"),
        ("Intelligence-Driven Incident Response", "Roberts & Brown"),
    ],
    "malware": [
        ("Practical Malware Analysis", "Sikorski & Honig"),
        ("The Art of Memory Forensics", "Ligh, Case, Levy & Walters"),
        ("Practical Binary Analysis", "Dennis Andriesse"),
    ],
    "forensics": [
        ("File System Forensic Analysis", "Brian Carrier"),
        ("The Art of Memory Forensics", "Ligh, Case, Levy & Walters"),
        ("Windows Forensic Analysis", "Harlan Carvey"),
    ],
    "exploit": [
        ("Hacking: The Art of Exploitation, 2nd ed.", "Jon Erickson"),
        ("The Shellcoder's Handbook, 2nd ed.", "Anley et al."),
        ("A Guide to Kernel Exploitation", "Perla & Oldani"),
    ],
    "cloud": [
        ("Hacking Kubernetes", "Martin & Hausenblas"),
        ("Practical Cloud Security", "Chris Dotson"),
        ("Container Security", "Liz Rice"),
    ],
    "secdev": [
        ("Threat Modeling: Designing for Security", "Adam Shostack"),
        ("Building Secure and Reliable Systems", "Google SRE"),
        ("Alice and Bob Learn Application Security", "Tanya Janca"),
    ],
    "grc": [
        ("The CISSP Study Guide", "Chapple, Stewart & Gibson"),
        ("Security Risk Management", "Evan Wheeler"),
        ("How to Measure Anything in Cybersecurity Risk", "Hubbard & Seiersen"),
    ],
    "foundations": [
        ("Computer Systems: A Programmer's Perspective, 3rd ed.", "Bryant & O'Hallaron"),
        ("Operating Systems: Three Easy Pieces", "Arpaci-Dusseau"),
        ("The Linux Programming Interface", "Michael Kerrisk"),
    ],
    "identity": [
        ("Active Directory, 5th ed.", "Desmond, Richards, Allen & Lowe-Norris"),
        ("Pentesting Active Directory & Windows-based Infrastructure", "Isakov"),
    ],
    "wireless": [
        ("Hacking Exposed Wireless, 3rd ed.", "Cache, Wright & Liu"),
        ("The Hardware Hacking Handbook", "van Woudenberg & O'Flynn"),
    ],
}

# General, discipline-shaping papers referenced widely.
PAPERS_GENERAL = [
    ("Reflections on Trusting Trust", "Ken Thompson, 1984"),
    ("Smashing the Stack for Fun and Profit", "Aleph One, Phrack 49, 1996"),
    ("The Protection of Information in Computer Systems", "Saltzer & Schroeder, 1975"),
]

DOCS_STD = [
    ("MITRE ATT&CK", "https://attack.mitre.org/"),
    ("OWASP", "https://owasp.org/"),
    ("NIST CSRC Publications", "https://csrc.nist.gov/publications"),
]

# --------------------------------------------------------------------------
# Per-slug references
# --------------------------------------------------------------------------
REFS = {
    # ---- 01 networking ----
    "tcp-ip": {
        "rfc": [(791, "Internet Protocol"), (793, "Transmission Control Protocol"),
                (9293, "TCP (updated)"), (768, "User Datagram Protocol"), (1122, "Host Requirements")],
        "attack": ["T1040", "T1046", "T1571"],
        "capec": [(94, "Adversary in the Middle")],
        "books": BOOKS["network"],
        "docs": [("IANA Port Registry", "https://www.iana.org/assignments/service-names-port-numbers/")],
    },
    "dns": {
        "rfc": [(1034, "Domain Names — Concepts"), (1035, "Domain Names — Implementation"),
                (4033, "DNSSEC Introduction"), (8484, "DNS over HTTPS"), (7858, "DNS over TLS")],
        "attack": ["T1071.004", "T1568.002", "T1590.002", "T1048.003"],
        "capec": [(142, "DNS Cache Poisoning"), (261, "Fuzzing for garnering other adjacent info")],
        "cwe": [(350, "Reliance on Reverse DNS Resolution")],
        "cve": ["CVE-2008-1447"],
        "books": BOOKS["network"],
    },
    "tls": {
        "rfc": [(8446, "TLS 1.3"), (5246, "TLS 1.2"), (6066, "TLS Extensions"),
                (7457, "Summarizing Known Attacks on TLS/DTLS")],
        "attack": ["T1557", "T1040"],
        "cwe": [(326, "Inadequate Encryption Strength"), (327, "Use of a Broken or Risky Cryptographic Algorithm")],
        "cve": ["CVE-2014-0160", "CVE-2014-3566"],
        "books": BOOKS["crypto"],
        "docs": [("SSL Labs Best Practices", "https://github.com/ssllabs/research/wiki/SSL-and-TLS-Deployment-Best-Practices")],
    },
    "ssh": {
        "rfc": [(4251, "SSH Protocol Architecture"), (4252, "SSH Authentication"),
                (4253, "SSH Transport Layer"), (4254, "SSH Connection Protocol")],
        "attack": ["T1021.004", "T1563.001", "T1098.004"],
        "cwe": [(1391, "Use of Weak Credentials")],
        "books": BOOKS["network"],
    },
    "kerberos": {
        "rfc": [(4120, "The Kerberos Network Authentication Service (V5)"), (6113, "Kerberos FAST")],
        "attack": ["T1558.003", "T1558.001", "T1558.002", "T1550.003", "T1208"],
        "capec": [(645, "Use of Captured Tickets (Pass The Ticket)")],
        "books": BOOKS["identity"],
    },
    "smb": {
        "attack": ["T1021.002", "T1570", "T1135", "T1187"],
        "cve": ["CVE-2017-0144", "CVE-2020-0796"],
        "capec": [(645, "Use of Captured Tickets")],
        "books": BOOKS["identity"],
    },
    "arp": {"attack": ["T1557.002", "T1040"], "capec": [(94, "Adversary in the Middle")], "books": BOOKS["network"]},
    "bgp": {"rfc": [(4271, "BGP-4"), (7454, "BGP Operations and Security"), (6811, "BGP Prefix Origin Validation")],
            "cve": ["CVE-2022-40318"], "books": BOOKS["network"]},
    "http": {"rfc": [(9110, "HTTP Semantics"), (9112, "HTTP/1.1"), (9113, "HTTP/2"), (9114, "HTTP/3")],
             "attack": ["T1071.001"], "books": BOOKS["web"]},
    "dhcp": {"rfc": [(2131, "Dynamic Host Configuration Protocol"), (3046, "DHCP Relay Agent Option")],
             "attack": ["T1557"], "books": BOOKS["network"]},
    "icmp": {"rfc": [(792, "Internet Control Message Protocol"), (4443, "ICMPv6")],
             "attack": ["T1095", "T1048"], "books": BOOKS["network"]},
    "ipv6": {"rfc": [(8200, "IPv6 Specification"), (4861, "Neighbor Discovery"), (4862, "IPv6 SLAAC")],
             "attack": ["T1557"], "books": BOOKS["network"]},
    "smtp": {"rfc": [(5321, "SMTP"), (7208, "SPF"), (6376, "DKIM"), (7489, "DMARC")],
             "attack": ["T1566.001", "T1114"], "books": BOOKS["network"]},
    "ldap": {"rfc": [(4511, "LDAP: The Protocol"), (4513, "LDAP Authentication Methods")],
             "attack": ["T1087.002", "T1069.002"], "cwe": [(90, "LDAP Injection")], "books": BOOKS["identity"]},

    # ---- 02 cryptography ----
    "aes": {"cwe": [(327, "Use of a Broken or Risky Cryptographic Algorithm"), (329, "Not Using a Random IV with CBC")],
            "docs": [("NIST FIPS 197 (AES)", "https://csrc.nist.gov/pubs/fips/197/final")],
            "books": BOOKS["crypto"]},
    "rsa": {"cwe": [(780, "Use of RSA Without OAEP")], "cve": ["CVE-2017-15361"],
            "papers": [("A Method for Obtaining Digital Signatures (RSA)", "Rivest, Shamir, Adleman, 1978")],
            "books": BOOKS["crypto"]},
    "hashes": {"cwe": [(328, "Use of Weak Hash"), (759, "Use of a One-Way Hash without a Salt")],
               "docs": [("NIST FIPS 180-4 (SHS)", "https://csrc.nist.gov/pubs/fips/180-4/final")],
               "books": BOOKS["crypto"]},
    "hmac": {"rfc": [(2104, "HMAC: Keyed-Hashing for Message Authentication")],
             "cwe": [(347, "Improper Verification of Cryptographic Signature")], "books": BOOKS["crypto"]},
    "certificates": {"rfc": [(5280, "X.509 PKIX Certificate and CRL Profile"), (6962, "Certificate Transparency")],
                     "cwe": [(295, "Improper Certificate Validation")],
                     "cve": ["CVE-2020-0601"], "books": BOOKS["crypto"]},
    "pki": {"rfc": [(5280, "PKIX Certificate Profile"), (8555, "ACME")],
            "attack": ["T1649"], "books": BOOKS["crypto"]},
    "post-quantum": {"docs": [("NIST FIPS 203 (ML-KEM)", "https://csrc.nist.gov/pubs/fips/203/final"),
                              ("NIST FIPS 204 (ML-DSA)", "https://csrc.nist.gov/pubs/fips/204/final")],
                     "papers": [("Polynomial-Time Algorithms for Factoring (Shor)", "Shor, 1994")],
                     "books": BOOKS["crypto"]},
    "password-storage": {"cwe": [(256, "Plaintext Storage of a Password"), (916, "Use of Password Hash With Insufficient Computational Effort")],
                         "docs": [("OWASP Password Storage Cheat Sheet", "https://cheatsheetseries.owasp.org/cheatsheets/Password_Storage_Cheat_Sheet.html")],
                         "books": BOOKS["crypto"]},
    "cryptanalysis": {"cwe": [(347, "Improper Verification of Cryptographic Signature"), (208, "Observable Timing Discrepancy")],
                      "attack": ["T1600"], "books": BOOKS["crypto"]},

    # ---- 03 web-security ----
    "owasp-top-10": {"owasp": [("OWASP Top 10 (2021)", "https://owasp.org/Top10/")],
                     "cwe": [(79, "XSS"), (89, "SQL Injection"), (287, "Improper Authentication"),
                             (352, "CSRF"), (918, "SSRF")],
                     "attack": ["T1190"], "books": BOOKS["web"]},
    "jwt": {"cwe": [(347, "Improper Verification of Cryptographic Signature"), (321, "Use of Hard-coded Cryptographic Key")],
            "rfc": [(7519, "JSON Web Token (JWT)"), (7515, "JSON Web Signature"), (8725, "JWT Best Current Practices")],
            "owasp": [("OWASP JWT Cheat Sheet", "https://cheatsheetseries.owasp.org/cheatsheets/JSON_Web_Token_for_Java_Cheat_Sheet.html")],
            "books": BOOKS["web"]},
    "oauth": {"rfc": [(6749, "OAuth 2.0 Framework"), (6819, "OAuth 2.0 Threat Model"),
                      (7636, "PKCE"), (9700, "OAuth 2.0 Security BCP")],
              "cwe": [(601, "Open Redirect"), (352, "CSRF")], "attack": ["T1528"], "books": BOOKS["web"]},
    "saml": {"cwe": [(347, "Improper Verification of Cryptographic Signature")],
             "capec": [(475, "Signature Spoofing by Improper Validation")],
             "cve": ["CVE-2017-11427"], "books": BOOKS["web"]},
    "cors": {"cwe": [(942, "Permissive Cross-domain Policy with Untrusted Domains")],
             "owasp": [("OWASP CORS", "https://owasp.org/www-community/attacks/CORS_OriginHeaderScrutiny")],
             "books": BOOKS["web"]},
    "csp": {"cwe": [(1021, "Improper Restriction of Rendered UI Layers (Clickjacking)")],
            "docs": [("MDN CSP", "https://developer.mozilla.org/en-US/docs/Web/HTTP/CSP"),
                     ("Google CSP Evaluator", "https://csp-evaluator.withgoogle.com/")],
            "books": BOOKS["web"]},
    "cookies": {"rfc": [(6265, "HTTP State Management (Cookies)")],
                "cwe": [(614, "Sensitive Cookie Without Secure"), (1004, "Sensitive Cookie Without HttpOnly")],
                "books": BOOKS["web"]},
    "request-smuggling": {"cwe": [(444, "HTTP Request/Response Smuggling")],
                          "capec": [(33, "HTTP Request Smuggling")],
                          "docs": [("PortSwigger: Request Smuggling", "https://portswigger.net/web-security/request-smuggling")],
                          "books": BOOKS["web"]},

    # ---- 04 vulnerabilities ----
    "sql-injection": {"cwe": [(89, "SQL Injection"), (564, "Hibernate Injection")],
                      "capec": [(66, "SQL Injection"), (7, "Blind SQL Injection")],
                      "owasp": [("A03:2021 Injection", "https://owasp.org/Top10/A03_2021-Injection/")],
                      "attack": ["T1190"], "cve": ["CVE-2012-1823", "CVE-2019-11510"],
                      "docs": [("OWASP SQLi Prevention Cheat Sheet", "https://cheatsheetseries.owasp.org/cheatsheets/SQL_Injection_Prevention_Cheat_Sheet.html")],
                      "books": BOOKS["web"]},
    "blind-sql-injection": {"cwe": [(89, "SQL Injection")], "capec": [(7, "Blind SQL Injection")],
                            "attack": ["T1190"], "books": BOOKS["web"]},
    "xss": {"cwe": [(79, "Improper Neutralization of Input During Web Page Generation")],
            "capec": [(63, "Cross-Site Scripting"), (591, "Reflected XSS"), (592, "Stored XSS")],
            "owasp": [("A03:2021 Injection", "https://owasp.org/Top10/A03_2021-Injection/")],
            "attack": ["T1059.007"],
            "docs": [("OWASP XSS Prevention Cheat Sheet", "https://cheatsheetseries.owasp.org/cheatsheets/Cross_Site_Scripting_Prevention_Cheat_Sheet.html")],
            "books": BOOKS["web"]},
    "dom-xss": {"cwe": [(79, "XSS")], "capec": [(588, "DOM-Based XSS")],
                "docs": [("OWASP DOM XSS Cheat Sheet", "https://cheatsheetseries.owasp.org/cheatsheets/DOM_based_XSS_Prevention_Cheat_Sheet.html")],
                "books": BOOKS["web"]},
    "stored-xss": {"cwe": [(79, "XSS")], "capec": [(592, "Stored XSS")], "books": BOOKS["web"]},
    "csrf": {"cwe": [(352, "Cross-Site Request Forgery")], "capec": [(62, "Cross Site Request Forgery")],
             "owasp": [("OWASP CSRF Prevention Cheat Sheet", "https://cheatsheetseries.owasp.org/cheatsheets/Cross-Site_Request_Forgery_Prevention_Cheat_Sheet.html")],
             "books": BOOKS["web"]},
    "ssrf": {"cwe": [(918, "Server-Side Request Forgery")], "capec": [(664, "Server Side Request Forgery")],
             "owasp": [("A10:2021 SSRF", "https://owasp.org/Top10/A10_2021-Server-Side_Request_Forgery_%28SSRF%29/")],
             "attack": ["T1190", "T1552.005"], "cve": ["CVE-2019-8451", "CVE-2021-26855"],
             "books": BOOKS["web"]},
    "rce": {"cwe": [(94, "Code Injection"), (78, "OS Command Injection")],
            "capec": [(248, "Command Injection")], "attack": ["T1190", "T1059"],
            "cve": ["CVE-2021-44228", "CVE-2017-5638"], "books": BOOKS["web"]},
    "command-injection": {"cwe": [(78, "OS Command Injection"), (77, "Command Injection")],
                          "capec": [(248, "Command Injection")], "attack": ["T1059"],
                          "docs": [("OWASP Command Injection Defense", "https://cheatsheetseries.owasp.org/cheatsheets/OS_Command_Injection_Defense_Cheat_Sheet.html")],
                          "books": BOOKS["web"]},
    "lfi": {"cwe": [(98, "PHP Remote File Inclusion"), (73, "External Control of File Name or Path")],
            "capec": [(252, "PHP Local File Inclusion")], "books": BOOKS["web"]},
    "rfi": {"cwe": [(98, "Improper Control of Filename for Include/Require in PHP")],
            "capec": [(193, "PHP Remote File Inclusion")], "books": BOOKS["web"]},
    "directory-traversal": {"cwe": [(22, "Improper Limitation of a Pathname (Path Traversal)")],
                            "capec": [(126, "Path Traversal")], "cve": ["CVE-2021-41773"], "books": BOOKS["web"]},
    "xxe": {"cwe": [(611, "Improper Restriction of XML External Entity Reference")],
            "capec": [(201, "XML Entity Linking")],
            "owasp": [("OWASP XXE Prevention", "https://cheatsheetseries.owasp.org/cheatsheets/XML_External_Entity_Prevention_Cheat_Sheet.html")],
            "books": BOOKS["web"]},
    "template-injection": {"cwe": [(1336, "Server-Side Template Injection"), (94, "Code Injection")],
                           "capec": [(242, "Code Injection")], "cve": ["CVE-2016-4977"], "books": BOOKS["web"]},
    "insecure-deserialization": {"cwe": [(502, "Deserialization of Untrusted Data")],
                                 "capec": [(586, "Object Injection")], "attack": ["T1059"],
                                 "cve": ["CVE-2015-4852", "CVE-2017-9805"], "books": BOOKS["web"]},
    "idor": {"cwe": [(639, "Authorization Bypass Through User-Controlled Key"), (284, "Improper Access Control")],
             "owasp": [("A01:2021 Broken Access Control", "https://owasp.org/Top10/A01_2021-Broken_Access_Control/")],
             "books": BOOKS["web"]},
    "race-conditions": {"cwe": [(362, "Race Condition"), (367, "TOCTOU Race Condition")],
                        "capec": [(29, "Leveraging TOCTOU Race Conditions")], "books": BOOKS["web"]},
    "buffer-overflow": {"cwe": [(120, "Buffer Copy without Checking Size"), (787, "Out-of-bounds Write")],
                        "capec": [(100, "Overflow Buffers")],
                        "papers": [("Smashing the Stack for Fun and Profit", "Aleph One, 1996")],
                        "cve": ["CVE-2014-0160"], "books": BOOKS["exploit"]},
    "stack-overflow": {"cwe": [(787, "Out-of-bounds Write"), (121, "Stack-based Buffer Overflow")],
                       "capec": [(100, "Overflow Buffers")], "books": BOOKS["exploit"]},
    "heap-overflow": {"cwe": [(122, "Heap-based Buffer Overflow"), (416, "Use After Free")],
                      "capec": [(92, "Forced Integer Overflow")], "books": BOOKS["exploit"]},
    "integer-overflow": {"cwe": [(190, "Integer Overflow or Wraparound"), (191, "Integer Underflow")],
                         "capec": [(92, "Forced Integer Overflow")], "books": BOOKS["exploit"]},
    "format-strings": {"cwe": [(134, "Use of Externally-Controlled Format String")],
                       "capec": [(67, "String Format Overflow")], "books": BOOKS["exploit"]},
    "memory-corruption": {"cwe": [(787, "Out-of-bounds Write"), (416, "Use After Free"), (476, "NULL Pointer Dereference")],
                          "books": BOOKS["exploit"]},
    "cwe-top-25": {"docs": [("CWE Top 25", "https://cwe.mitre.org/top25/")], "books": BOOKS["secdev"]},
    "supply-chain-vulnerabilities": {"cwe": [(1357, "Reliance on Insufficiently Trustworthy Component"), (829, "Inclusion of Functionality from Untrusted Control Sphere")],
                                     "attack": ["T1195", "T1195.001", "T1195.002"],
                                     "cve": ["CVE-2020-10148"], "books": BOOKS["secdev"]},

    # ---- 06 offensive ----
    "recon": {"attack": ["T1595", "T1592", "T1590", "T1589"], "books": BOOKS["offense"]},
    "osint": {"attack": ["T1593", "T1589", "T1591"], "books": BOOKS["offense"]},
    "enumeration": {"attack": ["T1046", "T1087", "T1135", "T1018"], "books": BOOKS["offense"]},
    "scanning": {"attack": ["T1046", "T1595.001", "T1595.002"], "books": BOOKS["offense"]},
    "exploitation": {"attack": ["T1190", "T1203", "T1210"], "books": BOOKS["offense"]},
    "persistence": {"attack": ["T1543", "T1547", "T1053", "T1136", "T1505.003"], "books": BOOKS["offense"]},
    "privilege-escalation": {"attack": ["T1068", "T1548", "T1055", "T1078"], "books": BOOKS["offense"]},
    "lateral-movement": {"attack": ["T1021", "T1570", "T1550", "T1563"], "books": BOOKS["offense"]},
    "defense-evasion": {"attack": ["T1027", "T1070", "T1055", "T1218", "T1562"], "books": BOOKS["offense"]},
    "credential-access": {"attack": ["T1003", "T1110", "T1555", "T1552", "T1558"], "books": BOOKS["offense"]},
    "command-and-control": {"attack": ["T1071", "T1573", "T1090", "T1105", "T1568"], "books": BOOKS["offense"]},
    "exfiltration": {"attack": ["T1041", "T1048", "T1567", "T1030"], "books": BOOKS["offense"]},
    "active-directory-attacks": {"attack": ["T1558.003", "T1207", "T1484", "T1550.002", "T1003.006"],
                                 "cve": ["CVE-2021-42287", "CVE-2020-1472"], "books": BOOKS["identity"]},
    "exploit-development": {"cwe": [(787, "Out-of-bounds Write")],
                            "papers": [("Return-into-libc without Function Calls (ROP)", "Shacham, 2007")],
                            "books": BOOKS["exploit"]},

    # ---- 07 defensive ----
    "siem": {"attack": ["T1562.008"], "docs": [("MITRE ATT&CK Data Sources", "https://attack.mitre.org/datasources/")],
             "books": BOOKS["defense"]},
    "threat-hunting": {"docs": [("The ThreatHunting Project", "https://www.threathunting.net/"),
                                ("MITRE ATT&CK", "https://attack.mitre.org/")],
                       "papers": [("The Pyramid of Pain", "David Bianco, 2013")], "books": BOOKS["defense"]},
    "incident-response": {"nist": [("SP 800-61 Rev.2", "Computer Security Incident Handling Guide")],
                          "books": BOOKS["defense"]},
    "detection-engineering": {"docs": [("Sigma HQ", "https://github.com/SigmaHQ/sigma"),
                                       ("Atomic Red Team", "https://github.com/redcanaryco/atomic-red-team")],
                              "books": BOOKS["defense"]},
    "yara": {"docs": [("YARA Documentation", "https://yara.readthedocs.io/")], "books": BOOKS["malware"]},
    "sigma": {"docs": [("Sigma Specification", "https://github.com/SigmaHQ/sigma-specification")], "books": BOOKS["defense"]},
    "memory-forensics": {"docs": [("Volatility 3", "https://volatility3.readthedocs.io/")], "books": BOOKS["forensics"]},

    # ---- 08 malware ----
    "ransomware": {"attack": ["T1486", "T1490", "T1489", "T1027"], "books": BOOKS["malware"]},
    "rootkit": {"attack": ["T1014", "T1547.006"], "books": BOOKS["malware"]},
    "bootkit": {"attack": ["T1542.003", "T1542.001"], "books": BOOKS["malware"]},
    "fileless-malware": {"attack": ["T1059.001", "T1047", "T1055", "T1546.003"], "books": BOOKS["malware"]},
    "reverse-engineering": {"docs": [("Ghidra", "https://ghidra-sre.org/")], "books": BOOKS["malware"]},

    # ---- 14 frameworks ----
    "mitre-attack": {"docs": [("MITRE ATT&CK", "https://attack.mitre.org/"),
                              ("ATT&CK Navigator", "https://mitre-attack.github.io/attack-navigator/")],
                     "books": BOOKS["defense"]},
    "capec": {"docs": [("CAPEC", "https://capec.mitre.org/")], "books": BOOKS["secdev"]},
    "cwe": {"docs": [("CWE", "https://cwe.mitre.org/"), ("CWE Top 25", "https://cwe.mitre.org/top25/")], "books": BOOKS["secdev"]},
    "cve": {"docs": [("CVE Program", "https://www.cve.org/"), ("NVD", "https://nvd.nist.gov/")], "books": BOOKS["secdev"]},
    "cvss": {"docs": [("CVSS v3.1 Specification", "https://www.first.org/cvss/v3-1/"),
                      ("CVSS v4.0 Specification", "https://www.first.org/cvss/v4-0/")], "books": BOOKS["secdev"]},
    "epss": {"docs": [("EPSS", "https://www.first.org/epss/")], "books": BOOKS["secdev"]},
    "kev": {"docs": [("CISA KEV Catalog", "https://www.cisa.gov/known-exploited-vulnerabilities-catalog")], "books": BOOKS["secdev"]},

    # ---- 15 compliance ----
    "nist-csf": {"nist": [("Cybersecurity Framework 2.0", "GV/ID/PR/DE/RS/RC")],
                 "docs": [("NIST CSF 2.0", "https://www.nist.gov/cyberframework")], "books": BOOKS["grc"]},
    "nist-800-53": {"nist": [("SP 800-53 Rev.5", "Security and Privacy Controls")], "books": BOOKS["grc"]},
    "nist-rmf": {"nist": [("SP 800-37 Rev.2", "Risk Management Framework")], "books": BOOKS["grc"]},
    "iso-27001": {"docs": [("ISO/IEC 27001", "https://www.iso.org/standard/27001")], "books": BOOKS["grc"]},
    "pci-dss": {"docs": [("PCI DSS v4.0", "https://www.pcisecuritystandards.org/")], "books": BOOKS["grc"]},
    "gdpr": {"docs": [("GDPR Full Text", "https://gdpr-info.eu/")], "books": BOOKS["grc"]},
}


# --------------------------------------------------------------------------
# Per-slug lab specifications (consumed by lab_platform.render_lab)
# --------------------------------------------------------------------------
LABS = {
    "sql-injection": dict(
        objective="Confirm, exploit and then fix an SQL injection, extracting data via UNION- and error-based techniques.",
        target={"kind": "prebuilt", "image": "raesene/bwapp", "service_name": "bwapp", "port": 80,
                "internal": False, "notes": "bWAPP (also works against DVWA / Juice Shop)"},
        attacker_tools=["sqlmap", "burpsuite", "curl"],
        steps=[
            "Browse the target and find a parameter that reaches a query (e.g. bWAPP's SQLi search).",
            "Manually probe with a single quote `'` and observe the error, then confirm with `' OR '1'='1`.",
            "Determine the column count with `ORDER BY n` and find a reflected column with a `UNION SELECT`.",
            "Enumerate the schema (`information_schema.tables`, `.columns`) and dump credentials.",
            "Automate and validate with `sqlmap -u '<url>' --batch --dbs`, then `--dump` a table.",
            "Remediate: rewrite the query with parameterisation/prepared statements and re-test to confirm the injection is closed.",
        ],
        expected=[
            "A single quote changes the response (error or differing content), proving the input reaches SQL.",
            "A working `UNION SELECT` returns database content in the page.",
            "sqlmap enumerates databases and dumps a table.",
            "After parameterising the query, the same payloads no longer alter the result.",
        ],
        detection=[
            "In the web server / WAF logs, spot the quote and `UNION`/`information_schema` markers.",
            "Write a Sigma rule for suspicious SQL keywords in URL parameters and test it against the captured logs.",
        ],
        study_minutes=60,
    ),
    "xss": dict(
        objective="Trigger reflected, stored and DOM XSS, understand output contexts, then neutralise each with correct encoding and CSP.",
        target={"kind": "prebuilt", "image": "bkimminich/juice-shop", "service_name": "juice-shop", "port": 3000,
                "internal": False, "notes": "OWASP Juice Shop (or bWAPP/DVWA)"},
        attacker_tools=["burpsuite", "browser devtools"],
        steps=[
            "Find a reflected sink (search box) and inject `<script>alert(document.domain)</script>`; note where it lands in the HTML.",
            "Find a stored sink (a review/comment) and persist a payload that fires for other users.",
            "Find a DOM sink by tracing a value from `location.hash` into `innerHTML`.",
            "Escalate impact safely in-lab: exfiltrate a cookie to a local listener you control (`nc -lvnp 9001`).",
            "Fix each: context-aware output encoding, a framework auto-escape, `HttpOnly` cookies and a strict CSP; re-test.",
        ],
        expected=[
            "The reflected payload executes in the page context.",
            "The stored payload executes when the page is re-opened.",
            "The DOM payload executes without the server ever seeing the script.",
            "After remediation, payloads render as inert text and CSP blocks inline execution.",
        ],
        detection=[
            "Observe the outbound request to your listener in a packet capture — this is the exfil signal a defender would hunt.",
        ],
        study_minutes=60,
    ),
    "ssrf": dict(
        objective="Exploit SSRF to reach an internal-only service and a mock cloud metadata endpoint, then constrain egress to fix it.",
        target={"kind": "compose", "service_name": "app",
                "compose": "```yaml\nservices:\n  app:            # vulnerable fetcher: GET /fetch?url=...\n    image: python:3.12-alpine\n    command: sh -c \"pip install flask requests -q && python /srv/app.py\"\n    volumes: [\"./app.py:/srv/app.py:ro\"]\n    ports: [\"18085:8080\"]\n    networks: [labnet]\n  metadata:         # stand-in for 169.254.169.254\n    image: hashicorp/http-echo\n    command: [\"-text=IAM-ROLE-CREDENTIALS-abc123\"]\n    networks: [labnet]\nnetworks:\n  labnet:\n    internal: true\n```\n> Write a tiny `app.py` that fetches the user-supplied `url` server-side — the deliberate flaw."},
        attacker_tools=["curl", "burpsuite"],
        steps=[
            "Confirm the app fetches arbitrary URLs: `curl 'http://localhost:18085/fetch?url=http://metadata:5678/'`.",
            "Pivot to the internal-only metadata service that is unreachable from your host directly.",
            "Try blind SSRF: point it at a local listener and confirm the callback (`nc -lvnp 9002`).",
            "Fix: all/deny-list destinations, resolve-then-validate the IP, block link-local/private ranges, and disable redirects; re-test.",
        ],
        expected=[
            "The app returns the internal service's response, proving server-side fetch.",
            "The metadata stand-in leaks its 'credentials' through the vulnerable app.",
            "After egress validation, requests to internal/link-local addresses are refused.",
        ],
        study_minutes=55,
    ),
    "buffer-overflow": dict(
        objective="Take a vulnerable C program from crash to controlled execution in a mitigations-off lab, then observe how each mitigation breaks the exploit.",
        target={"kind": "cyberforge", "image": "ubuntu:22.04", "service_name": "pwn-target",
                "command": "sleep infinity", "internal": True,
                "notes": "compile the vulnerable binary inside the container"},
        attacker_tools=["gdb", "pwndbg/gef", "pwntools", "gcc"],
        steps=[
            "Compile the target with mitigations off: `gcc -fno-stack-protector -z execstack -no-pie vuln.c -o vuln`.",
            "Find the offset to the saved return address with a cyclic pattern (`pwn cyclic`).",
            "Redirect execution to a `win()` function (ret2win), confirming control of RIP.",
            "Rebuild with `-fstack-protector-all`, then PIE+NX, and watch the exploit fail at each step.",
            "Re-develop against NX using a ret2libc / ROP chain to internalise why DEP alone is not enough.",
        ],
        expected=[
            "A cyclic pattern crashes the program and the offset is identified precisely.",
            "The ret2win payload calls the target function.",
            "The stack canary aborts the program (`stack smashing detected`) once enabled.",
            "The ROP chain achieves execution despite NX.",
        ],
        study_minutes=90,
    ),
    "active-directory-attacks": dict(
        objective="Walk a lab AD forest from an unprivileged foothold to Domain Admin via Kerberoasting and an ACL/DCSync path.",
        target={"kind": "compose", "service_name": "dc",
                "compose": "```yaml\n# Use GOAD (Game of Active Directory) or samba-ad-dc for a lightweight forest.\n# GOAD provisions a full multi-DC lab; see https://github.com/Orange-Cyberdefense/GOAD\nservices:\n  dc:\n    image: \"<your AD lab image>\"\n    networks: [labnet]\nnetworks:\n  labnet:\n    internal: true\n```\n> For a faithful AD lab, provision **GOAD** or a Windows Server eval VM; Samba AD-DC covers Kerberos/LDAP basics."},
        attacker_tools=["netexec", "bloodhound", "impacket", "kerbrute", "hashcat"],
        steps=[
            "Enumerate the domain with NetExec and collect graph data with the BloodHound collector.",
            "Spray/verify credentials, then Kerberoast SPN accounts (`impacket-GetUserSPNs`) and crack offline with hashcat.",
            "Use BloodHound to find the shortest path to Domain Admin (e.g. GenericAll → reset password → group add).",
            "Abuse the ACL path, then perform DCSync (`impacket-secretsdump`) to pull the KRBTGT hash.",
            "Map every step to MITRE ATT&CK and write the detections that would have caught it.",
        ],
        expected=[
            "BloodHound renders a concrete attack path to a high-value target.",
            "A Kerberoastable service account's password is recovered offline.",
            "DCSync returns domain hashes, demonstrating full compromise.",
        ],
        detection=[
            "Event ID 4769 (Kerberos service ticket) spikes with RC4 for Kerberoasting.",
            "Event ID 4662 / replication activity from a non-DC principal indicates DCSync.",
        ],
        study_minutes=120,
    ),
    "insecure-deserialization": dict(
        objective="Reach code execution through an unsafe deserialization sink, then fix it by removing polymorphic deserialization.",
        target={"kind": "cyberforge", "image": "python:3.12-alpine", "service_name": "deser-app",
                "command": "sh -c 'pip install flask -q && python /srv/app.py'", "port": 8080, "internal": True,
                "notes": "a Flask app that pickle-loads a cookie — the deliberate flaw"},
        attacker_tools=["python", "curl", "burpsuite"],
        steps=[
            "Identify the serialized blob (a base64 pickle in a cookie or body).",
            "Craft a malicious object whose `__reduce__` runs a benign command (e.g. touch a file), and submit it.",
            "Confirm execution inside the container (check for the file / callback).",
            "Fix: replace pickle with JSON and a strict schema, or sign+verify the blob; re-test.",
        ],
        expected=[
            "The crafted object executes on deserialization.",
            "After switching to schema-validated JSON, the payload is rejected.",
        ],
        study_minutes=60,
    ),
    "nmap": dict(
        objective="Fingerprint an isolated multi-service target with escalating Nmap techniques and read the results critically.",
        target={"kind": "prebuilt", "image": "tleemcjr/metasploitable2", "service_name": "metasploitable",
                "port": 0, "internal": True, "notes": "Metasploitable 2 (many open services)"},
        attacker_tools=["nmap"],
        steps=[
            "Discover the host: `nmap -sn <subnet>`.",
            "Fast top-ports sweep, then a full TCP scan: `nmap -p- <ip>`.",
            "Service/version and OS detection: `nmap -sV -O <ip>`.",
            "Run safe NSE scripts: `nmap -sC <ip>` and a targeted category (e.g. `--script vuln`).",
            "Save all formats (`-oA`) and compare a `-T4` timing run against a slower, quieter scan.",
        ],
        expected=[
            "The open-port set and service versions are enumerated.",
            "NSE surfaces at least one known-vulnerable service.",
            "You can explain the trade-off between scan speed and stealth from the timing runs.",
        ],
        detection=[
            "In a packet capture, the SYN scan appears as many half-open connections — the signature an IDS keys on.",
        ],
        study_minutes=45,
    ),
    "jwt": dict(
        objective="Break a misconfigured JWT implementation (alg confusion, weak secret, kid injection) and then harden verification.",
        target={"kind": "cyberforge", "image": "node:20-alpine", "service_name": "jwt-app",
                "command": "sh -c 'node /srv/app.js'", "port": 8080, "internal": True,
                "notes": "a Node app that verifies JWTs with a weak/blank secret"},
        attacker_tools=["jwt_tool", "hashcat", "burpsuite"],
        steps=[
            "Decode the token and inspect the header/claims with `jwt_tool <token>`.",
            "Test `alg:none` acceptance and RS256→HS256 confusion using the public key as the HMAC secret.",
            "Crack a weak HMAC secret offline: `hashcat -m 16500 token.txt rockyou.txt`.",
            "Forge an admin token and access a protected route.",
            "Fix: pin the algorithm, verify `kid` against a key allow-list, reject `none`, rotate to a strong key; re-test.",
        ],
        expected=[
            "A forged token is accepted before remediation.",
            "The weak secret is recovered by hashcat.",
            "After pinning the algorithm and key, all forgeries are rejected.",
        ],
        study_minutes=55,
    ),
    "yara": dict(
        objective="Write precise, performant YARA rules that match a family of lab samples without false-positiving on clean files.",
        target={"kind": "kali"},
        attacker_tools=["yara", "yextend"],
        steps=[
            "Collect several benign 'family' samples and a clean corpus in the lab.",
            "Extract distinguishing strings and byte patterns; draft a rule with `strings:` and a `condition:`.",
            "Tune with `nocase`, `wide`, and offsets; add a file-size guard for performance.",
            "Measure false positives against the clean corpus and iterate.",
        ],
        expected=[
            "The rule matches every family sample and none of the clean corpus.",
            "Scan time stays low thanks to anchored/size-guarded conditions.",
        ],
        study_minutes=45,
    ),
    "memory-forensics": dict(
        objective="Reconstruct a simulated intrusion from a RAM image using Volatility 3.",
        target={"kind": "kali"},
        attacker_tools=["volatility3"],
        steps=[
            "Acquire or download a lab memory image (e.g. from a CyberDefenders exercise).",
            "List processes and spot anomalies: `vol -f mem.raw windows.pslist` / `pstree` / `psscan`.",
            "Investigate network artefacts (`windows.netscan`) and injected code (`windows.malfind`).",
            "Dump a suspicious process and triage it statically.",
            "Build a short timeline of attacker activity and write it up.",
        ],
        expected=[
            "A hidden or injected process is identified.",
            "Network connections tie the host to a C2 endpoint.",
            "You produce a defensible narrative of what happened.",
        ],
        study_minutes=75,
    ),
}
