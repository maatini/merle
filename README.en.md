# Merle

**Modular Enterprise RPA Lifecycle Engine**  
_Python-first hybrid RPA framework for maintainable, testable, and cost-efficient automation at enterprise scale._

**80–90 % of automations in modern Python** (Playwright with Chromium or Lightpanda, pandas, loguru, tenacity, httpx, pydantic; optional NATS / OpenTelemetry / Azure Key Vault) — **UiPath only when it delivers a proven architectural advantage**.

## Quick Start (Recommended)

```bash
# 1. Clone & activate Devbox (recommended) or use uv directly
git clone https://github.com/maatini/merle.git
cd merle
direnv allow .          # or: devbox shell

# 2. Full setup (uv workspace + merle-core + pre-commit + CLI)
devbox run setup
# or manually:
# uv sync --group dev --all-packages
# uv run pre-commit install --install-hooks

# 3. Create a new production-grade bot from the official template
merle new-bot invoice_processor --playwright --pandas

cd python_bots/invoice_processor
uv run python main.py
```

See the [justfile](./justfile) for ergonomic commands: `just new-bot`, `just lint`, `just test`, `just docker`, `just ci`.

## Professional Status — v0.5.1

| Area                 | Status   | Notes                                                                                                                                                         |
| -------------------- | -------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `merle-core`         | ✅ 0.5.1 | `BaseBot`, `BaseTask`, retry (tenacity), observability (OTel, extra), secrets (Azure, extra), NATS client (extra), Playwright wrapper (Chromium + Lightpanda) |
| Copier Template      | ✅       | `templates/bot/` with feature flags (playwright, pandas, pdf, uipath_orchestrator, base_bot) + post-gen hook                                                  |
| CLI                  | ✅       | `merle new-bot`, governance validation via `tools/merle`                                                                                                      |
| OpenCode Integration | ✅       | `.opencode/` with `rpa-hybrid` agent, `governance-validator`, `rpa-bot-generator`, `/rpa-new-bot` command                                                     |
| CI / Quality         | ✅       | `.github/workflows/ci.yml` + `docker-build.yml` (Ruff, mypy, pytest, pre-commit, Trivy)                                                                       |
| Governance           | ✅       | `AGENTS.md`, 6+ ADRs, Entscheidungsmatrix, CODEOWNERS, issue/PR templates, SECURITY.md                                                                        |
| DX                   | ✅       | `justfile`, Devbox + direnv, uv workspace, excellent docs structure                                                                                           |

**📖 Source Available — Proprietary License**  
This repository is publicly visible (since 2026-05, see [ADR-0009](./docs/decisions/0009-repository-public-source-available.md)). All code remains **copyrighted property of Martin Richardt**. Productive use, modification or redistribution requires an explicit license / valid NDA. See [LICENSE](./LICENSE) and [ADR-0009](./docs/decisions/0009-repository-public-source-available.md). Unauthorized commercial use will be prosecuted.

**This repository is ready for authorized internal enterprise RPA teams** building production bots.

## Philosophy (identical to German primary)

| Principle                 | Description                                                                                                                |
| ------------------------- | -------------------------------------------------------------------------------------------------------------------------- |
| **Python-First**          | Python is the default for 80–90 % of all automations (Playwright, pandas, loguru, tenacity; NATS/Prefect optional/roadmap) |
| **UiPath only justified** | UiPath is used **only** when there is a proven qualitative/architectural advantage (see Entscheidungsmatrix)               |
| **Template-First**        | Every new Python bot **must** be created exclusively via `merle new-bot` / `templates/bot/` (Copier)                       |
| **Container-ready**       | Every bot runs in Linux containers (multi-stage Dockerfile.jinja, monorepo pattern)                                        |
| **Test-driven**           | Unit + integration tests, pre-commit, full CI matrix, `merle validate`                                                     |
| **Governance**            | Binding rules in AGENTS.md, ADRs, decision matrix, CODEOWNERS, strict review process                                       |

## Documentation (German primary — English parity in progress)

