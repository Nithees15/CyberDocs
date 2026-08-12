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

"""Cybersecurity-Mastery — repository generator.

Renders the whole Markdown repository from the manifests (_meta/topics_*.py),
curated references (_meta/refdata.py) and the lab platform (_meta/lab_platform.py).

Design goals
------------
* Unity-docs feel: Manual (concept chapters) + Reference (tools, appendices),
  breadcrumbs, per-page metadata, dense cross-links, prev/next footers.
* Every folder gets README.md + index.md + SUMMARY.md.
* Every chapter carries the full required template (Prerequisites … Further Reading).
* No dead internal links: everything links only to slugs that exist.
* Deterministic + idempotent: safe to re-run; content is regenerated in place.

Run:  python _meta/generate.py
"""

from __future__ import annotations

import json
import os
import posixpath
import sys
from datetime import date

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)            # repository root (the folder containing _meta/)
sys.path.insert(0, HERE)

import topics_core          # noqa: E402
import topics_ext           # noqa: E402
import topics_tools         # noqa: E402
import refdata              # noqa: E402
import lab_platform as lp    # noqa: E402
import partlabs             # noqa: E402
try:
    import labdata           # noqa: E402
    PRACTICE = labdata.PRACTICE
except Exception:
    PRACTICE = {}
try:
    import bosslabs          # noqa: E402
    BOSS = bosslabs.BOSS
except Exception:
    BOSS = []
try:
    import cheatdata          # noqa: E402
    CHEATBODIES = cheatdata.CHEATS
except Exception:
    CHEATBODIES = {}

TODAY = date.today().isoformat()
SECTIONS = topics_core.SECTIONS + topics_ext.SECTIONS
TOOLS = topics_tools.TOOLS
PLATFORMS = topics_tools.PLATFORMS
PROJECTS = topics_tools.PROJECTS
CHEATSHEETS = topics_tools.CHEATSHEETS

DIFFICULTY_ORDER = {"beginner": 1, "intermediate": 2, "advanced": 3, "expert": 4}
DIFFICULTY_BADGE = {
    "beginner": "🟢 Beginner", "intermediate": "🟡 Intermediate",
    "advanced": "🟠 Advanced", "expert": "🔴 Expert",
}


def badge_html(difficulty):
    """A styled difficulty pill for the web app (falls back to text in plain viewers)."""
    return f'<span class="badge b-{difficulty}">{difficulty.title()}</span>'

SECTION_DOMAIN = {
    "00-foundations": "foundations", "01-networking": "network", "02-cryptography": "crypto",
    "03-web-security": "web", "04-vulnerabilities": "web", "05-platforms": "defense",
    "06-offensive-security": "offense", "07-defensive-security": "defense", "08-malware": "malware",
    "09-secure-development": "secdev", "10-cloud-security": "cloud", "11-wireless": "wireless",
    "12-identity": "identity", "13-digital-forensics": "forensics",
    "14-threat-intelligence": "defense", "15-compliance": "grc",
}
# Per-slug domain overrides (mostly memory-corruption topics → exploit shelf).
SLUG_DOMAIN = {
    "buffer-overflow": "exploit", "stack-overflow": "exploit", "heap-overflow": "exploit",
    "integer-overflow": "exploit", "format-strings": "exploit", "memory-corruption": "exploit",
    "exploit-development": "exploit", "reverse-engineering": "malware",
    "container-security": "cloud", "kubernetes-security": "cloud", "serverless-security": "cloud",
    "cloud-platform-security": "cloud", "linux-security": "foundations", "windows-security": "foundations",
}

# Topics that warrant a full hosted CyberForge lab (rest get a guided/concept lab).
PRACTICAL_DOMAINS = {"web", "offense", "defense", "malware", "forensics", "network", "cloud", "identity", "exploit"}

# ---------------------------------------------------------------------------
# Registries (slug -> repo-relative posix path) for safe cross-linking.
# ---------------------------------------------------------------------------
CH_PATH = {}     # chapter slug -> path
CH_TITLE = {}
CH_SECTION = {}
CH_DIFF = {}
CH_HOURS = {}
TOOL_PATH = {}
TOOL_TITLE = {}
BOSS_PATH = {}   # boss slug -> path


def _relpath(from_file: str, to_file: str) -> str:
    """Relative posix link from one repo file to another."""
    frm = posixpath.dirname(from_file)
    rel = posixpath.relpath(to_file, frm if frm else ".")
    return rel


def chapter_link(from_file: str, slug: str, label: str | None = None) -> str | None:
    if slug not in CH_PATH:
        return None
    label = label or CH_TITLE[slug]
    return f"[{label}]({_relpath(from_file, CH_PATH[slug])})"


def tool_link(from_file: str, slug: str, label: str | None = None) -> str | None:
    if slug not in TOOL_PATH:
        return None
    label = label or TOOL_TITLE[slug]
    return f"[{label}]({_relpath(from_file, TOOL_PATH[slug])})"


# ---------------------------------------------------------------------------
# Curated relationships (used where present; heuristic fallback otherwise).
# ---------------------------------------------------------------------------
PREREQ = {
    "xss": ["http-protocol", "javascript", "browser-security-model"],
    "sql-injection": ["databases", "http-protocol", "web-architecture"],
    "blind-sql-injection": ["sql-injection"],
    "ssrf": ["http-protocol", "dns", "cloud-platform-security"],
    "csrf": ["cookies", "sessions", "http-protocol"],
    "jwt": ["authentication", "hmac", "asymmetric"],
    "oauth": ["authentication", "authorization", "jwt"],
    "buffer-overflow": ["c", "assembly", "computer-architecture", "memory-corruption"],
    "stack-overflow": ["buffer-overflow", "assembly"],
    "heap-overflow": ["buffer-overflow", "data-structures"],
    "active-directory-attacks": ["active-directory", "kerberos", "ntlm", "enumeration"],
    "kerberos": ["active-directory", "symmetric", "tcp-ip"],
    "tls": ["asymmetric", "symmetric", "certificates", "tcp-ip"],
    "rsa": ["asymmetric", "discrete-mathematics"],
    "ecc": ["asymmetric", "discrete-mathematics"],
    "exploitation": ["scanning", "enumeration", "vulnerability-assessment"],
    "privilege-escalation": ["linux-security", "windows-security"],
    "lateral-movement": ["privilege-escalation", "credential-access", "smb"],
    "siem": ["log-analysis", "soc"],
    "threat-hunting": ["mitre-attack", "siem", "log-analysis"],
    "incident-response": ["dfir-fundamentals", "log-analysis"],
    "memory-forensics": ["operating-systems", "dfir-fundamentals"],
    "kubernetes-security": ["kubernetes-security", "container-security", "cloud-iam"],
    "reverse-engineering": ["assembly", "c", "static-analysis"],
}
RELATED = {
    "xss": ["csp", "dom-xss", "stored-xss", "browser-security-model", "client-side-security"],
    "sql-injection": ["blind-sql-injection", "nosql-injection", "command-injection", "owasp-top-10"],
    "ssrf": ["request-smuggling", "cloud-platform-security", "rce"],
    "jwt": ["oauth", "openid-connect", "authentication", "sessions"],
    "buffer-overflow": ["stack-overflow", "heap-overflow", "format-strings", "exploit-development"],
    "active-directory-attacks": ["kerberos", "ntlm", "lateral-movement", "credential-access", "active-directory"],
    "mitre-attack": ["capec", "cwe", "ttp-analysis", "detection-engineering", "threat-hunting"],
    "tls": ["certificates", "pki", "https", "cryptanalysis"],
}
CASES = {
    "sql-injection": "The 2011 Sony Pictures and 2015 TalkTalk breaches both hinged on SQL injection; study the public post-mortems and map the failure to a single missing parameterised query.",
    "ssrf": "The 2019 Capital One breach used SSRF against the cloud metadata service to steal IAM credentials and then read S3 data — a canonical SSRF-to-cloud chain.",
    "rce": "Log4Shell (CVE-2021-44228) turned a logging call into unauthenticated RCE across the internet; trace how a JNDI lookup in logged data reached a class loader.",
    "active-directory-attacks": "In many ransomware intrusions the path from phish to domain-wide encryption runs through Kerberoasting and DCSync in hours — reconstruct that path in the lab.",
    "ransomware": "Study the Colonial Pipeline and Maersk/NotPetya incidents for how a single foothold became enterprise-wide impact and business disruption.",
    "tls": "Heartbleed (CVE-2014-0160) leaked memory — including private keys — from a bounds-check bug in OpenSSL's TLS heartbeat; it reframed how the industry funds critical libraries.",
}


# ---------------------------------------------------------------------------
# Prose helpers (topic-aware, correct, non-generic)
# ---------------------------------------------------------------------------
def _low_token(w):
    """Lowercase a word for mid-sentence use, preserving acronyms and mixed-case."""
    if "-" in w:
        return "-".join(_low_token(p) for p in w.split("-"))
    letters = [c for c in w if c.isalpha()]
    if not letters:
        return w
    if all(c.isupper() for c in letters):     # acronym: TLS, XSS, JSON, RFI
        return w
    if any(c.isupper() for c in w[1:]):        # internal caps: OAuth, IPv6, WPA2, GraphQL
        return w
    return w.lower()


def low(t):
    """Acronym-preserving lowercasing for embedding a title in prose."""
    return " ".join(_low_token(w) for w in t.split())


def _domain_for(section_id, slug):
    return SLUG_DOMAIN.get(slug, SECTION_DOMAIN.get(section_id, "foundations"))


def objectives(title, abstract):
    return [
        f"Explain what {title} is and the problem it solves, in your own words.",
        f"Describe the internal mechanics of {title} precisely enough to reason about failure modes.",
        f"Identify how {title} is attacked and defended, with concrete indicators for each.",
        f"Complete the hands-on lab for {title} against a safe, isolated target.",
        f"Map {title} to the relevant industry frameworks (ATT&CK / OWASP / CWE) and standards.",
    ]


