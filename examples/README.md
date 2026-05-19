# Merle Examples

This directory contains **production-grade reference implementations** and smaller demonstrations for typical Merle RPA patterns.

## Reference Implementation (Start Here)

| Example                   | Status               | Description                                                                                                                                                                                                                                                     |
| ------------------------- | -------------------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **`invoice-processing/`** | ✅ **Gold Standard** | Full end-to-end invoice bot using `BaseBot` + 4 `BaseTask`s, PDF parsing (`pdfplumber`), master data enrichment, professional Excel reporting, observability, retry policies, self-healing hooks. **This is the example you show new developers and auditors.** |

## Smaller Demonstrations

| Example                    | Technologies                                      | Purpose                                                 |
| -------------------------- | ------------------------------------------------- | ------------------------------------------------------- |
| `web-automation/`          | Playwright + `launch_robust_browser` + `BaseTask` | Stealth browser automation, failure artifacts, retry    |
| `excel-processing/`        | pandas + openpyxl                                 | Data transformation patterns                            |
| `nats-task-communication/` | `merle_core.nats` + JetStream                     | Early NATS / task queue patterns (Phase 4 foundation)   |
| `uipath-hybrid/`           | UiPath Orchestrator API                           | When UiPath is justified — Python ↔ UiPath integration |

## Quick Start — Reference Bot

```bash
cd examples/invoice-processing
uv sync --group dev
uv run python main.py
```

You will get:

- 3 simulated emails fetched and their attachments extracted
- Real PDF extraction using `pdfplumber`
- Structured data + master data enrichment
- A beautifully formatted Excel report in `data/reports/` containing native formulas and conditional rules
- You can also run the pytest suite: `uv run pytest`

## How to Use These Examples

1. **Study `invoice-processing/` first** — it is the complete, governance-compliant, observable pattern.
2. For new real bots: always start with `merle new-bot ...` (Copier template).
3. Copy proven task patterns from the reference implementation into your generated bot.
4. The smaller examples show specific technical capabilities (browser, NATS, UiPath bridge).

## Governance Note

All examples in this directory follow the Merle rules:

- Python is the default
- Every complex process is decomposed into `BaseTask` units
- Full observability + resilience
- No hard-coded secrets
- Ready for future NATS-based granular orchestration

See also: [docs/ROADMAP.md](../docs/ROADMAP.md) and the main [AGENTS.md](../AGENTS.md).
