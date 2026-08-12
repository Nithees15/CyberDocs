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

"""Build the offline, serverless web UI (Unity-documentation style).

Renders every Markdown file in the repo to a self-contained static HTML site
under ``site/``. Opens directly from ``site/index.html`` via file:// — no server,
no build tools, no network. Navigation tree, client-side search, breadcrumbs,
prev/next, on-this-page TOC, light/dark theme, and Mermaid diagrams (rendered if
``site/assets/mermaid.min.js`` is present or the machine is online; otherwise the
diagram source is shown).

Run:  python _meta/build_site.py   (run generate.py first)
"""

from __future__ import annotations

import html
import os
import posixpath
import re
import sys
import json

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
SITE = os.path.join(ROOT, "site")
sys.path.insert(0, HERE)

import topics_core          # noqa: E402
import topics_ext           # noqa: E402
import topics_tools         # noqa: E402

SECTIONS = topics_core.SECTIONS + topics_ext.SECTIONS
TOOLS = sorted(topics_tools.TOOLS, key=lambda x: x[1].lower())
PLATFORMS = topics_tools.PLATFORMS
PROJECTS = topics_tools.PROJECTS
CHEATSHEETS = topics_tools.CHEATSHEETS
try:
    import bosslabs
    BOSS = bosslabs.BOSS
except Exception:
    BOSS = []


# ==========================================================================
# Minimal, dependency-free Markdown -> HTML
# ==========================================================================
_INLINE_CODE = re.compile(r"`([^`]+)`")
_BOLD = re.compile(r"\*\*([^*]+)\*\*")
_ITALIC = re.compile(r"(?<!\*)\*([^*\n]+)\*(?!\*)")
_LINK = re.compile(r"\[([^\]]+)\]\(([^)]+)\)")
_IMG = re.compile(r"!\[([^\]]*)\]\(([^)]+)\)")


def slugify_anchor(text):
    text = re.sub(r"`", "", text)
    text = re.sub(r"[^\w\s-]", "", text).strip().lower()
    return re.sub(r"[\s]+", "-", text)


def rewrite_link(url):
    if url.startswith(("http://", "https://", "mailto:", "#")):
        return url
    # split anchor
    if "#" in url:
        path, anchor = url.split("#", 1)
        anchor = "#" + anchor
    else:
        path, anchor = url, ""
    if path.endswith(".md"):
        path = path[:-3] + ".html"
    return path + anchor


def inline(text):
    # protect inline code
    codes = []

    def stash(m):
        codes.append(m.group(1))
        return f"\x00{len(codes)-1}\x00"

    text = _INLINE_CODE.sub(stash, text)
    text = html.escape(text, quote=False)
    # images before links
    text = _IMG.sub(lambda m: f'<img src="{rewrite_link(m.group(2))}" alt="{html.escape(m.group(1))}" loading="lazy">', text)
    text = _LINK.sub(lambda m: f'<a href="{rewrite_link(m.group(2))}">{m.group(1)}</a>', text)
    text = _BOLD.sub(r"<strong>\1</strong>", text)
    text = _ITALIC.sub(r"<em>\1</em>", text)
    # underscore emphasis, but only at word boundaries (never intraword: snake_case is safe)
    text = re.sub(r"(?<![\w])_([^_\n]+)_(?![\w])", r"<em>\1</em>", text)

    def restore(m):
        return f"<code>{html.escape(codes[int(m.group(1))], quote=False)}</code>"

    text = re.sub(r"\x00(\d+)\x00", restore, text)
    return text


# --- interactive component renderers (cf-* fences) ---
_CMDID = [0]


def _esc(s):
    return html.escape(s or "", quote=True)


def render_codeblock(content, lang=""):
    """A code block with a language label + copy button; runnable if lang == 'sh'/'bash'."""
    _CMDID[0] += 1
    cid = f"code{_CMDID[0]}"
    runnable = lang in ("sh", "bash", "console", "shell")
    run_btn = (f'<button class="btn run" data-run="{cid}" title="Run in the lab terminal">▸ Run</button>'
               if runnable else "")
    label = lang or "text"
    body = html.escape(content, quote=False)
    out_panel = f'<div class="run-out" id="{cid}-out"></div>' if runnable else ""
    return (f'<div class="codewrap"><div class="code-tb"><span class="lang">{_esc(label)}</span>'
            f'<span class="btns">{run_btn}<button class="btn copy" data-copy="{cid}">📋 Copy</button></span></div>'
            f'<pre><code id="{cid}">{body}</code></pre>{out_panel}</div>')


def render_component(kind, content):
    try:
        data = json.loads(content)
    except Exception:
        return render_codeblock(content, kind)

    if kind == "cf-step":
        n = data.get("n", "")
        goal = _esc(data.get("goal", ""))
        cmd = data.get("cmd", "")
        output = data.get("output", "")
        why = inline(data.get("why", "")) if data.get("why") else ""
        runnable = bool(data.get("runnable"))
        _CMDID[0] += 1
        cid = f"step{_CMDID[0]}"
        run_btn = (f'<button class="btn run" data-run="{cid}" title="Run in the lab terminal">▸ Run</button>'
                   if runnable else "")
        cmdblock = (f'<div class="codewrap"><div class="code-tb"><span class="lang">command</span>'
                    f'<span class="btns">{run_btn}<button class="btn copy" data-copy="{cid}">📋 Copy</button></span></div>'
                    f'<pre><code id="{cid}">{html.escape(cmd, quote=False)}</code></pre>'
                    f'<div class="run-out" id="{cid}-out"></div></div>') if cmd else ""
        outblock = (f'<details><summary>Expected output</summary>\n\n'
                    f'<pre><code>{html.escape(output, quote=False)}</code></pre></details>') if output else ""
        whyblock = f'<div class="step-why">{why}</div>' if why else ""
        return (f'<div class="step"><div class="step-head"><span class="step-num">{_esc(str(n))}</span>'
                f'<span class="step-goal">{goal}</span></div><div class="step-body">'
                f'{cmdblock}{outblock}{whyblock}</div></div>')

    if kind == "cf-quiz":
        q = _esc(data.get("q", ""))
        opts = data.get("options", [])
        ans = data.get("answer", 0)
        explain = _esc(data.get("explain", ""))
        _CMDID[0] += 1
        qid = f"quiz{_CMDID[0]}"
        obtns = "".join(
            f'<button class="quiz-opt" data-q="{qid}" data-correct="{"1" if idx == ans else "0"}">'
            f'{_esc(o)}</button>' for idx, o in enumerate(opts))
        return (f'<div class="quiz" id="{qid}"><div class="quiz-q">{q}</div>{obtns}'
                f'<div class="quiz-explain" id="{qid}-ex">{explain}</div></div>')

    if kind == "cf-terminal":
        title = _esc(data.get("title", "kali@lab — interactive terminal"))
        return (f'<div class="terminal" data-terminal="1"><div class="term-head">'
                f'<span class="term-dot r"></span><span class="term-dot y"></span><span class="term-dot g"></span>'
                f'<span class="term-title">{title}</span>'
                f'<button class="btn term-connect" style="margin-left:auto">🔌 Connect lab runner</button>'
                f'<span class="term-status down">offline</span></div>'
                f'<div class="term-body">Start the Lab Runner (see <code>labserver/README.md</code>), then click '
                f'<b>Connect lab runner</b> and paste the token. Until then, copy commands from the walkthrough '
                f'and run them in your own Kali terminal.\n</div>'
                f'<div class="term-input"><span>$</span><input type="text" '
                f'placeholder="type a command and press Enter (needs the lab runner)" disabled></div></div>')

    if kind == "cf-lab":
        title = _esc(data.get("title", "Lab setup"))
        section = _esc(data.get("section", ""))
        targets = data.get("targets", [])
        compose = data.get("compose", "")
        tlist = "".join(f"<li><code>{_esc(t[0])}</code> — {inline(t[1])}</li>" for t in targets)
        _CMDID[0] += 1
        cid = f"lab{_CMDID[0]}"
        composeblock = (f'<div class="codewrap"><div class="code-tb"><span class="lang">docker-compose.yml</span>'
                        f'<span class="btns"><button class="btn copy" data-copy="{cid}">📋 Copy</button></span></div>'
                        f'<pre><code id="{cid}">{html.escape(compose, quote=False)}</code></pre></div>') if compose else ""
        return (f'<div class="labcard"><h4>🧪 Lab setup — {title}</h4>'
                f'<ul>{tlist}</ul>'
                f'<div class="lab-actions">'
                f'<button class="btn run" data-lab-up="{section}">▸ Start lab</button>'
                f'<button class="btn" data-lab-down="{section}">■ Stop lab</button></div>'
                f'{composeblock}</div>')

    return render_codeblock(content, kind)


