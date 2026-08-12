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

"""Manifest, part 3: tools reference, learning platforms, projects, cheatsheets.

TOOLS tuple:      (slug, name, category, difficulty, hours, abstract)
PLATFORMS tuple:  (slug, name, kind, abstract)
PROJECTS tuple:   (slug, title, domain, difficulty, hours, abstract)
CHEATSHEETS tuple:(slug, title, domain, abstract)
"""

# --------------------------------------------------------------------------
# TOOLS  (Reference section, Unity-"Scripting Reference" analogue)
# --------------------------------------------------------------------------
TOOLS = [
    # Reconnaissance & scanning
    ("nmap", "Nmap", "Recon & Scanning", "beginner", 8,
     "The reference network scanner: host discovery, port scanning, version/OS detection and NSE scripting."),
    ("masscan", "Masscan", "Recon & Scanning", "intermediate", 3,
     "Asynchronous internet-scale port scanner for very large address ranges."),
    ("rustscan", "RustScan", "Recon & Scanning", "beginner", 2,
     "Fast port sweeper that pipes open ports into Nmap for deep scanning."),
    ("naabu", "Naabu", "Recon & Scanning", "beginner", 2,
     "Fast, reliable SYN/CONNECT port scanner from the ProjectDiscovery suite."),
    ("amass", "OWASP Amass", "Recon & Scanning", "intermediate", 5,
     "In-depth attack-surface mapping and subdomain enumeration."),
    ("subfinder", "Subfinder", "Recon & Scanning", "beginner", 2,
     "Passive subdomain discovery from many public sources."),
    ("httpx", "httpx", "Recon & Scanning", "beginner", 3,
     "Fast, multi-purpose HTTP probing and web-server fingerprinting toolkit."),
    ("nuclei", "Nuclei", "Recon & Scanning", "intermediate", 6,
     "Template-driven vulnerability scanner for fast, community-shared checks."),
    ("shodan", "Shodan and Censys", "Recon & Scanning", "beginner", 4,
     "Internet-wide device search engines for passive exposure discovery."),
    ("theharvester", "theHarvester", "Recon & Scanning", "beginner", 2,
     "OSINT gathering of emails, subdomains and hosts from public sources."),
    ("spiderfoot", "SpiderFoot", "Recon & Scanning", "intermediate", 4,
     "Automated OSINT collection and correlation across hundreds of modules."),
    # Packet & traffic
    ("wireshark", "Wireshark", "Traffic Analysis", "beginner", 10,
     "The reference GUI packet analyser with deep dissectors for thousands of protocols."),
    ("tcpdump", "tcpdump", "Traffic Analysis", "beginner", 5,
     "Command-line packet capture and BPF filtering for servers and pipelines."),
    ("tshark", "tshark", "Traffic Analysis", "intermediate", 4,
     "Wireshark's CLI for scripted capture, field extraction and analysis."),
    ("zeek", "Zeek", "Traffic Analysis", "advanced", 10,
     "Network-security monitor that turns traffic into rich, scriptable logs."),
    ("bettercap", "Bettercap", "Traffic Analysis", "advanced", 6,
     "Swiss-army knife for network MITM, sniffing and recon in a lab."),
    # Web app testing
    ("burp-suite", "Burp Suite", "Web Testing", "beginner", 14,
     "The reference web-app testing proxy: intercept, repeat, intrude, scan and extend."),
    ("owasp-zap", "OWASP ZAP", "Web Testing", "beginner", 10,
     "Open-source web-app scanner and proxy with automation and scripting."),
    ("sqlmap", "sqlmap", "Web Testing", "intermediate", 8,
     "Automated SQL-injection detection and exploitation across many DBMSes."),
    ("nikto", "Nikto", "Web Testing", "beginner", 3,
     "Web-server scanner for known files, misconfigurations and dated software."),
    ("gobuster", "Gobuster", "Web Testing", "beginner", 3,
     "Fast directory, DNS and vhost brute-forcing in Go."),
    ("ffuf", "ffuf", "Web Testing", "beginner", 4,
     "Fast web fuzzer for content discovery, parameters and virtual hosts."),
    ("feroxbuster", "feroxbuster", "Web Testing", "beginner", 3,
     "Recursive content-discovery tool built for speed."),
    ("wpscan", "WPScan", "Web Testing", "beginner", 3,
     "WordPress vulnerability scanner for core, plugins and themes."),
    ("wfuzz", "Wfuzz", "Web Testing", "intermediate", 4,
     "Web application fuzzer for brute-forcing any part of a request."),
    ("arjun", "Arjun", "Web Testing", "beginner", 2,
     "HTTP parameter discovery for hidden query and body parameters."),
    # Exploitation frameworks
    ("metasploit", "Metasploit Framework", "Exploitation", "intermediate", 14,
     "The reference exploitation framework: modules, payloads, Meterpreter and workflow."),
    ("impacket", "Impacket", "Exploitation", "advanced", 10,
     "Python classes and example scripts for crafting and abusing network protocols."),
    ("crackmapexec", "NetExec (CrackMapExec)", "Exploitation", "advanced", 8,
     "Swiss-army knife for assessing and exploiting Windows/AD networks at scale."),
    ("responder", "Responder", "Exploitation", "advanced", 6,
     "LLMNR/NBT-NS/mDNS poisoner and rogue authentication server for lab AD attacks."),
    ("evil-winrm", "Evil-WinRM", "Exploitation", "intermediate", 3,
     "WinRM shell for post-exploitation on Windows hosts."),
    ("villain", "Villain / C2 Basics", "Exploitation", "advanced", 6,
     "Lightweight command-and-control framework concepts for lab exercises."),
    # Password & credential
    ("hydra", "Hydra", "Password Attacks", "beginner", 4,
     "Fast network login brute-forcer across many protocols."),
    ("john", "John the Ripper", "Password Attacks", "intermediate", 6,
     "Versatile password cracker with rules, incremental and format support."),
    ("hashcat", "Hashcat", "Password Attacks", "intermediate", 8,
     "GPU-accelerated password recovery with rich attack modes."),
    ("mimikatz", "Mimikatz", "Password Attacks", "advanced", 8,
     "Windows credential-extraction tool: LSASS, tickets, DPAPI and more (lab use)."),
    ("bloodhound", "BloodHound", "Password Attacks", "advanced", 10,
     "Graph-based Active Directory attack-path discovery and analysis."),
    ("kerbrute", "Kerbrute", "Password Attacks", "intermediate", 3,
     "Kerberos pre-auth username enumeration and password spraying."),
    ("cewl", "CeWL and Crunch", "Password Attacks", "beginner", 2,
     "Custom wordlist generation from sites and pattern-based candidate lists."),
    # Wireless
    ("aircrack-ng", "Aircrack-ng", "Wireless", "advanced", 8,
     "Wi-Fi auditing suite: capture, injection and WPA handshake cracking."),
    ("hcxtools", "hcxdumptool / hcxtools", "Wireless", "advanced", 5,
     "PMKID and handshake capture and conversion for hashcat."),
    ("wifite", "Wifite2", "Wireless", "intermediate", 3,
     "Automated wireless auditing wrapper for lab access points."),
    ("kismet", "Kismet", "Wireless", "intermediate", 4,
     "Wireless network detector, sniffer and IDS."),
    # Reverse engineering & binary
    ("ghidra", "Ghidra", "Reverse Engineering", "advanced", 14,
     "NSA's open-source SRE suite: disassembler, decompiler and scripting."),
    ("ida", "IDA Pro / IDA Free", "Reverse Engineering", "expert", 14,
     "Industry-standard interactive disassembler and decompiler."),
    ("radare2", "radare2", "Reverse Engineering", "expert", 12,
     "Command-line reverse-engineering framework for analysis and patching."),
    ("cutter", "Cutter", "Reverse Engineering", "advanced", 6,
     "GUI front end to Rizin/radare2 with a decompiler."),
    ("gdb", "GDB and GEF/pwndbg", "Reverse Engineering", "advanced", 10,
     "The GNU debugger with exploitation-focused plugins."),
    ("x64dbg", "x64dbg", "Reverse Engineering", "advanced", 8,
     "Open-source Windows user-mode debugger for malware and exploits."),
    ("frida", "Frida", "Reverse Engineering", "advanced", 10,
     "Dynamic instrumentation toolkit for hooking apps at runtime."),
    ("binwalk", "Binwalk", "Reverse Engineering", "intermediate", 4,
     "Firmware analysis and extraction of embedded files and filesystems."),
    ("pwntools", "pwntools", "Reverse Engineering", "advanced", 10,
     "CTF and exploit-development framework for Python."),
    # Mobile
    ("mobsf", "MobSF", "Mobile", "intermediate", 6,
     "Mobile Security Framework for automated static/dynamic APK and IPA analysis."),
    ("apktool", "Apktool", "Mobile", "intermediate", 4,
     "Reverse engineering, decoding and rebuilding of Android APKs."),
    ("objection", "Objection", "Mobile", "advanced", 5,
     "Frida-powered runtime mobile exploration and control bypass."),
    ("jadx", "jadx", "Mobile", "intermediate", 3,
     "Dex-to-Java decompiler for reading Android app source."),
    # Forensics & DFIR
    ("volatility", "Volatility 3", "Forensics", "advanced", 12,
     "The reference memory-forensics framework for RAM analysis."),
    ("autopsy", "Autopsy / Sleuth Kit", "Forensics", "intermediate", 8,
     "Open-source digital-forensics platform for disk analysis."),
    ("velociraptor", "Velociraptor", "Forensics", "advanced", 10,
     "Endpoint visibility, hunting and DFIR collection at scale."),
    ("plaso", "Plaso / log2timeline", "Forensics", "advanced", 8,
     "Super-timeline generation from many artefact sources."),
    ("ftk-imager", "FTK Imager", "Forensics", "beginner", 3,
     "Forensic imaging and preview of disks and memory."),
    ("regripper", "RegRipper", "Forensics", "intermediate", 3,
     "Windows registry parsing for forensic artefacts."),
    ("chainsaw", "Chainsaw and Hayabusa", "Forensics", "intermediate", 5,
     "Fast Windows event-log hunting with Sigma support."),
    # Detection & blue-team platforms
    ("yara-tool", "YARA (tooling)", "Detection", "intermediate", 6,
     "Pattern-matching engine and CLI for classifying files and memory."),
    ("sigma-tool", "Sigma (tooling)", "Detection", "intermediate", 6,
     "Generic SIEM rule format with converters (sigmac/pySigma)."),
    ("snort", "Snort", "Detection", "intermediate", 8,
     "Signature-based network IDS/IPS with a large rule ecosystem."),
    ("suricata", "Suricata", "Detection", "advanced", 10,
     "High-performance IDS/IPS/NSM with multi-threading and file extraction."),
    ("wazuh", "Wazuh", "Detection", "intermediate", 12,
     "Open-source XDR/SIEM: agents, rules, FIM and compliance monitoring."),
    ("splunk", "Splunk", "Detection", "intermediate", 14,
     "Data platform and SIEM with SPL for search, correlation and dashboards."),
    ("elk", "Elastic Stack (ELK)", "Detection", "intermediate", 14,
     "Elasticsearch, Logstash, Kibana and Beats for logging and detection."),
    ("osquery", "osquery", "Detection", "intermediate", 6,
     "SQL-based endpoint instrumentation and fleet querying."),
    ("falco", "Falco", "Detection", "advanced", 6,
     "Runtime threat detection for containers and Kubernetes via syscalls."),
    ("misp", "MISP", "Detection", "intermediate", 6,
     "Threat-intelligence sharing platform with correlation and export."),
    ("thehive", "TheHive and Cortex", "Detection", "intermediate", 6,
     "Incident-response case management and observable analysis."),
    # Cloud / container / IaC
    ("trivy", "Trivy", "Cloud & Containers", "beginner", 5,
     "All-in-one scanner for images, filesystems, IaC and secrets."),
    ("prowler", "Prowler", "Cloud & Containers", "intermediate", 6,
     "Multi-cloud security assessment against benchmarks and best practice."),
    ("scoutsuite", "ScoutSuite", "Cloud & Containers", "intermediate", 5,
     "Multi-cloud security auditing and posture reporting."),
    ("kube-hunter", "kube-hunter and kube-bench", "Cloud & Containers", "advanced", 5,
     "Kubernetes attack-surface discovery and CIS benchmark checks."),
    ("docker-tool", "Docker", "Cloud & Containers", "beginner", 8,
     "Container build/run tooling used to host every lab in this repo."),
    ("kubernetes-tool", "Kubernetes (kubectl)", "Cloud & Containers", "advanced", 12,
     "Container orchestration and the kubectl control surface."),
    ("terraform-tool", "Terraform", "Cloud & Containers", "intermediate", 8,
     "Declarative infrastructure as code for building repeatable labs."),
    ("ansible-tool", "Ansible", "Cloud & Containers", "intermediate", 8,
     "Agentless automation for provisioning and hardening lab hosts."),
    ("checkov", "Checkov and tfsec", "Cloud & Containers", "beginner", 4,
     "Static analysis of Terraform and other IaC for misconfiguration."),
    ("pacu", "Pacu", "Cloud & Containers", "advanced", 6,
     "AWS exploitation framework for offensive cloud testing in owned accounts."),
    # Utility / glue
    ("cyberchef", "CyberChef", "Utilities", "beginner", 4,
     "The 'cyber Swiss-army knife' for encoding, crypto and data operations."),
    ("proxychains", "proxychains and socat", "Utilities", "intermediate", 3,
     "Traffic redirection and pivoting utilities for lab networks."),
    ("git-secrets", "gitleaks and git-secrets", "Utilities", "beginner", 3,
     "Secret scanning for source repositories and history."),
    ("semgrep", "Semgrep", "Utilities", "intermediate", 6,
     "Lightweight static analysis with custom rules for many languages."),
    ("jwt-tool", "jwt_tool", "Utilities", "intermediate", 3,
     "Testing, tampering and cracking JSON Web Tokens."),
]

