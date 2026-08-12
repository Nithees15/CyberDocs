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

"""Boss labs — cross-topic capstone challenges for the standalone Labs pillar.

Each boss lab chains techniques from several chapters into one end-to-end
scenario (a full kill chain), with staged objectives, hints, and 'flags' to
capture. Rendered by lab_platform.render_boss_lab() into labs/boss/.

BOSS[] entries feed both the boss pages and the Labs campaign ordering.
"""

BOSS = [
    {
        "slug": "boss-01-web-to-root",
        "title": "Boss Lab 1 — Web App to Root",
        "difficulty": "intermediate",
        "hours": 4,
        "tracks": ["Web", "Offensive"],
        "chapters": ["scanning", "sql-injection", "command-injection", "rce", "privilege-escalation"],
        "env": "Use the Web Security + Offensive part environments (a vulnerable web app on `labnet`, "
               "Kali as attacker).",
        "scenario": "You have a single in-scope web application and nothing else. Get a shell on the server "
                    "and escalate to root, capturing a flag at each stage.",
        "stages": [
            ("Recon", "Map the app: pages, parameters, tech stack. Find every input that reaches the server.",
             "httpx + a directory brute-force (ffuf/gobuster) reveal hidden endpoints."),
            ("Foothold", "Exploit a web vulnerability (SQLi, command injection, or file upload) to reach code "
                         "execution. Capture flag 1 from the web root.",
             "Chain the injection to a reverse shell; keep the exact payload in your notes."),
            ("Situational awareness", "As the web user, enumerate the host: users, services, sudo, SUID, cron.",
             "linpeas, then verify by hand. Flag 2 is readable by a specific group."),
            ("Privilege escalation", "Escalate to root via a misconfiguration. Capture the root flag.",
             "GTFOBins for the sudo/SUID binary you found."),
            ("Report", "Write it up: the chain, each finding mapped to CWE/ATT&CK, and the one fix per stage that "
                       "would have broken it.",
             "A defender should be able to close any single link and stop you."),
        ],
        "flags": ["flag1 (web root)", "flag2 (group-readable file)", "root.txt"],
        "debrief": "Which single control at each stage would have stopped the chain? Now build the detection for "
                   "your foothold (web-server process spawning a shell) and your privesc (SUID/sudo abuse).",
    },
    {
        "slug": "boss-02-domain-domination",
        "title": "Boss Lab 2 — Assumed Breach to Domain Admin",
        "difficulty": "advanced",
        "hours": 6,
        "tracks": ["Identity", "Offensive"],
        "chapters": ["enumeration", "active-directory-attacks", "kerberos", "lateral-movement", "credential-access"],
        "env": "GOAD (recommended) or the Identity part environment (Samba AD-DC for the basics).",
        "scenario": "Assume-breach: you start with one low-privileged domain user's credentials. Reach Domain "
                    "Admin and prove domain persistence.",
        "stages": [
            ("Enumerate", "Collect the AD graph and identify high-value targets and paths.",
             "BloodHound 'shortest path to Domain Admins'."),
            ("Harvest credentials", "Kerberoast/AS-REP roast and crack a service account.",
             "impacket-GetUserSPNs + hashcat -m 13100."),
            ("Walk the path", "Abuse an ACL edge (GenericAll/WriteDACL/ForceChangePassword) to control a "
                              "privileged principal.",
             "Follow BloodHound's edges literally; each has a documented abuse."),
            ("Domain compromise", "DCSync the krbtgt hash and forge a Golden Ticket.",
             "impacket-secretsdump then impacket-ticketer."),
            ("Detect your own attack", "Re-run the chain while capturing 4768/4769/4662 and write detections.",
             "This is the purple-team half — map every step to an event ID."),
        ],
        "flags": ["service account password", "krbtgt hash", "Golden Ticket admin access"],
        "debrief": "Rank your steps by how detectable they were. Which AD hardening (gMSA, AES-only, tiering, "
                   "LAPS) would have broken the path earliest?",
    },
    {
        "slug": "boss-03-purple-killchain",
        "title": "Boss Lab 3 — Purple Team: Detect the Whole Chain",
        "difficulty": "advanced",
        "hours": 5,
        "tracks": ["Defensive", "Purple"],
        "chapters": ["detection-engineering", "threat-hunting", "sigma", "siem", "incident-response"],
        "env": "The Defensive part environment (Wazuh/ELK + Sysmon on the victim) plus Boss Lab 1 or 2 as the "
               "red activity to detect.",
        "scenario": "Instrument the environment, run a known attack chain (Boss 1 or 2), and build detections "
                    "that catch every stage. Measure your coverage against ATT&CK.",
        "stages": [
            ("Baseline", "Deploy telemetry (Sysmon config, Wazuh agent) and confirm the key data sources flow.",
             "You can't detect what you don't collect — verify process, network and auth logs."),
            ("Execute", "Run the red chain (or Atomic Red Team tests for each technique).",
             "Invoke-AtomicTest per technique gives clean, mapped telemetry."),
            ("Detect", "Write a Sigma rule for each stage; convert and deploy to the SIEM.",
             "One rule per ATT&CK technique; test each fires and doesn't flood."),
            ("Measure", "Build an ATT&CK Navigator layer of what you now detect; identify blind spots.",
             "Green/yellow/red per technique — honesty about gaps is the point."),
            ("Respond", "Run the incident-response loop on one detection: triage, scope, contain, write it up.",
             "Turn an alert into a defensible timeline and a containment decision."),
        ],
        "flags": ["a working Sigma rule per stage", "an ATT&CK coverage layer", "one IR write-up"],
        "debrief": "What did you fail to detect, and why — missing data source, noisy rule, or evasion? Close one "
                   "gap and re-test.",
    },
    {
        "slug": "boss-04-pivot",
        "title": "Boss Lab 4 — Pivot Across Segmented Networks",
        "difficulty": "advanced",
        "hours": 4,
        "tracks": ["Networking", "Offensive"],
        "chapters": ["scanning", "exploitation", "lateral-movement", "firewalls", "nat"],
        "env": "A three-network range: your `labnet`, an internal `dmz`, and a `secure` segment only reachable "
               "through a dual-homed host (compose with three networks).",
        "scenario": "Only the DMZ host is reachable. Compromise it, then pivot to reach a target on the isolated "
                    "`secure` segment that you cannot route to directly.",
        "stages": [
            ("Breach the DMZ", "Compromise the internet-facing host.", "Standard recon → exploit."),
            ("Discover the second network", "From the DMZ host, find the interface/route into `secure`.",
             "`ip a`, `ip r`, and ARP/ping sweeps from the pivot host."),
            ("Tunnel", "Stand up a pivot (chisel/ssh -D/ligolo) so your Kali tools reach `secure`.",
             "proxychains + a SOCKS proxy through the DMZ host."),
            ("Reach the crown jewel", "Scan and exploit the `secure`-segment target through the tunnel.",
             "Point nmap/exploits at the internal IP via proxychains."),
            ("Map the segmentation", "Document exactly which firewall rule allowed the pivot.",
             "The fix is usually one egress/segmentation rule on the dual-homed host."),
        ],
        "flags": ["DMZ host foothold", "internal network map", "secure-segment flag"],
        "debrief": "Which segmentation or egress control would have stopped the pivot? Why is 'NAT' not a "
                   "security boundary here?",
    },
    {
        "slug": "boss-05-malware-ir",
        "title": "Boss Lab 5 — Incident: Triage a Compromised Host",
        "difficulty": "advanced",
        "hours": 5,
        "tracks": ["Forensics", "Malware", "Defensive"],
        "chapters": ["memory-forensics", "disk-forensics", "malware-fundamentals", "incident-response", "yara"],
        "env": "The Forensics part environment (`dfir-box`) plus a provided memory + disk image of a compromised "
               "host (use a public DFIR dataset).",
        "scenario": "A host is suspected compromised. Investigate the evidence, extract IOCs, identify the "
                    "malware and initial access, and produce an incident report with detections.",
        "stages": [
            ("Memory triage", "Find the malicious process, its network connections and injected code.",
             "Volatility: pslist/psscan, netscan, malfind, cmdline."),
            ("Disk timeline", "Build a super timeline and find initial access and persistence.",
             "plaso/log2timeline + the browser/email/download artefacts."),
            ("Identify the malware", "Extract the artefact and triage it in isolation; classify the family.",
             "strings/capa/YARA on the dumped module — do not run it on your host."),
            ("Extract IOCs & detections", "Produce hashes, domains, mutexes; write YARA + Sigma.",
             "Turn every artefact into something a defender can hunt with."),
            ("Report", "Write the IR report: timeline, root cause, impact, containment, and recommendations.",
             "Defensible narrative + the one control that would have prevented initial access."),
        ],
        "flags": ["malicious process + C2", "initial-access vector", "a YARA rule that catches the sample"],
        "debrief": "What was the initial access, and which single preventive control (patch, macro policy, egress "
                   "filter) would have stopped the whole incident?",
    },
    {
        "slug": "boss-06-cloud-breach",
        "title": "Boss Lab 6 — SSRF to Cloud Account Takeover",
        "difficulty": "advanced",
        "hours": 4,
        "tracks": ["Cloud", "Web"],
        "chapters": ["ssrf", "cloud-iam", "cloud-platform-security", "cloud-incident-response"],
        "env": "The Cloud part environment (LocalStack emulating AWS) plus a vulnerable fetcher app with an SSRF, "
               "on `labnet`.",
        "scenario": "A web app has an SSRF. Use it to reach the (emulated) instance metadata service, steal role "
                    "credentials, enumerate the account, and exfiltrate from storage — then remediate.",
        "stages": [
            ("Find the SSRF", "Confirm the app fetches attacker-supplied URLs server-side.",
             "A callback to your listener proves server-side fetch."),
            ("Reach metadata", "Pivot the SSRF to the metadata endpoint and steal credentials.",
             "169.254.169.254 (or the LocalStack stand-in) → role credentials."),
            ("Enumerate", "Use the stolen credentials to map the account's permissions.",
             "aws --endpoint-url ... sts get-caller-identity; enumerate with prowler/scoutsuite."),
            ("Exfiltrate", "Find and read sensitive objects the role can access.",
             "List and get from the storage buckets the role permits."),
            ("Remediate", "Close the SSRF (egress + IP validation), scope the role down, require IMDSv2.",
             "Three independent fixes — any one breaks the chain (as in the real Capital One case)."),
        ],
        "flags": ["SSRF callback", "stolen role credentials", "exfiltrated object"],
        "debrief": "Map this to the Capital One breach. Which of the three fixes (egress, least-privilege role, "
                   "IMDSv2) is the strongest, and why is defence-in-depth the real answer?",
    },
]
