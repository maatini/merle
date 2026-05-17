# Security Policy — Merle RPA Framework

**⚠️ INTERNAL USE ONLY — Martin Richardt**

This repository contains **proprietary and confidential** software. It is **not** intended for public disclosure or external contribution without explicit written approval.

## Reporting a Vulnerability

**Please do NOT create public GitHub issues for security vulnerabilities.**

Instead, report security issues **privately** via one of the following channels:

1. **GitHub Security Advisories** (preferred for this repo)  
   → https://github.com/maatini/merle/security/advisories/new

2. **Direct email to maintainers**  
   martin.richardt@maatini.space  
   (PGP key available on request)

3. **Internal escalation**  
   - RPA Core Team via internal Slack / Jira Security ticket
   - For high-severity: immediate page to on-call (see .opencode/ or internal runbook)

## Supported Versions

| Version | Supported          |
|---------|--------------------|
| 0.2.x   | ✅ Current (Phase 1/2) |
| < 0.2   | ❌ No longer supported |

## Security Tooling (enforced in CI)

- Bandit (SAST)
- Trivy (container + fs)
- TruffleHog / gitleaks (secret scanning)
- Dependabot + Renovate (dependency updates)
- pre-commit (hook-based checks)
- `merle validate` (governance + basic hygiene)

All findings with CRITICAL/HIGH severity are treated as blocking for production bot deployments.  
   Use the `#security` or `#merle-rpa` channel in the internal Slack/Teams workspace and tag `@merle-security`.

## Scope

This policy covers:
- `merle-core` (python_bots/shared/src/merle_core)
- Official Copier bot template (`templates/bot/`)
- `merle` CLI (`tools/merle/`)
- `.opencode/` agent, skills, and commands
- CI/CD workflows, Dockerfiles, Devbox configuration
- Documentation that could leak internal architecture or secrets patterns

## Out of Scope (for this repo)

- Issues in the **rpa-opencode-hybrid/** directory → report in the upstream OpenCode project or the private `maatini/merle-opencode-hybrid` fork (if it exists).
- UiPath Orchestrator / Robot / Document Understanding vulnerabilities → follow UiPath responsible disclosure process.
- Third-party dependencies (report via their respective channels; we track critical ones in Dependabot / Trivy).

## Response SLA (Internal)

- **Critical** (remote code execution, secret leakage, supply-chain in template): 24–48h
- **High**: 5 business days
- **Medium/Low**: Next sprint planning

## Responsible Disclosure

We appreciate responsible disclosure. Internal reporters will be credited in the private security changelog (unless they prefer anonymity).

---

**Last updated:** 2026-05-16  
**Maintained by:** Merle RPA Platform Team