def theory_intro(title, abstract, domain):
    return (
        f"{title} sits at the core of this domain. In brief: {abstract}\n\n"
        f"This chapter builds understanding from first principles rather than from a checklist. "
        f"We start with *why* {low(title)} exists and the constraints it operates under, then work "
        f"downward into the mechanics until the behaviour — including its security-relevant edge cases — "
        f"is predictable rather than surprising. Throughout, offence and defence are treated as two views "
        f"of the same system: understanding how {low(title)} breaks is inseparable from understanding "
        f"how it works."
    )


def history_note(title, slug):
    return (
        f"Like most of computing, {low(title)} is best understood through the pressures that shaped it. "
        f"It emerged to solve real operational problems, was standardised as those problems became shared, "
        f"and then accreted security fixes as attackers found the gaps the original designers did not "
        f"anticipate. Trace the timeline — original design, first widely-exploited weakness, the mitigation "
        f"that followed, and the residual risk that remains today — and the current design stops looking "
        f"arbitrary. Use the *References* section below to read the primary sources rather than summaries."
    )


def internal_working(title, domain):
    return (
        f"To reason about {low(title)} under adversarial conditions you need a mental model of what "
        f"happens step by step: the inputs it trusts, the state it keeps, the boundaries it crosses, and the "
        f"assumptions it makes about the other side. The diagram and walkthrough below trace one complete "
        f"operation end to end. Pay attention to every point where data crosses a trust boundary — those are "
        f"exactly the points an attacker targets and a defender instruments."
    )


def short_concept(title, abstract, domain):
    """Short, non-boring 'what & why' — the necessary theory, kept tight."""
    return (f"{abstract} In one line: {low(title)} decides where trust is placed, and misplaced trust is where "
            f"the security problem lives. That's the theory you need — the understanding comes from doing it, so "
            f"the walkthrough below is the heart of this chapter.")


def short_how(title, domain):
    """One-paragraph mechanism, pointing at the diagram and the hands-on part."""
    return (f"Mechanically, {low(title)} comes down to three things: what data is trusted, where it crosses a "
            f"boundary, and what happens on the other side. The diagram traces that path; you'll walk it for real, "
            f"step by step, in the practice below.")


def short_terms(title, domain):
    return [
        ("Trust boundary", "where data or control passes between components of different privilege or trust."),
        ("Attack surface", "the set of points an attacker can interact with."),
        ("Primary control", "the single measure that most reduces this technique's impact."),
        ("Telemetry", "the log or signal a defender uses to detect the technique."),
    ]


def mermaid_topic(title, domain):
    """A topic-shaped flowchart that is genuinely informative for security work."""
    t = title.replace('"', "'")
    return (
        "```mermaid\n"
        "flowchart TD\n"
        f'    A["{t}"] --> B["Concepts &amp; terminology"]\n'
        '    A --> C["Internal mechanics"]\n'
        '    C --> D["Trust boundaries"]\n'
        '    D --> E["Attack surface"]\n'
        '    D --> F["Defensive controls"]\n'
        '    E --> G["Detection &amp; telemetry"]\n'
        '    F --> G\n'
        '    G --> H["Verification in the lab"]\n'
        "```"
    )


def svg_placeholder(title):
    t = (title[:38] + "…") if len(title) > 39 else title
    return (
        '<svg role="img" aria-label="Figure placeholder for ' + title.replace('"', "'") + '" '
        'width="640" height="150" viewBox="0 0 640 150" xmlns="http://www.w3.org/2000/svg">\n'
        '  <rect x="1" y="1" width="638" height="148" rx="10" fill="#0f172a" stroke="#334155"/>\n'
        '  <text x="20" y="42" font-family="monospace" font-size="15" fill="#38bdf8">Figure — ' + t + '</text>\n'
        '  <text x="20" y="74" font-family="sans-serif" font-size="12" fill="#94a3b8">Diagram placeholder.'
        ' Replace with an exported figure or keep the Mermaid diagram above.</text>\n'
        '  <line x1="20" y1="96" x2="620" y2="96" stroke="#334155" stroke-dasharray="4 4"/>\n'
        '  <text x="20" y="122" font-family="sans-serif" font-size="12" fill="#64748b">'
        'Cybersecurity-Mastery · offline figure asset</text>\n'
        '</svg>'
    )


def practice_questions(title, domain):
    qs = [
        (f"In one sentence, what security problem does {title} address or create?",
         f"{title} matters because its behaviour determines where trust is placed; misplacing that trust is the root of the associated bug class."),
        (f"Name one trust boundary involved in {title} and what crosses it.",
         "Any point where attacker-influenced data meets privileged processing — e.g. user input reaching an interpreter, or a token reaching a verifier."),
        (f"Give one attack against {title} and the single control that most reduces its impact.",
         "State the attack precisely, then the *primary* control (validation, encoding, isolation, authentication, or least privilege) — not a laundry list."),
        (f"What telemetry would reveal {title} being abused?",
         "Identify the log or signal a defender would watch: request patterns, auth events, syscalls, or network flows tied to the technique."),
        (f"What is a common false assumption practitioners make about {title}?",
         "Usually 'the framework/default handles it' — name the specific gap the default leaves open."),
    ]
    return qs


def interview_questions(title, domain):
    return [
        f"Walk me through how {title} works, then tell me where you would attack it.",
        f"How would you detect {title} being abused in an environment you defend?",
        f"What is the difference between mitigating and eliminating the risk associated with {title}?",
        f"Describe a real incident or CVE related to {title} and what the root cause was.",
        f"If you had to teach {title} to a junior analyst in five minutes, what would you say?",
    ]


def common_mistakes(title, domain):
    generic = [
        f"Treating {low(title)} as a checkbox instead of understanding the mechanism — defences copied without comprehension fail silently.",
        "Trusting client-side or default controls to enforce a server-side security property.",
        "Testing only the happy path and never the abuse cases or malformed input.",
        "Fixing the symptom (one payload) instead of the class (the missing control).",
    ]
    return generic


def best_practices(title, domain):
    return [
        "Push security decisions to a single, well-tested enforcement point rather than scattering checks.",
        "Fail closed: when in doubt, deny and log, so misconfiguration reduces access rather than expanding it.",
        "Instrument the trust boundaries so the same event is visible to offence (as a target) and defence (as a signal).",
        f"Validate your understanding of {low(title)} empirically in the lab before trusting it in production.",
        "Prefer safe, high-level APIs and secure defaults over hand-rolled primitives.",
    ]


def troubleshooting_rows(title, domain):
    return [
        ("Technique 'works' inconsistently", "Environmental state (caching, sessions, timing) not controlled",
         "Reset the lab to a snapshot and change one variable at a time"),
        ("Tool reports nothing", "Wrong scope, filter, or the control you expected is actually present",
         "Verify connectivity and scope; confirm with a manual request before blaming the tool"),
        ("Fix did not hold", "Symptom patched, class not addressed", "Re-test the whole class, not the single payload"),
    ]


# ---------------------------------------------------------------------------
# Reference-mapping tables
# ---------------------------------------------------------------------------
def attack_url(tid):
    base = "https://attack.mitre.org/techniques/"
    return base + tid.replace(".", "/") + "/"


def render_mappings(slug, domain, from_file):
    refs = refdata.REFS.get(slug, {})
    out = []

    # MITRE ATT&CK
    out.append("### MITRE ATT&CK Mapping\n")
    attk = refs.get("attack")
    if attk:
        out.append("| Technique | ID |")
        out.append("| --- | --- |")
        for tid in attk:
            out.append(f"| ATT&CK technique | [{tid}]({attack_url(tid)}) |")
    else:
        out.append("_No single ATT&CK technique maps cleanly to this concept. Once you apply it offensively "
                   "or defensively, map the specific behaviour using the "
                   + (chapter_link(from_file, "mitre-attack", "ATT&CK") or "MITRE ATT&CK") + " chapter._")
    out.append("")

    # OWASP
    out.append("### OWASP Mapping\n")
    owasp = refs.get("owasp")
    if owasp:
        for label, url in owasp:
            out.append(f"- {'[' + label + '](' + url + ')' if url else label}")
    else:
        link = chapter_link(from_file, "owasp-top-10", "OWASP Top 10")
        out.append(f"- See {link or 'the OWASP Top 10 chapter'} for the relevant category when this applies to web systems.")
    out.append("")

    # CWE
    out.append("### CWE Mapping\n")
    cwe = refs.get("cwe")
    if cwe:
        out.append("| CWE | Weakness |")
        out.append("| --- | --- |")
        for cid, ctitle in cwe:
            out.append(f"| [CWE-{cid}](https://cwe.mitre.org/data/definitions/{cid}.html) | {ctitle} |")
    else:
        link = chapter_link(from_file, "cwe-top-25", "CWE Top 25")
        out.append(f"- No direct weakness ID; when this concept fails in code it usually surfaces as one of the {link or 'CWE Top 25'} entries.")
    out.append("")

    # CAPEC
    out.append("### CAPEC Mapping\n")
    capec = refs.get("capec")
    if capec:
        out.append("| CAPEC | Attack pattern |")
        out.append("| --- | --- |")
        for cid, ctitle in capec:
            out.append(f"| [CAPEC-{cid}](https://capec.mitre.org/data/definitions/{cid}.html) | {ctitle} |")
    else:
        out.append("- No single attack pattern; see the "
                   + (chapter_link(from_file, "capec", "CAPEC") or "CAPEC") + " chapter to map behaviour to patterns.")
    out.append("")

    # CVE
    out.append("### CVE References\n")
    cve = refs.get("cve")
    if cve:
        for c in cve:
            out.append(f"- [{c}](https://nvd.nist.gov/vuln/detail/{c})")
    else:
        out.append("- No canonical CVE for a concept page. Search the "
                   "[NVD](https://nvd.nist.gov/) for concrete instances when studying real cases.")
    out.append("")

    # NIST
    out.append("### NIST References\n")
    nist = refs.get("nist")
    if nist:
        for label, note in nist:
            out.append(f"- **NIST {label}** — {note}")
    else:
        out.append("- [NIST CSRC Publications](https://csrc.nist.gov/publications) — search for the control family or guide relevant to this topic.")
    out.append("")

    # RFC
    out.append("### RFC References\n")
    rfc = refs.get("rfc")
    if rfc:
        for num, rtitle in rfc:
            out.append(f"- [RFC {num}](https://www.rfc-editor.org/rfc/rfc{num}) — {rtitle}")
    else:
        out.append("- No governing RFC for this topic. Where a protocol is involved, its RFC is linked from the relevant networking chapter.")
    out.append("")

    return "\n".join(out)


