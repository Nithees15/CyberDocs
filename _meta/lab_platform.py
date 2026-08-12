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

"""Lab platform integration — the SINGLE point where the docs bind to a lab
environment. Every "Hands-on Lab" section in the repository is rendered here.

Model
-----
* Attacker  : the reader's Kali Linux (``kali-linux-everything`` — all tools present).
* Targets   : hosted by **CyberForge** (local-first lab platform) as isolated
              containers, or a plain ``docker run`` / ``docker compose`` target,
              or one of the reader's ready-made vulnerable apps (bWAPP, DVWA,
              OWASP Juice Shop, Metasploitable).

CyberForge is used only where a hosted/vulnerable target is genuinely needed.
Pure-theory chapters render a lighter "concept lab" instead.

To retarget every lab in the repo (different platform, different defaults),
edit THIS FILE only and re-run ``generate.py`` — no content file changes.
"""

from __future__ import annotations

import json

try:
    import partlabs
except Exception:  # pragma: no cover
    partlabs = None
try:
    import labdata
except Exception:  # pragma: no cover
    labdata = None

CYBERFORGE = {
    "name": "CyberForge",
    "web_ui": "http://localhost:3000",
    "api": "http://localhost:8000",
    "api_docs": "http://localhost:8000/docs",
    "default_admin": "admin",
    "repo_hint": "<path-to>/CyberForge",   # your local CyberForge checkout
}

# Ready-made vulnerable targets the reader already has locally.
KNOWN_TARGETS = {
    "bwapp":         ("raesene/bwapp",                    80,   "bWAPP — 100+ web bugs, classic teaching target"),
    "dvwa":          ("vulnerables/web-dvwa",             80,   "Damn Vulnerable Web Application"),
    "juice-shop":    ("bkimminich/juice-shop",            3000, "OWASP Juice Shop — modern SPA, full Top 10"),
    "metasploitable":("tleemcjr/metasploitable2",         0,    "Metasploitable 2 — vulnerable Linux services"),
    "webgoat":       ("webgoat/webgoat",                  8080, "OWASP WebGoat — guided lessons"),
}


def _safe(tag: str) -> str:
    return "".join(c if (c.isalnum() or c in "-_") else "-" for c in tag).strip("-").lower()


def topology_diagram(target_service: str = "target", internal: bool = True,
                     extra_services=None) -> str:
    """Mermaid network topology for the lab."""
    extra_services = extra_services or []
    net = "labnet (internal — no route to host/internet)" if internal else "labnet (routed)"
    lines = ["```mermaid", "flowchart LR"]
    lines.append('    K["Kali attacker<br/>kali-linux-everything"]')
    lines.append(f'    subgraph CF["CyberForge lab — {net}"]')
    lines.append(f'      T["{target_service}<br/>vulnerable service"]')
    for i, s in enumerate(extra_services):
        lines.append(f'      X{i}["{s}"]')
    lines.append("    end")
    lines.append("    K -->|attack traffic| T")
    for i, _ in enumerate(extra_services):
        lines.append(f"    T --- X{i}")
    lines.append("```")
    return "\n".join(lines)


def _template_spec(lab_name: str, category: str, difficulty: str,
                   service_name: str, image: str, command, port,
                   env: dict, internal: bool, tags) -> str:
    """A CyberForge lab-template ``spec`` (JSON), matching the platform schema."""
    import json
    service = {
        "name": service_name,
        "description": f"Vulnerable target for the {lab_name} lab.",
        "image": image,
        "networks": ["labnet"],
        "memory_limit_mb": 256,
        "position": 0,
        "is_entrypoint": True,
    }
    if command:
        service["command"] = command
    if port:
        # routed network required for a host port to work
        service["ports"] = [{"container": port, "host": 18080 + (port % 1000)}]
    if env:
        service["environment"] = env
    spec = {
        "name": lab_name,
        "description": f"Isolated target environment for the '{lab_name}' hands-on lab.",
        "category": category,
        "difficulty": difficulty,
        "memory_limit_mb": 512,
        "auto_sleep_minutes": 30,
        "tags": list(tags),
        "networks": [
            {"name": "labnet", "internal": internal,
             "note": "internal=true keeps the target unreachable from host/internet (fail-closed default)."}
        ],
        "services": [service],
    }
    return "```json\n" + json.dumps(spec, indent=2) + "\n```"


