<!-- SPDX-License-Identifier: GPL-3.0-or-later | Copyright (C) 2026 Nithees Narendra S -->
[Home](../../README.md) › [Labs](../README.md) › **Boss Lab 6 — SSRF to Cloud Account Takeover**

# Boss Lab 6 — SSRF to Cloud Account Takeover

> A web app has an SSRF. Use it to reach the (emulated) instance metadata service, steal role credentials, enumerate the account, and exfiltrate from storage — then remediate.

| | |
| --- | --- |
| **Difficulty** | Advanced |
| **Est. time** | ~4 hours |
| **Tracks** | Cloud, Web |

## Environment

The Cloud part environment (LocalStack emulating AWS) plus a vulnerable fetcher app with an SSRF, on `labnet`.

> Everything is local and isolated. This is a capstone: it assumes you've worked the related chapters below.

## Objectives (capture the flags)

- [ ] SSRF callback
- [ ] stolen role credentials
- [ ] exfiltrated object

## Stages

_Work them in order. Each stage has a hint — try hard before opening it._

### Stage 1 — Find the SSRF

Confirm the app fetches attacker-supplied URLs server-side.

<details><summary>Hint</summary>

A callback to your listener proves server-side fetch.

</details>

### Stage 2 — Reach metadata

Pivot the SSRF to the metadata endpoint and steal credentials.

<details><summary>Hint</summary>

169.254.169.254 (or the LocalStack stand-in) → role credentials.

</details>

### Stage 3 — Enumerate

Use the stolen credentials to map the account's permissions.

<details><summary>Hint</summary>

aws --endpoint-url ... sts get-caller-identity; enumerate with prowler/scoutsuite.

</details>

### Stage 4 — Exfiltrate

Find and read sensitive objects the role can access.

<details><summary>Hint</summary>

List and get from the storage buckets the role permits.

</details>

### Stage 5 — Remediate

Close the SSRF (egress + IP validation), scope the role down, require IMDSv2.

<details><summary>Hint</summary>

Three independent fixes — any one breaks the chain (as in the real Capital One case).

</details>

## Debrief

Map this to the Capital One breach. Which of the three fixes (egress, least-privilege role, IMDSv2) is the strongest, and why is defence-in-depth the real answer?

## Chapters this draws on

- [Server-Side Request Forgery](../../manual/04-vulnerabilities/ssrf.md)
- [Cloud Identity and Access Management](../../manual/10-cloud-security/cloud-iam.md)
- [Cloud Platform Security](../../manual/05-platforms/cloud-platform-security.md)
- [Cloud Incident Response](../../manual/10-cloud-security/cloud-incident-response.md)

[← Back to the Labs campaign](../README.md)