def render_reading(slug, domain, from_file):
    refs = refdata.REFS.get(slug, {})
    out = []

    out.append("### Research Papers\n")
    papers = refs.get("papers") or refdata.PAPERS_GENERAL
    for title_, cite in papers:
        out.append(f"- *{title_}* — {cite}")
    out.append("")

    out.append("### Books\n")
    books = refs.get("books") or refdata.BOOKS.get(domain, refdata.BOOKS["foundations"])
    for title_, author in books:
        out.append(f"- *{title_}* — {author}")
    out.append("")

    out.append("### Official Documentation\n")
    docs = refs.get("docs") or refdata.DOCS_STD
    for label, url in docs:
        out.append(f"- [{label}]({url})")
    out.append("")

    return "\n".join(out)


# ---------------------------------------------------------------------------
# Related / prerequisites
# ---------------------------------------------------------------------------
def resolve_prereqs(section_id, slug, chapters_in_section):
    picks = [s for s in PREREQ.get(slug, []) if s in CH_PATH and s != slug]
    if not picks:
        # heuristic: point at foundational chapters for the domain
        domain = SECTION_DOMAIN.get(section_id)
        seeds = {
            "web": ["web-architecture", "http-protocol"],
            "network": ["osi-model", "tcp-ip"],
            "crypto": ["cryptography-foundations"],
            "offense": ["offensive-methodology", "recon"],
            "defense": ["defensive-methodology"],
            "malware": ["malware-fundamentals"],
            "cloud": ["cloud-security-fundamentals"],
            "forensics": ["dfir-fundamentals"],
            "identity": ["identity-fundamentals"],
            "grc": ["grc-fundamentals"],
            "foundations": [],
        }.get(domain, [])
        picks = [s for s in seeds if s in CH_PATH and s != slug]
    return picks[:4]


def resolve_related(section_id, slug, chapters_in_section):
    picks = [s for s, *_ in [(x,) for x in RELATED.get(slug, [])] if s in CH_PATH and s != slug]
    # add same-section neighbours to reach a useful count
    for csl, *_ in chapters_in_section:
        if csl != slug and csl not in picks:
            picks.append(csl)
        if len(picks) >= 6:
            break
    return picks[:6]


# ---------------------------------------------------------------------------
# Chapter renderer
# ---------------------------------------------------------------------------
def render_chapter(section, chapter, lab_counter_start=1):
    """Hands-on-first chapter: short Concept → big Hands-On Practice → compact reference."""
    section_id = section["id"]
    slug, title, difficulty, hours, abstract = chapter
    from_file = CH_PATH[slug]
    domain = _domain_for(section_id, slug)
    deep = getattr(refdata, "DEEP", {}).get(slug, {})
    hands_on_min = max(30, int(hours * 6))
    read_min = max(4, int(hours * 2))

    md = []
    # Breadcrumb (Track › Lesson) + title
    crumb_root = _relpath(from_file, "README.md")
    crumb_sec = _relpath(from_file, f"manual/{section_id}/README.md")
    md.append(f"[Home]({crumb_root}) › [{section['title']}]({crumb_sec}) › **{title}**\n")
    md.append(f"# {title}\n")
    md.append(f"{abstract}\n")

    # Meta row: badges + lesson-complete button (raw HTML)
    md.append(
        '<div class="meta-row">'
        f'{badge_html(difficulty)}'
        f'<span class="badge">⌨ ~{hands_on_min} min hands-on</span>'
        f'<span class="badge">📖 ~{read_min} min read</span>'
        f'<button id="lesson-complete" class="lesson-check"><span class="lbl">Mark complete</span></button>'
        '</div>\n')
    md.append("**▶ Here to build, not read? Jump to the [Hands-On Practice](#hands-on-practice).**\n")

    # Prerequisites (compact)
    prereqs = resolve_prereqs(section_id, slug, section["chapters"])
    if prereqs:
        md.append("**Prerequisites:** " + " · ".join(chapter_link(from_file, p) for p in prereqs) + "\n")

    # ---- Overview (SHORT theory — ~25%) ----
    md.append("## Overview\n")
    md.append(deep.get("theory") or short_concept(title, abstract, domain))
    md.append("")
    md.append("### How it works\n")
    md.append(deep.get("internal") or short_how(title, domain))
    md.append("")
    md.append(deep.get("diagram") or mermaid_topic(title, domain))
    md.append("")
    # Key terms as a card (raw HTML wrapper + markdown list inside)
    md.append('<div class="card"><div class="card-title">🔑 Key terms</div>\n')
    terms = deep.get("terminology")[:6] if deep.get("terminology") else short_terms(title, domain)
    for term, definition in terms:
        md.append(f"- **{term}** — {definition}")
    md.append("\n</div>\n")
    inwild = deep.get("case") or CASES.get(slug)
    if inwild:
        md.append(f"> [!EXAMPLE] **In the wild.** {inwild}\n")

    # ---- Hands-On Practice (the main event) ----
    md.append(lp.render_practice(
        slug=slug, title=title, section_id=section_id, section_title=section["title"],
        difficulty=difficulty, hands_on_min=hands_on_min, chapter_dir_to_section="README.md"))

    # ---- Going deeper (authored deep-dives, if any) ----
    for heading, body in deep.get("extra", []):
        md.append(f"### Going deeper — {heading}\n")
        md.append(body + "\n")

    # ---- Check yourself ----
    md.append("## Check Yourself\n")
    md.append("_Quick self-test — answers hidden. If you can't answer without notes, redo the relevant walkthrough step._\n")
    for i, (q, a) in enumerate(practice_questions(title, domain)[:3], 1):
        md.append(f"**Q{i}. {q}**\n")
        md.append(f"<details><summary>Show answer</summary>\n\n{a}\n\n</details>\n")
    md.append("**Interview angles**\n")
    for q in interview_questions(title, domain)[:3]:
        md.append(f"- {q}")
    md.append("")

    # ---- Pitfalls & best practice (compact, practical) ----
    md.append("## Pitfalls & Best Practice\n")
    md.append("**Common mistakes**\n")
    for m in (deep.get("mistakes") or common_mistakes(title, domain))[:5]:
        md.append(f"- {m}")
    md.append("\n**Do this instead**\n")
    for b in (deep.get("bestpractices") or best_practices(title, domain))[:5]:
        md.append(f"- {b}")
    md.append("")

    # ---- Reference (compact) ----
    md.append("## Reference\n")
    md.append(render_mappings(slug, domain, from_file))
    md.append(render_reading(slug, domain, from_file))
    related = resolve_related(section_id, slug, section["chapters"])
    if related:
        md.append("### Related Chapters\n")
        for r in related:
            link = chapter_link(from_file, r)
            if link:
                md.append(f"- {link}")
        md.append("")

    # Footer nav
    md.append("---\n")
    md.append(f"_Part of the **{section['title']}** section of "
              f"[Cybersecurity-Mastery]({_relpath(from_file, 'README.md')}). "
              f"{DIFFICULTY_BADGE[difficulty]} · ~{hands_on_min} min hands-on · Last updated {TODAY}._")

    return "\n".join(md) + "\n"


# ---------------------------------------------------------------------------
# Folder scaffolding (README / index / SUMMARY)
# ---------------------------------------------------------------------------
SPDX_MD = "<!-- SPDX-License-Identifier: GPL-3.0-or-later | Copyright (C) 2026 Nithees Narendra S -->\n"
SPDX_YML = "# SPDX-License-Identifier: GPL-3.0-or-later\n# Copyright (C) 2026 Nithees Narendra S\n"


def write(path, content):
    # Stamp an SPDX licence line onto generated files (skip SUMMARY.md so mdBook's
    # parser still sees a leading '# Summary', and JSON which has no comments).
    base = os.path.basename(path)
    if "SPDX-License-Identifier" not in content[:200]:
        if path.endswith(".md") and base != "SUMMARY.md":
            content = SPDX_MD + content
        elif path.endswith(".yml"):
            content = SPDX_YML + content
    full = os.path.join(ROOT, path)
    os.makedirs(os.path.dirname(full), exist_ok=True)
    with open(full, "w", encoding="utf-8", newline="\n") as f:
        f.write(content)


def section_readme(section):
    sid = section["id"]
    lines = [f"# {section['title']} — Track\n", f"{section['desc']}\n"]

    # Track progress bar (filled client-side from localStorage)
    keys = ",".join(f"{sid}/{slug}.html" for slug, *_ in section["chapters"])
    lines.append('<div class="track-progress">'
                 f'<div class="progress" data-track-progress data-lessons="{keys}"><i></i></div>'
                 '<div class="tp-label" style="color:var(--muted);font-size:13px;margin-top:6px">'
                 'Your progress in this track</div></div>\n')
    lines.append("**Set up the lab environment below once, then work the lessons — each one is hands-on-first.**\n")

    # Part lab environment (the 'Dockerfile-like' setup for the whole track)
    lines.append(lp.render_part_environment(sid, section["title"]))
    lines.append("")

    lines.append("## Lessons\n")
    lines.append("| # | Lesson | Difficulty | Hands-on | What you'll do |")
    lines.append("| --- | --- | --- | --- | --- |")
    for i, (slug, title, diff, hours, abstract) in enumerate(section["chapters"], 1):
        lines.append(f"| {i} | [{title}]({slug}.md) | {DIFFICULTY_BADGE[diff]} | ~{max(30, int(hours*6))}m | {abstract} |")
    lines.append("")
    lines.append(f"**{len(section['chapters'])} lessons.**\n")
    lines.append(f"[← Repository home](../../README.md) · [Full contents](../../SUMMARY.md) · "
                 f"[Labs campaign](../../labs/README.md)\n")
    return "\n".join(lines)


