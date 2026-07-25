#!/usr/bin/env python3
"""
Merle Web Automation Bot — Gold Reference Example

Demonstrates:
- BaseBot as lifecycle orchestrator
- Multiple fine-grained BaseTask classes (Navigate → Extract)
- pydantic-settings configuration
- Playwright robust browser + failure artifacts (live path)
- Injectable page mocks for unit tests (no live browser required)
"""

from __future__ import annotations

import asyncio
from typing import Any

from loguru import logger

from config import settings
from merle_core import BaseBot, configure_observability
from tasks import ExtractPageTitleTask, NavigateTask


class WebAutomationBot(BaseBot):
    """Orchestrates a simple navigate → extract pipeline."""

    def __init__(self, *, page: Any | None = None) -> None:
        super().__init__(settings, name="web-automation")
        settings.failure_dir.mkdir(parents=True, exist_ok=True)
        self._page = page

    async def execute(self) -> dict[str, Any]:
        self.logger.info(
            "Starting web automation (env={}, url={})",
            settings.environment,
            settings.target_url,
        )

        nav = NavigateTask(settings, page=self._page)
        nav_res = await nav.run()

        extract = ExtractPageTitleTask(
            settings,
            page=self._page,
            navigation_result=nav_res,
        )
        extract_res = await extract.run()

        return {
            "url": nav_res.get("url"),
            "title": extract_res.get("title"),
            "heading": extract_res.get("heading"),
            "mode": nav_res.get("mode"),
        }

    def _on_success(self, result: dict[str, Any]) -> None:
        self.logger.success("Web automation completed: title={!r}", result.get("title"))

    def _on_failure(self, exception: Exception) -> None:
        self.logger.error(
            "Web automation failed (artifacts in {}): {}",
            settings.failure_dir,
            exception,
        )


async def main() -> None:
    if settings.enable_tracing and configure_observability is not None:
        try:
            configure_observability(
                service_name="merle-web-automation-bot",
                service_version="0.1.0",
                otlp_endpoint=settings.otlp_endpoint,
                enable_tracing=True,
                enable_metrics=False,
                resource_attributes={"deployment.environment": settings.environment},
            )
        except Exception as e:
            logger.warning("Observability partially disabled: {}", e)

    bot = WebAutomationBot()
    result = await bot.run()
    logger.info("Final result: {}", result)
    logger.info("Health: {}", bot.health_check())


if __name__ == "__main__":
    asyncio.run(main())
