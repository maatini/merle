# Merle

**Modular Enterprise RPA Lifecycle Engine**

Python-first framework for building maintainable, testable, and scalable RPA bots.

- 80–90% of automations in modern Python
- UiPath only when it provides a proven advantage
- Strong core library (`merle-core`) with observability, resilience, and secrets management
- Template-first approach using Copier

## Quick Start

```bash
# Create a new bot
merle new-bot invoice_processor --playwright

cd python_bots/invoice_processor
uv sync --group dev
uv run python main.py
```

## Documentation

- [English Documentation (planned)](https://docs.merle.example.com)
- German documentation is currently the most complete

## Key Features (v0.2)

- `BaseBot` + `BaseTask` with lifecycle, metrics and self-healing hooks
- Centralized retry policies + custom exceptions
- OpenTelemetry integration (Tracing + Metrics + structured logging)
- Robust Playwright wrapper (stealth, auto-screenshots, proxy)
- Azure Key Vault integration via pydantic-settings

## Project Status

- **Current Phase**: 3 – Documentation & Polish
- **Next Vision**: NATS-based granular orchestration

## License

Proprietary – Internal Use Only (Antigravity GmbH)

---

For the full German documentation, please refer to the `docs/` folder and the German `README.md`.
