# Pull Request

**Merle — Modular Enterprise RPA Lifecycle Engine**

> **⚠️ INTERNAL USE ONLY** — Martin Richardt. All changes must follow the [Governance rules](AGENTS.md) and [Python-First Strategy](docs/concepts/strategie.md).

## Summary

<!-- One-line summary of the change + link to issue if applicable -->

## Motivation / Context

<!-- Why is this needed? Reference ADR, governance rule, or pain point. -->

## Changes

- [ ] New or modified code in `merle-core` (python_bots/shared)
- [ ] Changes to the official **Copier template** (`templates/bot/`)
- [ ] CLI update in `tools/merle/`
- [ ] Documentation / ADR added or updated
- [ ] Tests added or updated (`pytest`)

## Checklist (required)

- [ ] `uv run ruff check --fix . && uv run ruff format .` passed
- [ ] `uv run mypy python_bots/shared/src/merle_core --strict` (or relevant package) passes or has justified ignores
- [ ] `uv run pytest` (relevant tests) passes
- [ ] If template changed: `copier copy templates/bot /tmp/test-bot && uv run python /tmp/test-bot/main.py` works
- [ ] `uv run pre-commit run --all-files` (or at least the relevant hooks)
- [ ] Documentation updated (README, docs/, or inline docstrings)
- [ ] No hard-coded secrets, paths, or credentials
- [ ] Linux-container compatible (no Windows-only deps unless behind feature flag + documented)

## Screenshots / Logs (if UI, CLI, or bot output relevant)

<!-- Add before/after or relevant terminal output -->

## Related

- Closes #xxx
- ADR: [docs/decisions/00xx-....md](...)
- Related PR in `rpa-opencode-hybrid` (if patching OpenCode core): link

---

**Reviewer notes for Merle maintainers:**

- Does this change affect the **official template** or **merle-core** contract? → High priority review.
- Does it introduce new optional extras in `merle-core`? → Update `pyproject.toml` + docs/merle-core/
- Is a new ADR required? (architectural or governance impact)
