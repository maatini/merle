"""
Process queue items from UiPath Orchestrator (or simulated fixtures).

Uses merle_core.uipath as the SSOT client layer:
- UiPathOrchestratorClient — OAuth + jobs
- UiPathQueueHelper — add / get queue items
"""

from __future__ import annotations

from typing import Any

from merle_core import BaseTask
from merle_core.uipath import UiPathQueueHelper

# Sample queue items for SIMULATE=true (local / CI, no network)
SAMPLE_QUEUE_ITEMS: list[dict[str, Any]] = [
    {
        "Id": 1001,
        "SpecificContent": {
            "invoice_id": "INV-2026-001",
            "amount": 1500.00,
            "vendor": "ACME Corp",
        },
    },
    {
        "Id": 1002,
        "SpecificContent": {
            "invoice_id": "INV-2026-002",
            "amount": 420.50,
            "vendor": "Contoso Ltd",
        },
    },
    {
        "Id": 1003,
        "SpecificContent": {
            "invoice_id": "INV-2026-003",
            "amount": 89.99,
            "vendor": "Fabrikam GmbH",
        },
    },
]


def process_item_content(content: dict[str, Any]) -> dict[str, Any]:
    """Pure business logic: turn a queue item payload into a result payload."""
    invoice_id = str(content.get("invoice_id", "unknown"))
    amount = float(content.get("amount", 0.0))
    vendor = str(content.get("vendor", "unknown"))
    return {
        "invoice_id": invoice_id,
        "vendor": vendor,
        "amount": amount,
        "status": "processed",
        "approved": amount < 2000.0,
    }


class ProcessUiPathQueueTask(BaseTask):
    """
    Fetch items from a UiPath queue, process them, write results back.

    Modes:
    - simulate (default): uses SAMPLE_QUEUE_ITEMS, no HTTP
    - injected queue_helper: uses merle_core helper (real or mock)
    """

    def __init__(
        self,
        settings: Any,
        *,
        queue_helper: UiPathQueueHelper | None = None,
        sample_items: list[dict[str, Any]] | None = None,
    ) -> None:
        super().__init__(settings, name="process-uipath-queue")
        self._queue_helper = queue_helper
        self._sample_items = sample_items

    async def execute(self) -> dict[str, Any]:
        simulate = bool(getattr(self.settings, "simulate", True))
        queue_name = getattr(self.settings, "queue_name", "InvoiceQueue")
        result_queue = getattr(self.settings, "result_queue_name", "InvoiceResultsQueue")

        if self._queue_helper is None and simulate:
            return await self._run_simulate(result_queue)

        if self._queue_helper is None:
            raise ValueError(
                "queue_helper is required when SIMULATE=false (inject UiPathQueueHelper or enable SIMULATE=true)"
            )

        return await self._run_with_helper(queue_name, result_queue)

    async def _run_simulate(self, result_queue: str) -> dict[str, Any]:
        items = self._sample_items if self._sample_items is not None else list(SAMPLE_QUEUE_ITEMS)
        self.logger.info(
            "Simulate mode: processing {} fixture queue item(s) (no Orchestrator HTTP)",
            len(items),
        )
        results = [self._process_raw_item(item) for item in items]
        self.logger.info(
            "Simulate: would write {} result(s) to queue '{}'",
            len(results),
            result_queue,
        )
        return {
            "status": "success",
            "mode": "simulate",
            "processed_items": len(results),
            "results": results,
        }

    async def _run_with_helper(self, queue_name: str, result_queue: str) -> dict[str, Any]:
        assert self._queue_helper is not None
        self.logger.info("Fetching queue items from Orchestrator queue '{}'", queue_name)
        items = await self._queue_helper.get_queue_items(queue_name)
        self.logger.info("Retrieved {} queue item(s)", len(items))

        results: list[dict[str, Any]] = []
        for item in items:
            processed = self._process_raw_item(item)
            results.append(processed)
            await self._queue_helper.add_queue_item(result_queue, processed)

        self.logger.info(
            "{} queue item(s) processed; results written to '{}'",
            len(results),
            result_queue,
        )
        return {
            "status": "success",
            "mode": "live",
            "processed_items": len(results),
            "results": results,
        }

    def _process_raw_item(self, item: dict[str, Any]) -> dict[str, Any]:
        content = item.get("SpecificContent") if isinstance(item.get("SpecificContent"), dict) else item
        if not isinstance(content, dict):
            content = {"raw": content}
        result = process_item_content(content)
        source_id = item.get("Id")
        if source_id is not None:
            result["source_queue_item_id"] = source_id
        self.logger.info(
            "Processed invoice {} (approved={})",
            result.get("invoice_id"),
            result.get("approved"),
        )
        return result
