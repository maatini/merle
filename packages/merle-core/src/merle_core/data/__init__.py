"""
Data utilities for Merle core (Excel, PDF, Email).
"""

from __future__ import annotations

from .email import EmailClient
from .excel import ExcelReader, ExcelWriter
from .pdf import PdfExtractor

__all__ = [
    "EmailClient",
    "ExcelReader",
    "ExcelWriter",
    "PdfExtractor",
]
