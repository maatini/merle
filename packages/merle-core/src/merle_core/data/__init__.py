"""
Data utilities for Merle core (Excel, PDF, Email).
"""

from __future__ import annotations

from .excel import ExcelReader, ExcelWriter
from .pdf import PdfExtractor
from .email import EmailClient

__all__ = [
    "ExcelReader",
    "ExcelWriter",
    "PdfExtractor",
    "EmailClient",
]