- **Primary & most complete:** German documentation in `docs/` + [AGENTS.md](./AGENTS.md) (binding for AI agents & humans)
- Architecture & Concepts: [docs/concepts/](./docs/concepts/) (strategy, decision matrix, governance, secrets, architecture C4)
- Decision Records: [docs/decisions/](./docs/decisions/) (7+ ADRs)
- Merle Core: [docs/merle-core/](./docs/merle-core/) (BaseBot, observability, retry, playwright, secrets, nats)
- English parity effort: See completed analysis + plan in `docs/plans/07-dokumentation-visualisierung.md` and ROADMAP goals ("fully bilingual or English-primary")

## Documentation Status Note (from 2026-05 analysis)

English docs in `docs/` subdirectories are currently secondary. `README.en.md` is the main English entry point. Full parity (translated concepts/, decisions/, getting-started/, merle-core/ at equal depth) remains a roadmap priority. The German content is the source of truth for governance.

- **Primary & most complete:** German documentation in `docs/` + [AGENTS.md](./AGENTS.md) (binding rules for all AI agents and contributors)
- Architecture & Concepts: [docs/concepts/](./docs/concepts/)
- Decision Records (ADRs): [docs/decisions/](./docs/decisions/)
- Merle Core details: [docs/merle-core/](./docs/merle-core/)

## Stack (honest claims)

**Default / installed** (via `merle-core` + extras): loguru, tenacity, httpx, pydantic; optional extras for Playwright/Lightpanda, pandas/openpyxl/pdfplumber, Azure Key Vault + pydantic-settings, OpenTelemetry, nats-py.

**Not default installs** (roadmap / optional / UiPath-scope only):

- **Prefect 3** — planned optional orchestration layer for complex DAGs / HITL, not a merle-core dependency
- **rpaframework** — optional in UiPath Python Scope / integration examples, not the default Python bot stack
- Full **NATS orchestrator** — Phase-4 roadmap; `merle_core.nats` client is foundation only

## OpenCode: production vs. local fork

**Production path:** use the repo-local [`.opencode/`](./.opencode/) integration (`rpa-hybrid` agent, skills, commands).

**`rpa-opencode-hybrid/`:** local-optional, **gitignored**, patch-only OpenCode fork for core patches / custom desktop builds. Not shipped with clone; not part of the productive Merle stack. See root `.gitignore` entry `rpa-opencode-hybrid/`.

## Vision & Roadmap

See the detailed vision in the German [README.md](./README.md#vision--zukünftige-erweiterungen) and [`docs/ROADMAP.md`](./docs/ROADMAP.md).

**High-level (current = v0.5.1):**

- **Foundation (complete through v0.5.x):** Core library, Copier template, CLI, CI/CD, governance, `.opencode/` hybrid agent
- **DX & Hardening (ongoing):** More real-world examples, observability, self-healing patterns, Docker story for generated bots
- **Orchestration (roadmap):** NATS + JetStream backbone for granular task distribution, priority scheduling, resource-aware routing
- **Intelligence (future):** KI executors (LLM agents + vision), optional Prefect 3 patterns, BPMN-grade transparency via BPMNinja

## Contributing

See [CONTRIBUTING.md](./CONTRIBUTING.md) and the strict [AGENTS.md](./AGENTS.md) (especially "Python is the Default" and "Template-First").

All new bots **must** be created via:

```bash
merle new-bot my_process --playwright
# or
copier copy templates/bot python_bots/my_process
```

## License & Security

**Proprietary – Internal Use Only (Martin Richardt)**

- [LICENSE](./LICENSE)
- [SECURITY.md](./SECURITY.md) — report vulnerabilities privately

---

**For AI coding agents (DeepSeek-TUI, OpenCode, Claude, etc.):**  
You are operating as the **Merle RPA-Hybrid-Architekt**. Always enforce the rules in [AGENTS.md](./AGENTS.md). Never start a bot from scratch — always use the Copier template. Python-first. No UiPath without explicit decision matrix justification.
