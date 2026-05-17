# ADR 0008: Repository Visibility and Internal Governance

> **⚠️ SUPERSEDED** — Diese Entscheidung wurde durch [ADR-0009](./0009-repository-public-source-available.md) revidiert.  
> Das Repository `maatini/merle` ist seit 2026-05-17 **public** (Source-Available). Die strenge "MUST be private"-Regel gilt nicht mehr.

**Status:** Superseded (by ADR-0009)  
**Date:** 2026-05-16 (original)  
**Deciders:** Martin Richardt (persönlich)  
**Related:** ADR-0001, ADR-0002, ADR-0009, LICENSE

## Context

The Merle repository contains proprietary, business-critical RPA framework code, governance rules, decision records, and internal tooling of Martin Richardt. It is marked "INTERNAL USE ONLY" with a proprietary license.

Despite this, there is a risk that the repository on GitHub (`maatini/merle`) is configured as **public**. This violates the license, creates legal exposure, and contradicts the explicit "Repository ist privat (seit 2026-05)" statement in README.md.

## Decision

**The repository MUST be private on GitHub (and any other git hosting).**

### Concrete Steps for Maintainer (execute immediately)

1. **GitHub UI (one-time):**
   - Go to https://github.com/maatini/merle/settings
   - Under "Danger Zone" → "Change repository visibility" → Select **Private**
   - Confirm. All existing forks/clones of public version must be deleted by owners.
   - Immediately rotate any secrets that might have leaked (Azure keys, NATS creds, etc.) if any were ever committed.

2. **Update all public references (this repo):**
   - Badges in README.md / README.en.md must not promise public access.
   - Clone instructions must assume authenticated access (SSH or PAT).
   - No public PyPI / npm / Docker Hub publishing of merle-core or template without explicit approval.

3. **Legal & Compliance:**
   - Every contributor (employee/contractor) must have signed NDA + confidentiality agreement before gaining access.
   - Access via GitHub teams: `rpa-core`, `rpa-bots`, `rpa-infra` with least-privilege.
   - Audit log review enabled.

4. **If open-sourcing ever becomes desired (unlikely):**
   - Create a completely new public repo (`merle-framework` or similar).
   - Carefully audit and strip all proprietary ADRs, internal examples, Azure secrets patterns, customer-specific code.
   - Dual-license model or relicense under BUSL / proprietary + OSS core split.
   - Never just "make this repo public".

## Consequences

- **Positive:** Full legal compliance, protection of IP, controlled internal collaboration only.
- **Negative:** Slightly higher friction for external contractors (need GitHub invite + PAT/SSH).
- **Mitigation:** Provide `devbox.json` + direnv + one-command `just setup` so onboarding is still excellent for authorized personnel.

## Enforcement

- AGENTS.md (loaded by all AI agents) explicitly states Python-first + template-first + governance.
- Pre-commit + CI will eventually add a check that prevents accidental public references.
- `merle validate` (CLI) will include a "repo-visibility" check in the future.

## References

- LICENSE (Proprietary)
- README.md (strong warning banner)
- AGENTS.md § "Governance beachten"
- .github/CODEOWNERS
- docs/concepts/governance.md
