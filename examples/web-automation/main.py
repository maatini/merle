"""
Beispiel: Web-Automatisierung mit merle-core Playwright Wrapper.

Zeigt:
- launch_robust_browser mit Stealth
- BaseTask + Retry
- Automatische Failure Artifacts
"""

import asyncio
from loguru import logger

from merle_core import BaseTask
from merle_core.observability import configure_observability
from merle_core.playwright import launch_robust_browser, safe_click, safe_fill


class LoginAndExtractTask(BaseTask):
    async def execute(self) -> dict:
        async with launch_robust_browser(
            headless=True,
            stealth=True,
            screenshot_on_failure=True,
        ) as browser:
            page = await browser.new_page()

            await page.goto("https://httpbin.org/html")  # Demo-Seite

            # In einem realen Szenario: Login + Daten extrahieren
            title = await page.title()
            self.logger.info("Seite geladen: {}", title)

            return {"status": "success", "page_title": title}


async def main():
    configure_observability(service_name="web-automation-example")

    task = LoginAndExtractTask(settings=type("Settings", (), {"bot_name": "web_demo"})())
    result = await task.run()

    logger.info("Ergebnis: {}", result)


if __name__ == "__main__":
    asyncio.run(main())