def md_to_html(md, headings_out=None):
    lines = md.split("\n")
    out = []
    i = 0
    n = len(lines)

    def flush_para(buf):
        if buf:
            out.append("<p>" + inline(" ".join(buf)) + "</p>")
            buf.clear()

    para = []
    while i < n:
        line = lines[i]
        stripped = line.strip()

        # blank
        if not stripped:
            flush_para(para)
            i += 1
            continue

        # fenced code / mermaid
        if stripped.startswith("```"):
            flush_para(para)
            lang = stripped[3:].strip()
            block = []
            i += 1
            while i < n and not lines[i].strip().startswith("```"):
                block.append(lines[i])
                i += 1
            i += 1  # closing fence
            content = "\n".join(block)
            if lang == "mermaid":
                # verbatim: the source already carries HTML entities the browser decodes for Mermaid
                out.append('<pre class="mermaid">' + content + "</pre>")
            elif lang in ("cf-step", "cf-quiz", "cf-lab", "cf-terminal"):
                out.append(render_component(lang, content))
            else:
                out.append(render_codeblock(content, lang))
            continue

        # raw HTML passthrough (svg, details, summary, etc.)
        if stripped.startswith("<") and not stripped.startswith("</p>"):
            flush_para(para)
            out.append(line)
            i += 1
            continue

        # headings
        m = re.match(r"^(#{1,6})\s+(.*)$", stripped)
        if m:
            flush_para(para)
            level = len(m.group(1))
            text = m.group(2).strip()
            anchor = slugify_anchor(text)
            if headings_out is not None and level in (2, 3):
                headings_out.append((level, text, anchor))
            out.append(f'<h{level} id="{anchor}">{inline(text)}</h{level}>')
            i += 1
            continue

        # horizontal rule
        if re.match(r"^(---|\*\*\*|___)$", stripped):
            flush_para(para)
            out.append("<hr>")
            i += 1
            continue

        # blockquote / callout
        if stripped.startswith(">"):
            flush_para(para)
            quote = []
            while i < n and lines[i].strip().startswith(">"):
                quote.append(lines[i].strip()[1:].lstrip())
                i += 1
            first = quote[0] if quote else ""
            m_alert = re.match(r"^\[!(NOTE|TIP|WARNING|DANGER|EXAMPLE)\]\s*(.*)$", first, re.I)
            if m_alert:
                kind = m_alert.group(1).lower()
                rest = [m_alert.group(2)] + quote[1:]
                label = {"note": "Note", "tip": "Tip", "warning": "Warning",
                         "danger": "Danger", "example": "Example"}[kind]
                body = inline(" ".join(x for x in rest if x).strip())
                out.append(f'<div class="callout {kind}"><div class="ct">{label}</div>{body}</div>')
            else:
                out.append("<blockquote>" + inline(" ".join(quote)) + "</blockquote>")
            continue

        # table
        if "|" in stripped and i + 1 < n and re.match(r"^\s*\|?[\s:\-|]+\|?\s*$", lines[i + 1]) and "-" in lines[i + 1]:
            flush_para(para)
            header = [c.strip() for c in stripped.strip("|").split("|")]
            i += 2
            rows = []
            while i < n and "|" in lines[i] and lines[i].strip():
                rows.append([c.strip() for c in lines[i].strip().strip("|").split("|")])
                i += 1
            t = ["<table><thead><tr>"]
            t += [f"<th>{inline(h)}</th>" for h in header]
            t.append("</tr></thead><tbody>")
            for r in rows:
                t.append("<tr>" + "".join(f"<td>{inline(c)}</td>" for c in r) + "</tr>")
            t.append("</tbody></table>")
            out.append("".join(t))
            continue

        # lists (supports nesting by indentation)
        if re.match(r"^(\s*)([-*+]|\d+\.)\s+", line):
            flush_para(para)
            html_list, i = parse_list(lines, i)
            out.append(html_list)
            continue

        # paragraph text
        para.append(stripped)
        i += 1

    flush_para(para)
    return "\n".join(out)


def parse_list(lines, i):
    n = len(lines)

    def indent_of(l):
        return len(l) - len(l.lstrip(" "))

    def build(cur_indent):
        nonlocal i
        first = lines[i]
        ordered = bool(re.match(r"^\s*\d+\.\s+", first))
        tag = "ol" if ordered else "ul"
        items = []
        while i < n:
            line = lines[i]
            if not line.strip():
                # allow single blank line inside list, then check continuation
                if i + 1 < n and re.match(r"^\s*([-*+]|\d+\.)\s+", lines[i + 1]) and indent_of(lines[i + 1]) >= cur_indent:
                    i += 1
                    continue
                break
            m = re.match(r"^(\s*)([-*+]|\d+\.)\s+(.*)$", line)
            if not m:
                # lazy continuation: an indented, non-marker line extends the current item
                if items:
                    items[-1] += " " + inline(line.strip())
                    i += 1
                    continue
                break
            ind = len(m.group(1))
            if ind < cur_indent:
                break
            if ind > cur_indent:
                # nested list belongs to previous item
                nested = build(ind)
                if items:
                    items[-1] += nested
                continue
            itxt = m.group(3)
            mt = re.match(r"^\[([ xX])\]\s+(.*)$", itxt)
            if mt:
                checked = "checked" if mt.group(1).lower() == "x" else ""
                items.append(f'<li class="task"><label><input type="checkbox" {checked}> '
                             + inline(mt.group(2)) + "</label>")
            else:
                items.append("<li>" + inline(itxt))
            i += 1
        return f"<{tag}>" + "".join(it + "</li>" for it in items) + f"</{tag}>"

    start_indent = indent_of(lines[i])
    result = build(start_indent)
    return result, i


