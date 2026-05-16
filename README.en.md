# Merle

**Modular Enterprise RPA Lifecycle Engine**  
*Python-first hybrid RPA framework for maintainable, testable, and cost-efficient automation at enterprise scale.*

**80–90 % of automations in modern Python** (Playwright with Chromium or Lightpanda engine, pandas, Prefect 3, NATS, OpenTelemetry) — **UiPath only when it delivers a proven architectural advantage**.

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

## Professional Status — v0.2 (Foundation Complete)

| Area                    | Status     | Notes |
|-------------------------|------------|-------|
| `merle-core`            | ✅ 0.2.0   | `BaseBot`, `BaseTask`, retry (tenacity), observability (OTel), secrets (Azure), NATS client, Playwright wrapper (Chromium + Lightpanda) |
| Copier Template         | ✅         | `templates/bot/` with feature flags (playwright, pandas, pdf, uipath_orchestrator, base_bot) + post-gen hook |
| CLI                     | ✅         | `merle new-bot`, governance validation via `tools/merle` |
| OpenCode Integration    | ✅         | `.opencode/` with `rpa-hybrid` agent, `governance-validator`, `rpa-bot-generator`, `/rpa-new-bot` command |
| CI / Quality            | ✅         | `.github/workflows/ci.yml` + `docker-build.yml` (Ruff, mypy, pytest, pre-commit, Trivy) |
| Governance              | ✅         | `AGENTS.md`, 6+ ADRs, Entscheidungsmatrix, CODEOWNERS, issue/PR templates, SECURITY.md |
| DX                      | ✅         | `justfile`, Devbox + direnv, uv workspace, excellent docs structure |

**This repository is ready for internal enterprise RPA teams** building production bots.

## Documentation

- **Primary & most complete:** German documentation in `docs/` + [AGENTS.md](./AGENTS.md) (binding rules for all AI agents and contributors)
- Architecture & Concepts: [docs/concepts/](./docs/concepts/)
- Decision Records (ADRs): [docs/decisions/](./docs/decisions/)
- Merle Core details: [docs/merle-core/](./docs/merle-core/)

## Vision & Roadmap

See the detailed vision in the German [README.md](./README.md#vision--zukünftige-erweiterungen) and the upcoming `docs/ROADMAP.md`.

**High-level phases:**
- **Foundation (v0.2 – current):** Core library, Copier template, CLI, CI/CD, governance, OpenCode hybrid agent
- **DX & Hardening (v0.3):** More real-world examples, observability dashboards, self-healing patterns, Docker story for generated bots
- **Orchestration (v0.4+):** NATS + JetStream as the backbone for granular task distribution, priority scheduling, resource-aware routing
- **Intelligence (future):** KI executors (LLM agents + vision), Prefect 3 integration, BPMN-grade transparency via BPMNinja

## Contributing

See [CONTRIBUTING.md](./CONTRIBUTING.md) and the strict [AGENTS.md](./AGENTS.md) (especially "Python is the Default" and "Template-First").

All new bots **must** be created via:
```bash
merle new-bot my_process --playwright
# or
copier copy templates/bot python_bots/my_process
```

## License & Security

**Proprietary – Internal Use Only (Antigravity GmbH)**

- [LICENSE](./LICENSE)
- [SECURITY.md](./SECURITY.md) — report vulnerabilities privately

---

**For AI coding agents (DeepSeek-TUI, OpenCode, Claude, etc.):**  
You are operating as the **Merle RPA-Hybrid-Architekt**. Always enforce the rules in [AGENTS.md](./AGENTS.md). Never start a bot from scratch — always use the Copier template. Python-first. No UiPath without explicit decision matrix justification.
