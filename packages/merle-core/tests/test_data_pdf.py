"""
Unit tests for the PDF utilities (PdfExtractor).
"""

from __future__ import annotations

from unittest.mock import MagicMock, patch
from pathlib import Path
import pytest

from merle_core.data import PdfExtractor
from merle_core.exceptions import PdfError


def test_pdf_extractor_extract_text_success(tmp_path: Path):
    """Test extracting text from PDF file with mocked pdfplumber."""
    pdf_path = tmp_path / "dummy.pdf"
    pdf_path.touch()

    mock_pdf = MagicMock()
    mock_pdf.__enter__.return_value = mock_pdf
    mock_page = MagicMock()
    mock_page.extract_text.return_value = "Page content text"
    mock_pdf.pages = [mock_page]

    with patch("pdfplumber.open", return_value=mock_pdf) as mock_open:
        text = PdfExtractor.extract_text(pdf_path)
        assert text == "Page content text\n"
        mock_open.assert_called_once_with(pdf_path)


def test_pdf_extractor_extract_tables_success(tmp_path: Path):
    """Test extracting tables from PDF file with mocked pdfplumber."""
    pdf_path = tmp_path / "dummy.pdf"
    pdf_path.touch()

    mock_pdf = MagicMock()
    mock_pdf.__enter__.return_value = mock_pdf
    mock_page = MagicMock()
    mock_page.extract_tables.return_value = [["Row 1 Col 1", "Row 1 Col 2"]]
    mock_pdf.pages = [mock_page]

    with patch("pdfplumber.open", return_value=mock_pdf) as mock_open:
        tables = PdfExtractor.extract_tables(pdf_path)
        assert tables == [["Row 1 Col 1", "Row 1 Col 2"]]
        mock_open.assert_called_once_with(pdf_path)


def test_pdf_extractor_raises_on_missing_file():
    """Test that PdfExtractor raises PdfError when the file does not exist."""
    missing_path = Path("this_file_does_not_exist_12345.pdf")
    with pytest.raises(PdfError) as exc_info:
        PdfExtractor.extract_text(missing_path)
    assert "PDF file not found" in str(exc_info.value)