# ==========================================================================
# Site navigation model
# ==========================================================================
def build_nav():
    """Ordered nav tree + flat page order (site-relative .html paths)."""
    nav = []
    order = []

    def add(label, url):
        order.append(url)
        return {"label": label, "url": url}

    # Home
    nav.append(add("Introduction", "index.html"))

    # Tracks (the 16 domains)
    manual = {"label": "Tracks", "url": None, "children": []}
    for section in SECTIONS:
        sid = section["id"]
        sec_node = {"label": section["title"], "url": f"manual/{sid}/README.html", "children": []}
        order.append(f"manual/{sid}/README.html")
        for slug, title, *_ in section["chapters"]:
            u = f"manual/{sid}/{slug}.html"
            sec_node["children"].append({"label": title, "url": u})
            order.append(u)
        manual["children"].append(sec_node)
    nav.append(manual)

    # Labs (hands-on campaign + boss labs)
    labs = {"label": "Labs", "url": "labs/README.html", "children": []}
    order.append("labs/README.html")
    for b in BOSS:
        u = f"labs/boss/{b['slug']}.html"
        labs["children"].append({"label": b["title"], "url": u})
        order.append(u)
    nav.append(labs)

    # Reference
    ref = {"label": "Reference", "url": "reference/README.html", "children": []}
    order.append("reference/README.html")
    tools_node = {"label": "Tools", "url": "reference/tools/README.html", "children": []}
    order.append("reference/tools/README.html")
    for slug, name, *_ in TOOLS:
        u = f"reference/tools/{slug}.html"
        tools_node["children"].append({"label": name, "url": u})
        order.append(u)
    ref["children"].append(tools_node)
    plat_node = {"label": "Learning Platforms", "url": "reference/platforms/README.html", "children": []}
    order.append("reference/platforms/README.html")
    for slug, name, *_ in PLATFORMS:
        u = f"reference/platforms/{slug}.html"
        plat_node["children"].append({"label": name, "url": u})
        order.append(u)
    ref["children"].append(plat_node)
    for label, u in [("Glossary", "reference/glossary.html"), ("ATT&CK Index", "reference/attack-index.html"),
                     ("CWE Index", "reference/cwe-index.html"), ("RFC Index", "reference/rfc-index.html")]:
        ref["children"].append({"label": label, "url": u})
        order.append(u)
    nav.append(ref)

    # Projects
    proj = {"label": "Projects", "url": "projects/README.html", "children": []}
    order.append("projects/README.html")
    for slug, title, *_ in PROJECTS:
        u = f"projects/{slug}.html"
        proj["children"].append({"label": title, "url": u})
        order.append(u)
    nav.append(proj)

    # Cheatsheets
    cheat = {"label": "Cheatsheets", "url": "cheatsheets/README.html", "children": []}
    order.append("cheatsheets/README.html")
    for slug, title, *_ in CHEATSHEETS:
        u = f"cheatsheets/{slug}.html"
        cheat["children"].append({"label": title, "url": u})
        order.append(u)
    nav.append(cheat)

    return nav, order


def build_search_index():
    idx = []

    def snip(abstract):
        return abstract

    idx.append({"t": "Introduction", "u": "index.html", "s": "Repository home and how to use it", "k": "Home"})
    idx.append({"t": "Labs — Hands-On Campaign", "u": "labs/README.html",
                "s": "Ordered hands-on labs by track plus cross-topic boss labs", "k": "Labs"})
    for b in BOSS:
        idx.append({"t": b["title"], "u": f"labs/boss/{b['slug']}.html", "s": b["scenario"], "k": "Boss Lab"})
    for section in SECTIONS:
        sid = section["id"]
        idx.append({"t": section["title"], "u": f"manual/{sid}/README.html", "s": section["desc"], "k": "Manual"})
        for slug, title, diff, hours, abstract in section["chapters"]:
            idx.append({"t": title, "u": f"manual/{sid}/{slug}.html", "s": abstract, "k": section["title"]})
    for slug, name, category, diff, hours, abstract in TOOLS:
        idx.append({"t": name, "u": f"reference/tools/{slug}.html", "s": abstract, "k": "Tool"})
    for slug, name, kind, abstract in PLATFORMS:
        idx.append({"t": name, "u": f"reference/platforms/{slug}.html", "s": abstract, "k": "Platform"})
    for slug, title, domain, diff, hours, abstract in PROJECTS:
        idx.append({"t": title, "u": f"projects/{slug}.html", "s": abstract, "k": "Project"})
    for slug, title, domain, abstract in CHEATSHEETS:
        idx.append({"t": title, "u": f"cheatsheets/{slug}.html", "s": abstract, "k": "Cheatsheet"})
    return idx


# ==========================================================================
# Page shell
# ==========================================================================
def rel_root(page_url):
    depth = page_url.count("/")
    return "../" * depth


def page_shell(page_url, title, content_html, toc, prev_url, next_url,
               prev_title="Previous", next_title="Next"):
    root = rel_root(page_url)
    toc_html = ""
    if toc:
        items = []
        for level, text, anchor in toc:
            cls = "toc-h3" if level == 3 else "toc-h2"
            items.append(f'<a class="{cls}" href="#{anchor}">{html.escape(text)}</a>')
        toc_html = '<nav class="toc"><div class="toc-title">On this page</div>' + "".join(items) + "</nav>"

    prev_html = (f'<a class="prev" href="{root}{prev_url}"><div class="dir">◀ Previous</div>'
                 f'<div class="ttl">{html.escape(prev_title)}</div></a>') if prev_url else "<span></span>"
    next_html = (f'<a class="next" href="{root}{next_url}"><div class="dir">Next ▶</div>'
                 f'<div class="ttl">{html.escape(next_title)}</div></a>') if next_url else "<span></span>"

    return f"""<!doctype html>
<!-- SPDX-License-Identifier: GPL-3.0-or-later | Copyright (C) 2026 Nithees Narendra S -->
<html lang="en" data-theme="dark">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{html.escape(title)} · Cybersecurity-Mastery</title>
<link rel="stylesheet" href="{root}assets/style.css">
</head>
<body data-root="{root}" data-page="{page_url}">
<header class="topbar">
  <button id="menu-toggle" aria-label="Toggle navigation">☰</button>
  <a class="brand" href="{root}index.html"><span class="logo"></span>Cybersecurity-Mastery</a>
  <div class="search-wrap">
    <input id="search" type="search" placeholder="Search ({len_index} pages)…" autocomplete="off">
    <div id="search-results"></div>
  </div>
  <button id="theme-toggle" aria-label="Toggle theme">◐</button>
</header>
<div class="layout">
  <aside id="sidebar" class="sidebar"><nav id="nav"></nav></aside>
  <main class="content">
    <article class="doc">
    {content_html}
    </article>
    <div class="pager">{prev_html}{next_html}</div>
    <footer class="foot">Cybersecurity-Mastery — interactive security learning · runs locally</footer>
  </main>
  {toc_html}
</div>
<script src="{root}assets/nav.js"></script>
<script src="{root}assets/search-index.js"></script>
<script src="{root}assets/mermaid.min.js" onerror="window.__noLocalMermaid=1"></script>
<script src="{root}assets/app.js"></script>
</body>
</html>
"""


len_index = 0  # filled in main for the placeholder