def render_lab(*, lab_no: int, chapter_title: str, category: str, difficulty: str,
               objective: str, target: dict, attacker_tools, steps, expected,
               detection=None, cleanup_extra=None, study_minutes: int = 45) -> str:
    """Render a full CyberForge-hosted hands-on lab section (Markdown).

    ``target`` keys: kind (cyberforge|prebuilt|compose|kali), image, service_name,
    port, command, env, internal, notes.
    """
    kind = target.get("kind", "cyberforge")
    service_name = target.get("service_name", "target")
    image = target.get("image", "alpine:3.20")
    port = target.get("port", 0)
    command = target.get("command")
    env = target.get("env", {})
    internal = target.get("internal", True)
    notes = target.get("notes", "")
    lab_slug = _safe(f"{chapter_title}-lab")

    out = []
    out.append(f"### Lab {lab_no}: {chapter_title} — hands-on\n")
    out.append(f"> **Difficulty:** {difficulty.title()} · **Time:** ~{study_minutes} min · "
               f"**Platform:** CyberForge (target) + Kali (attacker) · **Cost:** free, fully local\n")
    out.append(f"**Objective.** {objective}\n")

    out.append("**Topology**\n")
    out.append(topology_diagram(service_name, internal=internal))
    out.append("")

    out.append("**Prerequisites**\n")
    out.append("- CyberForge running locally (`docker compose up -d` in the CyberForge repo); "
               f"web UI at [{CYBERFORGE['web_ui']}]({CYBERFORGE['web_ui']}), API at `{CYBERFORGE['api']}`.")
    out.append("- Kali Linux with the standard toolset on the same Docker host or a routed lab network.")
    out.append("- You are attacking **only** this local, isolated target. Never point these techniques at a "
               "system you do not own or lack written authorisation to test.\n")

    # --- Part A: provision the target ---
    out.append("#### A. Provision the target\n")
    if kind == "prebuilt":
        tname = notes or "prebuilt vulnerable app"
        out.append(f"This lab uses a ready-made vulnerable target ({tname}). Host it under CyberForge as a "
                   "service, or run it directly with Docker.\n")
        out.append("**Option 1 — as a CyberForge service (recommended: isolation + lifecycle):** create a lab, "
                   "add a service with the settings below, put it on an `internal` network for a jeopardy-style "
                   "target or a routed network if you need host access, then **Start**.\n")
        out.append(_template_spec(f"{chapter_title} Lab", category, difficulty, service_name,
                                  image, command, port, env, internal, [category, "vulnerable-app"]))
        out.append("")
        out.append("**Option 2 — plain Docker (quick):**\n")
        hostport = 18080 + (port % 1000) if port else 8080
        run = f"docker run -d --name {service_name} "
        if port:
            run += f"-p {hostport}:{port} "
        for k, v in env.items():
            run += f'-e {k}="{v}" '
        run += image
        out.append("```bash\n" + run + "\n```")
        if port:
            out.append(f"\nTarget URL from Kali: `http://<docker-host>:{hostport}/`\n")
    elif kind == "compose":
        out.append("Provision the multi-container target with the compose file below (drop it in an empty "
                   "directory and `docker compose up -d`). Keep it on an isolated bridge network.\n")
        out.append(target.get("compose", "```yaml\n# see chapter body\n```"))
        out.append("")
    elif kind == "kali":
        out.append("No hosted target is required — this lab runs entirely from Kali against local files, a "
                   "loopback service you start, or generated data. Follow the steps below.\n")
    else:  # cyberforge (custom challenge image)
        out.append("Provision the target as a CyberForge lab. Create a new lab, add the service below, keep it "
                   "on an **internal** network (fail-closed default), then **Start**. Sleeping the lab later "
                   "frees CPU while preserving state.\n")
        out.append(_template_spec(f"{chapter_title} Lab", category, difficulty, service_name,
                                  image, command, port, env, internal, [category, "hands-on"]))
        out.append("")
        out.append("**Automating provisioning via the API** (token from `POST /api/v1/auth/login`):\n")
        out.append("```bash\n"
                   f'TOKEN=$(curl -s {CYBERFORGE["api"]}/api/v1/auth/login \\\n'
                   '  -H "Content-Type: application/json" \\\n'
                   '  -d \'{"identifier":"admin","password":"<your-password>"}\' | jq -r .access_token)\n'
                   f'curl -s {CYBERFORGE["api"]}/api/v1/labs -H "Authorization: Bearer $TOKEN" \\\n'
                   '  -H "Content-Type: application/json" -d @lab.json   # lab.json = the spec above\n'
                   "```")
        out.append("")

    # --- Part B: attack ---
    out.append("#### B. Work the target from Kali\n")
    if attacker_tools:
        out.append("Primary tooling: " + ", ".join(f"`{t}`" for t in attacker_tools) + ".\n")
    for i, step in enumerate(steps, 1):
        out.append(f"{i}. {step}")
    out.append("")

    # --- Expected results ---
    out.append("#### Expected results\n")
    for e in expected:
        out.append(f"- {e}")
    out.append("")

    # --- Blue-team observation ---
    if detection:
        out.append("#### Observe it from the defender's side\n")
        out.append("Run the same activity while watching telemetry — attack and detection are two views of one "
                   "event:\n")
        for d in detection:
            out.append(f"- {d}")
        out.append("")

    # --- Snapshots / cleanup ---
    out.append("#### Snapshots and cleanup\n")
    out.append("- **Snapshot** the lab before making changes so you can restore the known-good definition "
               "(CyberForge takes an automatic safety snapshot first; note that volume *data* is not captured).")
    out.append("- **Sleep** the lab between sessions to free CPU while keeping state; **Stop** to free memory; "
               "**Archive** when finished to release everything and make it read-only.")
    if cleanup_extra:
        for c in cleanup_extra:
            out.append(f"- {c}")
    if kind == "prebuilt" or kind == "compose":
        out.append(f"- Plain-Docker teardown: `docker rm -f {service_name}` "
                   "(or `docker compose down -v` for the compose target).")
    out.append("")

    # --- Troubleshooting ---
    out.append("#### Troubleshooting\n")
    out.append("| Symptom | Likely cause | Fix |")
    out.append("| --- | --- | --- |")
    out.append("| Lab says `running` but nothing answers on the port | Service bound to `127.0.0.1`, or a host "
               "port was mapped on an **internal** network | Bind to `0.0.0.0`; move the service to a routed "
               "network (`internal: false`) for host access |")
    out.append("| Container crash-loops immediately | Stale `command` overriding the image `CMD`, or a dropped "
               "capability the process needs | Clear the service `command`; add the *specific* capability rather "
               "than `privileged` |")
    out.append("| Port refused / connection reset | Target still starting, or wrong host port | `docker logs "
               f"{service_name}`; confirm the published host port |")
    out.append("| Kali cannot reach the target by name | Attacker not on the same lab network | Attach Kali to "
               "`labnet`, or use the published host port instead of the service name |")
    out.append("")
    out.append("> **Safety.** Every lab in this repository is designed to run against local, isolated targets "
               "only. Keeping the target on an `internal` CyberForge network guarantees it cannot reach the "
               "internet or the host — the platform fails closed by design.\n")
    return "\n".join(out)


