"""Web automation tasks package."""

from .extract_title import ExtractPageTitleTask
from .navigate import NavigateTask

__all__ = [
    "NavigateTask",
    "ExtractPageTitleTask",
]
