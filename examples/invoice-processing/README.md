# Invoice Processing Bot — Merle Reference Example

**This is the first full production-grade reference implementation** for the Merle framework (v0.2 Professional Foundation).

It demonstrates exactly how a real, maintainable, observable, and resilient RPA bot should look in 2026 when built with Merle.

## What This Example Shows

| Pattern                        | Implementation in This Bot                              | Why It Matters |
|--------------------------------|---------------------------------------------------------|----------------|
| **Task Decomposition**         | 4 independent `BaseTask` classes                        | Testability, retry isolation, reusability, NATS readiness |
| **BaseBot Orchestration**      | `InvoiceProcessingBot` coordinates the pipeline         | Clear lifecycle, error boundaries, self-healing hooks |
| **Observability**              | `configure_observability()` + structured logging        | Distributed tracing, metrics, production debugging |
| **Resilience**                 | `@with_retry`, `@sensitive_operation_retry`             | Automatic backoff, jitter, different policies per task type |
| **PDF Handling**               | `pdfplumber` pattern + graceful fallback                | Real-world document understanding (even when layout varies) |
| **Excel Output**               | `pandas` + `openpyxl` with professional formatting      | Business users expect beautiful, formula-ready reports |
| **Configuration**              | `pydantic-settings` via `InvoiceBotSettings`            | Type-safe, 12-factor, environment-aware |
| **Self-Healing Hooks**         | `on_error` + task-level `_attempt_self_healing`         | First step toward autonomous repair (Phase 3+) |

## Architecture

```
InvoiceProcessingBot (BaseBot)
├── DownloadInvoicesTask     → Fetch from email/SFTP/ERP
├── ParsePdfInvoicesTask     → pdfplumber + layout heuristics
├── EnrichWithMasterDataTask → ERP / MDM lookup
└── WriteExcelReportTask     → pandas + styled openpyxl
```

Each task is independently testable, retryable, and (in future phases) distributable via NATS.

## Quick Start

```bash
cd examples/invoice-processing

# Install dependencies (merle-core + data extras)
uv sync --group dev

# Run the bot
uv run python main.py
```

Expected output:
- 3 synthetic invoices "downloaded" into `data/invoices/`
- Structured data extracted and enriched
- Professional Excel report in `data/reports/invoice_report_....xlsx`

## Running with Real PDFs

1. Place real invoice PDFs into `data/invoices/`
2. (Optional) Add sidecar `.json` metadata files with `invoice_id`, `supplier`, `amount`, `date`
3. The `ParsePdfInvoicesTask` will automatically use `pdfplumber` when available

## How This Was Created

This example was built **manually** to serve as the gold standard.

In day-to-day work you would start with:

```bash
merle new-bot invoice_processing --playwright --pandas --pdf
# or
copier copy templates/bot examples/invoice-processing
```

Then copy the task patterns from this reference implementation.

## Key Files

- `main.py` — Bot orchestrator (inherits `BaseBot`)
- `config.py` — All settings via pydantic-settings
- `tasks/` — Four fine-grained, reusable tasks
- `pyproject.toml` — Workspace-aware dependency on `merle-core[data,observability]`

## Next-Level Enhancements (for real projects)

- Replace synthetic download with real IMAP + attachment handling or S3/SFTP
- Add LLM-based extraction fallback when pdfplumber confidence is low
- Persist `TaskResult` / `TaskSpec` to NATS JetStream (see Phase 4)
- Add human approval step for invoices > €10.000 via ServiceNow / Action Center
- Write results to ERP (SAP IDoc, Navision, DATEV, etc.)
- Add unit + integration tests with `pytest` + `respx` for HTTP mocks

## Governance Compliance

This bot follows all Merle rules:
- Python-first (no UiPath)
- Template spirit (even though hand-crafted as reference)
- Full observability + retry
- No hard-coded credentials or paths
- Clear task boundaries ready for future NATS distribution

---

**This is the example you show new team members and auditors.**  
It proves that Merle bots are not "scripts" — they are proper, production-grade, observable software.
