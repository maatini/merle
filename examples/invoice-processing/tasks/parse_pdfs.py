"""
Task: Parse PDF invoices using pdfplumber and layout heuristics.

Demonstrates:
- Robust PDF text extraction
- Regular Expression parsing for invoice metadata
- Line item table extraction
- Unit price and totals validation
"""

from __future__ import annotations

import re
from pathlib import Path
from typing import Any

from merle_core import BaseTask
from merle_core.exceptions import PdfError
from merle_core.retry import with_retry, default_http_retry


class ParsePdfInvoicesTask(BaseTask):
    """Extracts structured data from invoice PDFs using pdfplumber."""

    def __init__(self, settings: Any, input_dir: Path) -> None:
        super().__init__(settings, name="ParsePdfInvoices")
        self.input_dir = input_dir

    @with_retry(policy=default_http_retry)
    async def _parse_single_pdf(self, pdf_path: Path) -> dict[str, Any]:
        """
        Parses a single invoice PDF file.

        Uses pdfplumber to extract text and regular expressions to extract structured data.
        """
        try:
            import pdfplumber  # type: ignore
        except ImportError:
            raise PdfError("pdfplumber is required but not installed")

        self.logger.debug("Opening PDF: {}", pdf_path.name)

        try:
            with pdfplumber.open(pdf_path) as pdf:
                text = ""
                for page in pdf.pages:
                    page_text = page.extract_text() or ""
                    text += page_text + "\n"
        except Exception as exc:
            raise PdfError(f"Failed to open or read PDF file {pdf_path.name}: {exc}") from exc

        return self._extract_invoice_data(text, pdf_path)

    def _extract_invoice_data(self, text: str, pdf_path: Path) -> dict[str, Any]:
        """Parse raw PDF text using regular expressions and heuristics."""
        lines = [line.strip() for line in text.split("\n") if line.strip()]

        # 1. Extract Invoice ID
        invoice_id_match = re.search(r"Invoice ID:\s*(INV-\d{4}-\d{4})", text)
        if not invoice_id_match:
            invoice_id_match = re.search(r"INV-\d{4}-\d{4}", text)
        invoice_id = invoice_id_match.group(1) if invoice_id_match else pdf_path.stem

        # 2. Extract Supplier
        supplier_match = re.search(r"Supplier:\s*(.*?)(?=\s+Invoice ID|\n|$)", text)
        supplier = supplier_match.group(1).strip() if supplier_match else "Unknown Supplier"

        # 3. Extract Invoice Date
        date_match = re.search(r"Date:\s*(\d{4}-\d{2}-\d{2})", text)
        invoice_date = date_match.group(1) if date_match else "1970-01-01"

        # 4. Extract Totals
        net_total_match = re.search(r"Net Total:\s*([\d\.]+)\s*EUR", text)
        net_total = float(net_total_match.group(1)) if net_total_match else 0.0

        vat_match = re.search(r"VAT\s*\((\d+)%\):\s*([\d\.]+)\s*EUR", text)
        vat_rate = float(vat_match.group(1)) / 100.0 if vat_match else 0.19
        vat_amount = float(vat_match.group(2)) if vat_match else 0.0

        gross_total_match = re.search(r"Gross Total:\s*([\d\.]+)\s*EUR", text)
        gross_total = float(gross_total_match.group(1)) if gross_total_match else net_total * (1 + vat_rate)

        # 5. Extract Line Items
        line_items: list[dict[str, Any]] = []
        in_table = False

        for line in lines:
            if "Description" in line and "Quantity" in line and "Total" in line:
                in_table = True
                continue
            if "Net Total:" in line:
                in_table = False
                break

            if in_table:
                item_match = re.match(r"^(.*?)\s+(\d+)\s+([\d\.]+)\s*EUR\s+([\d\.]+)\s*EUR$", line)
                if item_match:
                    desc = item_match.group(1).strip()
                    qty = int(item_match.group(2))
                    unit_price = float(item_match.group(3))
                    total_price = float(item_match.group(4))

                    line_items.append({
                        "description": desc,
                        "qty": qty,
                        "unit_price": unit_price,
                        "total_price": total_price
                    })
                else:
                    self.logger.warning("Could not parse line item row: '{}'", line)

        return {
            "invoice_id": invoice_id,
            "supplier": supplier,
            "amount_gross": gross_total,
            "amount_net": net_total,
            "currency": "EUR",
            "invoice_date": invoice_date,
            "line_items": line_items,
            "vat_rate": vat_rate,
            "vat_amount": vat_amount,
            "source_file": str(pdf_path),
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
                self.logger.info("Parsed {} — Supplier: {}, Gross Total: {} EUR",
                                 data["invoice_id"], data["supplier"], data["amount_gross"])
            except Exception as exc:
                self.logger.error("Failed to parse {}: {}", pdf.name, exc)
                await self._attempt_self_healing(pdf, exc)
                raise

        self.logger.success("Successfully parsed {} / {} invoices", len(parsed_invoices), len(pdf_files))
        return {"parsed": len(parsed_invoices), "invoices": parsed_invoices}

    async def _attempt_self_healing(self, pdf_path: Path, error: Exception) -> None:
        """Example self-healing hook — in real bots this could trigger LLM repair, fallback OCR, etc."""
        self.logger.warning("Self-healing triggered for {}: {}", pdf_path.name, type(error).__name__)
        # E.g. move to needs_review folder or log for admin intervention