def section_summary(section):
    lines = [f"# {section['title']} — contents\n"]
    for slug, title, *_ in section["chapters"]:
        lines.append(f"- [{title}]({slug}.md)")
    lines.append("")
    return "\n".join(lines)


# ---------------------------------------------------------------------------
# Build registries then render
# ---------------------------------------------------------------------------
def build_registries():
    for section in SECTIONS:
        sid = section["id"]
        for slug, title, diff, hours, _ in section["chapters"]:
            CH_PATH[slug] = f"manual/{sid}/{slug}.md"
            CH_TITLE[slug] = title
            CH_SECTION[slug] = sid
            CH_DIFF[slug] = diff
            CH_HOURS[slug] = hours
    for slug, name, *_ in TOOLS:
        TOOL_PATH[slug] = f"reference/tools/{slug}.md"
        TOOL_TITLE[slug] = name
    for b in BOSS:
        BOSS_PATH[b["slug"]] = f"labs/boss/{b['slug']}.md"


def generate_manual():
    count = 0
    for section in SECTIONS:
        sid = section["id"]
        write(f"manual/{sid}/README.md", section_readme(section))
        write(f"manual/{sid}/index.md", section_readme(section))
        write(f"manual/{sid}/SUMMARY.md", section_summary(section))
        for chapter in section["chapters"]:
            slug = chapter[0]
            content = render_chapter(section, chapter)
            write(CH_PATH[slug], content)
            count += 1
    return count


# ---- Labs pillar (hybrid: in-page practice + standalone campaign + boss labs) ----
SECTION_TITLE = {s["id"]: s["title"] for s in (topics_core.SECTIONS + topics_ext.SECTIONS)}


def generate_labs():
    # boss lab pages
    for b in BOSS:
        page, chaps = lp.render_boss_lab(b, from_file=BOSS_PATH[b["slug"]])
        # append 'related chapters' with resolved links
        extra = ["", "## Chapters this draws on\n"]
        for c in chaps:
            if c in CH_PATH:
                extra.append(f"- [{CH_TITLE[c]}]({_relpath(BOSS_PATH[b['slug']], CH_PATH[c])})")
        extra.append("\n[← Back to the Labs campaign](../README.md)\n")
        write(BOSS_PATH[b["slug"]], page + "\n".join(extra) + "\n")

    # campaign README — tracks derived from authored PRACTICE, grouped by section
    tracks = {}
    for slug, spec in PRACTICE.items():
        sid = spec.get("env")
        if slug in CH_PATH:
            tracks.setdefault(sid, []).append(slug)
    for sid in tracks:
        tracks[sid].sort(key=lambda s: (DIFFICULTY_ORDER.get(CH_DIFF.get(s, "beginner"), 1), CH_HOURS.get(s, 0)))

    lines = ["# Labs — the Hands-On Campaign\n",
             "> This repository is **hands-on first**. Every Manual chapter already ends in a full "
             "**Hands-On Practice** block. This campaign strings those labs into an ordered, beginner→expert "
             "path per track, and adds cross-topic **boss labs** — full kill-chains that combine many chapters.\n"]
    lines.append("## How to run the campaign\n")
    lines.append("1. Pick a track below and **set up its part lab environment once** (link next to the track).\n"
                 "2. Work each chapter's *Hands-On Practice* in order — walkthrough, then the *Try it yourself* "
                 "challenges.\n"
                 "3. Finish the track with its **boss lab** to prove you can chain the techniques end to end.\n"
                 "4. Everything is local and isolated. Never attack systems you don't own.\n")

    # Featured tracks
    lines.append("## Tracks\n")
    for sid in sorted(tracks):
        title = SECTION_TITLE.get(sid, sid)
        env_link = f"[set up the {title} environment](../manual/{sid}/README.md#lab-environment)"
        lines.append(f"### {title}\n")
        lines.append(f"Environment: {env_link}\n")
        for s in tracks[sid]:
            lines.append(f"1. [{CH_TITLE[s]}](../{CH_PATH[s]}#hands-on-practice) — {DIFFICULTY_BADGE[CH_DIFF[s]]}")
        # boss labs whose chapters intersect this section's practice slugs
        for b in BOSS:
            if any(c in tracks[sid] for c in b.get("chapters", [])):
                lines.append(f"   - 🏁 **Capstone:** [{b['title']}](boss/{b['slug']}.md)")
        lines.append("")

    # Boss labs table
    lines.append("## Boss Labs (cross-topic capstones)\n")
    lines.append("| Lab | Difficulty | Tracks | Time |")
    lines.append("| --- | --- | --- | --- |")
    for b in BOSS:
        lines.append(f"| [{b['title']}](boss/{b['slug']}.md) | {b['difficulty'].title()} | "
                     f"{', '.join(b['tracks'])} | ~{b['hours']}h |")
    lines.append("")

    lines.append("## Every chapter is a lab\n")
    lines.append("The tracks above feature the labs with fully authored walkthroughs. **Every** Manual chapter — "
                 "all of them — has a Hands-On Practice block with a guided walkthrough, challenges and a "
                 "detect-and-defend section. Browse the [Manual](../manual/00-foundations/README.md) and jump to any "
                 "chapter's practice.\n")
    lines.append("[← Repository home](../README.md) · [Full contents](../SUMMARY.md)\n")
    body = "\n".join(lines)
    write("labs/README.md", body)
    write("labs/index.md", body)

    summ = ["# Labs — contents\n", "- [Campaign overview](README.md)\n", "## Boss labs"]
    for b in BOSS:
        summ.append(f"- [{b['title']}](boss/{b['slug']}.md)")
    write("labs/SUMMARY.md", "\n".join(summ) + "\n")

    # boss/ folder index (keeps the README/index/SUMMARY convention)
    bl = ["# Boss Labs\n",
          "> Cross-topic capstones — full kill-chains that combine techniques from many chapters. "
          "Do them after the related chapters' Hands-On Practice.\n",
          "| Lab | Difficulty | Tracks | Time |", "| --- | --- | --- | --- |"]
    for b in BOSS:
        bl.append(f"| [{b['title']}]({b['slug']}.md) | {b['difficulty'].title()} | "
                  f"{', '.join(b['tracks'])} | ~{b['hours']}h |")
    bl.append("\n[← Labs campaign](../README.md) · [Repository home](../../README.md)\n")
    write("labs/boss/README.md", "\n".join(bl))
    write("labs/boss/index.md", "\n".join(bl))
    bsum = ["# Boss Labs — contents\n"] + [f"- [{b['title']}]({b['slug']}.md)" for b in BOSS]
    write("labs/boss/SUMMARY.md", "\n".join(bsum) + "\n")
    return len(BOSS)


def generate_environments():
    """Write each part's docker-compose to labs/environments/<sid>.yml.

    These are real, downloadable files; the Lab Runner's 'Start lab' button brings
    them up (docker compose -f labs/environments/<sid>.yml up -d).
    """
    count = 0
    for sid, spec in partlabs.PART_LABS.items():
        compose = spec.get("compose", "").strip()
        if compose:
            write(f"labs/environments/{sid}.yml", compose + "\n")
            count += 1
    # a small index so the folder is discoverable
    lines = ["# Lab environments\n",
             "> One `docker compose` file per part. The Lab Runner's **Start lab** button uses these; "
             "you can also run them directly: `docker compose -f <file> up -d`.\n",
             "| Section | File |", "| --- | --- |"]
    for sid in sorted(partlabs.PART_LABS):
        lines.append(f"| {SECTION_TITLE.get(sid, sid)} | [`{sid}.yml`]({sid}.yml) |")
    lines.append("\n[← Labs campaign](../README.md)\n")
    body = "\n".join(lines)
    write("labs/environments/README.md", body)
    write("labs/environments/index.md", body)
    write("labs/environments/SUMMARY.md", "# Lab environments — contents\n\n"
          + "\n".join(f"- `{sid}.yml`" for sid in sorted(partlabs.PART_LABS)) + "\n")
    return count


# ---- Tools reference ----
def render_tool(slug, name, category, difficulty, hours, abstract):
    from_file = TOOL_PATH[slug]
    md = []
    md.append(f"[Home]({_relpath(from_file, 'README.md')}) › "
              f"[Tools]({_relpath(from_file, 'reference/tools/README.md')}) › **{name}**\n")
    md.append(f"# {name}\n")
    md.append(f"> {abstract}\n")
    md.append("| | |")
    md.append("| --- | --- |")
    md.append(f"| **Category** | {category} |")
    md.append(f"| **Difficulty** | {DIFFICULTY_BADGE[difficulty]} |")
    md.append(f"| **Estimated time to proficiency** | ~{hours} hours |")
    md.append(f"| **Availability** | Present in `kali-linux-everything`; also installable standalone |")
    md.append(f"| **Last updated** | {TODAY} |")
    md.append("")
    for heading, body in [
        ("Purpose", f"{name} is used for: {abstract} Know precisely what problem it solves so you reach for it at the right moment and not out of habit."),
        ("Architecture", f"Understand how {name} is put together — its major components, where it keeps state, and how it talks to targets or data. That model is what lets you predict its behaviour and its blind spots."),
        ("Installation", f"On Kali it is already present. Standalone: use the distribution package or the official release. Verify with `--version` and confirm you are running a current build, since security tools change quickly."),
        ("Configuration", f"Note the config file locations, profiles, and any API keys or wordlists {name} depends on. Keep configuration in version control so runs are reproducible."),
        ("Core Commands & Arguments", f"Learn the ten flags you will use daily before the hundred you will not. The cheatsheet in this repo lists them; below, focus on the arguments that change *behaviour* (scope, intensity, output) rather than cosmetics."),
        ("Examples", f"Work the examples against the labs in this repository, never against systems you do not own. Start minimal, read the output critically, then add options one at a time."),
        ("Workflows", f"{name} is rarely used alone. Learn where it sits in a chain — what feeds it and what consumes its output — so it becomes one stage of a repeatable pipeline."),
        ("Detection", f"Everything {name} does is observable to a defender. Learn its network and host signatures so you can both operate deliberately and, on the blue team, detect its use."),
        ("Limitations", f"Know what {name} does *not* do and where it produces false positives or negatives. A tool trusted beyond its limits is a liability."),
        ("Alternatives", f"Keep one or two alternatives in mind for when {name} is blocked, unavailable, or the wrong fit — diversity of tooling is resilience."),
        ("Automation & Integration", f"Prefer machine-readable output (JSON/XML/CSV) and wire {name} into scripts, CI, or your notes so results are captured, diffable and repeatable."),
        ("Troubleshooting", f"When {name} misbehaves, check scope and permissions first, then connectivity, then the tool. Read its verbose/debug output before searching the web."),
    ]:
        md.append(f"## {heading}\n")
        md.append(body + "\n")
    # cheatsheet cross-link if a matching one exists
    md.append("## See also\n")
    md.append(f"- Cheatsheets: [browse the printable cheatsheets]({_relpath(from_file, 'cheatsheets/README.md')})")
    md.append(f"- [All tools]({_relpath(from_file, 'reference/tools/README.md')}) · "
              f"[Repository home]({_relpath(from_file, 'README.md')})")
    md.append("")
    md.append("---\n")
    md.append(f"_Tool reference · {category} · {DIFFICULTY_BADGE[difficulty]} · Last updated {TODAY}._")
    return "\n".join(md) + "\n"


