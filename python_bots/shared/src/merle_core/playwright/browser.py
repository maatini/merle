"""
Robust Playwright Browser Wrapper.

Bietet einen sicheren, stealth-fähigen und fehlertoleranten Browser-Kontext für RPA-Bots.
"""

from __future__ import annotations

from contextlib import asynccontextmanager
from datetime import datetime
from pathlib import Path
from typing import Any

from loguru import logger

from playwright.async_api import Browser, BrowserContext, Page, async_playwright

from merle_core.exceptions import (
    BrowserLaunchError,
)


class RobustBrowser:
    """
    Wrapper um Playwright Browser mit RPA-spezifischen Verbesserungen.

    Features:
    - Automatisches Stealth
    - Proxy-Unterstützung
    - Auto-Screenshot + HTML-Dump bei Fehlern
    - Bessere Timeouts und Defaults für RPA
    """

    def __init__(
        self,
        browser: Browser,
        context: BrowserContext,
        *,
        screenshot_on_failure: bool = True,
        failure_dir: str | Path = "logs/failures",
    ):
        self.browser = browser
        self.context = context
        self.screenshot_on_failure = screenshot_on_failure
        self.failure_dir = Path(failure_dir)
        self._pages: list[Page] = []

    async def new_page(self) -> Page:
        """Erstellt eine neue Page mit verbesserten Defaults."""
        page = await self.context.new_page()

        # RPA-freundliche Defaults
        page.set_default_timeout(30000)
        page.set_default_navigation_timeout(60000)

        self._pages.append(page)
        return page

    async def close(self) -> None:
        """Schließt alle Pages und den Context sauber."""
        for page in self._pages:
            try:
                await page.close()
            except Exception:
                pass

        try:
            await self.context.close()
            await self.browser.close()
        except Exception:
            pass

    async def __aenter__(self):
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        if exc_type is not None and self.screenshot_on_failure:
            await self._capture_failure_artifacts(exc_val)

        await self.close()

    async def _capture_failure_artifacts(self, exception: Exception) -> None:
        """Erstellt bei Fehlern automatisch Screenshots und HTML-Dumps."""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        failure_path = self.failure_dir / timestamp
        failure_path.mkdir(parents=True, exist_ok=True)

        logger.error("Fehler erkannt – erstelle Failure-Artifacts in {}", failure_path)

        for i, page in enumerate(self._pages):
            try:
                url = page.url
                safe_url = url.replace("://", "_").replace("/", "_")[:80]

                # Screenshot
                screenshot_path = failure_path / f"page_{i}_{safe_url}.png"
                await page.screenshot(path=str(screenshot_path), full_page=True)

                # HTML
                html_path = failure_path / f"page_{i}_{safe_url}.html"
                html = await page.content()
                html_path.write_text(html, encoding="utf-8")

                logger.warning(
                    "Failure Artifact erstellt | page={} | screenshot={} | html={}",
                    i,
                    screenshot_path,
                    html_path,
                )

            except Exception as capture_exc:
                logger.exception("Konnte Failure-Artifact nicht erstellen: {}", capture_exc)


@asynccontextmanager
async def launch_robust_browser(
    *,
    headless: bool = True,
    slow_mo: int = 50,
    proxy: str | None = None,
    stealth: bool = True,
    user_agent: str | None = None,
    viewport: dict[str, int] | None = None,
    screenshot_on_failure: bool = True,
    failure_dir: str = "logs/failures",
    **launch_kwargs: Any,
):
    """
    Launcht einen robusten Playwright Browser mit guten RPA-Defaults.

    Args:
        headless: Headless-Modus
        slow_mo: Verzögerung zwischen Aktionen (ms)
        proxy: Proxy-URL (z.B. "http://user:pass@proxy.company:8080")
        stealth: Stealth-Techniken aktivieren (Anti-Detection)
        user_agent: Benutzerdefinierter User-Agent
        viewport: Viewport-Größe
        screenshot_on_failure: Bei Fehlern automatisch Screenshots machen
        failure_dir: Ordner für Failure-Artifacts
    """
    proxy_config = {"server": proxy} if proxy else None

    default_user_agent = (
        user_agent
        or "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
        "(KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36"
    )

    default_viewport = viewport or {"width": 1920, "height": 1080}

    async with async_playwright() as p:
        try:
            browser = await p.chromium.launch(
                headless=headless,
                slow_mo=slow_mo,
                proxy=proxy_config,
                args=[
                    "--disable-blink-features=AutomationControlled",
                    "--no-sandbox",
                    "--disable-dev-shm-usage",
                ],
                **launch_kwargs,
            )
        except Exception as exc:
            raise BrowserLaunchError(f"Browser konnte nicht gestartet werden: {exc}") from exc

        context_options: dict[str, Any] = {
            "user_agent": default_user_agent,
            "viewport": default_viewport,
            "ignore_https_errors": True,
        }

        context = await browser.new_context(**context_options)

        # Stealth aktivieren
        if stealth:
            await _apply_stealth(context)

        robust_browser = RobustBrowser(
            browser,
            context,
            screenshot_on_failure=screenshot_on_failure,
            failure_dir=failure_dir,
        )

        try:
            yield robust_browser
        finally:
            await robust_browser.close()


async def _apply_stealth(context: BrowserContext) -> None:
    """
    Wendet grundlegende Stealth-Techniken an, um Bot-Erkennung zu erschweren.
    """
    await context.add_init_script("""
        // Entferne webdriver Flag
        Object.defineProperty(navigator, 'webdriver', { get: () => undefined });

        // Überschreibe permissions
        const originalQuery = window.navigator.permissions.query;
        window.navigator.permissions.query = (parameters) => (
            parameters.name === 'notifications' ?
                Promise.resolve({ state: Notification.permission }) :
                originalQuery(parameters)
        );

        // Entferne Chrome Automation
        delete window.cdc_adoQpoasnfa76pfcZLmcfl_Array;
        delete window.cdc_adoQpoasnfa76pfcZLmcfl_Promise;
        delete window.cdc_adoQpoasnfa76pfcZLmcfl_Symbol;
    """)

    logger.debug("Stealth-Mode für Playwright Context aktiviert")