def render_concept_lab(*, lab_no: int, chapter_title: str, objective: str,
                       steps, expected, study_minutes: int = 25) -> str:
    """A lighter lab for theory chapters: no hosted target, Kali/local only."""
    out = []
    out.append(f"### Lab {lab_no}: {chapter_title} — guided exercise\n")
    out.append(f"> **Time:** ~{study_minutes} min · **Platform:** Kali / local · **Cost:** free\n")
    out.append(f"**Objective.** {objective}\n")
    out.append("**Steps**\n")
    for i, step in enumerate(steps, 1):
        out.append(f"{i}. {step}")
    out.append("\n**Expected results**\n")
    for e in expected:
        out.append(f"- {e}")
    out.append("")
    return "\n".join(out)


# ==========================================================================
# NEW hands-on-first renderers (part environment, in-page practice, boss labs)
# ==========================================================================
def _codeblock(text, lang=""):
    return f"```{lang}\n{text}\n```"


def render_part_environment(section_id, section_title):
    """The 'set up once for this part' lab environment, for a section README."""
    spec = partlabs.env_for(section_id) if partlabs else None
    out = []
    out.append("## Lab Environment\n")
    out.append(f"_Set up once, then use it for every chapter in the **{section_title}** part. "
               "Everything runs locally and isolated — you never touch a system you don't own._\n")
    if not spec:
        out.append("Work from Kali and the tools named in each chapter; no dedicated targets are required.\n")
        return "\n".join(out)

    out.append(spec["intro"] + "\n")
    out.append("**What you get**\n")
    out.append("| Target | How to reach it |")
    out.append("| --- | --- |")
    for name, note in spec["targets"]:
        out.append(f"| `{name}` | {note} |")
    out.append("")
    out.append("**Provision it** — save this as `docker-compose.yml` and run `docker compose up -d` "
               "(or import the equivalent spec into CyberForge):\n")
    out.append(_codeblock(spec["compose"].strip(), "yaml"))
    out.append("")
    out.append("**Attacker box.** " + spec["attacker"] + "\n")
    if spec.get("verify"):
        out.append("**Verify it works**\n")
        for v in spec["verify"]:
            out.append(f"- {v}")
        out.append("")
    if spec.get("notes"):
        out.append("**Notes**\n")
        for n in spec["notes"]:
            out.append(f"- {n}")
        out.append("")
    out.append("**Teardown.** `docker compose down` stops it; add `-v` to also drop volumes. "
               "Snapshot before big changes so you can revert.\n")
    out.append("> **Safety.** Keep intentionally-vulnerable targets on an isolated/`internal` network. "
               "Never expose them to the internet or attack anything outside this lab.\n")
    return "\n".join(out)


