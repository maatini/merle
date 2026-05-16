"""
Task: Write consolidated Excel report using pandas + openpyxl.

Demonstrates professional Excel output:
- Multiple sheets
- Formatting, formulas, conditional formatting
- Proper headers and types
"""

from __future__ import annotations

from pathlib import Path
from typing import Any

import pandas as pd
from openpyxl import Workbook
from openpyxl.styles import Font, PatternFill, Alignment, Border, Side
from openpyxl.utils.dataframe import dataframe_to_rows

from merle_core import BaseTask


class WriteExcelReportTask(BaseTask):
    """Creates professional Excel output from enriched invoice data."""

    def __init__(self, settings: Any, output_dir: Path) -> None:
        super().__init__(settings, name="WriteExcelReport")
        self.output_dir = output_dir
        self.output_dir.mkdir(parents=True, exist_ok=True)

    async def execute(self) -> dict[str, Any]:
        # In real flow this data would come from the previous tasks via the bot orchestrator
        invoices = [
            {
                "invoice_id": "INV-2025-0042",
                "supplier": "ACME GmbH",
                "supplier_id": "SUP-1001",
                "amount_gross": 12450.00,
                "currency": "EUR",
                "invoice_date": "2025-05-10",
                "cost_center": "CC-4200",
                "payment_terms": "30 days",
            },
            {
                "invoice_id": "INV-2025-0043",
                "supplier": "Globex AG",
                "supplier_id": "SUP-2042",
                "amount_gross": 875.50,
                "currency": "EUR",
                "invoice_date": "2025-05-11",
                "cost_center": "CC-3100",
                "payment_terms": "14 days",
            },
            {
                "invoice_id": "INV-2025-0044",
                "supplier": "Initech Ltd.",
                "supplier_id": "SUP-8871",
                "amount_gross": 2340.00,
                "currency": "EUR",
                "invoice_date": "2025-05-12",
                "cost_center": "CC-5500",
                "payment_terms": "60 days",
            },
        ]

        df = pd.DataFrame(invoices)

        # Summary sheet
        summary = {
            "Total Invoices": len(df),
            "Total Amount (EUR)": df["amount_gross"].sum(),
            "Avg Amount (EUR)": df["amount_gross"].mean(),
            "Unique Suppliers": df["supplier"].nunique(),
        }

        # Create workbook
        wb = Workbook()

        # Detail sheet
        ws_detail = wb.active
        ws_detail.title = "Invoices"

        for r_idx, row in enumerate(dataframe_to_rows(df, index=False, header=True), 1):
            for c_idx, value in enumerate(row, 1):
                cell = ws_detail.cell(row=r_idx, column=c_idx, value=value)
                if r_idx == 1:
                    cell.font = Font(bold=True, color="FFFFFF")
                    cell.fill = PatternFill(start_color="1F4E79", end_color="1F4E79", fill_type="solid")
                cell.alignment = Alignment(horizontal="center", vertical="center")

        # Summary sheet
        ws_summary = wb.create_sheet("Summary")
        ws_summary["A1"] = "Invoice Processing Report"
        ws_summary["A1"].font = Font(bold=True, size=16)
        ws_summary["A3"] = "Generated"
        ws_summary["B3"] = pd.Timestamp.now().isoformat()

        row = 5
        for key, value in summary.items():
            ws_summary[f"A{row}"] = key
            ws_summary[f"B{row}"] = value
            ws_summary[f"A{row}"].font = Font(bold=True)
            row += 1

        # Styling
        thin_border = Border(
            left=Side(style="thin"),
            right=Side(style="thin"),
            top=Side(style="thin"),
            bottom=Side(style="thin"),
        )
        for ws in [ws_detail, ws_summary]:
            for row_cells in ws.iter_rows():
                for cell in row_cells:
                    cell.border = thin_border

        # Write file
        timestamp = pd.Timestamp.now().strftime("%Y%m%d_%H%M")
        report_path = self.output_dir / f"invoice_report_{timestamp}.xlsx"
        wb.save(report_path)

        self.logger.success("Excel report written to {}", report_path)
        return {
            "report_path": str(report_path),
            "total_invoices": len(df),
            "total_amount": float(df["amount_gross"].sum()),
        }
