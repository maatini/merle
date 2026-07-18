"""
Unit tests for the Web Automation Bot (no live browser / network).

Uses an AsyncMock page so CI can run without Playwright browsers installed.
Mark live browser scenarios with @pytest.mark.integration.
"""

from __future__ import annotations

import sys
from pathlib import Path
from unittest.mock import AsyncMock, MagicMock

import pytest

# Isolate this example's modules from other examples/* (shared names: config, tasks, main)
_EXAMPLE_ROOT = Path(__file__).resolve().parent.parent
for _key in list(sys.modules):
    if _key in ("config", "main", "tasks") or _key.startswith("tasks."):
        del sys.modules[_key]
sys.path = [p for p in sys.path if Path(p).resolve() != _EXAMPLE_ROOT]
sys.path.insert(0, str(_EXAMPLE_ROOT))

from config import WebBotSettings  # noqa: E402
from main import WebAutomationBot  # noqa: E402
from tasks import ExtractPageTitleTask, NavigateTask  # noqa: E402


@pytest.fixture
def mock_settings(tmp_path: Path) -> WebBotSettings:
    return WebBotSettings(
        bot_name="web-automation-test",
        environment="dev",
        target_url="https://example.com",
        headless=True,
        stealth=False,
        screenshot_on_failure=True,
        failure_dir=tmp_path / "failures",
        enable_tracing=False,
    )


@pytest.fixture
def mock_page() -> AsyncMock:
    page = AsyncMock()
    page.url = "https://example.com/"
    page.goto = AsyncMock(return_value=None)
    page.title = AsyncMock(return_value="Example Domain")
    h1 = AsyncMock()
    h1.inner_text = AsyncMock(return_value="Example Domain")
    page.locator = MagicMock(return_value=h1)
    return page


@pytest.mark.asyncio
async def test_navigate_with_injected_page(mock_settings: WebBotSettings, mock_page: AsyncMock) -> None:
    task = NavigateTask(mock_settings, page=mock_page)
    result = await task.run()

    mock_page.goto.assert_awaited_once_with("https://example.com")
    assert result["title"] == "Example Domain"
    assert result["mode"] == "injected"
    assert result["url"] == "https://example.com/"


@pytest.mark.asyncio
async def test_extract_title_from_page(mock_settings: WebBotSettings, mock_page: AsyncMock) -> None:
    task = ExtractPageTitleTask(mock_settings, page=mock_page)
    result = await task.run()

    assert result["title"] == "Example Domain"
    assert result["heading"] == "Example Domain"
    assert result["source"] == "page"


@pytest.mark.asyncio
async def test_extract_title_from_navigation_result(
    mock_settings: WebBotSettings,
) -> None:
    nav = {"title": "From Nav", "url": "https://example.com"}
    task = ExtractPageTitleTask(mock_settings, navigation_result=nav)
    result = await task.run()

    assert result["title"] == "From Nav"
    assert result["source"] == "navigation_result"


@pytest.mark.asyncio
async def test_bot_pipeline_with_mock_page(
    mock_settings: WebBotSettings, mock_page: AsyncMock, monkeypatch: pytest.MonkeyPatch
) -> None:
    # Point module-level settings used by WebAutomationBot to test settings
    import config as config_mod
    import main as main_mod

    monkeypatch.setattr(config_mod, "settings", mock_settings)
    monkeypatch.setattr(main_mod, "settings", mock_settings)

    bot = WebAutomationBot(page=mock_page)
    result = await bot.run()

    assert result["title"] == "Example Domain"
    assert result["mode"] == "injected"
    assert bot.status == "success"
    health = bot.health_check()
    assert health["status"] == "healthy"


@pytest.mark.integration
@pytest.mark.asyncio
async def test_live_navigate_optional(mock_settings: WebBotSettings) -> None:
    """Live browser path — skipped in default CI unless integration selected."""
    pytest.importorskip("playwright")
    task = NavigateTask(mock_settings, page=None)
    # This hits the network; only run when explicitly requested
    result = await task.run()
    assert "title" in result
