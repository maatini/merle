"""
Producer-side helpers: build TaskSpec payloads for web-scrape work.
"""

from __future__ import annotations

import uuid
from typing import Any

from merle_core import TaskSpec


def build_scrape_spec(
    url: str,
    *,
    selectors: list[str] | None = None,
    metadata: dict[str, Any] | None = None,
    task_id: str | None = None,
) -> TaskSpec:
    """Create a serializable TaskSpec for a web scrape job."""
    return TaskSpec(
        task_id=task_id or str(uuid.uuid4()),
        task_type="web_scrape",
        payload={
            "url": url,
            "selectors": selectors or [".title", ".price"],
        },
        metadata=metadata or {"source": "web-scraper-bot"},
    )
