# Security Policy — Merle RPA Framework

**License:** Proprietary / source-available (see [LICENSE](./LICENSE) and [ADR-0009](docs/decisions/0009-repository-public-source-available.md)).  
The source is publicly visible; **unauthorized commercial use, redistribution, or derivative commercial products are not permitted** without a separate written license from the copyright holder.

## Reporting a Vulnerability

**Please do NOT create public GitHub issues for security vulnerabilities.**

Instead, report security issues **privately** via one of the following channels:

1. **GitHub Security Advisories** (preferred)  
   → https://github.com/maatini/merle/security/advisories/new

2. **Direct email to maintainers**  
   martin.richardt@maatini.space  
   (PGP key available on request)

We appreciate responsible disclosure. Please allow reasonable time for remediation before any public discussion of the issue.

## Supported Versions

| Version | Supported              |
| ------- | ---------------------- |
| 0.6.x   | ✅ Current             |
| < 0.6   | ❌ No longer supported |

## Security Tooling (CI)

Configured in `.github/workflows/ci.yml`:

| Tool                                      | Role                                                   | CI severity                                                                |
| ----------------------------------------- | ------------------------------------------------------ | -------------------------------------------------------------------------- |
| **Bandit** (SAST, medium+)                | Python static analysis on `merle-core` + `tools/merle` | **HARD** — fails the Security job                                          |
| **Trivy** (fs, CRITICAL+HIGH)             | Dependency / IaC vulnerability scan                    | **HARD** — `exit-code: "1"`; `ignore-unfixed: true` (only fixed CVEs fail) |
| **TruffleHog**                            | Secret scanning (event-aware PR/push diff)             | **HARD** — `extra_args: --fail`; pinned action version                     |
| **Ruff / mypy / pytest / merle validate** | Quality gates                                          | **HARD** (Quality job)                                                     |
| **pre-commit**                            | Hook suite + formatters                                | **HARD**                                                                   |
| **Dependabot**                            | Dependency update PRs                                  | Advisory / PR-based                                                        |

Unfixed Trivy findings are ignored (`ignore-unfixed: true`) so only remediatable CRITICAL/HIGH CVEs fail CI.

## Scope

This policy covers:

- `merle-core` (`packages/merle-core/src/merle_core`)
- Official Copier bot template (`templates/bot/`)
- `merle` CLI (`tools/merle/`)
- `.opencode/` agent, skills, and commands
- CI/CD workflows, Dockerfiles, Devbox configuration
- Documentation that could leak secrets patterns or credentials guidance

## Out of Scope (for this repo)

- Issues in the **rpa-opencode-hybrid/** directory → report in the upstream OpenCode project or the `maatini/merle-opencode-hybrid` fork (if it exists).
- UiPath Orchestrator / Robot / Document Understanding vulnerabilities → follow UiPath responsible disclosure process.
- Third-party dependencies (report via their respective channels; we track critical ones via Dependabot / Trivy).

## Response Targets

- **Critical** (remote code execution, secret leakage, supply-chain in template): 24–48h initial response
- **High**: 5 business days
- **Medium/Low**: Next planning cycle

## Responsible Disclosure

We appreciate responsible disclosure. Reporters may be credited in release notes or a security changelog unless they prefer anonymity.

---

**Last updated:** 2026-07-25  
**Maintained by:** Merle RPA Platform Team  
**Related:** ADR-0009 (public source-available visibility)
