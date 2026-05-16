# ⚠️ DEPRECATED — DO NOT USE

**This directory (`python_bots/template/`) is the legacy manual-copy template.**

It has been **superseded** since Phase 0.2 / 2026-05 by the professional Copier-based template:

**Official source of truth:** `templates/bot/`  
**Official command:** `just new-bot <name>` **or** `uv run merle new-bot <name>` **or** `copier copy templates/bot python_bots/<name>`

## Why deprecated?

- No feature flags (playwright, pandas, pdf, uipath, basebot)
- No post-generation hook (uv sync + ruff auto-fix)
- No Jinja2 templating for pyproject.toml / Dockerfile
- Duplicates logic that now lives in `merle-core` (SSOT)
- Violates "Template-First" + "Single Source of Truth" governance (see AGENTS.md)

## Migration for existing projects

1. Generate fresh bot with `merle new-bot`
2. Manually port your tasks/ and business logic into the new structure
3. Delete this legacy directory after migration (or keep for git history only)

## Enforcement

- `merle validate --strict` will FAIL if this directory still exists in strict mode.
- All AI agents (via AGENTS.md) and the governance-validator skill refuse to work with legacy template.
- CI (docker-build.yml) still builds it for comparison but marks it informational + will be removed in Phase 3.

**Last updated:** 2026-05-16 — Merle RPA-Hybrid-Architekt
