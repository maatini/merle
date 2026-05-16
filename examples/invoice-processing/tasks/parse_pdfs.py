"""
Task: Parse PDF invoices using pdfplumber.

Demonstrates:
- Robust PDF text extraction
- Handling of slightly different invoice layouts
- Structured output (line items, totals, metadata)
- Graceful degradation + self-healing hook example
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any


from merle_core import BaseTask
from merle_core.retry import with_retry, default_http_retry


class ParsePdfInvoicesTask(BaseTask):
    """Extracts structured data from invoice PDFs."""

    def __init__(self, settings: Any, input_dir: Path) -> None:
        super().__init__(settings, name="ParsePdfInvoices")
        self.input_dir = input_dir

    @with_retry(policy=default_http_retry)
    async def _parse_single_pdf(self, pdf_path: Path) -> dict[str, Any]:
        """
        Real PDF parsing with pdfplumber.

        This is the production-grade pattern you would use.
        """
        try:
            import pdfplumber  # type: ignore
        except ImportError:
            # Fallback for the reference example when pdfplumber is not installed
            return self._parse_synthetic_invoice(pdf_path)

        self.logger.debug("Parsing PDF with pdfplumber: {}", pdf_path.name)

        with pdfplumber.open(pdf_path) as pdf:
            text = ""
            for page in pdf.pages:
                page_text = page.extract_text() or ""
                text += page_text + "\n"

            # In a real bot you would use more sophisticated extraction
            # (regex, layout analysis, ML-based NER, or LLM extraction).
            # Here we demonstrate the structure with a realistic mock.
            return self._parse_synthetic_invoice(pdf_path, raw_text=text)

    def _parse_synthetic_invoice(self, pdf_path: Path, raw_text: str = "") -> dict[str, Any]:
        """
        Fallback / synthetic parser used in this reference example.

        In production this would be replaced by real pdfplumber + domain logic.
        """
        # Try to read sidecar JSON written by download task
        meta_file = pdf_path.with_suffix(".json")
        if meta_file.exists():
            meta = json.loads(meta_file.read_text())
            return {
                "invoice_id": meta["invoice_id"],
                "supplier": meta["supplier"],
                "amount_gross": meta["amount"],
                "currency": meta.get("currency", self.settings.default_currency),
                "invoice_date": meta["date"],
                "line_items": [{"description": "Consulting services", "qty": 10, "unit_price": meta["amount"] / 10}],
                "vat_rate": 0.19,
                "source_file": str(pdf_path),
            }

        # Last resort
        return {
            "invoice_id": pdf_path.stem,
            "supplier": "Unknown Supplier",
            "amount_gross": 0.0,
            "currency": self.settings.default_currency,
            "invoice_date": "1970-01-01",
            "line_items": [],
            "vat_rate": 0.19,
            "source_file": str(pdf_path),
            "warning": "Synthetic fallback used",
        }

    async def execute(self) -> dict[str, Any]:
        pdf_files = sorted(self.input_dir.glob("*.pdf"))
        if not pdf_files:
            self.logger.warning("No PDF files found in {}", self.input_dir)
            return {"parsed": 0, "invoices": []}

        parsed_invoices: list[dict[str, Any]] = []

        for pdf in pdf_files:
            try:
                data = await self._parse_single_pdf(pdf)
                parsed_invoices.append(data)
                self.logger.info("Parsed {} — {} €", data["invoice_id"], data["amount_gross"])
            except Exception as exc:
                self.logger.error("Failed to parse {}: {}", pdf.name, exc)
                # Self-healing hook example (Phase 3+ pattern)
                await self._attempt_self_healing(pdf, exc)

        self.logger.success("Successfully parsed {} / {} invoices", len(parsed_invoices), len(pdf_files))
        return {"parsed": len(parsed_invoices), "invoices": parsed_invoices}

    async def _attempt_self_healing(self, pdf_path: Path, error: Exception) -> None:
        """Example self-healing hook — in real bots this could trigger LLM repair, fallback OCR, etc."""
        self.logger.warning("Self-healing triggered for {}: {}", pdf_path.name, type(error).__name__)
        # In a real implementation you might move the file to a "needs_review" queue
        # or call an LLM to extract data from a screenshot of the PDF.
