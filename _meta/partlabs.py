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

"""Per-part (per-section) lab environments.

Each entry is the "set it up once for the whole part" environment — a
docker-compose / CyberForge lab that provisions every target the chapters in
that section need. Rendered at the TOP of each section's README by
lab_platform.render_part_environment(), and linked from each chapter's
Hands-On Practice block.

Shape: PART_LABS[section_id] = {
    "intro":   short line on what the environment provides,
    "network": "labnet" isolation note,
    "targets": [(name, url_or_note), ...],   # what you can reach and how
    "compose": "<docker-compose yaml>",       # the runnable environment
    "attacker":"kali note",
    "verify":  ["how to confirm it works", ...],
    "notes":   ["caveats / heavy targets", ...],
}
Sections without a dedicated target environment fall back to a Kali/local note.
"""

# Reusable attacker note
KALI = ("Your Kali box is the attacker. Put it on the same `labnet` network "
        "(`docker network connect labnet kali`) or use the published host ports. "
        "All targets are on an **internal, isolated** network by default — they cannot reach the "
        "internet or your host, which is exactly what we want.")

PART_LABS = {
    "01-networking": {
        "intro": "A small network range: a multi-service Linux target plus a packet-capture point, so you can "
                 "scan, sniff and dissect real traffic.",
        "targets": [
            ("metasploitable", "Many open services (FTP/SSH/Telnet/SMB/HTTP/MySQL) — the scan & enumerate target"),
            ("Kali (you)", "Attacker + capture host (tcpdump/wireshark/tshark/nmap)"),
        ],
        "compose": """# net-lab/docker-compose.yml  —  Networking part environment
services:
  metasploitable:
    image: tleemcjr/metasploitable2
    container_name: net-target
    networks: [labnet]
    # intentionally vulnerable services; keep it OFF any routed network
    command: /bin/sh -c "/etc/rc.local; tail -f /dev/null"

networks:
  labnet:
    driver: bridge
    internal: true          # no route to host/internet — fail closed
""",
        "attacker": KALI,
        "verify": [
            "`docker compose up -d` then `docker network inspect labnet` shows the target's IP.",
            "From Kali on labnet: `nmap -sn <subnet>` finds the target; `nmap -sV <ip>` lists services.",
        ],
        "notes": ["Metasploitable 2 is deliberately vulnerable — never expose it on a routed network."],
    },

    "03-web-security": {
        "intro": "Four classic vulnerable web apps on one isolated network. Point Burp/ZAP and your browser at "
                 "any of them; every web-security and vulnerability chapter uses one of these.",
        "targets": [
            ("bWAPP", "http://localhost:8081  — 100+ web bugs, best for targeted practice"),
            ("DVWA", "http://localhost:8082  — adjustable security levels"),
            ("Juice Shop", "http://localhost:8083 — modern SPA, full OWASP Top 10"),
            ("WebGoat", "http://localhost:8084 — guided lessons"),
        ],
        "compose": """# web-lab/docker-compose.yml  —  Web Security part environment
services:
  bwapp:
    image: raesene/bwapp
    ports: ["8081:80"]
    networks: [labnet]
  dvwa:
    image: vulnerables/web-dvwa
    ports: ["8082:80"]
    networks: [labnet]
  juice-shop:
    image: bkimminich/juice-shop
    ports: ["8083:3000"]
    networks: [labnet]
  webgoat:
    image: webgoat/webgoat
    ports: ["8084:8080"]
    networks: [labnet]

networks:
  labnet:
    driver: bridge
    # routed here so your browser/Burp on the host can reach the apps;
    # for a jeopardy-style setup put the attacker box on labnet and set internal: true
""",
        "attacker": "Drive these from your browser through **Burp Suite** or **OWASP ZAP** as an intercepting "
                    "proxy. `sqlmap`, `ffuf`, `nikto`, `wpscan` and friends all run from Kali against the "
                    "published ports.",
        "verify": [
            "`docker compose up -d` then browse to http://localhost:8081 (bWAPP install page) — run its "
            "`install.php` once to initialise the database.",
            "Juice Shop answers on http://localhost:8083 immediately.",
        ],
        "notes": [
            "First bWAPP run: visit `/install.php` to create the DB. DVWA: log in `admin/password`, click "
            "'Create/Reset Database', then set the security level per exercise.",
        ],
    },

    "04-vulnerabilities": {
        "intro": "Reuses the Web Security apps for injection/logic bugs, and adds a disposable build box for the "
                 "memory-corruption chapters (compile and exploit vulnerable C locally).",
        "targets": [
            ("bWAPP / DVWA / Juice Shop", "the web bug targets (see the Web Security part environment)"),
            ("pwn-box", "Ubuntu build/debug container for buffer/heap/format-string labs"),
        ],
        "compose": """# vuln-lab/docker-compose.yml  —  Vulnerabilities part environment
services:
  bwapp:
    image: raesene/bwapp
    ports: ["8081:80"]
    networks: [labnet]
  dvwa:
    image: vulnerables/web-dvwa
    ports: ["8082:80"]
    networks: [labnet]
  pwn-box:
    image: ubuntu:22.04
    container_name: pwn-box
    cap_add: ["SYS_PTRACE"]          # allow gdb inside the container
    security_opt: ["seccomp=unconfined"]
    command: sleep infinity
    networks: [labnet]

networks:
  labnet:
    driver: bridge
""",
        "attacker": "Web bugs: Burp/ZAP + Kali web tooling. Memory corruption: work *inside* `pwn-box` "
                    "(`docker exec -it pwn-box bash`), install `build-essential gdb python3-pip`, add "
                    "`pwntools`/`pwndbg`, and compile targets with mitigations toggled.",
        "verify": [
            "`docker exec -it pwn-box bash` gives a root shell in the build box.",
            "`gcc --version` after installing build-essential; `gdb ./vuln` works with SYS_PTRACE.",
        ],
        "notes": ["`pwn-box` grants SYS_PTRACE and unconfined seccomp *for debugging only* — keep it on the "
                  "isolated network."],
    },

    "06-offensive-security": {
        "intro": "A mini attack range: a vulnerable Linux host to own, a web target to breach, and (optionally) "
                 "an Active Directory forest for the domain-attack chapters.",
        "targets": [
            ("metasploitable", "boot-to-root Linux target (recon → exploit → loot)"),
            ("dvwa / juice-shop", "web foothold targets"),
            ("AD forest (optional)", "GOAD or a Windows Server eval VM for AD chapters — see notes"),
        ],
        "compose": """# offsec-lab/docker-compose.yml  —  Offensive part environment
services:
  target-linux:
    image: tleemcjr/metasploitable2
    networks: [labnet]
    command: /bin/sh -c "/etc/rc.local; tail -f /dev/null"
  target-web:
    image: vulnerables/web-dvwa
    ports: ["8082:80"]
    networks: [labnet]

networks:
  labnet:
    driver: bridge
    internal: true
""",
        "attacker": "Kali on `labnet` runs the full kill chain: `nmap`/`nuclei` (recon), `metasploit`/manual "
                    "exploits, then local privesc enumeration (`linpeas`). For AD, use `netexec`, `bloodhound`, "
                    "`impacket`, `kerbrute`.",
        "verify": ["`nmap -sV target-linux` from a Kali container attached to labnet lists exploitable services."],
        "notes": [
            "**Active Directory:** containers can't host a real DC well. For AD chapters, provision **GOAD** "
            "(github.com/Orange-Cyberdefense/GOAD) or a Windows Server evaluation VM in VirtualBox/VMware on an "
            "isolated host-only network. A Samba AD-DC container covers Kerberos/LDAP basics only.",
        ],
    },

    "07-defensive-security": {
        "intro": "A blue-team stack: ship logs into a SIEM, generate attacker telemetry, and write detections. "
                 "Wazuh gives you agent telemetry, rules and a dashboard in one container set.",
        "targets": [
            ("Wazuh dashboard", "https://localhost:5601 (or :443) — SIEM/XDR UI, rules, alerts"),
            ("victim host + agent", "generates the telemetry you hunt over"),
        ],
        "compose": """# blue-lab/docker-compose.yml  —  Defensive part environment
# Wazuh ships an official single-node compose. Pull it and bring it up:
#   git clone https://github.com/wazuh/wazuh-docker -b v4.x
#   cd wazuh-docker/single-node && docker compose up -d
# Then add a target that generates events:
services:
  victim:
    image: ubuntu:22.04
    container_name: blue-victim
    command: sleep infinity
    networks: [labnet]
  # (install the Wazuh agent in 'victim', or run Sysmon on a Windows VM,
  #  then run Atomic Red Team tests to generate detections.)

networks:
  labnet:
    driver: bridge
""",
        "attacker": "Generate telemetry with **Atomic Red Team** (`Invoke-AtomicTest`) or manual technique "
                    "execution on the victim, then hunt in Wazuh/Kibana and author **Sigma** rules. **Zeek**/"
                    "**Suricata** on a span port give you network detections.",
        "verify": ["Wazuh dashboard loads and the agent on `victim` reports as active.",
                   "An Atomic test (e.g. T1059) produces a matching alert."],
        "notes": ["Wazuh single-node needs ~4 GB RAM. ELK (Elasticsearch+Kibana+Filebeat) is an alternative "
                  "stack if you prefer raw log hunting."],
    },

    "08-malware": {
        "intro": "A DISPOSABLE, air-gapped analysis box. Nothing here touches your host or the internet. Snapshot "
                 "before detonation and revert after. Analyse only benign lab samples.",
        "targets": [
            ("analysis-box", "isolated container/VM with static+dynamic tooling"),
        ],
        "compose": """# malware-lab/docker-compose.yml  —  Malware analysis (ISOLATED)
services:
  analysis-box:
    image: remnux/remnux-distro:focal    # REMnux: malware-analysis toolkit
    container_name: analysis-box
    command: sleep infinity
    networks: [airgap]
    # NO published ports. NO internet.

networks:
  airgap:
    driver: bridge
    internal: true         # hard requirement: no route out
""",
        "attacker": "You are the analyst, not an attacker. Work inside `analysis-box` "
                    "(`docker exec -it analysis-box bash`): triage with `file`, `strings`, `pecheck`, `capa`, "
                    "`yara`; detonate benign samples and observe. For Windows malware, use a FLARE-VM snapshot in "
                    "VirtualBox on a host-only network.",
        "verify": ["`docker network inspect airgap` shows `internal: true` (no gateway to the host).",
                   "`yara --version` and `strings` are available inside the box."],
        "notes": ["**Never** attach this network to the internet. Prefer a full VM with snapshots for real "
                  "(non-lab) samples; a container is fine for the benign teaching samples used here."],
    },

    "10-cloud-security": {
        "intro": "Cloud, locally: LocalStack emulates AWS APIs so you can create, misconfigure, attack and fix "
                 "cloud resources with zero cost and zero blast radius.",
        "targets": [
            ("LocalStack", "http://localhost:4566 — emulated AWS (IAM, S3, EC2 metadata, Lambda)"),
        ],
        "compose": """# cloud-lab/docker-compose.yml  —  Cloud Security part environment
services:
  localstack:
    image: localstack/localstack
    ports: ["4566:4566"]
    environment:
      - SERVICES=iam,s3,ec2,lambda,sts,logs
    networks: [labnet]

networks:
  labnet:
    driver: bridge
""",
        "attacker": "Drive it with the AWS CLI pointed at LocalStack: "
                    "`aws --endpoint-url http://localhost:4566 s3 ls`. Attack tooling: `pacu`, `prowler`, "
                    "`scoutsuite`, `cloudsplaining` all work against the emulated endpoint or a real free-tier "
                    "account you own.",
        "verify": ["`curl http://localhost:4566/_localstack/health` returns running services.",
                   "`aws --endpoint-url http://localhost:4566 iam list-users` succeeds."],
        "notes": ["For behaviours LocalStack can't emulate (GuardDuty, real IMDS), use a **free-tier account you "
                  "own** and delete resources after."],
    },

    "12-identity": {
        "intro": "An identity lab. Samba AD-DC gives you Kerberos, LDAP and NTLM to attack; for full Windows AD "
                 "attack paths, provision GOAD.",
        "targets": [
            ("samba-ad", "LDAP/Kerberos/SMB directory services to enumerate and attack"),
            ("GOAD (optional)", "full multi-DC Windows forest for realistic AD attacks"),
        ],
        "compose": """# id-lab/docker-compose.yml  —  Identity part environment
services:
  samba-ad:
    image: nowsci/samba-domain            # or diladele/samba-ad-dc
    environment:
      - DOMAIN=LAB.LOCAL
      - DOMAINPASS=Passw0rd!Passw0rd!
      - HOSTIP=172.20.0.10
    networks:
      labnet: { ipv4_address: 172.20.0.10 }
    cap_add: ["SYS_ADMIN"]

networks:
  labnet:
    driver: bridge
    ipam: { config: [{ subnet: 172.20.0.0/24 }] }
""",
        "attacker": "`netexec ldap/smb`, `kerbrute`, `impacket-*`, `bloodhound-python` from Kali. Samba covers "
                    "enumeration, Kerberoasting basics and LDAP; GOAD covers delegation, ACL abuse and DCSync "
                    "faithfully.",
        "verify": ["`netexec smb 172.20.0.10` shows the domain and hostname.",
                   "`ldapsearch -x -H ldap://172.20.0.10 -b 'dc=lab,dc=local'` returns the base DN."],
        "notes": ["**GOAD** (github.com/Orange-Cyberdefense/GOAD) is the recommended full AD lab; it provisions "
                  "Windows VMs via Vagrant on an isolated network."],
    },

    "13-digital-forensics": {
        "intro": "A forensics workbench with the analysis tools pre-installed. Bring your own disk/memory images "
                 "(CyberDefenders and public DFIR datasets are ideal, and safe).",
        "targets": [
            ("dfir-box", "Volatility 3, Sleuth Kit/Autopsy, plaso, RegRipper, Chainsaw"),
        ],
        "compose": """# dfir-lab/docker-compose.yml  —  Forensics part environment
services:
  dfir-box:
    image: sk4la/plaso                    # plaso + timeline tooling; or build a custom SIFT-like image
    container_name: dfir-box
    command: sleep infinity
    volumes:
      - ./evidence:/evidence:ro           # drop disk/memory images here (read-only)
    networks: [labnet]

networks:
  labnet:
    driver: bridge
    internal: true
""",
        "attacker": "You're the investigator. Work inside `dfir-box` over the read-only `/evidence` mount: "
                    "`vol -f mem.raw windows.pslist`, `log2timeline.py`, `mmls`/`fls` (Sleuth Kit). Keep "
                    "originals read-only and work on copies/hashes.",
        "verify": ["`docker exec -it dfir-box vol -h` runs Volatility 3.",
                   "Your image appears under `/evidence` inside the container."],
        "notes": ["Use public, shareable DFIR datasets (CyberDefenders, DFIR CTFs). Never process real "
                  "case evidence in a teaching lab."],
    },
}

# Sections that use local tooling / no dedicated target stack.
GENERIC_ENV = {
    "intro": "This part is mostly conceptual and tool-driven — no dedicated vulnerable targets are needed. Work "
             "from Kali (or any Linux box) and the tools called out in each chapter.",
    "targets": [("Kali / local shell", "everything you need is a terminal and the tools named per chapter")],
    "compose": """# Optional scratch box for trying commands in isolation:
services:
  scratch:
    image: kalilinux/kali-rolling        # or debian:stable-slim
    container_name: scratch
    command: sleep infinity
    networks: [labnet]
networks:
  labnet: { driver: bridge, internal: true }
""",
    "attacker": "Run the chapter's commands directly on Kali, or in the disposable `scratch` container to keep "
                "your main system clean.",
    "verify": ["`docker exec -it scratch bash` gives an isolated shell."],
    "notes": [],
}


def env_for(section_id):
    return PART_LABS.get(section_id, GENERIC_ENV)
