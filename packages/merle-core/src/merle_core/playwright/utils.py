"""
Hilfsfunktionen für robuste Playwright-Operationen.
"""

from __future__ import annotations

from typing import Literal

from loguru import logger
from playwright.async_api import Page
from playwright.async_api import TimeoutError as PlaywrightTimeout

from merle_core.exceptions import ElementNotFoundError

WaitUntilState = Literal["commit", "domcontentloaded", "load", "networkidle"]


async def robust_goto(
    page: Page,
    url: str,
    *,
    wait_until: WaitUntilState = "domcontentloaded",
    timeout: int = 60000,
    retries: int = 2,
) -> None:
    """
    Erweiterte Version von page.goto() mit besseren Defaults und Retry.
    """
    for attempt in range(1, retries + 1):
        try:
            await page.goto(url, wait_until=wait_until, timeout=timeout)
            logger.debug("Seite erfolgreich geladen: {}", url)
            return
        except PlaywrightTimeout as exc:
            logger.warning("Timeout beim Laden von {} (Versuch {}/{})", url, attempt, retries)
            if attempt == retries:
                raise ElementNotFoundError(f"Timeout beim Laden der Seite: {url}") from exc
            await page.wait_for_timeout(2000)


async def safe_click(
    page: Page,
    selector: str,
    *,
    timeout: int = 15000,
    force: bool = False,
) -> None:
    """
    Klickt ein Element sicher und wirft eine klare Exception bei Timeout.
    """
    try:
        await page.click(selector, timeout=timeout, force=force)
    except PlaywrightTimeout as exc:
        raise ElementNotFoundError(selector, page.url) from exc


async def safe_fill(
    page: Page,
    selector: str,
    value: str,
    *,
    timeout: int = 15000,
) -> None:
    """Füllt ein Input-Feld sicher."""
    try:
        await page.fill(selector, value, timeout=timeout)
    except PlaywrightTimeout as exc:
        raise ElementNotFoundError(selector, page.url) from exc