def _default_walkthrough(section_id, title):
    """Concrete-ish fallback steps for chapters without an authored PRACTICE entry."""
    env = partlabs.env_for(section_id) if partlabs else None
    target = env["targets"][0][0] if env and env.get("targets") else "the lab target"
    return [
        ("Provision & baseline",
         f"# bring up the part environment, then confirm you can reach `{target}` from Kali",
         "Target reachable; you have a clean starting point.",
         "Always capture 'normal' before you change anything — it's your reference."),
        ("Reproduce the technique",
         f"# perform the core {title.lower()} technique step by step against {target}",
         "You observe the expected effect and can repeat it reliably.",
         "Owning the mechanism by hand beats running a tool you don't understand."),
        ("Observe what happened",
         "# inspect logs / responses / process or network activity",
         "You can point to exactly where and why it worked.",
         "The evidence here is what a defender would alert on."),
        ("Apply the primary control",
         "# implement the single most important fix for this technique",
         "Repeating the technique now fails.",
         "Fix the class, not the one payload — then prove it's closed."),
    ]


def _runnable(cmd):
    """Heuristic: is this walkthrough 'command' a real shell command we can execute?"""
    c = (cmd or "").strip()
    first = c.split("\n")[0].strip()
    if not first or first.startswith(("http://", "https://", "#", "//", "<", "{")):
        return False
    return True


def _json_fence(kind, obj):
    return "```" + kind + "\n" + json.dumps(obj, ensure_ascii=False) + "\n```"


