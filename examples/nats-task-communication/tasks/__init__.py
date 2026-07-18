"""NATS task communication helpers."""

from .processor import build_success_result, handle_scrape_spec
from .scraper import build_scrape_spec

__all__ = [
    "build_scrape_spec",
    "build_success_result",
    "handle_scrape_spec",
]
