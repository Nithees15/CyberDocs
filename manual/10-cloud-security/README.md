<!-- SPDX-License-Identifier: GPL-3.0-or-later | Copyright (C) 2026 Nithees Narendra S -->
# Cloud Security — Track

Provider-specific and provider-agnostic security for modern cloud-native systems.

<div class="track-progress"><div class="progress" data-track-progress data-lessons="10-cloud-security/cloud-security-fundamentals.html,10-cloud-security/aws-security.html,10-cloud-security/azure-security.html,10-cloud-security/gcp-security.html,10-cloud-security/cloud-iam.html,10-cloud-security/cloud-networking-security.html,10-cloud-security/cloud-container-security.html,10-cloud-security/cloud-kubernetes-security.html,10-cloud-security/iac-security.html,10-cloud-security/cspm.html,10-cloud-security/cloud-detection.html,10-cloud-security/cloud-incident-response.html,10-cloud-security/serverless-cloud-security.html,10-cloud-security/multicloud-security.html"><i></i></div><div class="tp-label" style="color:var(--muted);font-size:13px;margin-top:6px">Your progress in this track</div></div>

**Set up the lab environment below once, then work the lessons — each one is hands-on-first.**

## Lab Environment

_Set up once, then use it for every chapter in the **Cloud Security** part. Everything runs locally and isolated — you never touch a system you don't own._

Cloud, locally: LocalStack emulates AWS APIs so you can create, misconfigure, attack and fix cloud resources with zero cost and zero blast radius.

**What you get**

| Target | How to reach it |
| --- | --- |
| `LocalStack` | http://localhost:4566 — emulated AWS (IAM, S3, EC2 metadata, Lambda) |

**Provision it** — save this as `docker-compose.yml` and run `docker compose up -d` (or import the equivalent spec into CyberForge):

```yaml
# cloud-lab/docker-compose.yml  —  Cloud Security part environment
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
```

**Attacker box.** Drive it with the AWS CLI pointed at LocalStack: `aws --endpoint-url http://localhost:4566 s3 ls`. Attack tooling: `pacu`, `prowler`, `scoutsuite`, `cloudsplaining` all work against the emulated endpoint or a real free-tier account you own.

**Verify it works**

- `curl http://localhost:4566/_localstack/health` returns running services.
- `aws --endpoint-url http://localhost:4566 iam list-users` succeeds.

**Notes**

- For behaviours LocalStack can't emulate (GuardDuty, real IMDS), use a **free-tier account you own** and delete resources after.

**Teardown.** `docker compose down` stops it; add `-v` to also drop volumes. Snapshot before big changes so you can revert.

> **Safety.** Keep intentionally-vulnerable targets on an isolated/`internal` network. Never expose them to the internet or attack anything outside this lab.


## Lessons

| # | Lesson | Difficulty | Hands-on | What you'll do |
| --- | --- | --- | --- | --- |
| 1 | [Cloud Security Fundamentals](cloud-security-fundamentals.md) | 🟢 Beginner | ~48m | Shared responsibility, cloud-native threat models, the control plane and blast radius. |
| 2 | [AWS Security](aws-security.md) | 🟡 Intermediate | ~96m | IAM, organisations, VPC, GuardDuty, S3 exposure and common AWS attack paths. |
| 3 | [Azure Security](azure-security.md) | 🟡 Intermediate | ~84m | Entra ID, RBAC, management groups, Defender and Azure-specific privilege escalation. |
| 4 | [GCP Security](gcp-security.md) | 🟡 Intermediate | ~72m | IAM, org policy, service accounts, VPC-SC and GCP privilege-escalation chains. |
| 5 | [Cloud Identity and Access Management](cloud-iam.md) | 🟠 Advanced | ~72m | Policy evaluation, trust relationships, privilege escalation and least-privilege design. |
| 6 | [Cloud Networking Security](cloud-networking-security.md) | 🟡 Intermediate | ~48m | VPCs, security groups, private endpoints, egress control and network segmentation. |
| 7 | [Cloud Container and Registry Security](cloud-container-security.md) | 🟠 Advanced | ~60m | Managed Kubernetes, registry trust, IRSA/workload identity and runtime protection. |
| 8 | [Managed Kubernetes Security](cloud-kubernetes-security.md) | 🟠 Advanced | ~72m | EKS/AKS/GKE hardening, node identity, admission control and multi-tenant isolation. |
| 9 | [Infrastructure as Code Security](iac-security.md) | 🟡 Intermediate | ~60m | Terraform/CloudFormation scanning, drift, module trust and policy as code. |
| 10 | [Cloud Security Posture Management](cspm.md) | 🟡 Intermediate | ~48m | Misconfiguration detection, benchmarks, guardrails and remediation automation. |
| 11 | [Cloud Detection and Monitoring](cloud-detection.md) | 🟠 Advanced | ~72m | CloudTrail/Activity logs, threat detection services and cloud-native SIEM. |
| 12 | [Cloud Incident Response](cloud-incident-response.md) | 🟠 Advanced | ~72m | Cloud evidence acquisition, containment via API, credential invalidation and forensics. |
| 13 | [Serverless and PaaS Security](serverless-cloud-security.md) | 🟡 Intermediate | ~48m | Function isolation, event-source trust, secrets and cold-path telemetry gaps. |
| 14 | [Multi-Cloud and Hybrid Security](multicloud-security.md) | 🟠 Advanced | ~48m | Identity federation, consistent policy, cross-cloud blast radius and tooling. |

**14 lessons.**

[← Repository home](../../README.md) · [Full contents](../../SUMMARY.md) · [Labs campaign](../../labs/README.md)