def render_practice(*, slug, title, section_id, section_title, difficulty, hands_on_min, chapter_dir_to_section=""):
    """The in-page 'Hands-On Practice' block — interactive components (cf-* fences)."""
    spec = labdata.PRACTICE.get(slug) if labdata else None
    quizzes = getattr(labdata, "QUIZZES", {}).get(slug) if labdata else None
    env = partlabs.env_for(section_id) if partlabs else None
    env_link = f"[{section_title} lab environment]({chapter_dir_to_section or 'README.md'}#lab-environment)"

    out = []
    out.append("## Hands-On Practice\n")
    out.append(f"> [!TIP] This is the main event. Bring up the lab, then work the walkthrough — every command "
               f"has a **▸ Run** button (needs the lab runner) and a **📋 Copy** button. "
               f"~{hands_on_min} min, Kali attacker, fully local.\n")
    if spec and spec.get("intro"):
        out.append("**Mission.** " + spec["intro"] + "\n")

    # Lab setup card (interactive: Start/Stop)
    if env:
        out.append(_json_fence("cf-lab", {
            "title": section_title, "section": section_id,
            "targets": [[t[0], t[1]] for t in env.get("targets", [])],
            "compose": env.get("compose", "").strip(),
        }))
        out.append("")
    target = (spec or {}).get("target")
    if target:
        out.append(f"**Target for this lesson:** {target}. Full setup: {env_link}.\n")
    else:
        out.append(f"Uses the {env_link}.\n")

    # Guided walkthrough → stepper of cf-step components
    out.append("### Guided walkthrough\n")
    steps = (spec.get("walkthrough") if spec else None) or _default_walkthrough(section_id, title)
    out.append('<div class="stepper">\n')
    for i, (goal, cmd, output, why) in enumerate(steps, 1):
        out.append(_json_fence("cf-step", {
            "n": i, "goal": goal, "cmd": cmd.strip(), "output": output.strip(),
            "why": why, "runnable": _runnable(cmd),
        }))
    out.append("\n</div>\n")

    # Interactive terminal
    out.append("### Live terminal\n")
    out.append(_json_fence("cf-terminal", {"title": f"kali@{slug} — start the lab runner for a live shell"}))
    out.append("")

    # Try it yourself
    out.append("### Try it yourself\n")
    out.append("> [!NOTE] Try each for real. Open the hint only when stuck, the solution only to check.\n")
    challenges = (spec.get("challenges") if spec else None) or [
        (f"Extend the walkthrough with one variation of the {title.lower()} technique and predict the result "
         "before running it.",
         "Change one variable (payload, target, or control) at a time.",
         "Answers vary — the goal is a correct prediction confirmed by observation."),
        (f"Find and apply a second defensive control for {title.lower()} and show it also blocks the technique.",
         "Think in layers: prevention, detection, and least privilege.",
         "Any independent control that breaks the chain counts — name why it works."),
        (f"Write a one-paragraph report of your {title.lower()} test mapped to CWE/ATT&CK and the fix.",
         "Structure: finding → impact → evidence → remediation.",
         "A defender should be able to act on your report without asking you anything."),
    ]
    for i, (task, hint, solution) in enumerate(challenges, 1):
        out.append(f"**Challenge {i}.** {task}\n")
        out.append(f"<details><summary>Hint</summary>\n\n{hint}\n\n</details>")
        out.append(f"<details><summary>Solution</summary>\n\n{solution}\n\n</details>\n")

    # Quiz (interactive MCQ) — only when authored
    if quizzes:
        out.append("### Quick quiz\n")
        for qz in quizzes:
            out.append(_json_fence("cf-quiz", qz))
        out.append("")

    # Detect & defend
    out.append("### Detect & defend (blue-team view)\n")
    detect = (spec.get("detect") if spec else None) or [
        "Re-run the technique while watching your telemetry — attack and detection are two views of one event.",
        "Turn what you observed into a detection rule (Sigma/YARA) and confirm it fires without flooding.",
    ]
    for d in detect:
        out.append(f"- {d}")
    out.append("")

    # Skills check
    out.append("### Skills check\n")
    out.append("You can move on when you can, without notes:\n")
    skills = (spec.get("skills") if spec else None) or [
        f"Reproduce the core {title.lower()} technique on demand against the lab.",
        f"Explain the root cause and the single most effective control.",
        "Describe the telemetry a defender would use to catch it.",
    ]
    for s in skills:
        out.append(f"- [ ] {s}")
    out.append("")
    return "\n".join(out)


def render_boss_lab(spec, from_file="labs/boss/x.md"):
    """A full standalone boss-lab page (multi-stage kill chain)."""
    out = []
    out.append(f"[Home](../../README.md) › [Labs](../README.md) › **{spec['title']}**\n")
    out.append(f"# {spec['title']}\n")
    out.append(f"> {spec['scenario']}\n")
    out.append("| | |")
    out.append("| --- | --- |")
    out.append(f"| **Difficulty** | {spec['difficulty'].title()} |")
    out.append(f"| **Est. time** | ~{spec['hours']} hours |")
    out.append(f"| **Tracks** | {', '.join(spec['tracks'])} |")
    out.append("")
    out.append("## Environment\n")
    out.append(spec["env"] + "\n")
    out.append("> Everything is local and isolated. This is a capstone: it assumes you've worked the related "
               "chapters below.\n")
    out.append("## Objectives (capture the flags)\n")
    for f in spec["flags"]:
        out.append(f"- [ ] {f}")
    out.append("")
    out.append("## Stages\n")
    out.append("_Work them in order. Each stage has a hint — try hard before opening it._\n")
    for i, (name, objective, hint) in enumerate(spec["stages"], 1):
        out.append(f"### Stage {i} — {name}\n")
        out.append(objective + "\n")
        out.append(f"<details><summary>Hint</summary>\n\n{hint}\n\n</details>\n")
    out.append("## Debrief\n")
    out.append(spec["debrief"] + "\n")
    return "\n".join(out), spec.get("chapters", [])