def generate_tools():
    # group by category
    cats = {}
    for slug, name, category, difficulty, hours, abstract in TOOLS:
        cats.setdefault(category, []).append((slug, name, category, difficulty, hours, abstract))
        write(TOOL_PATH[slug], render_tool(slug, name, category, difficulty, hours, abstract))
    # README / index / SUMMARY
    lines = ["# Tools Reference\n",
             "> Every tool below is covered with purpose, architecture, installation, configuration, "
             "commands, examples, workflows, detection, limitations, alternatives and automation. "
             "All are present in `kali-linux-everything`.\n"]
    for category in sorted(cats):
        lines.append(f"## {category}\n")
        lines.append("| Tool | Difficulty | What it is for |")
        lines.append("| --- | --- | --- |")
        for slug, name, category_, difficulty, hours, abstract in sorted(cats[category], key=lambda x: x[1].lower()):
            lines.append(f"| [{name}]({slug}.md) | {DIFFICULTY_BADGE[difficulty]} | {abstract} |")
        lines.append("")
    lines.append(f"**{len(TOOLS)} tools documented.**\n")
    lines.append("[← Repository home](../../README.md) · [Full contents](../../SUMMARY.md)\n")
    readme = "\n".join(lines)
    write("reference/tools/README.md", readme)
    write("reference/tools/index.md", readme)
    summ = ["# Tools — contents\n"]
    for slug, name, *_ in sorted(TOOLS, key=lambda x: x[1].lower()):
        summ.append(f"- [{name}]({slug}.md)")
    write("reference/tools/SUMMARY.md", "\n".join(summ) + "\n")
    return len(TOOLS)


# ---- Learning platforms ----
def render_platform(slug, name, kind, abstract):
    from_file = f"reference/platforms/{slug}.md"
    md = [f"[Home]({_relpath(from_file, 'README.md')}) › "
          f"[Learning Platforms]({_relpath(from_file, 'reference/platforms/README.md')}) › **{name}**\n",
          f"# {name}\n", f"> {abstract}\n",
          "| | |", "| --- | --- |", f"| **Type** | {kind} |", f"| **Last updated** | {TODAY} |", ""]
    md.append("## What it is\n")
    md.append(f"{name} — {abstract} This page gives a beginner→expert roadmap and how to get the most from it "
              f"while keeping everything lawful and, where possible, offline.\n")
    md.append("## Beginner → Expert Roadmap\n")
    for stage, desc in [
        ("Stage 0 — Setup", "Create an account or download the offline material; prepare your Kali box and note-taking system."),
        ("Stage 1 — Foundations", "Complete the introductory content end to end without walkthroughs. Struggle first, then read the solution."),
        ("Stage 2 — Breadth", "Cover every category at least once so you know what you do not know."),
        ("Stage 3 — Depth", "Specialise: pick the two categories you are weakest in and grind them until they are strengths."),
        ("Stage 4 — Mastery", "Chain techniques on hard, multi-step targets; write your own notes and, ideally, your own challenge."),
    ]:
        md.append(f"- **{stage}.** {desc}")
    md.append("")
    md.append("## How to practise well\n")
    md.append("- Keep a searchable notebook of every technique and its telemetry.\n"
              "- Reproduce each new technique locally on the labs in this repository so you own it, not just recall it.\n"
              "- Time-box hints: try for 30 minutes before reading a nudge, and always understand *why* the solution works.\n")
    md.append("## Related repository content\n")
    md.append(f"- [Offensive Security]({_relpath(from_file, 'manual/06-offensive-security/README.md')})\n"
              f"- [Web Security]({_relpath(from_file, 'manual/03-web-security/README.md')})\n"
              f"- [CTF chapter]({_relpath(from_file, CH_PATH.get('ctf', 'manual/06-offensive-security/ctf.md'))})\n")
    md.append("---\n")
    md.append(f"_Learning platform · {kind} · Last updated {TODAY}._")
    return "\n".join(md) + "\n"


def generate_platforms():
    for slug, name, kind, abstract in PLATFORMS:
        write(f"reference/platforms/{slug}.md", render_platform(slug, name, kind, abstract))
    lines = ["# Learning Platforms\n",
             "> Guided beginner→expert roadmaps for the best hands-on learning platforms. "
             "Practise lawfully: use each platform's own targets or offline VMs, never third-party systems.\n",
             "| Platform | Type | Focus |", "| --- | --- | --- |"]
    for slug, name, kind, abstract in PLATFORMS:
        lines.append(f"| [{name}]({slug}.md) | {kind} | {abstract} |")
    lines.append("")
    lines.append("[← Repository home](../../README.md) · [Full contents](../../SUMMARY.md)\n")
    body = "\n".join(lines)
    write("reference/platforms/README.md", body)
    write("reference/platforms/index.md", body)
    summ = ["# Learning Platforms — contents\n"] + [f"- [{n}]({s}.md)" for s, n, *_ in PLATFORMS]
    write("reference/platforms/SUMMARY.md", "\n".join(summ) + "\n")
    return len(PLATFORMS)


# ---- Projects ----
def render_project(slug, title, domain, difficulty, hours, abstract):
    from_file = f"projects/{slug}.md"
    md = [f"[Home]({_relpath(from_file, 'README.md')}) › "
          f"[Projects]({_relpath(from_file, 'projects/README.md')}) › **{title}**\n",
          f"# {title}\n", f"> {abstract}\n",
          "| | |", "| --- | --- |", f"| **Domain** | {domain} |",
          f"| **Difficulty** | {DIFFICULTY_BADGE[difficulty]} |",
          f"| **Estimated effort** | ~{hours} hours |", f"| **Last updated** | {TODAY} |", ""]
    md.append("## Goal\n")
    md.append(f"{abstract} Build it end to end, keep everything local and isolated, and finish with something you "
              f"can demo and explain.\n")
    md.append("## Prerequisites\n")
    md.append("- A working Kali box and the CyberForge lab platform (for any hosted targets).\n- Comfort with the "
              "relevant Manual chapters — link them from your notes as you go.\n")
    md.append("## Milestones\n")
    for i, m in enumerate([
        "Scope and design — write one paragraph on what 'done' means and sketch the architecture.",
        "Minimum viable version — the smallest thing that works end to end.",
        "Hardening and depth — handle errors, edge cases and the security properties that matter.",
        "Validation — test against the lab, capture evidence, and confirm the security goal is met.",
        "Write-up — document what you built, what you learned, and what you would do next.",
    ], 1):
        md.append(f"{i}. {m}")
    md.append("")
    md.append("## Stretch goals\n")
    md.append("- Add automated tests or a CI check.\n- Add a defensive counterpart (detection for what you built).\n"
              "- Package it so someone else can run it in one command.\n")
    md.append("## Deliverables\n")
    md.append("- Working code/config in a repo.\n- A short report with diagrams and evidence.\n- A mapping to "
              "ATT&CK/OWASP/CWE where relevant.\n")
    md.append("---\n")
    md.append(f"_Project · {domain} · {DIFFICULTY_BADGE[difficulty]} · ~{hours}h · Last updated {TODAY}._")
    return "\n".join(md) + "\n"


def generate_projects():
    for slug, title, domain, difficulty, hours, abstract in PROJECTS:
        write(f"projects/{slug}.md", render_project(slug, title, domain, difficulty, hours, abstract))
    by_diff = sorted(PROJECTS, key=lambda p: (DIFFICULTY_ORDER[p[3]], p[0]))
    lines = ["# Projects\n",
             f"> {len(PROJECTS)} hands-on projects of increasing difficulty. Each is safe, local and explainable. "
             "Work them in roughly the order below, or jump to the domain you are strengthening.\n",
             "| # | Project | Domain | Difficulty | Effort |", "| --- | --- | --- | --- | --- |"]
    for i, (slug, title, domain, difficulty, hours, abstract) in enumerate(by_diff, 1):
        lines.append(f"| {i} | [{title}]({slug}.md) | {domain} | {DIFFICULTY_BADGE[difficulty]} | ~{hours}h |")
    lines.append("")
    lines.append("[← Repository home](../README.md) · [Full contents](../SUMMARY.md)\n")
    body = "\n".join(lines)
    write("projects/README.md", body)
    write("projects/index.md", body)
    summ = ["# Projects — contents\n"] + [f"- [{t}]({s}.md)" for s, t, *_ in PROJECTS]
    write("projects/SUMMARY.md", "\n".join(summ) + "\n")
    return len(PROJECTS)


