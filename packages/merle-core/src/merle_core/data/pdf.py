"""
PDF utilities wrapping pdfplumber with dynamic imports and error handling.
"""

from __future__ import annotations

from pathlib import Path

from ..exceptions import PdfError


class PdfExtractor:
    """Extracts text and tables from PDF files using pdfplumber."""

    @staticmethod
    def extract_text(path: str | Path) -> str:
        """
        Extract raw text content from all pages of a PDF file.
        Import pdfplumber dynamically to keep dependencies optional.
        """
        try:
            import pdfplumber
        except ImportError as exc:
            raise PdfError(
                "pdfplumber is required for PDF text extraction but not installed. "
                "Install it using `pip install pdfplumber` or use extra `data`.",
            ) from exc

        filepath = Path(path)
        if not filepath.exists():
            raise PdfError(f"PDF file not found at path: {filepath}")

        try:
            text = ""
            with pdfplumber.open(filepath) as pdf:
                for page in pdf.pages:
                    page_text = page.extract_text() or ""
                    text += page_text + "\n"
            return text
        except Exception as exc:
            raise PdfError(f"Failed to extract text from PDF file {filepath.name}: {exc}") from exc

    @staticmethod
    def extract_tables(path: str | Path) -> list[list[list[str | None]]]:
        """
        Extract structured tables from all pages of a PDF file.
        Returns a list of tables, where each table is a list of rows, and each row is a list of cell values.
        """
        try:
            import pdfplumber
        except ImportError as exc:
            raise PdfError(
                "pdfplumber is required for PDF table extraction but not installed. "
                "Install it using `pip install pdfplumber` or use extra `data`.",
            ) from exc

        filepath = Path(path)
        if not filepath.exists():
            raise PdfError(f"PDF file not found at path: {filepath}")

        try:
            all_tables = []
            with pdfplumber.open(filepath) as pdf:
                for page in pdf.pages:
                    tables = page.extract_tables()
                    for table in tables:
                        all_tables.append(table)
            return all_tables
        except Exception as exc:
            raise PdfError(f"Failed to extract tables from PDF file {filepath.name}: {exc}") from exc
