# Web Automation Bot — Merle Gold Example

Reference bot showing Playwright-based web automation with Merle's
`BaseBot` / `BaseTask` lifecycle, pydantic-settings config, and failure artifacts.

## What This Example Shows

| Pattern                   | Implementation                          | Why It Matters                    |
| ------------------------- | --------------------------------------- | --------------------------------- |
| **BaseBot Orchestration** | `WebAutomationBot`                      | Lifecycle, hooks, metrics         |
| **Task Decomposition**    | `NavigateTask` + `ExtractPageTitleTask` | Testable units, retry isolation   |
| **Configuration**         | `WebBotSettings` (pydantic-settings)    | Type-safe, env-driven             |
| **Playwright Wrapper**    | `launch_robust_browser`                 | Stealth, failure screenshots/HTML |
| **Testability**           | Injected page mock                      | CI without live browser           |

## Architecture

```
WebAutomationBot (BaseBot)
├── NavigateTask          → goto target_url (live browser or mock page)
└── ExtractPageTitleTask  → title + optional H1
```

## Quick Start

```bash
cd examples/web-automation
uv sync --group dev

# Unit tests (no browser / network)
uv run pytest tests/ -q -m "not integration"

# Live run (needs Playwright browsers + network)
uv run playwright install chromium   # once
uv run python main.py
```

## Failure Artifacts

On live browser errors, `RobustBrowser` writes screenshots and HTML dumps to
`logs/failures/<timestamp>/` (configurable via `FAILURE_DIR`).

## Key Files

- `main.py` — Bot orchestrator (`BaseBot`)
- `config.py` — `WebBotSettings`
- `tasks/` — Navigate + Extract tasks
- `tests/` — Mocked unit tests (CI-safe)

## Governance

- Python-first, no hard-coded credentials
- Optional observability via `ENABLE_TRACING` / `OTLP_ENDPOINT`
- Live browser tests marked `@pytest.mark.integration`
