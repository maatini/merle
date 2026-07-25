"""
Robust Playwright Browser Wrapper.

Bietet einen sicheren, stealth-fähigen und fehlertoleranten Browser-Kontext für RPA-Bots.
"""

from __future__ import annotations

import asyncio
from collections.abc import AsyncIterator
from contextlib import asynccontextmanager
from datetime import datetime
from pathlib import Path
from types import TracebackType
from typing import Any, Literal

from loguru import logger
from playwright.async_api import Browser, BrowserContext, Page, async_playwright

from merle_core.exceptions import BrowserLaunchError

BrowserEngine = Literal["chromium", "lightpanda"]


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
    ) -> None:
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

    async def __aenter__(self) -> RobustBrowser:
        return self

    async def __aexit__(
        self,
        exc_type: type[BaseException] | None,
        exc_val: BaseException | None,
        exc_tb: TracebackType | None,
    ) -> None:
        if exc_type is not None and self.screenshot_on_failure:
            await self._capture_failure_artifacts(exc_val)

        await self.close()

    async def _capture_failure_artifacts(self, exception: BaseException | None) -> None:
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
    engine: BrowserEngine = "chromium",
    headless: bool = True,
    slow_mo: int = 50,
    proxy: str | None = None,
    stealth: bool = True,
    user_agent: str | None = None,
    viewport: dict[str, int] | None = None,
    screenshot_on_failure: bool = True,
    failure_dir: str = "logs/failures",
    # Lightpanda-spezifisch
    lightpanda_host: str = "127.0.0.1",
    lightpanda_port: int = 9222,
    lightpanda_log_level: str = "error",
    **launch_kwargs: Any,
) -> AsyncIterator[RobustBrowser]:
    """
    Launcht einen robusten Playwright Browser (Chromium oder Lightpanda via CDP).

    Lightpanda ist eine hochperformante, ressourcenschonende Zig-basierte
    Alternative zu Chromium – ideal für hochvolumige, cloud-native Automatisierung.

    Args:
        engine: "chromium" (Default, maximale Kompatibilität) oder "lightpanda"
        headless: Headless-Modus (nur bei chromium relevant)
        slow_mo: Verzögerung zwischen Aktionen (ms) – nur chromium
        proxy: Proxy-URL
        stealth: Stealth-Techniken aktivieren (funktioniert bei beiden Engines)
        user_agent, viewport, screenshot_on_failure, failure_dir: wie bisher
        lightpanda_host / lightpanda_port / lightpanda_log_level: Lightpanda CDP Server
    """
    default_user_agent = (
        user_agent
        or "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
        "(KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36"
    )
    default_viewport = viewport or {"width": 1920, "height": 1080}

    lp_proc: Any | None = None
    browser: Browser | None = None
    context: BrowserContext | None = None

    try:
        async with async_playwright() as p:
            if engine == "lightpanda":
                browser, lp_proc = await _connect_lightpanda(
                    p,
                    host=lightpanda_host,
                    port=lightpanda_port,
                    log_level=lightpanda_log_level,
                    proxy=proxy,
                )
            else:
                browser = await _launch_chromium(
                    p,
                    headless=headless,
                    slow_mo=slow_mo,
                    proxy=proxy,
                    **launch_kwargs,
                )

            context_options: dict[str, Any] = {
                "user_agent": default_user_agent,
                "viewport": default_viewport,
                "ignore_https_errors": True,
            }
            if proxy and engine == "lightpanda":
                context_options["proxy"] = {"server": proxy}

            context = await browser.new_context(**context_options)

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
                if context:
                    try:
                        await context.close()
                    except Exception:
                        pass
                if browser:
                    try:
                        await browser.close()
                    except Exception:
                        pass
                if lp_proc is not None:
                    try:
                        lp_proc.terminate()
                        await asyncio.wait_for(asyncio.to_thread(lp_proc.wait), timeout=5.0)
                    except Exception:
                        try:
                            lp_proc.kill()
                        except Exception:
                            pass

    except Exception as exc:
        if lp_proc is not None:
            try:
                lp_proc.kill()
            except Exception:
                pass
        raise BrowserLaunchError(f"{engine} Browser konnte nicht gestartet werden: {exc}") from exc


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


# ─────────────────────────────────────────────────────────────
# Interne Engine-Helper (nicht öffentlich)
# ─────────────────────────────────────────────────────────────


async def _launch_chromium(
    playwright: Any,
    *,
    headless: bool,
    slow_mo: int,
    proxy: str | None,
    **launch_kwargs: Any,
) -> Browser:
    """Startet einen lokalen Chromium-Prozess (bisheriges Verhalten)."""
    proxy_config = {"server": proxy} if proxy else None
    try:
        browser: Browser = await playwright.chromium.launch(
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
        return browser
    except Exception as exc:
        raise BrowserLaunchError(f"Chromium konnte nicht gestartet werden: {exc}") from exc


async def _connect_lightpanda(
    playwright: Any,
    *,
    host: str,
    port: int,
    log_level: str,
    proxy: str | None,
) -> tuple[Browser, Any]:
    """
    Startet den Lightpanda CDP Server und verbindet sich via connect_over_cdp.
    Gibt (Browser, lightpanda_process) zurück.
    """
    try:
        import lightpanda
    except ImportError as exc:
        raise BrowserLaunchError(
            "lightpanda-py ist nicht installiert. Installiere mit: uv add 'merle-core[lightpanda]'"
        ) from exc

    lp_proc = lightpanda.serve(host=host, port=port, log_level=log_level)

    # Robuster Readiness-Check statt festem Sleep
    await _wait_for_lightpanda_ready(host, port, timeout=20.0)

    endpoint = f"http://{host}:{port}"
    try:
        browser: Browser = await playwright.chromium.connect_over_cdp(endpoint)
        logger.info("Lightpanda CDP erfolgreich verbunden: {}", endpoint)
        return browser, lp_proc
    except Exception as exc:
        try:
            lp_proc.kill()
        except Exception:
            pass
        raise BrowserLaunchError(f"Verbindung zu Lightpanda CDP fehlgeschlagen: {exc}") from exc


async def _wait_for_lightpanda_ready(
    host: str,
    port: int,
    *,
    timeout: float = 15.0,
    poll_interval: float = 0.25,
) -> None:
    """
    Pollt den Lightpanda CDP Endpoint (/json/version), bis der Server bereit ist.
    Verwendet httpx (bereits Core-Dependency).
    """
    import httpx

    url = f"http://{host}:{port}/json/version"
    deadline = asyncio.get_running_loop().time() + timeout

    async with httpx.AsyncClient(timeout=httpx.Timeout(2.0)) as client:
        while True:
            try:
                resp = await client.get(url)
                if resp.status_code == 200:
                    logger.debug("Lightpanda CDP Server bereit auf {}:{}", host, port)
                    return
            except Exception:
                pass  # Server noch nicht bereit oder Netzwerk-Transient

            if asyncio.get_running_loop().time() > deadline:
                raise BrowserLaunchError(f"Lightpanda CDP Server auf {host}:{port} nicht bereit nach {timeout}s")
            await asyncio.sleep(poll_interval)