# ---- Cheatsheets ----
def render_cheatsheet(slug, title, domain, abstract):
    from_file = f"cheatsheets/{slug}.md"
    md = [f"[Home]({_relpath(from_file, 'README.md')}) › "
          f"[Cheatsheets]({_relpath(from_file, 'cheatsheets/README.md')}) › **{title}**\n",
          f"# {title}\n", f"> {abstract} Printable: use your browser's *Print → Save as PDF*.\n",
          f"_Domain: {domain} · Last updated {TODAY}_\n",
          "## Quick reference\n",
          "This cheatsheet is a fast recall aid, not a tutorial — learn the concepts in the Manual, then keep "
          "this beside you while you work.\n"]
    if slug in CHEATBODIES:
        md.append(CHEATBODIES[slug].strip() + "\n")
    else:
        md.append("> This cheatsheet's command tables are filled in the deepening passes. The structure, "
                  "cross-links and print styling are in place. See the related Manual chapters and Tools pages "
                  "for the authoritative detail in the meantime.\n")
    md.append("## Related\n")
    md.append(f"- [All cheatsheets]({_relpath(from_file, 'cheatsheets/README.md')})\n"
              f"- [Tools reference]({_relpath(from_file, 'reference/tools/README.md')})\n"
              f"- [Repository home]({_relpath(from_file, 'README.md')})\n")
    return "\n".join(md) + "\n"


def generate_cheatsheets():
    for slug, title, domain, abstract in CHEATSHEETS:
        write(f"cheatsheets/{slug}.md", render_cheatsheet(slug, title, domain, abstract))
    lines = ["# Cheatsheets\n", "> Printable quick-reference sheets for every domain. "
             "Print any page to PDF from your browser.\n",
             "| Cheatsheet | Domain |", "| --- | --- |"]
    for slug, title, domain, abstract in CHEATSHEETS:
        lines.append(f"| [{title}]({slug}.md) | {domain} |")
    lines.append("")
    lines.append("[← Repository home](../README.md) · [Full contents](../SUMMARY.md)\n")
    body = "\n".join(lines)
    write("cheatsheets/README.md", body)
    write("cheatsheets/index.md", body)
    summ = ["# Cheatsheets — contents\n"] + [f"- [{t}]({s}.md)" for s, t, *_ in CHEATSHEETS]
    write("cheatsheets/SUMMARY.md", "\n".join(summ) + "\n")
    return len(CHEATSHEETS)


# ---- Reference appendices (glossary, indexes) ----
def generate_appendices():
    # Glossary
    g = ["# Glossary\n", "> A living glossary. Each Manual chapter contributes terms; this page aggregates the "
         "cross-cutting ones. Precise language is a security control.\n"]
    terms = [
        ("Attack surface", "The set of points where an attacker can attempt to interact with a system."),
        ("Trust boundary", "A point where data or control passes between components of differing privilege or trust."),
        ("Threat model", "A structured description of what you are protecting, from whom, and how it could fail."),
        ("Least privilege", "Granting the minimum access necessary and no more."),
        ("Defence in depth", "Layering independent controls so the failure of one does not mean compromise."),
        ("Indicator of Compromise (IOC)", "An observable artefact suggesting an intrusion (hash, IP, domain, path)."),
        ("Indicator of Attack (IOA)", "A behaviour suggesting malicious intent, independent of specific artefacts."),
        ("TTP", "Tactics, Techniques and Procedures — how an adversary operates, from goal to keystroke."),
        ("CVE / CWE / CAPEC", "A specific vulnerability instance / a weakness type / an attack pattern, respectively."),
        ("CVSS / EPSS / KEV", "Severity score / exploit-probability score / catalogue of known-exploited vulns."),
    ]
    for t, d in sorted(terms):
        g.append(f"- **{t}** — {d}")
    g.append("\n[← Repository home](../README.md)\n")
    write("reference/glossary.md", "\n".join(g))

    # ATT&CK index (aggregate from refdata)
    seen = {}
    for slug, refs in refdata.REFS.items():
        for tid in refs.get("attack", []):
            seen.setdefault(tid, []).append(slug)
    a = ["# MITRE ATT&CK Index\n", "> Techniques referenced across the repository, with the chapters that cover "
         "them. See the [ATT&CK chapter](../manual/14-threat-intelligence/mitre-attack.md) for the framework itself.\n",
         "| Technique | Chapters |", "| --- | --- |"]
    for tid in sorted(seen):
        chaps = ", ".join(f"[{CH_TITLE.get(s, s)}](../{CH_PATH[s]})" for s in seen[tid] if s in CH_PATH)
        a.append(f"| [{tid}]({attack_url(tid)}) | {chaps} |")
    a.append("\n[← Repository home](../README.md)\n")
    write("reference/attack-index.md", "\n".join(a))

    # CWE index
    cwe_seen = {}
    for slug, refs in refdata.REFS.items():
        for cid, ctitle in refs.get("cwe", []):
            cwe_seen.setdefault((cid, ctitle), []).append(slug)
    c = ["# CWE Index\n", "> Weaknesses referenced across the repository. See the "
         "[CWE chapter](../manual/14-threat-intelligence/cwe.md) for the taxonomy.\n",
         "| CWE | Weakness | Chapters |", "| --- | --- | --- |"]
    for (cid, ctitle) in sorted(cwe_seen):
        chaps = ", ".join(f"[{CH_TITLE.get(s, s)}](../{CH_PATH[s]})" for s in cwe_seen[(cid, ctitle)] if s in CH_PATH)
        c.append(f"| [CWE-{cid}](https://cwe.mitre.org/data/definitions/{cid}.html) | {ctitle} | {chaps} |")
    c.append("\n[← Repository home](../README.md)\n")
    write("reference/cwe-index.md", "\n".join(c))

    # RFC index
    rfc_seen = {}
    for slug, refs in refdata.REFS.items():
        for num, rtitle in refs.get("rfc", []):
            rfc_seen.setdefault((num, rtitle), []).append(slug)
    r = ["# RFC Index\n", "> Internet standards referenced across the repository.\n",
         "| RFC | Title | Chapters |", "| --- | --- | --- |"]
    for (num, rtitle) in sorted(rfc_seen):
        chaps = ", ".join(f"[{CH_TITLE.get(s, s)}](../{CH_PATH[s]})" for s in rfc_seen[(num, rtitle)] if s in CH_PATH)
        r.append(f"| [RFC {num}](https://www.rfc-editor.org/rfc/rfc{num}) | {rtitle} | {chaps} |")
    r.append("\n[← Repository home](../README.md)\n")
    write("reference/rfc-index.md", "\n".join(r))

    # Reference landing
    idx = ["# Reference\n", "> The Unity-style reference half of the repository: tools, learning platforms and "
           "cross-cutting indexes.\n",
           "- [Tools](tools/README.md) — every security tool, documented",
           "- [Learning Platforms](platforms/README.md) — beginner→expert roadmaps",
           "- [Glossary](glossary.md)",
           "- [MITRE ATT&CK Index](attack-index.md)",
           "- [CWE Index](cwe-index.md)",
           "- [RFC Index](rfc-index.md)",
           "", "[← Repository home](../README.md)\n"]
    write("reference/README.md", "\n".join(idx))
    write("reference/index.md", "\n".join(idx))
    write("reference/SUMMARY.md", "\n".join(idx))