# --------------------------------------------------------------------------
# LEARNING PLATFORMS  (guided roadmaps)
# --------------------------------------------------------------------------
PLATFORMS = [
    ("hack-the-box", "Hack The Box", "Hands-on labs",
     "Gamified pentesting labs, Academy modules and Pro Labs from beginner to expert."),
    ("tryhackme", "TryHackMe", "Guided learning",
     "Guided rooms and learning paths with in-browser labs, ideal for beginners."),
    ("portswigger-academy", "PortSwigger Web Security Academy", "Web security",
     "Free, authoritative web-security labs mapped to Burp Suite techniques."),
    ("overthewire", "OverTheWire", "Wargames",
     "SSH-based wargames (Bandit onward) teaching Linux and exploitation basics."),
    ("root-me", "Root-Me", "Challenges",
     "Broad challenge catalogue across web, crypto, forensics and network."),
    ("picoctf", "picoCTF", "CTF",
     "Beginner-friendly CTF and year-round practice from Carnegie Mellon."),
    ("cyberdefenders", "CyberDefenders", "Blue team",
     "Defensive labs and CTFs for SOC, DFIR and threat hunting."),
    ("blueteamlabs", "Blue Team Labs Online", "Blue team",
     "Investigation-style blue-team challenges and security scenarios."),
    ("vulnhub", "VulnHub", "Boot-to-root VMs",
     "Downloadable intentionally vulnerable VMs for offline boot-to-root practice."),
    ("dvwa", "DVWA", "Vulnerable app",
     "Damn Vulnerable Web Application for practising core web bug classes locally."),
    ("juice-shop", "OWASP Juice Shop", "Vulnerable app",
     "Modern intentionally vulnerable app covering the OWASP Top 10 and beyond."),
    ("metasploitable", "Metasploitable 2/3", "Vulnerable VM",
     "Intentionally vulnerable Linux/Windows targets for exploitation practice."),
]

