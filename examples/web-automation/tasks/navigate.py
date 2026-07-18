"""
Task: Navigate to a target URL via Playwright (or an injected page mock).

Demonstrates BaseTask + optional browser injection for unit tests.
"""

from __future__ import annotations

from typing import Any

from merle_core import BaseTask


class NavigateTask(BaseTask):
    """Open a page at settings.target_url and return its URL/title."""

    def __init__(
        self,
        settings: Any,
        *,
        page: Any | None = None,
        name: str | None = None,
    ) -> None:
        super().__init__(settings, name=name or "Navigate")
        self._page = page

    async def execute(self) -> dict[str, Any]:
        target = str(self.settings.target_url)
        self.logger.info("Navigating to {}", target)

        if self._page is not None:
            await self._page.goto(target)
            url = getattr(self._page, "url", target)
            title = await self._page.title()
            return {"url": url, "title": title, "mode": "injected"}

        # Live path: launch browser (requires playwright extra + network)
        from merle_core.playwright import launch_robust_browser

        async with launch_robust_browser(
            headless=bool(self.settings.headless),
            stealth=bool(self.settings.stealth),
            screenshot_on_failure=bool(self.settings.screenshot_on_failure),
            failure_dir=str(self.settings.failure_dir),
        ) as browser:
            page = await browser.new_page()
            await page.goto(target)
            title = await page.title()
            return {"url": page.url, "title": title, "mode": "live"}
