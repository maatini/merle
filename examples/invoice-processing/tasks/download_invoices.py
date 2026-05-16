"""
Task: Download / Fetch new invoices.

In a real implementation this would:
- Connect to an SFTP server, email inbox (IMAP), or ERP API
- Download PDF files
- Store them in the input directory with proper naming + metadata
"""

from __future__ import annotations

import asyncio
from pathlib import Path
from typing import Any


from merle_core import BaseTask
from merle_core.retry import with_retry, default_http_retry


class DownloadInvoicesTask(BaseTask):
    """
    Fetches new invoices from source systems.

    This is a synthetic implementation for the reference example.
    Replace the `_fetch_from_source` method with real integration logic.
    """

    def __init__(self, settings: Any, input_dir: Path) -> None:
        super().__init__(settings, name="DownloadInvoices")
        self.input_dir = input_dir
        self.input_dir.mkdir(parents=True, exist_ok=True)

    @with_retry(policy=default_http_retry)
    async def _fetch_from_source(self) -> list[dict[str, Any]]:
        """
        Simulate fetching 3 invoices from an upstream system.

        Real version would do IMAP, SFTP, REST, etc.
        """
        self.logger.info("Fetching invoices from source system (simulated)...")
        await asyncio.sleep(0.2)  # Simulate network latency

        # Synthetic invoice metadata (in real life this comes from the source)
        invoices = [
            {
                "invoice_id": "INV-2025-0042",
                "supplier": "ACME GmbH",
                "amount": 12450.00,
                "currency": "EUR",
                "date": "2025-05-10",
                "pdf_bytes": self._create_minimal_pdf("INV-2025-0042", "ACME GmbH", 12450.00),
            },
            {
                "invoice_id": "INV-2025-0043",
                "supplier": "Globex AG",
                "amount": 875.50,
                "currency": "EUR",
                "date": "2025-05-11",
                "pdf_bytes": self._create_minimal_pdf("INV-2025-0043", "Globex AG", 875.50),
            },
            {
                "invoice_id": "INV-2025-0044",
                "supplier": "Initech Ltd.",
                "amount": 2340.00,
                "currency": "EUR",
                "date": "2025-05-12",
                "pdf_bytes": self._create_minimal_pdf("INV-2025-0044", "Initech Ltd.", 2340.00),
            },
        ]
        return invoices

    def _create_minimal_pdf(self, invoice_id: str, supplier: str, amount: float) -> bytes:
        """
        Return placeholder PDF bytes.

        In a real implementation this would download actual PDFs from email, SFTP,
        or an ERP system. The placeholder keeps the example fully self-contained.
        """
        return f"PDF-BYTES-FOR-{invoice_id}".encode("utf-8")

    async def execute(self) -> dict[str, Any]:
        invoices = await self._fetch_from_source()

        saved_files: list[Path] = []
        for inv in invoices:
            filename = f"{inv['invoice_id']}.pdf"
            target = self.input_dir / filename

            # In real life: write inv["pdf_bytes"] to disk
            # For this reference example we write a small marker file + metadata sidecar
            target.write_bytes(inv.get("pdf_bytes", b"PLACEHOLDER-PDF"))
            (target.with_suffix(".json")).write_text(
                f'{{"invoice_id": "{inv["invoice_id"]}", "supplier": "{inv["supplier"]}", '
                f'"amount": {inv["amount"]}, "date": "{inv["date"]}"}}'
            )
            saved_files.append(target)
            self.logger.info("Saved invoice {}", filename)

        self.logger.success("Downloaded {} invoices", len(saved_files))
        return {
            "count": len(saved_files),
            "files": [str(f) for f in saved_files],
            "invoices": invoices,
        }