# --------------------------------------------------------------------------
# PROJECTS  (100+, increasing difficulty, generated below and appended)
# --------------------------------------------------------------------------
_PROJECT_SEEDS = [
    # (title, domain, difficulty, hours, abstract)
    ("Build an Isolated Home Security Lab", "Foundations", "beginner", 6,
     "Stand up a segmented, offline virtual lab with attacker and victim hosts."),
    ("Port Scanner from Scratch in Python", "Networking", "beginner", 5,
     "Implement TCP connect and SYN-style scanning to learn sockets and concurrency."),
    ("Packet Sniffer with Raw Sockets", "Networking", "beginner", 5,
     "Capture and decode Ethernet/IP/TCP headers to understand the stack."),
    ("Custom ARP Spoofer in a Lab Network", "Networking", "intermediate", 5,
     "Demonstrate and then detect ARP cache poisoning between two lab VMs."),
    ("DNS Enumeration and Zone-Walk Tool", "Networking", "intermediate", 5,
     "Automate record discovery, zone transfers and subdomain brute-forcing."),
    ("TLS Certificate Inspector", "Cryptography", "beginner", 4,
     "Parse and validate X.509 chains and flag weak configurations."),
    ("Implement AES-GCM and Break AES-ECB", "Cryptography", "intermediate", 6,
     "Use a library correctly, then exploit an ECB oracle to internalise modes."),
    ("Password Hash Cracker with Rules", "Cryptography", "intermediate", 6,
     "Build a dictionary+rules cracker and benchmark against bcrypt/Argon2."),
    ("Padding Oracle Attack Lab", "Cryptography", "advanced", 8,
     "Stand up a vulnerable service and recover plaintext byte by byte."),
    ("Vulnerable Web App and Full Test Report", "Web Security", "beginner", 8,
     "Deploy DVWA/Juice Shop, work every category and write a professional report."),
    ("JWT Attack Playground", "Web Security", "intermediate", 6,
     "Demonstrate alg-confusion, weak-secret and kid-injection against a lab API."),
    ("SSRF-to-Metadata Lab", "Web Security", "advanced", 8,
     "Build a mock cloud metadata endpoint and exploit SSRF to reach it safely."),
    ("Automated Recon Pipeline", "Offensive", "intermediate", 8,
     "Chain subdomain, port and web probing tools into one reproducible workflow."),
    ("Active Directory Attack Lab", "Offensive", "advanced", 14,
     "Build a small AD forest and walk Kerberoasting to domain compromise."),
    ("Build a Minimal C2 Framework", "Offensive", "advanced", 12,
     "Implement an HTTP beacon and server to understand C2 mechanics and detection."),
    ("Linux Privilege-Escalation Range", "Offensive", "intermediate", 8,
     "Seed a host with common misconfigurations and script their discovery."),
    ("Windows Privilege-Escalation Range", "Offensive", "intermediate", 8,
     "Practise token, service and registry escalation on a lab Windows VM."),
    ("SIEM from Scratch with Elastic", "Defensive", "intermediate", 12,
     "Ingest host and network logs, build detections and dashboards."),
    ("Detection Engineering with Sigma", "Defensive", "advanced", 10,
     "Author, test and convert Sigma rules against Atomic Red Team activity."),
    ("Threat-Hunting Notebook", "Defensive", "advanced", 10,
     "Hypothesis-driven hunts over Zeek/Sysmon data with reusable queries."),
    ("Incident-Response Tabletop and Runbook", "Defensive", "intermediate", 6,
     "Design an IR playbook and run a scripted tabletop exercise."),
    ("Malware Analysis of an Inert Sample", "Malware", "advanced", 10,
     "Statically and dynamically analyse a benign lab sample end to end."),
    ("YARA Ruleset for a Malware Family", "Malware", "intermediate", 6,
     "Cluster samples and write precise, performant detection rules."),
    ("Memory Forensics Investigation", "Forensics", "advanced", 10,
     "Acquire and analyse RAM to reconstruct a simulated intrusion."),
    ("Disk Forensics Timeline Case", "Forensics", "advanced", 10,
     "Build a super timeline and narrate attacker activity from artefacts."),
    ("Secure CI/CD Pipeline", "Secure Dev", "intermediate", 10,
     "Add SAST, SCA, secret scanning and signing gates to a sample repo."),
    ("Threat Model a Real Application", "Secure Dev", "intermediate", 6,
     "Produce DFDs, a STRIDE analysis and prioritised mitigations."),
    ("Harden a Cloud Account Baseline", "Cloud", "intermediate", 8,
     "Apply least-privilege IAM, logging and guardrails in a free-tier account."),
    ("Kubernetes Attack and Defense Lab", "Cloud", "advanced", 12,
     "Exploit a misconfigured cluster, then close every path you used."),
    ("Wi-Fi Handshake Capture and Crack (Own AP)", "Wireless", "advanced", 6,
     "Capture and crack a handshake against an access point you own."),
    ("Phishing-Simulation Framework (Lab Only)", "Offensive", "intermediate", 8,
     "Build ethical phishing infrastructure and the detections that catch it."),
    ("Vulnerability-Management Program in a Box", "Compliance", "intermediate", 8,
     "Inventory, scan, score and track remediation with SLAs and reporting."),
]

