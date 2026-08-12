<!-- SPDX-License-Identifier: GPL-3.0-or-later | Copyright (C) 2026 Nithees Narendra S -->
# Tools Reference

> Every tool below is covered with purpose, architecture, installation, configuration, commands, examples, workflows, detection, limitations, alternatives and automation. All are present in `kali-linux-everything`.

## Cloud & Containers

| Tool | Difficulty | What it is for |
| --- | --- | --- |
| [Ansible](ansible-tool.md) | 🟡 Intermediate | Agentless automation for provisioning and hardening lab hosts. |
| [Checkov and tfsec](checkov.md) | 🟢 Beginner | Static analysis of Terraform and other IaC for misconfiguration. |
| [Docker](docker-tool.md) | 🟢 Beginner | Container build/run tooling used to host every lab in this repo. |
| [kube-hunter and kube-bench](kube-hunter.md) | 🟠 Advanced | Kubernetes attack-surface discovery and CIS benchmark checks. |
| [Kubernetes (kubectl)](kubernetes-tool.md) | 🟠 Advanced | Container orchestration and the kubectl control surface. |
| [Pacu](pacu.md) | 🟠 Advanced | AWS exploitation framework for offensive cloud testing in owned accounts. |
| [Prowler](prowler.md) | 🟡 Intermediate | Multi-cloud security assessment against benchmarks and best practice. |
| [ScoutSuite](scoutsuite.md) | 🟡 Intermediate | Multi-cloud security auditing and posture reporting. |
| [Terraform](terraform-tool.md) | 🟡 Intermediate | Declarative infrastructure as code for building repeatable labs. |
| [Trivy](trivy.md) | 🟢 Beginner | All-in-one scanner for images, filesystems, IaC and secrets. |

## Detection

| Tool | Difficulty | What it is for |
| --- | --- | --- |
| [Elastic Stack (ELK)](elk.md) | 🟡 Intermediate | Elasticsearch, Logstash, Kibana and Beats for logging and detection. |
| [Falco](falco.md) | 🟠 Advanced | Runtime threat detection for containers and Kubernetes via syscalls. |
| [MISP](misp.md) | 🟡 Intermediate | Threat-intelligence sharing platform with correlation and export. |
| [osquery](osquery.md) | 🟡 Intermediate | SQL-based endpoint instrumentation and fleet querying. |
| [Sigma (tooling)](sigma-tool.md) | 🟡 Intermediate | Generic SIEM rule format with converters (sigmac/pySigma). |
| [Snort](snort.md) | 🟡 Intermediate | Signature-based network IDS/IPS with a large rule ecosystem. |
| [Splunk](splunk.md) | 🟡 Intermediate | Data platform and SIEM with SPL for search, correlation and dashboards. |
| [Suricata](suricata.md) | 🟠 Advanced | High-performance IDS/IPS/NSM with multi-threading and file extraction. |
| [TheHive and Cortex](thehive.md) | 🟡 Intermediate | Incident-response case management and observable analysis. |
| [Wazuh](wazuh.md) | 🟡 Intermediate | Open-source XDR/SIEM: agents, rules, FIM and compliance monitoring. |
| [YARA (tooling)](yara-tool.md) | 🟡 Intermediate | Pattern-matching engine and CLI for classifying files and memory. |

## Exploitation

| Tool | Difficulty | What it is for |
| --- | --- | --- |
| [Evil-WinRM](evil-winrm.md) | 🟡 Intermediate | WinRM shell for post-exploitation on Windows hosts. |
| [Impacket](impacket.md) | 🟠 Advanced | Python classes and example scripts for crafting and abusing network protocols. |
| [Metasploit Framework](metasploit.md) | 🟡 Intermediate | The reference exploitation framework: modules, payloads, Meterpreter and workflow. |
| [NetExec (CrackMapExec)](crackmapexec.md) | 🟠 Advanced | Swiss-army knife for assessing and exploiting Windows/AD networks at scale. |
| [Responder](responder.md) | 🟠 Advanced | LLMNR/NBT-NS/mDNS poisoner and rogue authentication server for lab AD attacks. |
| [Villain / C2 Basics](villain.md) | 🟠 Advanced | Lightweight command-and-control framework concepts for lab exercises. |

## Forensics

