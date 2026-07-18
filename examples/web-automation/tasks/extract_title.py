"""
Task: Extract the page title (and optional H1) from an already-open page mock
or by running a lightweight fetch simulation.

Used to demo multi-task BaseBot pipelines without a live browser when a page
mock is injected.
"""

from __future__ import annotations

from typing import Any

from merle_core import BaseTask


class ExtractPageTitleTask(BaseTask):
    """Extract title / heading text from a page object or prior navigation result."""

    def __init__(
        self,
        settings: Any,
        *,
        page: Any | None = None,
        navigation_result: dict[str, Any] | None = None,
        name: str | None = None,
    ) -> None:
        super().__init__(settings, name=name or "ExtractPageTitle")
        self._page = page
        self._nav = navigation_result or {}

    async def execute(self) -> dict[str, Any]:
        if self._page is not None:
            title = await self._page.title()
            heading = ""
            try:
                # Optional H1 — mocks can implement or skip
                locator = self._page.locator("h1")
                if hasattr(locator, "inner_text"):
                    heading = await locator.inner_text()
            except Exception:
                heading = ""
            self.logger.info("Extracted title={!r} heading={!r}", title, heading)
            return {
                "title": title,
                "heading": heading,
                "source": "page",
            }

        # Fallback: reuse navigation result (no browser needed)
        title = self._nav.get("title", "")
        self.logger.info("Using title from navigation result: {!r}", title)
        return {
            "title": title,
            "heading": "",
            "source": "navigation_result",
        }
