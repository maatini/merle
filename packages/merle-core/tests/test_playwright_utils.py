"""
Unit tests for merle_core.playwright.utils (robust_goto, safe_click, safe_fill).

Uses mocked Playwright Page — no real browser required.
"""

from __future__ import annotations

from unittest.mock import AsyncMock, MagicMock

from playwright.async_api import TimeoutError as PlaywrightTimeout
import pytest

from merle_core.exceptions import ElementNotFoundError
from merle_core.playwright.utils import robust_goto, safe_click, safe_fill


@pytest.fixture
def page() -> MagicMock:
    """Async-capable mocked Playwright Page for utils tests."""
    p = MagicMock()
    p.url = "https://example.com/app"
    p.goto = AsyncMock()
    p.click = AsyncMock()
    p.fill = AsyncMock()
    p.wait_for_timeout = AsyncMock()
    return p


# ─────────────────────────────────────────────────────────────
# robust_goto
# ─────────────────────────────────────────────────────────────


@pytest.mark.asyncio
async def test_robust_goto_success(page: MagicMock) -> None:
    await robust_goto(page, "https://example.com", timeout=5000, retries=1)

    page.goto.assert_awaited_once_with(
        "https://example.com",
        wait_until="domcontentloaded",
        timeout=5000,
    )


@pytest.mark.asyncio
async def test_robust_goto_retries_then_succeeds(page: MagicMock) -> None:
    page.goto = AsyncMock(side_effect=[PlaywrightTimeout("slow"), None])

    await robust_goto(page, "https://example.com", retries=2, timeout=1000)

    assert page.goto.await_count == 2
    page.wait_for_timeout.assert_awaited_once_with(2000)


@pytest.mark.asyncio
async def test_robust_goto_timeout_raises_element_not_found(page: MagicMock) -> None:
    page.goto = AsyncMock(side_effect=PlaywrightTimeout("timeout"))

    with pytest.raises(ElementNotFoundError) as exc_info:
        await robust_goto(page, "https://example.com/fail", retries=2)

    assert "Timeout beim Laden der Seite" in str(exc_info.value)
    assert page.goto.await_count == 2
    # One wait between attempt 1 and 2; no wait after final failure
    page.wait_for_timeout.assert_awaited_once_with(2000)


# ─────────────────────────────────────────────────────────────
# safe_click
# ─────────────────────────────────────────────────────────────


@pytest.mark.asyncio
async def test_safe_click_success(page: MagicMock) -> None:
    await safe_click(page, "#submit", timeout=5000, force=True)

    page.click.assert_awaited_once_with("#submit", timeout=5000, force=True)


@pytest.mark.asyncio
async def test_safe_click_timeout_raises_element_not_found(page: MagicMock) -> None:
    page.click = AsyncMock(side_effect=PlaywrightTimeout("not found"))

    with pytest.raises(ElementNotFoundError) as exc_info:
        await safe_click(page, "#missing")

    assert exc_info.value.selector == "#missing"
    assert exc_info.value.page_url == "https://example.com/app"


# ─────────────────────────────────────────────────────────────
# safe_fill
# ─────────────────────────────────────────────────────────────


@pytest.mark.asyncio
async def test_safe_fill_success(page: MagicMock) -> None:
    await safe_fill(page, "input[name=email]", "user@example.com", timeout=3000)

    page.fill.assert_awaited_once_with(
        "input[name=email]",
        "user@example.com",
        timeout=3000,
    )


@pytest.mark.asyncio
async def test_safe_fill_timeout_raises_element_not_found(page: MagicMock) -> None:
    page.fill = AsyncMock(side_effect=PlaywrightTimeout("not found"))

    with pytest.raises(ElementNotFoundError) as exc_info:
        await safe_fill(page, "#field", "value")

    assert exc_info.value.selector == "#field"
    assert exc_info.value.page_url == "https://example.com/app"