# ==========================================================================
# Assets
# ==========================================================================
CSS = r"""
/* ===== Cybersecurity-Mastery — interactive learning app · dark black/grey + terminal green ===== */
:root{
  --bg:#0a0a0a; --panel:#141414; --panel2:#1b1b1b; --panel3:#232323; --border:#2a2a2a; --text:#eaeaea;
  --muted:#9a9a9a; --accent:#39d353; --accent-hover:#2ea043; --accent-soft:rgba(57,211,83,.14);
  --code:#0e0e0e; --link:#7fe39a; --sidebar:#0e0e0e;
  --warn:#f5a623; --danger:#ef4444; --info:#8a8a8a;
  --mono:"SFMono-Regular",ui-monospace,Consolas,"Liberation Mono",monospace;
  --topbar-h:56px;
}
html[data-theme="light"]{
  --bg:#ffffff; --panel:#f7f8f7; --panel2:#eef1ee; --panel3:#e6eae6; --border:#dcdfdc; --text:#141a15;
  --muted:#5c635d; --accent:#1a7f37; --accent-hover:#166a2e; --accent-soft:rgba(26,127,55,.12);
  --code:#f2f4f2; --link:#166a2e; --sidebar:#f2f4f2; --warn:#b5730d; --danger:#c1362f; --info:#6b726c;
}
*{box-sizing:border-box}
html{scroll-behavior:smooth}
body{margin:0;background:var(--bg);color:var(--text);font:16px/1.7 -apple-system,BlinkMacSystemFont,"Segoe UI",Roboto,Helvetica,Arial,sans-serif}
a{color:var(--link);text-decoration:none}
a:hover{text-decoration:underline}
::selection{background:var(--accent-soft)}
::-webkit-scrollbar{width:10px;height:10px}
::-webkit-scrollbar-thumb{background:#333;border-radius:6px}
html[data-theme="light"] ::-webkit-scrollbar-thumb{background:#ccc}

/* Topbar */
.topbar{position:sticky;top:0;z-index:50;display:flex;align-items:center;gap:12px;padding:9px 16px;height:var(--topbar-h);
  background:linear-gradient(var(--panel),var(--panel));border-bottom:1px solid var(--border)}
.brand{font-weight:800;color:var(--text);white-space:nowrap;display:flex;align-items:center;letter-spacing:-.02em}
.brand .logo{display:inline-block;width:14px;height:14px;background:var(--accent);margin-right:9px;border-radius:3px;box-shadow:0 0 12px var(--accent-soft)}
.topbar button{background:transparent;border:1px solid var(--border);color:var(--text);border-radius:9px;padding:7px 11px;cursor:pointer;font-size:15px}
.topbar button:hover{border-color:var(--accent);color:var(--accent)}
#menu-toggle{display:none}
.search-wrap{position:relative;flex:1;max-width:620px;margin:0 auto}
#search{width:100%;padding:9px 14px;border-radius:10px;border:1px solid var(--border);background:var(--panel2);color:var(--text);font-size:14px}
#search:focus{outline:none;border-color:var(--accent);box-shadow:0 0 0 3px var(--accent-soft)}
#search-results{position:absolute;top:112%;left:0;right:0;background:var(--panel);border:1px solid var(--border);
  border-radius:12px;max-height:64vh;overflow:auto;display:none;box-shadow:0 24px 48px rgba(0,0,0,.5)}
#search-results a{display:block;padding:10px 13px;border-bottom:1px solid var(--border);color:var(--text)}
#search-results a:hover,#search-results a.active{background:var(--panel2);text-decoration:none}
#search-results .sr-t{font-weight:600}
#search-results .sr-k{font-size:11px;color:var(--accent);margin-left:8px;text-transform:uppercase;letter-spacing:.05em}
#search-results .sr-s{font-size:13px;color:var(--muted)}

/* Layout */
.layout{display:grid;grid-template-columns:290px minmax(0,1fr) 236px;gap:0;align-items:start}
.sidebar{position:sticky;top:var(--topbar-h);height:calc(100vh - var(--topbar-h));overflow:auto;background:var(--sidebar);
  border-right:1px solid var(--border);padding:14px 8px}
#nav details{margin:1px 0}
#nav summary{cursor:pointer;padding:7px 9px;border-radius:7px;font-weight:600;list-style:none;font-size:14px}
#nav summary::-webkit-details-marker{display:none}
#nav summary::before{content:"▸";color:var(--muted);margin-right:7px;font-size:11px;display:inline-block;transition:transform .15s}
#nav details[open]>summary::before{transform:rotate(90deg)}
#nav summary:hover{background:var(--panel2)}
#nav a{display:block;padding:6px 11px;border-radius:7px;color:var(--muted);font-size:13.5px}
#nav a:hover{background:var(--panel2);color:var(--text);text-decoration:none}
#nav a.active{background:var(--accent-soft);color:var(--accent);font-weight:600;box-shadow:inset 3px 0 0 var(--accent)}
#nav a.done::after{content:"✓";color:var(--accent);float:right;font-weight:700}
#nav .lvl2{margin-left:9px;border-left:1px solid var(--border);padding-left:5px}
#nav .lvl3{margin-left:9px;border-left:1px solid var(--border);padding-left:5px}

.content{min-width:0;padding:26px 44px 90px;max-width:940px}

/* Doc typography */
.doc h1{font-size:2.15rem;margin:.1em 0 .35em;line-height:1.15;letter-spacing:-.02em}
.doc h2{font-size:1.5rem;margin-top:2em;padding-bottom:.25em;border-bottom:2px solid var(--border);letter-spacing:-.01em}
.doc h2::before{content:"";display:inline-block;width:8px;height:20px;background:var(--accent);border-radius:2px;margin-right:11px;vertical-align:-3px}
.doc h3{font-size:1.2rem;margin-top:1.5em}
.doc h4{font-size:1.02rem;margin-top:1.2em;color:var(--accent)}
.doc p{margin:.7em 0}
.doc>p:first-of-type,.doc .lead{color:var(--muted)}
.doc code{background:var(--code);border:1px solid var(--border);padding:.1em .38em;border-radius:5px;font-family:var(--mono);font-size:.88em}
.doc pre{background:var(--code);border:1px solid var(--border);border-radius:11px;padding:14px 16px;overflow:auto;font-size:13.5px}
.doc pre code{background:transparent;border:none;padding:0}
.doc pre.mermaid{color:var(--muted);text-align:center;border-style:dashed}
.doc blockquote{margin:1em 0;padding:.7em 1.1em;border-left:4px solid var(--accent);background:var(--panel2);border-radius:0 10px 10px 0}
.doc table{border-collapse:collapse;width:100%;margin:1.1em 0;display:block;overflow-x:auto;font-size:14.5px}
.doc th,.doc td{border:1px solid var(--border);padding:9px 12px;text-align:left;vertical-align:top}
.doc th{background:var(--panel2);font-weight:600}
.doc tr:nth-child(even) td{background:var(--panel)}
.doc ul,.doc ol{padding-left:1.4em}
.doc li{margin:.32em 0}
li.task{list-style:none;margin-left:-1.15em}
li.task label{display:flex;gap:9px;align-items:flex-start;cursor:pointer}
li.task input{margin-top:5px;width:16px;height:16px;accent-color:var(--accent);flex:none}
.doc img,.doc svg{max-width:100%;height:auto}
.doc hr{border:none;border-top:1px solid var(--border);margin:2em 0}

/* Badges */
.badge{display:inline-block;padding:2px 10px;border-radius:999px;font-size:12px;font-weight:600;border:1px solid var(--border);background:var(--panel2);color:var(--muted)}
.badge.b-beginner{color:#39d353;border-color:rgba(57,211,83,.4)}
.badge.b-intermediate{color:#f5a623;border-color:rgba(245,166,35,.4)}
.badge.b-advanced{color:#ff8c42;border-color:rgba(255,140,66,.4)}
.badge.b-expert{color:#ef4444;border-color:rgba(239,68,68,.4)}
.meta-row{display:flex;flex-wrap:wrap;gap:8px;align-items:center;margin:.4em 0 1.1em}

/* Callouts */
.callout{border:1px solid var(--border);border-left-width:4px;border-radius:10px;padding:12px 15px;margin:1.1em 0;background:var(--panel2)}
.callout .ic{font-weight:700;margin-right:7px}
.callout.note{border-left-color:var(--info)}
.callout.tip{border-left-color:var(--accent);background:var(--accent-soft)}
.callout.warning{border-left-color:var(--warn)}
.callout.danger{border-left-color:var(--danger)}
.callout.example{border-left-color:var(--muted)}
.callout .ct{font-weight:700;text-transform:uppercase;font-size:12px;letter-spacing:.06em;margin-bottom:4px}
.callout.tip .ct{color:var(--accent)} .callout.warning .ct{color:var(--warn)} .callout.danger .ct{color:var(--danger)}

/* Cards */
.card{background:var(--panel);border:1px solid var(--border);border-radius:12px;padding:16px 18px;margin:1.1em 0}
.card>h4:first-child,.card>.card-title{margin-top:0;color:var(--accent);font-weight:700}
.grid-cards{display:grid;grid-template-columns:repeat(auto-fill,minmax(230px,1fr));gap:14px;margin:1.1em 0}
.grid-cards a.card{text-decoration:none;color:var(--text);transition:border-color .15s,transform .15s}
.grid-cards a.card:hover{border-color:var(--accent);transform:translateY(-2px)}

/* Code toolbar (copy/run) */
.codewrap{margin:1em 0;border:1px solid var(--border);border-radius:11px;overflow:hidden;background:var(--code)}
.code-tb{display:flex;align-items:center;justify-content:space-between;gap:8px;padding:6px 10px;background:var(--panel2);border-bottom:1px solid var(--border);font-size:12px;color:var(--muted)}
.code-tb .lang{font-family:var(--mono);text-transform:uppercase;letter-spacing:.05em}
.code-tb .btns{display:flex;gap:6px}
.btn{cursor:pointer;border:1px solid var(--border);background:var(--panel);color:var(--text);border-radius:7px;padding:4px 10px;font-size:12px;font-weight:600;display:inline-flex;align-items:center;gap:5px}
.btn:hover{border-color:var(--accent);color:var(--accent)}
.btn.run{background:var(--accent);color:#04140a;border-color:var(--accent)}
.btn.run:hover{background:var(--accent-hover);color:#04140a}
.btn.run:disabled{opacity:.5;cursor:not-allowed;background:var(--panel2);color:var(--muted);border-color:var(--border)}
.codewrap pre{border:none;border-radius:0;margin:0}
.run-out{border-top:1px dashed var(--border);background:#080808;color:#cfe;font-family:var(--mono);font-size:13px;padding:10px 14px;white-space:pre-wrap;max-height:340px;overflow:auto;display:none}
.run-out.show{display:block}
html[data-theme="light"] .run-out{background:#0e120e;color:#d7f5df}

/* Stepper */
.stepper{margin:1.2em 0}
.step{border:1px solid var(--border);border-radius:12px;margin:12px 0;background:var(--panel);overflow:hidden}
.step-head{display:flex;align-items:center;gap:12px;padding:12px 16px;background:var(--panel2);cursor:pointer}
.step-num{flex:none;width:28px;height:28px;border-radius:50%;background:var(--accent-soft);color:var(--accent);font-weight:800;display:grid;place-items:center;font-size:14px;border:1px solid var(--accent)}
.step.done .step-num{background:var(--accent);color:#04140a}
.step-goal{font-weight:600}
.step-body{padding:0 16px 14px}
.step-why{color:var(--muted);font-size:14.5px;margin-top:6px;border-left:3px solid var(--accent);padding-left:10px}

/* Tabs */
.tabs{margin:1.1em 0}
.tab-btns{display:flex;gap:4px;border-bottom:1px solid var(--border);flex-wrap:wrap}
.tab-btn{cursor:pointer;padding:8px 14px;border:none;background:transparent;color:var(--muted);font-weight:600;font-size:14px;border-bottom:2px solid transparent}
.tab-btn.active{color:var(--accent);border-bottom-color:var(--accent)}
.tab-panel{display:none;padding-top:12px}
.tab-panel.active{display:block}

/* Quiz */
.quiz{border:1px solid var(--border);border-radius:12px;padding:16px 18px;margin:1.1em 0;background:var(--panel)}
.quiz-q{font-weight:600;margin-bottom:10px}
.quiz-q::before{content:"Quiz  ";color:var(--accent);font-weight:800;font-size:12px;letter-spacing:.05em}
.quiz-opt{display:block;width:100%;text-align:left;cursor:pointer;border:1px solid var(--border);background:var(--panel2);color:var(--text);border-radius:9px;padding:10px 13px;margin:7px 0;font-size:14.5px}
.quiz-opt:hover{border-color:var(--accent)}
.quiz-opt.correct{border-color:var(--accent);background:var(--accent-soft);color:var(--accent);font-weight:600}
.quiz-opt.wrong{border-color:var(--danger);background:rgba(239,68,68,.12);color:var(--danger)}
.quiz-explain{margin-top:10px;padding:10px 13px;border-radius:9px;background:var(--panel2);border-left:3px solid var(--accent);font-size:14px;display:none}
.quiz-explain.show{display:block}

/* Terminal */
.terminal{border:1px solid var(--border);border-radius:12px;overflow:hidden;margin:1.1em 0;background:#050505}
.term-head{display:flex;align-items:center;gap:8px;padding:8px 12px;background:var(--panel2);border-bottom:1px solid var(--border);font-size:13px}
.term-dot{width:11px;height:11px;border-radius:50%}
.term-dot.r{background:#ff5f56}.term-dot.y{background:#ffbd2e}.term-dot.g{background:#27c93f}
.term-title{margin-left:6px;color:var(--muted);font-family:var(--mono);font-size:12px}
.term-status{margin-left:auto;font-size:11px;padding:2px 8px;border-radius:999px;border:1px solid var(--border);color:var(--muted)}
.term-status.up{color:var(--accent);border-color:var(--accent)}
.term-status.down{color:var(--warn);border-color:var(--warn)}
.term-body{height:300px;padding:8px 10px;font-family:var(--mono);font-size:13px;color:#d7f5df;overflow:auto;white-space:pre-wrap}
.term-input{display:flex;border-top:1px solid var(--border);background:#0a0a0a}
.term-input span{color:var(--accent);padding:8px 4px 8px 12px;font-family:var(--mono)}
.term-input input{flex:1;background:transparent;border:none;color:#d7f5df;font-family:var(--mono);font-size:13px;padding:8px 12px 8px 4px;outline:none}

/* Lab setup card */
.labcard{border:1px solid var(--border);border-left:4px solid var(--accent);border-radius:12px;padding:16px 18px;margin:1.2em 0;background:var(--panel)}
.labcard h4{margin:0 0 6px;color:var(--accent)}
.labcard .lab-actions{display:flex;gap:8px;flex-wrap:wrap;margin:10px 0}

/* Big pager */
.pager{display:grid;grid-template-columns:1fr 1fr;gap:14px;margin:2.4em 0 0}
.pager a{border:1px solid var(--border);border-radius:12px;padding:14px 18px;background:var(--panel);display:block;transition:border-color .15s}
.pager a:hover{border-color:var(--accent);text-decoration:none}
.pager .dir{font-size:12px;color:var(--muted);text-transform:uppercase;letter-spacing:.06em}
.pager .ttl{font-weight:700;color:var(--text);margin-top:3px}
.pager a.next{text-align:right}
.pager a.next .ttl{color:var(--accent)}

/* Progress */
.progress{height:9px;border-radius:999px;background:var(--panel2);overflow:hidden;border:1px solid var(--border)}
.progress>i{display:block;height:100%;background:var(--accent);width:0;transition:width .4s}
.track-progress{margin:1.1em 0;max-width:560px}
.lesson-check{display:inline-flex;align-items:center;gap:8px;cursor:pointer;border:1px solid var(--border);background:var(--panel);border-radius:9px;padding:7px 12px;font-weight:600;font-size:13.5px}
.lesson-check.done{border-color:var(--accent);color:var(--accent);background:var(--accent-soft)}

/* Details */
.doc details{background:var(--panel2);border:1px solid var(--border);border-radius:10px;padding:9px 14px;margin:.6em 0}
.doc summary{cursor:pointer;font-weight:600}
.doc summary:hover{color:var(--accent)}

.foot{margin-top:44px;color:var(--muted);font-size:13px;border-top:1px solid var(--border);padding-top:16px}
.toc{position:sticky;top:var(--topbar-h);height:calc(100vh - var(--topbar-h));overflow:auto;padding:22px 14px;font-size:13px}
.toc-title{color:var(--muted);text-transform:uppercase;font-size:11px;letter-spacing:.08em;margin-bottom:8px}
.toc a{display:block;color:var(--muted);padding:3px 0;border-left:2px solid transparent;padding-left:10px}
.toc a:hover,.toc a.active{color:var(--accent);border-left-color:var(--accent)}
.toc .toc-h3{padding-left:22px;font-size:12px}
.breadcrumb{color:var(--muted);font-size:13px;margin-bottom:8px}
@media(max-width:1120px){.layout{grid-template-columns:270px minmax(0,1fr)}.toc{display:none}}
@media(max-width:820px){
  .layout{grid-template-columns:1fr}
  #menu-toggle{display:inline-block}
  .sidebar{position:fixed;left:0;top:var(--topbar-h);z-index:40;width:84%;max-width:330px;transform:translateX(-100%);transition:transform .2s}
  .sidebar.open{transform:none}
  .content{padding:20px 18px 70px}
  .pager{grid-template-columns:1fr}
}
"""