| Tool | Difficulty | What it is for |
| --- | --- | --- |
| [Autopsy / Sleuth Kit](autopsy.md) | 🟡 Intermediate | Open-source digital-forensics platform for disk analysis. |
| [Chainsaw and Hayabusa](chainsaw.md) | 🟡 Intermediate | Fast Windows event-log hunting with Sigma support. |
| [FTK Imager](ftk-imager.md) | 🟢 Beginner | Forensic imaging and preview of disks and memory. |
| [Plaso / log2timeline](plaso.md) | 🟠 Advanced | Super-timeline generation from many artefact sources. |
| [RegRipper](regripper.md) | 🟡 Intermediate | Windows registry parsing for forensic artefacts. |
| [Velociraptor](velociraptor.md) | 🟠 Advanced | Endpoint visibility, hunting and DFIR collection at scale. |
| [Volatility 3](volatility.md) | 🟠 Advanced | The reference memory-forensics framework for RAM analysis. |

## Mobile

| Tool | Difficulty | What it is for |
| --- | --- | --- |
| [Apktool](apktool.md) | 🟡 Intermediate | Reverse engineering, decoding and rebuilding of Android APKs. |
| [jadx](jadx.md) | 🟡 Intermediate | Dex-to-Java decompiler for reading Android app source. |
| [MobSF](mobsf.md) | 🟡 Intermediate | Mobile Security Framework for automated static/dynamic APK and IPA analysis. |
| [Objection](objection.md) | 🟠 Advanced | Frida-powered runtime mobile exploration and control bypass. |

## Password Attacks

| Tool | Difficulty | What it is for |
| --- | --- | --- |
| [BloodHound](bloodhound.md) | 🟠 Advanced | Graph-based Active Directory attack-path discovery and analysis. |
| [CeWL and Crunch](cewl.md) | 🟢 Beginner | Custom wordlist generation from sites and pattern-based candidate lists. |
| [Hashcat](hashcat.md) | 🟡 Intermediate | GPU-accelerated password recovery with rich attack modes. |
| [Hydra](hydra.md) | 🟢 Beginner | Fast network login brute-forcer across many protocols. |
| [John the Ripper](john.md) | 🟡 Intermediate | Versatile password cracker with rules, incremental and format support. |
| [Kerbrute](kerbrute.md) | 🟡 Intermediate | Kerberos pre-auth username enumeration and password spraying. |
| [Mimikatz](mimikatz.md) | 🟠 Advanced | Windows credential-extraction tool: LSASS, tickets, DPAPI and more (lab use). |

## Recon & Scanning

| Tool | Difficulty | What it is for |
| --- | --- | --- |
| [httpx](httpx.md) | 🟢 Beginner | Fast, multi-purpose HTTP probing and web-server fingerprinting toolkit. |
| [Masscan](masscan.md) | 🟡 Intermediate | Asynchronous internet-scale port scanner for very large address ranges. |
| [Naabu](naabu.md) | 🟢 Beginner | Fast, reliable SYN/CONNECT port scanner from the ProjectDiscovery suite. |
| [Nmap](nmap.md) | 🟢 Beginner | The reference network scanner: host discovery, port scanning, version/OS detection and NSE scripting. |
| [Nuclei](nuclei.md) | 🟡 Intermediate | Template-driven vulnerability scanner for fast, community-shared checks. |
| [OWASP Amass](amass.md) | 🟡 Intermediate | In-depth attack-surface mapping and subdomain enumeration. |
| [RustScan](rustscan.md) | 🟢 Beginner | Fast port sweeper that pipes open ports into Nmap for deep scanning. |
| [Shodan and Censys](shodan.md) | 🟢 Beginner | Internet-wide device search engines for passive exposure discovery. |
| [SpiderFoot](spiderfoot.md) | 🟡 Intermediate | Automated OSINT collection and correlation across hundreds of modules. |
| [Subfinder](subfinder.md) | 🟢 Beginner | Passive subdomain discovery from many public sources. |
| [theHarvester](theharvester.md) | 🟢 Beginner | OSINT gathering of emails, subdomains and hosts from public sources. |

## Reverse Engineering

