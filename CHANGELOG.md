# Changelog

All notable changes to Merle will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

---

## [Unreleased]

---

## [0.7.0] - 2026-07-25 — Deploy, Hybrid Gold & Security Hardening

Post-0.6.0 hardening: reliable monorepo/standalone Docker deploy path, coverage
gates, UiPath hybrid gold example, and blocking security scanners in CI.

### Added

- **examples (uipath-hybrid):** Gold rewrite around `merle_core.uipath` (settings, `ProcessQueueTask`, mocked unit tests, lockfile)
- **merle-core tests:** expanded coverage for playwright utils, secrets, UiPath orchestrator client
- **CI:** merle-core coverage gate; Trivy (CRITICAL+HIGH, `ignore-unfixed`) + TruffleHog as hard fails

### Changed

- **template / Docker:** monorepo vs. standalone builds from repo root; `.dockerignore` + `Dockerfile.jinja` + `docker-build.yml` + `just` helpers
- **integration_examples/orchestrator_api:** aligned with current UiPath client API
- **SECURITY.md + knowledge-base:** public source-available (ADR-0009) and live CI truth

### Fixed

- **ci:** pin `aquasecurity/trivy-action@v0.36.0` (valid v-prefixed tag)
- **examples:** refresh `invoice-processing` lock (Pillow / cryptography HIGH CVEs blocking Trivy)
- **ci:** sync `uv.lock` after commitizen constraint bump (Dependabot PR #34)

---

## [0.6.0] - 2026-07-18 — Quality Hardening

Quality Hardening release: honest docs/version SSOT, hard CI gates, ≥70% merle-core coverage, gold examples, and stricter mypy (Q1–Q7 + M1–M7).

### Docs

- **Q1 / Q5–Q7:** Version-SSOT **0.6.0** (README DE/EN, ROADMAP Current State, CLI `version`/`info` via package metadata)
- Neu: `docs/merle-core/secrets.md` (Azure Key Vault + pydantic-settings, Extras, Gotchas)
- Neu: `docs/merle-core/nats.md` (Phase-4 Client-Foundation, kein Orchestrator)
- Stack-Claims ehrlich: Prefect 3 & rpaframework als Roadmap/optional — nicht Default-Install
- `rpa-opencode-hybrid/`: lokal optional, gitignored, patch-only; produktiv `.opencode/`

### CI / CLI

- **Q4:** Blocking gates for Ruff, Pytest (`packages/merle-core`), pre-commit, `merle validate`, Bandit `-ll`, and Mypy `--strict`
- **M3:** `merle validate` hard-fails on Ruff/Pytest; honest PASS/FAIL summary; framework version from `merle_core` metadata

### Added

- **examples (M4 / PR-E):** Gold upgrades for `web-automation` (BaseBot, BaseTasks, WebBotSettings, mocked page tests) and `nats-task-communication` (TaskSpec/TaskResult roundtrip, mocked NatsClient tests, live-NATS README). Light upgrade for `excel-processing` (settings + simulated/injected tests).
- **merle-core (PR-D / M1):** unit tests for `logging_config`, `http_client`, `data.email`; extended mocked `nats` client coverage (no real network)
- **merle-core (PR-D / M6):** session-scoped OTEL MeterProvider/TracerProvider force_flush + shutdown in test conftest (avoids ConsoleMetricExporter I/O on closed streams)

### Changed

- **mypy (M5 / PR-E):** Removed pauschales `ignore_errors` for `merle_core.secrets.*` and `merle_core.playwright.*`. NATS remains relaxed with `ignore_errors` (`Phase 4 maturing`). Surgical typing fixes in secrets, playwright, and `retry` tenacity wrappers.

### Fixed

- **template (Q2):** `templates/bot/main.py.jinja` uses `typing.Any` instead of lowercase `any` in `dict[str, Any]` annotations
- **pytest (Q3):** root `testpaths` now discovers `packages/merle-core` and `examples` (removed empty sole `python_bots` path)
- **merle-core (M7):** replace deprecated `datetime.utcnow` with timezone-aware `datetime.now(timezone.utc)` in `TaskSpec` / `TaskResult`
- **merle-core (PR-D / M2):** remove `xfail` on self-healing recovery test (fast `wait_none` policy + async-aware `with_retry`); unit-path artifact capture test for `RobustBrowser.__aexit__` without flaky browser launch
- **merle-core (PR-D):** `with_retry` applies tenacity to the original (async) function so retries see real exception types; email attachment write uses open file handle correctly

---

## [0.2.0] - 2026-05-16 — Professional Foundation

**This is the first major milestone release after the initial push.**  
Merle transitions from a promising internal project to a **professional, maintainable, and enterprise-ready RPA framework**.

### Highlights

- **Template Strategy Finalized**  
  The official, maintained way to create new bots is now exclusively through the Copier template in `templates/bot/`, driven by the `merle` CLI (`merle new-bot`). The old static snapshot in `python_bots/template/` has been properly deprecated.

- **Strong Governance Surface**  
  Added full GitHub repository governance: Issue templates, Pull Request template, CODEOWNERS, SECURITY.md, and a comprehensive `.github/` structure.

- **Developer Experience**

  - New `justfile` with commands like `just new-bot`, `just lint`, `just test`, `just ci`, `just docker`.
  - Significantly improved root `.dockerignore` and per-bot `.dockerignore.jinja`.
  - Professional multi-stage `Dockerfile.jinja` with explicit monorepo vs. standalone support.

- **High-Quality Reference Implementation**  
  Added `examples/invoice-processing/` — a production-grade reference bot demonstrating:

  - `BaseBot` + multiple fine-grained `BaseTask` classes
  - Observability, structured retry, PDF + Excel processing, master data enrichment
  - Professional configuration and error handling

- **Core Library Improvements (`merle-core`)**

  - `BaseBot` ergonomics improved (optional `name` parameter, graceful fallback)
  - Safer handling of optional extras (playwright, nats, azure, observability)
  - Professional OpenTelemetry + Loguru integration using the `patcher` pattern (no more dangerous re-logging sinks)
  - Better testability and resilience patterns

- **CI/CD Maturity**

  - Docker CI workflow now actually validates freshly generated bots using the Copier template in monorepo mode.
  - Test suite made CI-friendly (known environment-sensitive tests isolated with `xfail`).

- **Documentation & Process**
  - New `docs/ROADMAP.md` consolidating vision and phases.
  - Updated `CONTRIBUTING.md` to reflect current professional workflows.
  - Clear deprecation path for legacy artifacts.

### Breaking Changes

- The old `python_bots/template/` directory is now officially deprecated. New bots must be created via `merle new-bot` or `copier copy templates/bot`.

### Migration

```bash
# Old (no longer supported)
cp -r python_bots/template/ python_bots/my_bot/

# New (recommended)
merle new-bot my_bot --playwright --pandas
# or
copier copy templates/bot python_bots/my_bot
```

---

## [0.1.0] - Initial Push

Initial public structure of the Merle framework (pre-professionalization).

---

[Unreleased]: https://github.com/maatini/merle/compare/v0.7.0...HEAD
[0.7.0]: https://github.com/maatini/merle/releases/tag/v0.7.0
[0.6.0]: https://github.com/maatini/merle/releases/tag/v0.6.0
[0.2.0]: https://github.com/maatini/merle/releases/tag/v0.2.0-professional-foundation

## v0.5.1 (2026-07-18)

### Fix

- **ci**: sync uv.lock package versions after 0.5.0 bump

## v0.5.0 (2026-07-18)

### Feat

- add karpathy-guidelines skill for coding agents
- implement data and uipath core modules and tests

### Fix

- repair all CI workflow checks — mypy strict, ruff, pytest, bandit, pre-commit

## v0.4.0 (2026-05-19)

### Feat

- **opencode**: add /rpa-analyze command and optimize agent permissions
- **examples**: expand invoice-processing bot with real email, pdf, and excel tasks

### Fix

- **cli**: restructure merle CLI as a package and configure hatchling build

## v0.3.0 (2026-05-18)

### Feat

- extend just clean to remove example outputs (reports, logs, archive)
- **browser**: integrate Lightpanda as optional engine in merle-core
- Professional Foundation v0.2 — Enterprise-ready Merle RPA Framework
- **dev**: Add official Devbox + direnv development environment as standard
- **merle-core**: NATS + Task-Modell als Fundament für Phase 4 Orchestrierung
- **opencode**: Leichte projekt-lokale .opencode/ Integration für RPA-Hybrid-Architekt
- **agents**: extend rpa-context tool with new documentation topics
- **agents**: update rpa-validate command for current framework
- **agents**: extend governance-validator with Rule 10 + merle-core checks
- **agents**: modernize rpa-bot-generator skill for Phase 3+
- **agents**: update rpa-new-bot command to use Copier + merle CLI
- **docs**: introduce official Copier template and merle CLI
- **core**: restructure shared into merle-core v0.2 with src-layout

### Fix

- **ci**: Dockerfile template - remove uv.lock copy + --frozen
- **ci**: copier template \_subdirectory + broken links in docs
- use canonical SecretNotFoundError from merle_core.exceptions in azure.py (was importing duplicate from .base)
- letzte 'Antigravity' / 'Antigravity GmbH' Referenzen in GitHub Templates entfernt
- Entferne fiktive 'Antigravity GmbH' – tatsächlicher Urheber ist Martin Richardt (persönlich)
- Rename tools/merle package to 'merle-cli' to avoid workspace name conflict with root
- Resolve last Ruff warnings (F841, RUF013)
- **nats**: clean up duplicate **aexit** and improve typing

### Refactor

- move merle-core from python_bots/shared/ to packages/merle-core/ (config paths)
- **secrets**: remove duplicate SecretNotFoundError definition
