<!-- SPDX-License-Identifier: GPL-3.0-or-later | Copyright (C) 2026 Nithees Narendra S -->
[Home](../../README.md) › [Labs](../README.md) › **Boss Lab 3 — Purple Team: Detect the Whole Chain**

# Boss Lab 3 — Purple Team: Detect the Whole Chain

> Instrument the environment, run a known attack chain (Boss 1 or 2), and build detections that catch every stage. Measure your coverage against ATT&CK.

| | |
| --- | --- |
| **Difficulty** | Advanced |
| **Est. time** | ~5 hours |
| **Tracks** | Defensive, Purple |

## Environment

The Defensive part environment (Wazuh/ELK + Sysmon on the victim) plus Boss Lab 1 or 2 as the red activity to detect.

> Everything is local and isolated. This is a capstone: it assumes you've worked the related chapters below.

## Objectives (capture the flags)

- [ ] a working Sigma rule per stage
- [ ] an ATT&CK coverage layer
- [ ] one IR write-up

## Stages

_Work them in order. Each stage has a hint — try hard before opening it._

### Stage 1 — Baseline

Deploy telemetry (Sysmon config, Wazuh agent) and confirm the key data sources flow.

<details><summary>Hint</summary>

You can't detect what you don't collect — verify process, network and auth logs.

</details>

### Stage 2 — Execute

Run the red chain (or Atomic Red Team tests for each technique).

<details><summary>Hint</summary>

Invoke-AtomicTest per technique gives clean, mapped telemetry.

</details>

### Stage 3 — Detect

Write a Sigma rule for each stage; convert and deploy to the SIEM.

<details><summary>Hint</summary>

One rule per ATT&CK technique; test each fires and doesn't flood.

</details>

### Stage 4 — Measure

Build an ATT&CK Navigator layer of what you now detect; identify blind spots.

<details><summary>Hint</summary>

Green/yellow/red per technique — honesty about gaps is the point.

</details>

### Stage 5 — Respond

Run the incident-response loop on one detection: triage, scope, contain, write it up.

<details><summary>Hint</summary>

Turn an alert into a defensible timeline and a containment decision.

</details>

## Debrief

What did you fail to detect, and why — missing data source, noisy rule, or evasion? Close one gap and re-test.

## Chapters this draws on

- [Detection Engineering](../../manual/07-defensive-security/detection-engineering.md)
- [Threat Hunting](../../manual/07-defensive-security/threat-hunting.md)
- [Sigma](../../manual/07-defensive-security/sigma.md)
- [SIEM](../../manual/07-defensive-security/siem.md)
- [Incident Response](../../manual/07-defensive-security/incident-response.md)

[← Back to the Labs campaign](../README.md)