APP_JS = r"""
(function(){
  var root = document.body.dataset.root || "";
  var page = document.body.dataset.page || "";

  // Theme
  var saved = localStorage.getItem("cm-theme");
  if(saved){ document.documentElement.dataset.theme = saved; }
  document.getElementById("theme-toggle").addEventListener("click", function(){
    var cur = document.documentElement.dataset.theme === "dark" ? "light" : "dark";
    document.documentElement.dataset.theme = cur; localStorage.setItem("cm-theme", cur);
    runMermaid(true);
  });

  // Sidebar nav from NAV
  function el(tag, cls, txt){var e=document.createElement(tag); if(cls)e.className=cls; if(txt)e.textContent=txt; return e;}
  function link(node){
    var a=el("a", null, node.label); a.href=root+node.url;
    if(node.url===page) a.className="active";
    return a;
  }
  function renderNode(node, container, level){
    if(node.children && node.children.length){
      var d=el("details");
      // open the branch that contains the current page
      if(containsPage(node)) d.open=true;
      var s=el("summary", null, node.label); d.appendChild(s);
      var wrap=el("div", "lvl"+level);
      node.children.forEach(function(c){ renderNode(c, wrap, level+1); });
      d.appendChild(wrap); container.appendChild(d);
      if(node.url){ /* section landing reachable via summary click? add a link */
        s.addEventListener("dblclick", function(){location.href=root+node.url;});
      }
    } else {
      container.appendChild(link(node));
    }
  }
  function containsPage(node){
    if(node.url===page) return true;
    if(node.children) return node.children.some(containsPage);
    return false;
  }
  var nav=document.getElementById("nav");
  (window.NAV||[]).forEach(function(n){ renderNode(n, nav, 2); });

  // Menu toggle (mobile)
  var mt=document.getElementById("menu-toggle");
  if(mt){ mt.addEventListener("click", function(){ document.getElementById("sidebar").classList.toggle("open"); }); }

  // Search
  var box=document.getElementById("search"), res=document.getElementById("search-results");
  var SEARCH=window.SEARCH||[];
  function doSearch(q){
    q=q.trim().toLowerCase();
    if(!q){res.style.display="none";res.innerHTML="";return;}
    var terms=q.split(/\s+/);
    var scored=[];
    SEARCH.forEach(function(item){
      var hay=(item.t+" "+item.s+" "+item.k).toLowerCase();
      var ok=terms.every(function(t){return hay.indexOf(t)>=0;});
      if(ok){
        var score=0; if(item.t.toLowerCase().indexOf(q)>=0)score+=10;
        terms.forEach(function(t){ if(item.t.toLowerCase().indexOf(t)>=0)score+=3; });
        scored.push([score,item]);
      }
    });
    scored.sort(function(a,b){return b[0]-a[0];});
    res.innerHTML="";
    scored.slice(0,40).forEach(function(p){
      var it=p[1]; var a=document.createElement("a"); a.href=root+it.u;
      a.innerHTML='<span class="sr-t">'+esc(it.t)+'</span><span class="sr-k">'+esc(it.k)+'</span><div class="sr-s">'+esc(it.s)+'</div>';
      res.appendChild(a);
    });
    res.style.display=scored.length?"block":"none";
  }
  function esc(s){return (s||"").replace(/[&<>"]/g,function(c){return{"&":"&amp;","<":"&lt;",">":"&gt;",'"':"&quot;"}[c];});}
  if(box){
    box.addEventListener("input", function(){doSearch(box.value);});
    box.addEventListener("keydown", function(e){
      if(e.key==="Enter"){var first=res.querySelector("a"); if(first)location.href=first.href;}
      if(e.key==="Escape"){res.style.display="none";}
    });
    document.addEventListener("click", function(e){ if(!e.target.closest(".search-wrap")) res.style.display="none"; });
  }

  // Mermaid
  function runMermaid(rerun){
    if(window.mermaid){
      try{
        var dark = document.documentElement.dataset.theme==="dark";
        window.mermaid.initialize({startOnLoad:false, securityLevel:"loose", theme:"base",
          themeVariables: dark ? {
            background:"#0a0a0a", primaryColor:"#1c1c1c", primaryTextColor:"#e8e8e8",
            primaryBorderColor:"#3a3a3a", lineColor:"#9b9b9b", secondaryColor:"#141414",
            tertiaryColor:"#0f0f0f", clusterBkg:"#121212", clusterBorder:"#2b2b2b",
            fontFamily:"ui-sans-serif,system-ui,sans-serif"
          } : {
            background:"#ffffff", primaryColor:"#efefef", primaryTextColor:"#141414",
            primaryBorderColor:"#bdbdbd", lineColor:"#5c5c5c", secondaryColor:"#f5f5f5",
            tertiaryColor:"#fafafa", clusterBkg:"#f5f5f5", clusterBorder:"#dcdcdc",
            fontFamily:"ui-sans-serif,system-ui,sans-serif"
          }});
        var nodes=document.querySelectorAll("pre.mermaid");
        if(rerun){ nodes.forEach(function(n){ if(n.dataset.processed){ n.removeAttribute("data-processed"); n.innerHTML=n.getAttribute("data-src")||n.textContent; } }); }
        nodes.forEach(function(n){ if(!n.getAttribute("data-src")) n.setAttribute("data-src", n.textContent); });
        window.mermaid.run({querySelector:"pre.mermaid"});
      }catch(e){}
    }
  }
  function ensureMermaid(){
    if(window.mermaid){ runMermaid(false); return; }
    if(navigator.onLine){
      var s=document.createElement("script");
      s.src="https://cdn.jsdelivr.net/npm/mermaid@11/dist/mermaid.min.js";
      s.onload=function(){ runMermaid(false); };
      document.head.appendChild(s);
    }
    // else: offline and no local mermaid -> diagram source stays visible (graceful)
  }
  ensureMermaid();

  // ===================== interactive learning app =====================
  var LAB = { url: (localStorage.getItem("cm-lab-url")||"http://127.0.0.1:8777"),
              token: (localStorage.getItem("cm-lab-token")||""), up:false };

  // ---- copy buttons ----
  document.addEventListener("click", function(e){
    var c=e.target.closest("[data-copy]"); if(!c) return;
    var el=document.getElementById(c.getAttribute("data-copy")); if(!el) return;
    var txt=el.innerText;
    navigator.clipboard && navigator.clipboard.writeText(txt);
    var old=c.textContent; c.textContent="✓ Copied"; setTimeout(function(){c.textContent=old;},1200);
  });

  // ---- tabs ----
  document.querySelectorAll(".tabs").forEach(function(t){
    var btns=t.querySelectorAll(".tab-btn"), panels=t.querySelectorAll(".tab-panel");
    btns.forEach(function(b,idx){ b.addEventListener("click",function(){
      btns.forEach(function(x){x.classList.remove("active");}); panels.forEach(function(x){x.classList.remove("active");});
      b.classList.add("active"); if(panels[idx]) panels[idx].classList.add("active");
    });});
  });

  // ---- quiz ----
  document.addEventListener("click", function(e){
    var o=e.target.closest(".quiz-opt"); if(!o) return;
    var quiz=document.getElementById(o.getAttribute("data-q")); if(!quiz) return;
    if(quiz.dataset.answered) return;
    quiz.dataset.answered="1";
    var correct=o.getAttribute("data-correct")==="1";
    o.classList.add(correct?"correct":"wrong");
    if(!correct){ quiz.querySelectorAll(".quiz-opt").forEach(function(x){ if(x.getAttribute("data-correct")==="1") x.classList.add("correct"); }); }
    var ex=document.getElementById(o.getAttribute("data-q")+"-ex"); if(ex) ex.classList.add("show");
  });

  // ---- stepper: click head toggles done ----
  document.querySelectorAll(".step-head").forEach(function(h){
    h.addEventListener("click", function(){ h.parentElement.classList.toggle("done"); });
  });

  // ---- lesson progress (localStorage) ----
  function progKey(){ return "cm-done"; }
  function getDone(){ try{ return JSON.parse(localStorage.getItem(progKey())||"{}"); }catch(e){ return {}; } }
  function setDone(map){ localStorage.setItem(progKey(), JSON.stringify(map)); }
  // mark nav links done
  (function markNav(){ var done=getDone(); document.querySelectorAll("#nav a").forEach(function(a){
    var u=a.getAttribute("href")||""; var key=u.split("/").slice(-2).join("/");
    if(done[key]) a.classList.add("done");
  }); })();
  // per-lesson complete button
  var lc=document.getElementById("lesson-complete");
  if(lc){
    var key=page.split("/").slice(-2).join("/");
    var done=getDone(); if(done[key]) lc.classList.add("done"), lc.querySelector(".lbl") && (lc.querySelector(".lbl").textContent="Completed ✓");
    lc.addEventListener("click", function(){
      var d=getDone(); if(d[key]){ delete d[key]; lc.classList.remove("done"); if(lc.querySelector(".lbl")) lc.querySelector(".lbl").textContent="Mark complete"; }
      else { d[key]=1; lc.classList.add("done"); if(lc.querySelector(".lbl")) lc.querySelector(".lbl").textContent="Completed ✓"; }
      setDone(d);
    });
  }
  // track progress bars (on track landing pages)
  document.querySelectorAll("[data-track-progress]").forEach(function(bar){
    var lessons=(bar.getAttribute("data-lessons")||"").split(",").filter(Boolean);
    var done=getDone(), n=0; lessons.forEach(function(k){ if(done[k]) n++; });
    var pct=lessons.length?Math.round(100*n/lessons.length):0;
    var i=bar.querySelector("i"); if(i) i.style.width=pct+"%";
    var lbl=bar.parentElement.querySelector(".tp-label"); if(lbl) lbl.textContent=n+" / "+lessons.length+" lessons ("+pct+"%)";
  });

  // ---- lab runner backend ----
  function labHeaders(){ return LAB.token?{"X-Lab-Token":LAB.token,"Content-Type":"application/json"}:{"Content-Type":"application/json"}; }
  function setTermStatus(up, msg){
    document.querySelectorAll(".term-status").forEach(function(s){
      s.className="term-status "+(up?"up":"down"); s.textContent=up?"live":"offline";
    });
    document.querySelectorAll(".term-input input").forEach(function(inp){ inp.disabled=!up;
      if(up) inp.placeholder="type a command and press Enter"; });
    document.querySelectorAll(".btn.run").forEach(function(b){ b.title = up?"Run in the lab terminal":"Start the lab runner to run live"; });
  }
  function pingLab(){
    fetch(LAB.url+"/health",{headers:labHeaders()}).then(function(r){return r.json();}).then(function(j){
      LAB.up=true; setTermStatus(true); if(j&&j.container) document.querySelectorAll(".term-title").forEach(function(t){ t.textContent=j.container+" — live"; });
    }).catch(function(){ LAB.up=false; setTermStatus(false); });
  }
  function termWrite(sel, txt){ var b=(typeof sel==="string")?document.querySelector(sel):sel; if(b){ b.textContent+=txt; b.scrollTop=b.scrollHeight; } }
  function runCmd(cmd, outEl){
    if(!LAB.up){ if(outEl){ outEl.classList.add("show"); outEl.textContent="⚠ Lab runner not detected at "+LAB.url+".\nStart it (see labserver/README) or copy the command and run it in your Kali terminal."; } return; }
    if(outEl){ outEl.classList.add("show"); outEl.textContent="$ "+cmd+"\n"; }
    fetch(LAB.url+"/run",{method:"POST",headers:labHeaders(),body:JSON.stringify({cmd:cmd})})
      .then(function(r){ return r.text(); })
      .then(function(t){ if(outEl){ outEl.textContent+=t; outEl.scrollTop=outEl.scrollHeight; } })
      .catch(function(err){ if(outEl){ outEl.textContent+="\n[error] "+err; } });
  }
  // run buttons
  document.addEventListener("click", function(e){
    var r=e.target.closest("[data-run]"); if(r){ var id=r.getAttribute("data-run");
      var code=document.getElementById(id); var out=document.getElementById(id+"-out");
      if(code) runCmd(code.innerText.trim(), out); return; }
    var up=e.target.closest("[data-lab-up]"); if(up){ var sec=up.getAttribute("data-lab-up");
      if(!LAB.up){ alert("Start the lab runner first (labserver/). See the repo README."); return; }
      fetch(LAB.url+"/lab/up",{method:"POST",headers:labHeaders(),body:JSON.stringify({section:sec})})
        .then(function(r){return r.text();}).then(function(t){ up.textContent="✓ Lab starting"; setTimeout(function(){up.textContent="▸ Start lab";},2000); })
        .catch(function(){ alert("Could not reach the lab runner."); }); return; }
    var dn=e.target.closest("[data-lab-down]"); if(dn){ var sec2=dn.getAttribute("data-lab-down");
      if(!LAB.up) return;
      fetch(LAB.url+"/lab/down",{method:"POST",headers:labHeaders(),body:JSON.stringify({section:sec2})})
        .then(function(r){return r.text();}).then(function(){ dn.textContent="✓ Stopped"; setTimeout(function(){dn.textContent="■ Stop lab";},2000); }); return; }
  });
  // interactive terminal input
  document.querySelectorAll(".term-input input").forEach(function(inp){
    inp.addEventListener("keydown", function(e){
      if(e.key!=="Enter"||!LAB.up) return;
      var cmd=inp.value; inp.value="";
      var body=inp.closest(".terminal").querySelector(".term-body");
      termWrite(body, "$ "+cmd+"\n");
      fetch(LAB.url+"/run",{method:"POST",headers:labHeaders(),body:JSON.stringify({cmd:cmd})})
        .then(function(r){return r.text();}).then(function(t){ termWrite(body, t+"\n"); })
        .catch(function(err){ termWrite(body, "[error] "+err+"\n"); });
    });
  });
  // connect button: capture URL + token, persist, re-ping
  document.addEventListener("click", function(e){
    if(!e.target.closest(".term-connect")) return;
    var url=prompt("Lab Runner URL:", LAB.url||"http://127.0.0.1:8777"); if(url===null) return;
    var tok=prompt("Session token (printed when you started labserver/server.py):", LAB.token||""); if(tok===null) return;
    LAB.url=url.trim().replace(/\/$/,""); LAB.token=tok.trim();
    localStorage.setItem("cm-lab-url",LAB.url); localStorage.setItem("cm-lab-token",LAB.token);
    pingLab();
  });
  if(document.querySelector(".term-input, [data-run], [data-lab-up]")) { pingLab(); setInterval(pingLab, 15000); }

  // ---- active TOC on scroll ----
  var tocLinks=document.querySelectorAll(".toc a");
  if(tocLinks.length){
    var heads=[].map.call(tocLinks,function(a){ return document.getElementById((a.getAttribute("href")||"").slice(1)); });
    window.addEventListener("scroll", function(){
      var y=window.scrollY+90, idx=0;
      heads.forEach(function(h,k){ if(h&&h.offsetTop<=y) idx=k; });
      tocLinks.forEach(function(a){a.classList.remove("active");});
      if(tocLinks[idx]) tocLinks[idx].classList.add("active");
    }, {passive:true});
  }
})();
"""