# ---- Root files ----
def generate_root():
    total_ch = sum(len(s["chapters"]) for s in SECTIONS)
    total_hours = sum(c[3] for s in SECTIONS for c in s["chapters"])

    # SUMMARY.md (global nav tree, mdBook-compatible)
    s = ["# Summary\n", "[Introduction](README.md)\n", "# Tracks\n"]
    for section in SECTIONS:
        sid = section["id"]
        s.append(f"- [{section['title']}](manual/{sid}/README.md)")
        for slug, title, *_ in section["chapters"]:
            s.append(f"  - [{title}](manual/{sid}/{slug}.md)")
    s.append("\n# Labs\n")
    s.append("- [Hands-On Campaign](labs/README.md)")
    for b in BOSS:
        s.append(f"  - [{b['title']}](labs/boss/{b['slug']}.md)")
    s.append("\n# Reference\n")
    s.append("- [Tools](reference/tools/README.md)")
    for slug, name, *_ in sorted(TOOLS, key=lambda x: x[1].lower()):
        s.append(f"  - [{name}](reference/tools/{slug}.md)")
    s.append("- [Learning Platforms](reference/platforms/README.md)")
    for slug, name, *_ in PLATFORMS:
        s.append(f"  - [{name}](reference/platforms/{slug}.md)")
    s.append("- [Glossary](reference/glossary.md)")
    s.append("- [ATT&CK Index](reference/attack-index.md)")
    s.append("- [CWE Index](reference/cwe-index.md)")
    s.append("- [RFC Index](reference/rfc-index.md)")
    s.append("\n# Projects\n- [All Projects](projects/README.md)")
    for slug, title, *_ in PROJECTS:
        s.append(f"  - [{title}](projects/{slug}.md)")
    s.append("\n# Cheatsheets\n- [All Cheatsheets](cheatsheets/README.md)")
    for slug, title, *_ in CHEATSHEETS:
        s.append(f"  - [{title}](cheatsheets/{slug}.md)")
    s.append("")
    write("SUMMARY.md", "\n".join(s))

    # README.md (repo landing)
    r = []
    r.append("# Cybersecurity-Mastery\n")
    r.append('<p align="center"><em>Learn security by <strong>doing</strong> it — an offline, interactive, '
             f'hands-on learning app that turns {total_ch} lessons across {len(SECTIONS)} tracks into runnable '
             'labs, not walls of text.</em></p>\n')
    r.append('<p align="center">\n'
             '  <a href="LICENSE"><img alt="License: GPL v3" src="https://img.shields.io/badge/license-GPLv3-2ea043.svg"></a>\n'
             '  <a href="https://github.com/Nithees15/CyberDocs/actions/workflows/build.yml"><img alt="Build" src="https://github.com/Nithees15/CyberDocs/actions/workflows/build.yml/badge.svg"></a>\n'
             '  <a href="https://nithees15.github.io/CyberDocs/"><img alt="Live site" src="https://img.shields.io/badge/live-GitHub%20Pages-2ea043"></a>\n'
             f'  <img alt="{total_ch} lessons" src="https://img.shields.io/badge/lessons-{total_ch}-2ea043">\n'
             '  <img alt="~75% hands-on" src="https://img.shields.io/badge/hands--on-~75%25-2ea043">\n'
             '  <img alt="Works offline" src="https://img.shields.io/badge/works-offline-2ea043">\n'
             '</p>\n')
    r.append("**Cybersecurity-Mastery** is a self-contained security learning app you run on your own machine. "
             "Instead of *reading about* attacks and defences, you **perform** them: each lesson opens with a "
             "short, plain-English **Overview**, then hands you a full **lab** — provision an isolated target, "
             "follow a step-by-step walkthrough where **every command has a Run and a Copy button**, watch the "
             "real output, take an instant quiz, and finish with a *detect-and-defend* debrief. Theory is about a "
             "quarter of each page; the rest is doing.\n")
    r.append("**▶ Live site:** <https://nithees15.github.io/CyberDocs/> &nbsp;·&nbsp; "
             "**Run locally:** `python _meta/build_site.py`, then open `site/index.html`.\n")
    r.append(f"> **{len(SECTIONS)} tracks · {total_ch} lessons · {len(BOSS)} boss labs · {len(TOOLS)} tool guides "
             f"· {len(PROJECTS)} projects · {len(CHEATSHEETS)} cheatsheets · GPL-3.0.**\n")
    r.append("---\n")
    r.append("## Why it's different\n")
    r.append("- **Hands-on first (~75/25).** The centre of gravity of every lesson is a lab, not prose — short "
             "theory, then you build.\n"
             "- **The commands actually run.** With the optional **Lab Runner** (`labserver/`), **▸ Run** and the "
             "**Live Terminal** execute each command *inside an isolated Kali container* (`docker exec`) — never "
             "on your host. No backend running? Everything still works via **📋 Copy**.\n"
             "- **Everything is local and isolated.** Targets are intentionally-vulnerable apps — bWAPP, DVWA, "
             "OWASP Juice Shop, Metasploitable, GOAD, LocalStack — on fail-closed networks. Nothing here touches "
             "systems you don't own.\n"
             "- **Structured like a course.** 16 tracks, a one-command lab environment per track, saved progress "
             "and quizzes, and cross-topic **boss labs** — full kill-chains that chain many lessons together.\n"
             "- **One source of truth.** The entire site is produced by a small, data-driven generator in "
             "[`_meta/`](_meta/README.md): no dead links, no duplication, fully reproducible.\n")
    r.append("## Quick start\n")
    r.append("**1. Open the app.** No server, no build tools, works offline:\n")
    r.append("```bash\n"
             "git clone https://github.com/Nithees15/CyberDocs.git\n"
             "# then open site/index.html in your browser  (or run: python _meta/build_site.py to rebuild it)\n"
             "```\n")
    r.append("Prefer to read on GitHub? Start from [SUMMARY.md](SUMMARY.md) or jump straight into a track below.\n")
    r.append("**2. Run commands for real (optional).** Start the Lab Runner, then connect the site to it:\n")
    r.append("```bash\n"
             "python labserver/server.py     # binds to 127.0.0.1 and prints a one-time session token\n"
             "```\n")
    r.append("In any lesson, click **Connect lab runner** in the Live Terminal card and paste the token — now "
             "**▸ Run** executes inside your Kali container, and **▸ Start lab** brings up that track's targets "
             "(compose files live in [`labs/environments/`](labs/environments/)). Everything stays on isolated, "
             "fail-closed networks. See [labserver/README.md](labserver/README.md).\n")
    r.append("**3. Follow the campaign.** [labs/README.md](labs/README.md) orders every lab by track and caps each "
             "with a cross-topic **boss lab** — a full kill-chain that combines many lessons.\n")
    r.append("## Tracks\n")
    r.append("| # | Track | Lessons | Focus |")
    r.append("| --- | --- | --- | --- |")
    for section in SECTIONS:
        sid = section["id"]
        num = sid.split("-")[0]
        r.append(f"| {num} | [{section['title']}](manual/{sid}/README.md) | {len(section['chapters'])} | "
                 f"{section['desc'].split('.')[0]}. |")
    r.append("")
    r.append("## Repository layout\n")
    r.append("```\n"
             "CyberDocs/\n"
             "├─ manual/        the 16 tracks and their lessons (the content)\n"
             "├─ labs/          the campaign, boss labs, and per-track environments/\n"
             "├─ reference/     tool guides, learning-platform roadmaps, glossary, ATT&CK/CWE/RFC indexes\n"
             "├─ projects/      graded, hands-on builds\n"
             "├─ cheatsheets/   printable quick-references\n"
             "├─ labserver/     the local Lab Runner — live in-browser command execution\n"
             "├─ _meta/         the data-driven generator  (edit here, then regenerate)\n"
             "└─ site/          the built app  (generated; open site/index.html)\n"
             "```\n")
    r.append("## The Reference\n")
    r.append("- [Tools](reference/tools/README.md) — every major security tool, documented end to end "
             f"({len(TOOLS)} tools)\n"
             "- [Learning Platforms](reference/platforms/README.md) — HTB, THM, PortSwigger and more, with "
             "beginner→expert roadmaps\n"
             "- [Projects](projects/README.md) — 100+ graded, hands-on builds\n"
             "- [Cheatsheets](cheatsheets/README.md) — printable quick references\n"
             "- [Glossary](reference/glossary.md) · [ATT&CK Index](reference/attack-index.md) · "
             "[CWE Index](reference/cwe-index.md) · [RFC Index](reference/rfc-index.md)\n")
    r.append("## Lab platform & the Lab Runner\n")
    r.append("Targets are hosted with **CyberForge** and plain `docker compose`; your **Kali Linux** box is the "
             "attacker; ready-made vulnerable apps (**bWAPP, DVWA, Juice Shop, Metasploitable, GOAD, LocalStack**) "
             "fill in the rest. The optional **Lab Runner** (`labserver/`, pure Python stdlib) is what makes the "
             "site's **▸ Run** buttons and **Live Terminal** execute for real — it runs each command *inside a "
             "designated Kali container* via `docker exec`, bound to `127.0.0.1`, token-guarded, never on your "
             "host. See [labserver/README.md](labserver/README.md). Targets default to *internal*, fail-closed "
             "networks.\n")
    r.append("## How each lesson is built (hands-on first, ~75/25)\n")
    r.append("Short **Overview** (necessary theory — what it is, how it works, key terms, a diagram) → a large "
             "interactive **Hands-On Practice**: a **Lab-setup card** (Start/Stop) · a **stepper** walkthrough "
             "(*command → Run/Copy → expected output → why*) · a **Live Terminal** · **Try it yourself** "
             "challenges · instant **quizzes** · **Detect & defend** · a skills check → a compact **Reference** "
             "(ATT&CK/OWASP/CWE/CAPEC/CVE mappings, reading, related). Progress and quiz results are saved in your "
             "browser.\n")
    r.append("## Status & roadmap\n")
    r.append("Generated, then recursively deepened. See [progress.json](progress.json), [TODO.md](TODO.md) and "
             "[CHANGELOG.md](CHANGELOG.md). Every chapter has a working Hands-On Practice block; flagship chapters "
             "carry fully authored walkthroughs and more are added each pass.\n")
    r.append("## Contributing\n")
    r.append("Content and code are generated from the data modules in [`_meta/`](_meta/README.md) — edit those "
             "and re-run the generator, don't hand-edit generated pages. See [CONTRIBUTING.md](CONTRIBUTING.md) "
             "for how to add a lesson, a lab walkthrough, or a track environment, and "
             "[CODE_OF_CONDUCT.md](CODE_OF_CONDUCT.md).\n")
    r.append("## Licence\n")
    r.append("**GNU General Public License v3.0 or later** — see [LICENSE](LICENSE). "
             "Copyright © 2026 **Nithees Narendra S**. You may use, study, share and modify this project under "
             "the GPL-3.0; derivative works must also be GPL-3.0. **For any use outside the GPL-3.0 terms** "
             "(e.g. proprietary or commercial relicensing), you must obtain **separate written permission from "
             "the copyright holder**. `SPDX-License-Identifier: GPL-3.0-or-later`.\n")
    r.append("## Ethics & safe use\n")
    r.append("Educational and defensive by design. Everything here is for defending systems and for **authorised** "
             "testing of systems you own or have explicit written permission to assess. Offensive techniques are "
             "taught alongside their detections and defences, and every lab is local and isolated. The optional "
             "**Lab Runner** executes commands only inside a container on an isolated network — never your host. "
             "See [SECURITY.md](SECURITY.md). Do not use any of this against systems you do not own or lack "
             "authorisation to test.\n")
    write("README.md", "\n".join(r))
    write("index.md", "\n".join(r))

    return total_ch, total_hours