| Tool | Difficulty | What it is for |
| --- | --- | --- |
| [Binwalk](binwalk.md) | 🟡 Intermediate | Firmware analysis and extraction of embedded files and filesystems. |
| [Cutter](cutter.md) | 🟠 Advanced | GUI front end to Rizin/radare2 with a decompiler. |
| [Frida](frida.md) | 🟠 Advanced | Dynamic instrumentation toolkit for hooking apps at runtime. |
| [GDB and GEF/pwndbg](gdb.md) | 🟠 Advanced | The GNU debugger with exploitation-focused plugins. |
| [Ghidra](ghidra.md) | 🟠 Advanced | NSA's open-source SRE suite: disassembler, decompiler and scripting. |
| [IDA Pro / IDA Free](ida.md) | 🔴 Expert | Industry-standard interactive disassembler and decompiler. |
| [pwntools](pwntools.md) | 🟠 Advanced | CTF and exploit-development framework for Python. |
| [radare2](radare2.md) | 🔴 Expert | Command-line reverse-engineering framework for analysis and patching. |
| [x64dbg](x64dbg.md) | 🟠 Advanced | Open-source Windows user-mode debugger for malware and exploits. |

## Traffic Analysis

| Tool | Difficulty | What it is for |
| --- | --- | --- |
| [Bettercap](bettercap.md) | 🟠 Advanced | Swiss-army knife for network MITM, sniffing and recon in a lab. |
| [tcpdump](tcpdump.md) | 🟢 Beginner | Command-line packet capture and BPF filtering for servers and pipelines. |
| [tshark](tshark.md) | 🟡 Intermediate | Wireshark's CLI for scripted capture, field extraction and analysis. |
| [Wireshark](wireshark.md) | 🟢 Beginner | The reference GUI packet analyser with deep dissectors for thousands of protocols. |
| [Zeek](zeek.md) | 🟠 Advanced | Network-security monitor that turns traffic into rich, scriptable logs. |

## Utilities

| Tool | Difficulty | What it is for |
| --- | --- | --- |
| [CyberChef](cyberchef.md) | 🟢 Beginner | The 'cyber Swiss-army knife' for encoding, crypto and data operations. |
| [gitleaks and git-secrets](git-secrets.md) | 🟢 Beginner | Secret scanning for source repositories and history. |
| [jwt_tool](jwt-tool.md) | 🟡 Intermediate | Testing, tampering and cracking JSON Web Tokens. |
| [proxychains and socat](proxychains.md) | 🟡 Intermediate | Traffic redirection and pivoting utilities for lab networks. |
| [Semgrep](semgrep.md) | 🟡 Intermediate | Lightweight static analysis with custom rules for many languages. |

## Web Testing

| Tool | Difficulty | What it is for |
| --- | --- | --- |
| [Arjun](arjun.md) | 🟢 Beginner | HTTP parameter discovery for hidden query and body parameters. |
| [Burp Suite](burp-suite.md) | 🟢 Beginner | The reference web-app testing proxy: intercept, repeat, intrude, scan and extend. |
| [feroxbuster](feroxbuster.md) | 🟢 Beginner | Recursive content-discovery tool built for speed. |
| [ffuf](ffuf.md) | 🟢 Beginner | Fast web fuzzer for content discovery, parameters and virtual hosts. |
| [Gobuster](gobuster.md) | 🟢 Beginner | Fast directory, DNS and vhost brute-forcing in Go. |
| [Nikto](nikto.md) | 🟢 Beginner | Web-server scanner for known files, misconfigurations and dated software. |
| [OWASP ZAP](owasp-zap.md) | 🟢 Beginner | Open-source web-app scanner and proxy with automation and scripting. |
| [sqlmap](sqlmap.md) | 🟡 Intermediate | Automated SQL-injection detection and exploitation across many DBMSes. |
| [Wfuzz](wfuzz.md) | 🟡 Intermediate | Web application fuzzer for brute-forcing any part of a request. |
| [WPScan](wpscan.md) | 🟢 Beginner | WordPress vulnerability scanner for core, plugins and themes. |

## Wireless

| Tool | Difficulty | What it is for |
| --- | --- | --- |
| [Aircrack-ng](aircrack-ng.md) | 🟠 Advanced | Wi-Fi auditing suite: capture, injection and WPA handshake cracking. |
| [hcxdumptool / hcxtools](hcxtools.md) | 🟠 Advanced | PMKID and handshake capture and conversion for hashcat. |
| [Kismet](kismet.md) | 🟡 Intermediate | Wireless network detector, sniffer and IDS. |
| [Wifite2](wifite.md) | 🟡 Intermediate | Automated wireless auditing wrapper for lab access points. |

**89 tools documented.**

[← Repository home](../../README.md) · [Full contents](../../SUMMARY.md)