def write(path, content, binary=False):
    full = os.path.join(SITE, path)
    os.makedirs(os.path.dirname(full), exist_ok=True)
    mode = "wb" if binary else "w"
    with open(full, mode, **({} if binary else {"encoding": "utf-8", "newline": "\n"})) as f:
        f.write(content)


def main():
    global len_index
    nav, order = build_nav()
    search = build_search_index()
    len_index = len(search)

    # position lookup for prev/next + titles
    pos = {u: idx for idx, u in enumerate(order)}
    title_by_url = {it["u"]: it["t"] for it in search}

    # gather all .md files (skip _meta, site, _suggestions kept)
    md_files = []
    for dirpath, dirs, files in os.walk(ROOT):
        rel = os.path.relpath(dirpath, ROOT)
        if rel.split(os.sep)[0] in ("_meta", "site"):
            continue
        for fn in files:
            if fn.endswith(".md"):
                md_files.append(os.path.relpath(os.path.join(dirpath, fn), ROOT))

    rendered = 0
    for mdrel in md_files:
        with open(os.path.join(ROOT, mdrel), encoding="utf-8") as f:
            md = f.read()
        htmlrel = mdrel.replace(os.sep, "/")
        htmlrel = htmlrel[:-3] + ".html"
        toc = []
        body = md_to_html(md, headings_out=toc)
        # title from first h1
        m = re.search(r"<h1[^>]*>(.*?)</h1>", body, re.S)
        title = re.sub("<.*?>", "", m.group(1)) if m else os.path.basename(mdrel)
        prev_url = order[pos[htmlrel] - 1] if htmlrel in pos and pos[htmlrel] > 0 else None
        next_url = order[pos[htmlrel] + 1] if htmlrel in pos and pos[htmlrel] + 1 < len(order) else None
        page = page_shell(htmlrel, title, body, toc, prev_url, next_url,
                          title_by_url.get(prev_url, "Previous"), title_by_url.get(next_url, "Next"))
        write(htmlrel, page)
        rendered += 1

    # index.html from README.md
    readme_path = os.path.join(ROOT, "README.md")
    if os.path.exists(readme_path):
        with open(readme_path, encoding="utf-8") as f:
            md = f.read()
        toc = []
        body = md_to_html(md, headings_out=toc)
        nxt = order[1] if len(order) > 1 else None
        page = page_shell("index.html", "Home", body, toc, None, nxt,
                          "Previous", title_by_url.get(nxt, "Next"))
        write("index.html", page)

    # assets
    write("assets/style.css", CSS)
    write("assets/app.js", APP_JS)
    write("assets/nav.js", "window.NAV=" + json.dumps(nav, ensure_ascii=False) + ";")
    write("assets/search-index.js", "window.SEARCH=" + json.dumps(search, ensure_ascii=False) + ";")
    # placeholder so the local mermaid <script> 404 is silent-ish and offline degrades gracefully
    write("assets/mermaid.min.js", "/* Optional: drop the real mermaid.min.js here for offline diagram rendering. */\n")
    # small readme for the site dir
    write("README-SITE.md", "# Offline site\n\nOpen `index.html` in a browser. No server needed.\n"
                            "For offline Mermaid diagrams, place a real `mermaid.min.js` in `assets/`.\n")

    print(f"Site built: {rendered} pages + index.html at {SITE}")
    print("Open site/index.html in a browser (no server required).")


if __name__ == "__main__":
    main()