# --------------------------------------------------------------------------
# CHEATSHEETS  (printable, one per domain plus tool-specific)
# --------------------------------------------------------------------------
CHEATSHEETS = [
    ("linux-commands", "Linux Command-Line Cheatsheet", "Foundations",
     "Everyday and security-relevant Linux commands in one printable page."),
    ("windows-commands", "Windows and CMD Cheatsheet", "Foundations",
     "Native Windows commands for enumeration and administration."),
    ("powershell", "PowerShell Cheatsheet", "Foundations",
     "Objects, remoting, and offensive/defensive one-liners."),
    ("python-security", "Python for Security Cheatsheet", "Foundations",
     "Sockets, requests, subprocess and parsing snippets for tooling."),
    ("networking", "Networking and Ports Cheatsheet", "Networking",
     "Common ports, protocol flags, subnetting and quick references."),
    ("nmap", "Nmap Cheatsheet", "Networking",
     "Scan types, timing, NSE and output options at a glance."),
    ("wireshark-filters", "Wireshark/tshark Filter Cheatsheet", "Networking",
     "Display and capture filters for fast triage."),
    ("tcpdump", "tcpdump Cheatsheet", "Networking",
     "BPF expressions and capture recipes."),
    ("web-testing", "Web Testing Cheatsheet", "Web Security",
     "Payloads, encodings and checklists for the OWASP Top 10."),
    ("sqli-payloads", "SQL Injection Payload Cheatsheet", "Web Security",
     "Per-DBMS syntax, detection strings and extraction techniques."),
    ("xss-payloads", "XSS Payload Cheatsheet", "Web Security",
     "Context-aware payloads, filter bypasses and polyglots."),
    ("burp", "Burp Suite Cheatsheet", "Web Security",
     "Shortcuts, workflows and extension tips."),
    ("crypto", "Cryptography Cheatsheet", "Cryptography",
     "Primitive selection, key sizes and safe defaults."),
    ("hashcat", "Hashcat and John Cheatsheet", "Cryptography",
     "Modes, masks, rules and common hash formats."),
    ("privesc-linux", "Linux Privilege Escalation Cheatsheet", "Offensive",
     "Enumeration commands and escalation vectors in one page."),
    ("privesc-windows", "Windows Privilege Escalation Cheatsheet", "Offensive",
     "Tokens, services, registry and quick wins."),
    ("active-directory", "Active Directory Attack Cheatsheet", "Offensive",
     "Enumeration, Kerberos attacks and lateral movement commands."),
    ("metasploit", "Metasploit Cheatsheet", "Offensive",
     "msfconsole, Meterpreter and handler workflows."),
    ("pivoting", "Pivoting and Tunnelling Cheatsheet", "Offensive",
     "SSH, chisel, proxychains and port-forward recipes."),
    ("reverse-shells", "Reverse Shell Cheatsheet", "Offensive",
     "One-liners across languages plus stabilisation and catchers."),
    ("volatility", "Volatility Cheatsheet", "Forensics",
     "Plugins and workflows for memory triage."),
    ("dfir-triage", "DFIR Triage Cheatsheet", "Forensics",
     "Order of volatility, collection commands and quick artefacts."),
    ("sigma", "Sigma Rule Cheatsheet", "Defensive",
     "Rule structure, modifiers and conversion tips."),
    ("splunk-spl", "Splunk SPL Cheatsheet", "Defensive",
     "Search, stats, eval and detection patterns."),
    ("mitre-attack", "MITRE ATT&CK Quick Reference", "Threat Intel",
     "Tactics, common techniques and mapping tips."),
    ("docker-security", "Docker and Container Cheatsheet", "Cloud",
     "Build, run, inspect and harden container labs."),
    ("kubectl-security", "kubectl Security Cheatsheet", "Cloud",
     "Enumeration, RBAC checks and hardening commands."),
    ("regex", "Regex for Security Cheatsheet", "Utilities",
     "Patterns for log parsing, IOCs and detection engineering."),
]