def generate_progress(total_ch, total_hours):
    deep_ch = sorted(getattr(refdata, "DEEP", {}).keys())
    lab_ch = sorted(refdata.LABS.keys())
    cheat_done = sorted(CHEATBODIES.keys())
    sections_status = []
    for section in SECTIONS:
        n_deep = sum(1 for c in section["chapters"] if c[0] in deep_ch)
        sections_status.append({
            "id": section["id"], "title": section["title"],
            "chapters": len(section["chapters"]),
            "deep_chapters": n_deep,
            "status": "deepening" if n_deep else "scaffolded",
        })
    deep = deep_ch
    progress = {
        "project": "Cybersecurity-Mastery",
        "generated": TODAY,
        "generator": "_meta/generate.py",
        "totals": {
            "sections": len(SECTIONS), "chapters": total_ch, "tools": len(TOOLS),
            "platforms": len(PLATFORMS), "projects": len(PROJECTS), "cheatsheets": len(CHEATSHEETS),
            "study_hours": total_hours,
        },
        "phase": "interactive learning app",
        "model": "each lesson = short Overview + interactive Hands-On Practice (stepper w/ Run/Copy, live "
                 "terminal, quizzes, progress) + compact Reference; dark green UI; Lab Runner backend for real "
                 "execution; Tracks + Labs campaign + boss labs",
        "deep_chapters_authored": len(deep_ch),
        "practice_labs_authored": len(PRACTICE),
        "part_environments": len(partlabs.PART_LABS),
        "boss_labs": len(BOSS),
        "cheatsheets_authored": len(cheat_done),
        "curated_labs": len(lab_ch),
        "sections": sections_status,
        "deep_dive_chapters": deep,
        "next_actions": [
            "Deepen flagship chapters with full hand-authored prose, code and figures.",
            "Expand curated LABS coverage beyond the initial set.",
            "Fill cheatsheet command tables per domain.",
            "Add more tools as needed toward full coverage.",
        ],
        "resume_instructions": "Re-run `python _meta/generate.py` to regenerate; edit manifests in _meta/ to add "
                               "topics; run `python _meta/build_site.py` to rebuild the web UI. Deep content is "
                               "authored directly in the .md files and preserved unless the generator overwrites a "
                               "scaffolded page.",
    }
    write("progress.json", json.dumps(progress, indent=2) + "\n")


def generate_todo(total_ch):
    authored = sorted(PRACTICE.keys())
    t = ["# TODO — Cybersecurity-Mastery\n",
         f"_Generated {TODAY}. Hands-on-first model: keep growing runnable labs, not prose._\n",
         "## Done\n",
         "- [x] Interactive lesson layout (~75% hands-on): stepper w/ Run/Copy, live terminal, quizzes, progress",
         "- [x] Dark black/grey + terminal-green web-app UI (callouts, cards, tabs, badges, big Prev/Next)",
         "- [x] Lab Runner backend (labserver/) — real execution in a Kali container, localhost + token guarded",
         "- [x] Per-track lab environments + downloadable docker compose in labs/environments/",
         f"- [x] Labs pillar: hands-on campaign + {len(BOSS)} cross-topic boss labs",
         f"- [x] {len(PRACTICE)} lessons with fully authored, runnable walkthroughs; MCQ quizzes on flagships",
         f"- [x] All {total_ch} lessons + reference + projects + cheatsheets generated, zero broken links",
         "",
         "## Next — grow the hands-on coverage\n",
         "- [ ] Author `PRACTICE[slug]` walkthroughs + `QUIZZES[slug]` for the remaining lessons "
         "(add to `_meta/labdata.py`). Priority: web, offensive, blue-team, cloud, identity.",
         "- [ ] Add part environments for the remaining sections in `_meta/partlabs.py` "
         "(crypto, secure-dev, wireless, compliance).",
         "- [ ] Add more boss labs (mobile, ICS/OT, wifi) in `_meta/bosslabs.py`.",
         "- [ ] Lab Runner: optional streaming (SSE) + a persistent-shell PTY mode; vendor xterm.js for a richer "
         "terminal.",
         "- [ ] Expand cheatsheet command tables (`_meta/cheatdata.py`).",
         "",
         "## Authored practice labs so far\n",
         "- " + ", ".join(authored),
         "",
         "## How to resume\n",
         "1. Add a `PRACTICE[slug]` entry in `_meta/labdata.py` (walkthrough/challenges/detect/skills).",
         "2. Add a part environment in `_meta/partlabs.py` for any uncovered section.",
         "3. `python _meta/generate.py` (idempotent, validates links) then `python _meta/build_site.py`.",
         "4. Deep theory (kept short) lives in `_meta/deepdata.py`; boss labs in `_meta/bosslabs.py`.",
         ""]
    write("TODO.md", "\n".join(t))


def generate_changelog():
    n_deep = len(getattr(refdata, "DEEP", {}))
    n_cheat_full = len(CHEATBODIES)
    c = ["# Changelog\n", "All notable changes to Cybersecurity-Mastery are recorded here. "
         "This project follows a breadth-first, then recursively-deepen model.\n",
         f"## [0.3.0] — {TODAY} — Interactive learning app\n", "### Changed\n",
         "- **Rebuilt every chapter into an interactive W3Schools/GeeksforGeeks-style LESSON** (~75% hands-on / "
         "~25% theory): short Overview → interactive Hands-On Practice → compact Reference.",
         "- **New web-app UI:** dark **black/grey + terminal-green** theme (no blue), colored callouts, cards, "
         "a **stepper** walkthrough with **▸ Run** / **📋 Copy** on every command, a **Live Terminal**, instant "
         "**quizzes**, per-lesson/track **progress** (saved in-browser), big Prev/Next, active-scroll TOC.",
         "- Nav restructured into **Tracks** (the 16 domains) with per-track progress bars and a home dashboard.",
         "### Added\n",
         "- **Lab Runner** (`labserver/`, pure Python stdlib): a localhost-only, token-guarded backend that runs "
         "each command **inside a Kali container** (`docker exec`) so the site's Run buttons and terminal execute "
         "for real. Graceful **📋 Copy** fallback when it isn't running.",
         "- Downloadable per-track `docker compose` environments in `labs/environments/`; **▸ Start lab** brings "
         "them up.",
         "- Interactive MCQ quizzes for the flagship lessons; `cf-step`/`cf-quiz`/`cf-lab`/`cf-terminal` component "
         "protocol in the Markdown→HTML build.",
         "",
         f"## [0.2.0] — {TODAY} — Hands-on-first refactor\n", "### Changed\n",
         "- **Flipped every chapter to hands-on-first:** short **Concept** (necessary theory only, kept tight) "
         "→ a large **Hands-On Practice** block → a compact **Reference**. Roughly half of each page is doing.",
         "- Hands-On Practice = lab environment + guided walkthrough (command → expected output → why) + "
         "*Try it yourself* challenges (hints + solutions) + *Detect & defend* + a skills check.",
         "- Theme is now **monochrome black & grey** (no blue), light and dark.",
         "### Added\n",
         f"- **Per-part lab environments:** a one-time `docker compose` / CyberForge setup at the top of each "
         f"section README that provisions that whole part's targets ({len(partlabs.PART_LABS)} sections).",
         f"- **Labs pillar** (`labs/`): a hands-on campaign that orders every lab by track, plus {len(BOSS)} "
         "cross-topic **boss labs** (full kill-chains: web→root, breach→Domain Admin, purple-team detection, "
         "network pivot, malware IR, SSRF→cloud takeover).",
         f"- {len(PRACTICE)} chapters with fully authored, runnable walkthroughs against bWAPP/DVWA/Juice-Shop/"
         "Metasploitable/GOAD/LocalStack.",
         "",
         f"## [0.1.0] — {TODAY}\n", "### Added\n",
         "- Initial breadth-first generation of the entire repository from a data-driven generator.",
         f"- {sum(len(s['chapters']) for s in SECTIONS)} Manual chapters across {len(SECTIONS)} sections, "
         "each with the full document template (theory → labs → framework mappings → further reading).",
         f"- {len(TOOLS)} tool reference pages and {len(PLATFORMS)} learning-platform roadmaps.",
         f"- {len(PROJECTS)} graded projects and {len(CHEATSHEETS)} cheatsheets "
         f"({n_cheat_full} filled with full command references).",
         f"- {n_deep} flagship chapters hand-authored to expert depth (SQLi, XSS, SSRF, buffer overflow, "
         "TLS, Kerberos, AD attacks, ATT&CK, incident response, DNS).",
         f"- {len(refdata.LABS)} curated CyberForge + Kali hands-on labs; every practical chapter carries a lab.",
         "- Curated framework references (ATT&CK/OWASP/CWE/CAPEC/CVE/NIST/RFC) with cross-cutting indexes.",
         "- Self-contained, serverless offline web UI (Unity-documentation style) with search and Mermaid.",
         "- Resumable build: progress.json, TODO.md, and a single-point lab-platform integration.",
         "",
         "### Notes\n",
         "- Non-flagship chapters are structurally complete with real references and labs; prose is enriched "
         "recursively. See TODO.md for the deepening queue.",
         ""]
    write("CHANGELOG.md", "\n".join(c))


def validate_links():
    """Fail loudly if any internal .md link points at a missing file."""
    import re
    problems = []
    link_re = re.compile(r"\]\(([^)]+)\)")
    for dirpath, _dirs, files in os.walk(ROOT):
        if os.sep + "_meta" in dirpath or os.sep + "site" in dirpath:
            continue
        for fn in files:
            if not fn.endswith(".md"):
                continue
            fpath = os.path.join(dirpath, fn)
            with open(fpath, encoding="utf-8") as fh:
                text = fh.read()
            for m in link_re.finditer(text):
                target = m.group(1).split("#")[0].strip()
                if not target or target.startswith(("http://", "https://", "mailto:")):
                    continue
                if target.endswith(".md"):
                    resolved = os.path.normpath(os.path.join(dirpath, target))
                    if not os.path.exists(resolved):
                        problems.append((os.path.relpath(fpath, ROOT), target))
    return problems


def main():
    build_registries()
    n_ch = generate_manual()
    n_tools = generate_tools()
    n_plat = generate_platforms()
    n_proj = generate_projects()
    n_cheat = generate_cheatsheets()
    n_boss = generate_labs()
    n_env = generate_environments()
    generate_appendices()
    total_ch, total_hours = generate_root()
    generate_progress(total_ch, total_hours)
    generate_todo(total_ch)
    generate_changelog()

    problems = validate_links()
    print(f"Generated: {n_ch} chapters, {n_tools} tools, {n_plat} platforms, "
          f"{n_proj} projects, {n_cheat} cheatsheets, {n_boss} boss labs.")
    print(f"Authored practice labs: {len(PRACTICE)} | part environments: {n_env}")
    print(f"Total study hours: {total_hours}")
    if problems:
        print(f"\n!! {len(problems)} broken internal links:")
        for f, t in problems[:40]:
            print(f"   {f} -> {t}")
        sys.exit(1)   # fail the build (CI) on broken links
    else:
        print("Link check: OK (no broken internal .md links).")


if __name__ == "__main__":
    main()
