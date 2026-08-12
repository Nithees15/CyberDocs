<!-- SPDX-License-Identifier: GPL-3.0-or-later | Copyright (C) 2026 Nithees Narendra S -->
[Home](../README.md) › [Cheatsheets](README.md) › **Windows Privilege Escalation Cheatsheet**

# Windows Privilege Escalation Cheatsheet

> Tokens, services, registry and quick wins. Printable: use your browser's *Print → Save as PDF*.

_Domain: Offensive · Last updated 2026-08-13_

## Quick reference

This cheatsheet is a fast recall aid, not a tutorial — learn the concepts in the Manual, then keep this beside you while you work.

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

## Related

- [All cheatsheets](README.md)
- [Tools reference](../reference/tools/README.md)
- [Repository home](../README.md)