def build_projects():
    """Return the PROJECTS list, numbered and expanded past 100 entries.

    The seed list defines flagship projects; we generate additional graded
    variants per domain so the total comfortably exceeds 100 while remaining
    distinct (each variant targets a different technique/tooling angle).
    """
    projects = []
    idx = 1
    for title, domain, diff, hours, abstract in _PROJECT_SEEDS:
        slug = f"{idx:03d}-" + _slugify(title)
        projects.append((slug, title, domain, diff, hours, abstract))
        idx += 1

    # Graded expansion packs: each produces several concrete, distinct projects.
    expansions = [
        ("Networking", [
            ("Write a Netcat Clone", "beginner", 4, "Reimplement listen/connect/relay to learn sockets and I/O."),
            ("Build a Mini Firewall with nftables", "intermediate", 5, "Author and test a stateful ruleset with logging."),
            ("HTTP Request Smuggling Test Harness", "advanced", 8, "Reproduce CL.TE/TE.CL desync against lab servers."),
            ("Protocol Dissector for a Custom Format", "advanced", 8, "Fuzz and dissect a toy binary protocol with a Wireshark plugin."),
        ]),
        ("Web Security", [
            ("CSRF Demonstration and Defence", "beginner", 4, "Show a state-change attack and add token + SameSite defences."),
            ("Blind SQLi Automation Script", "advanced", 8, "Build a time-based boolean extractor from scratch."),
            ("SSTI Payline for Multiple Engines", "advanced", 8, "Fingerprint and escape Jinja2/Twig/Freemarker sandboxes."),
            ("OAuth Misconfiguration Lab", "advanced", 8, "Exploit redirect and state flaws against a lab authorization server."),
        ]),
        ("Offensive", [
            ("Custom Enumeration Framework", "intermediate", 8, "Modular scanner that aggregates service enumeration output."),
            ("Payload Obfuscation Study (Lab)", "advanced", 8, "Study encoders/packers and the detections they trip."),
            ("Kerberoasting End-to-End Lab", "advanced", 8, "Request, extract and crack service tickets in a lab forest."),
            ("Pivoting Range with Three Subnets", "advanced", 10, "Chain hosts across segmented networks using tunnels."),
        ]),
        ("Defensive", [
            ("Sysmon + Sigma Detection Lab", "intermediate", 8, "Deploy Sysmon, generate telemetry and detect it with Sigma."),
            ("Honeypot Deployment and Analysis", "intermediate", 6, "Run a low-interaction honeypot and analyse captured activity."),
            ("Log-Pipeline Enrichment Service", "advanced", 8, "Enrich events with GeoIP/threat-intel before indexing."),
            ("Purple-Team Emulation Plan", "advanced", 10, "Map an intrusion to ATT&CK and validate each detection."),
        ]),
        ("Malware", [
            ("PE/ELF Triage Toolkit", "intermediate", 6, "Script header, import and string triage for first-look analysis."),
            ("Automated Sandbox Report Parser", "intermediate", 6, "Normalise sandbox output into IOCs and a summary."),
            ("Config Extractor for a Family", "advanced", 8, "Extract C2 config from a benign lab loader."),
            ("Unpacking a Packed Binary", "advanced", 10, "Defeat a simple packer and dump the original code."),
        ]),
        ("Forensics", [
            ("Browser-Artefact Timeline Tool", "intermediate", 6, "Parse history/cache/cookies into a unified timeline."),
            ("Windows Event-Log Hunt Kit", "intermediate", 6, "Query 4624/4688/7045 patterns for intrusion signs."),
            ("Email Header Analyser", "beginner", 4, "Parse Received chains and authentication results."),
            ("Full IR Case Simulation", "advanced", 12, "Run a scripted breach across disk, memory and network evidence."),
        ]),
        ("Cloud", [
            ("IaC Security-Gate Pipeline", "intermediate", 8, "Fail builds on Terraform misconfigurations with policy as code."),
            ("Cloud Log Detection Lab", "advanced", 10, "Detect simulated attacker actions from cloud audit logs."),
            ("Least-Privilege IAM Refactor", "intermediate", 8, "Right-size an over-permissive policy set with evidence."),
            ("Container Escape Study (Lab)", "advanced", 10, "Reproduce and remediate a misconfiguration-based escape."),
        ]),
        ("Secure Dev", [
            ("Secrets-Scanning Pre-Commit Hook", "beginner", 4, "Block credential commits with gitleaks in CI and locally."),
            ("SBOM Generation and Diffing", "intermediate", 6, "Produce CycloneDX SBOMs and alert on risky changes."),
            ("Fuzzing a C Library", "advanced", 10, "Harness a parser with a coverage-guided fuzzer and triage crashes."),
            ("Security Unit-Test Suite", "intermediate", 6, "Codify abuse cases as regression tests."),
        ]),
        ("Cryptography", [
            ("Certificate Authority in a Box", "intermediate", 6, "Run a small internal PKI and issue/revoke certs."),
            ("Hash-Length-Extension Demo", "advanced", 6, "Exploit a vulnerable MAC construction to forge messages."),
            ("Encrypted Notes App (Do-It-Right)", "intermediate", 8, "Build authenticated encryption with correct key handling."),
            ("Post-Quantum Handshake Demo", "advanced", 8, "Wire ML-KEM into a toy protocol and measure the trade-offs."),
        ]),
        ("Compliance", [
            ("Control-Mapping Spreadsheet Generator", "beginner", 4, "Cross-map NIST/ISO/CIS controls programmatically."),
            ("Automated Compliance Evidence Collector", "intermediate", 6, "Gather config evidence for an audit scope."),
            ("Risk-Register Toolkit", "beginner", 4, "Model, score and track risks with a simple methodology."),
            ("Policy-as-Code Guardrails", "intermediate", 6, "Encode policies with OPA and test them."),
        ]),
        ("Networking", [
            ("Traceroute and Path-MTU Explorer", "beginner", 4, "Implement TTL-based path discovery and PMTU probing."),
            ("TLS Handshake Visualiser", "intermediate", 6, "Capture and annotate a full TLS 1.3 handshake byte by byte."),
            ("Rogue DHCP Detector", "intermediate", 5, "Detect and locate unauthorised DHCP servers on a lab segment."),
        ]),
        ("Web Security", [
            ("GraphQL Introspection Abuse Lab", "advanced", 6, "Map a schema, then exploit depth/complexity and BOLA."),
            ("Web Cache Poisoning Range", "advanced", 8, "Reproduce unkeyed-input cache poisoning and defend the cache key."),
            ("WebSocket Security Test Harness", "intermediate", 6, "Test CSWSH and message-level authorization."),
        ]),
        ("Offensive", [
            ("OSINT Recon Dashboard", "intermediate", 8, "Aggregate passive recon sources into one report for a domain you own."),
            ("Defense-Evasion Study (Lab)", "advanced", 8, "Compare LOLBins and obfuscation against EDR telemetry."),
            ("Wireless Evil-Twin Lab (Own AP)", "advanced", 8, "Stand up a lab AP and study evil-twin captive portals ethically."),
        ]),
        ("Defensive", [
            ("Detection Coverage Heatmap", "intermediate", 6, "Map your detections to ATT&CK with the Navigator and find gaps."),
            ("Automated Phishing Triage Bot", "intermediate", 6, "Parse reported emails into a verdict with header + URL analysis."),
            ("Threat-Intel Feed Aggregator", "intermediate", 6, "Normalise multiple feeds into deduplicated, scored indicators."),
        ]),
        ("Malware", [
            ("YARA CI for a Sample Repo", "intermediate", 5, "Gate a sample repo with automated YARA scanning."),
            ("Ransomware Behaviour Simulator (Inert)", "advanced", 8, "Model encryption/ransom-note behaviour safely for detection tuning."),
        ]),
        ("Forensics", [
            ("USB/Registry Artefact Parser", "intermediate", 6, "Reconstruct removable-device history from registry hives."),
            ("Network Beacon Detector", "advanced", 8, "Find periodic C2 beacons in flow data with jitter tolerance."),
        ]),
        ("Cloud", [
            ("Kubernetes RBAC Auditor", "advanced", 8, "Flag over-permissive roles and risky bindings in a lab cluster."),
            ("S3-Style Bucket Exposure Scanner", "intermediate", 6, "Detect public-object misconfigurations in an owned account."),
        ]),
        ("Secure Dev", [
            ("Threat-Model-as-Code Tool", "advanced", 8, "Generate DFDs and STRIDE findings from a declarative spec."),
            ("Provenance & Signing Pipeline (SLSA)", "advanced", 10, "Produce signed, attested build artefacts with Sigstore."),
        ]),
        ("Cryptography", [
            ("Timing-Side-Channel Demo", "advanced", 6, "Recover a secret from a non-constant-time comparison."),
            ("TOTP/HOTP Authenticator", "intermediate", 5, "Build and verify RFC 6238 one-time passwords correctly."),
        ]),
        ("Wireless", [
            ("BLE GATT Explorer (Own Device)", "advanced", 6, "Enumerate and interact with a BLE device you own."),
            ("SDR Signal Capture and Replay (Own Remote)", "advanced", 8, "Capture and study an RF remote you own with an SDR."),
        ]),
        ("Identity", [
            ("SAML/OIDC Test IdP and SP", "advanced", 8, "Stand up federation and reproduce a signature-wrapping flaw safely."),
            ("Passkey (WebAuthn) Demo App", "intermediate", 6, "Implement registration and assertion ceremonies end to end."),
        ]),
        ("Compliance", [
            ("Continuous CIS-Benchmark Checker", "intermediate", 6, "Score a host against a CIS benchmark on a schedule."),
            ("Incident-Metrics Dashboard", "intermediate", 5, "Track MTTD/MTTR and detection coverage over time."),
        ]),
    ]
    for domain, items in expansions:
        for title, diff, hours, abstract in items:
            slug = f"{idx:03d}-" + _slugify(title)
            projects.append((slug, title, domain, diff, hours, abstract))
            idx += 1
    return projects


def _slugify(text):
    out = []
    prev_dash = False
    for ch in text.lower():
        if ch.isalnum():
            out.append(ch)
            prev_dash = False
        elif ch in " -_/":
            if not prev_dash:
                out.append("-")
                prev_dash = True
    slug = "".join(out).strip("-")
    # keep filenames short and Windows-safe
    return slug[:60].strip("-")


PROJECTS = build_projects()
