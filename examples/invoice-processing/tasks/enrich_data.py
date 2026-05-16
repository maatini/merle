"""
Task: Enrich invoice data with master data (supplier master, cost centers, GL accounts, etc.).

This is a very common RPA pattern: the PDF only contains raw data;
we need to look up additional information from ERP / MDM systems.
"""

from __future__ import annotations

from typing import Any


from merle_core import BaseTask
from merle_core.retry import sensitive_operation_retry


class EnrichWithMasterDataTask(BaseTask):
    """Enriches raw invoice data with internal master data."""

    def __init__(self, settings: Any) -> None:
        super().__init__(settings, name="EnrichWithMasterData")

    @sensitive_operation_retry
    async def _lookup_supplier(self, supplier_name: str) -> dict[str, Any]:
        """Simulate master data lookup (in reality: SAP, Navision, Salesforce, etc.)."""
        await __import__("asyncio").sleep(0.05)

        master = {
            "ACME GmbH": {"supplier_id": "SUP-1001", "payment_terms": "30 days", "cost_center": "CC-4200"},
            "Globex AG": {"supplier_id": "SUP-2042", "payment_terms": "14 days", "cost_center": "CC-3100"},
            "Initech Ltd.": {"supplier_id": "SUP-8871", "payment_terms": "60 days", "cost_center": "CC-5500"},
        }
        return master.get(
            supplier_name, {"supplier_id": "SUP-0000", "payment_terms": "30 days", "cost_center": "CC-9999"}
        )

    async def execute(self) -> dict[str, Any]:
        # In a real bot the previous task would pass the list of parsed invoices.
        # For this reference example we demonstrate the enrichment pattern on synthetic data.
        raw_invoices = [
            {"invoice_id": "INV-2025-0042", "supplier": "ACME GmbH", "amount_gross": 12450.00},
            {"invoice_id": "INV-2025-0043", "supplier": "Globex AG", "amount_gross": 875.50},
            {"invoice_id": "INV-2025-0044", "supplier": "Initech Ltd.", "amount_gross": 2340.00},
        ]

        enriched: list[dict[str, Any]] = []
        for inv in raw_invoices:
            master = await self._lookup_supplier(inv["supplier"])
            enriched.append({**inv, **master})
            self.logger.debug("Enriched {} with master data", inv["invoice_id"])

        self.logger.success("Enriched {} invoices with master data", len(enriched))
        return {"enriched": len(enriched), "invoices": enriched}
