#!/usr/bin/env python3
"""
Merle Invoice Processing Bot — Production Reference Example

Demonstrates the recommended 2026 Merle architecture:
- BaseBot as the lifecycle orchestrator
- Multiple fine-grained BaseTask classes (Download → Parse → Enrich → Report)
- Observability (OpenTelemetry)
- Structured logging + retry policies
- Clean separation of configuration, tasks, and orchestration
- Self-healing hooks (example)

This is the kind of bot you should generate with `merle new-bot` and then extend.
"""

from __future__ import annotations

import asyncio
from typing import Any

from loguru import logger

from merle_core import BaseBot, configure_observability

from config import settings
from tasks import (
    DownloadInvoicesTask,
    ParsePdfInvoicesTask,
    EnrichWithMasterDataTask,
    WriteExcelReportTask,
)


class InvoiceProcessingBot(BaseBot):
    """
    Clean orchestrator inheriting from the hardened BaseBot.

    Demonstrates the recommended pattern:
    - Inherit from BaseBot
    - Implement `execute()` (the extension point)
    - Decompose work into multiple BaseTask classes
    - Use hooks (_on_success, _on_failure) for cross-cutting concerns
    """

    def __init__(self) -> None:
        super().__init__(settings, name="invoice-processing")
        for d in (settings.input_dir, settings.output_dir, settings.archive_dir):
            d.mkdir(parents=True, exist_ok=True)

    async def execute(self) -> dict[str, Any]:
        """Main pipeline — called by BaseBot.run()."""
        self.logger.info("Starting Invoice Processing pipeline (env={})", settings.environment)

        # 1. Download / Fetch invoices
        dl = DownloadInvoicesTask(settings, settings.input_dir)
        d_res = await dl.run()

        # 2. Parse PDFs
        pr = ParsePdfInvoicesTask(settings, settings.input_dir)
        p_res = await pr.run()
        parsed_invoices = p_res.get("invoices", [])

        # 3. Enrich with master data
        en = EnrichWithMasterDataTask(settings, raw_invoices=parsed_invoices)
        e_res = await en.run()
        enriched_invoices = e_res.get("invoices", [])

        # 4. Write professional Excel report
        rp = WriteExcelReportTask(settings, settings.output_dir, invoices=enriched_invoices)
        r_res = await rp.run()

        summary = {
            "downloaded": d_res.get("count", 0),
            "parsed": p_res.get("parsed", 0),
            "enriched": e_res.get("enriched", 0),
            "report_path": r_res.get("report_path"),
            "total_amount": r_res.get("total_amount"),
        }
        return summary

    def _on_success(self, result: dict[str, Any]) -> None:
        """Example success hook — could send metrics, notifications, etc."""
        self.logger.success("Invoice processing pipeline completed successfully")

    def _on_failure(self, exception: Exception) -> None:
        """Example failure hook — escalation, alerting, dead-letter queue."""
        self.logger.error("Invoice processing pipeline failed: {}", exception)


async def main() -> None:
    # Initialize observability early (before any bot logging)
    if settings.enable_tracing and configure_observability is not None:
        try:
            configure_observability(
                service_name="merle-invoice-bot",
                service_version="0.1.0",
                otlp_endpoint=settings.otlp_endpoint,
                enable_tracing=True,
                enable_metrics=False,
                resource_attributes={"deployment.environment": settings.environment},
            )
        except Exception as e:
            logger.warning("Observability partially disabled: {}", e)

    bot = InvoiceProcessingBot()

    # BaseBot.run() handles timing, logging, hooks and metrics automatically
    result = await bot.run()
    logger.info("Final pipeline result: {}", result)

    # Demonstrate health/metrics API
    logger.info("Health: {}", bot.health_check())


if __name__ == "__main__":
    asyncio.run(main())
