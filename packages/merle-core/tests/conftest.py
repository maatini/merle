"""
Common test fixtures for merle-core.
"""

from __future__ import annotations

from unittest.mock import AsyncMock, MagicMock, patch

import pytest


class FakeSettings:
    """Minimal fake settings object for testing BaseBot / BaseTask."""

    def __init__(self, bot_name: str = "test_bot", environment: str = "testing"):
        self.bot_name = bot_name
        self.environment = environment


@pytest.fixture
def fake_settings() -> FakeSettings:
    return FakeSettings(bot_name="test_invoice_bot", environment="test")


@pytest.fixture
def mock_page():
    """Fully async-capable mocked Playwright Page."""
    page = MagicMock()
    page.url = "https://example.com"
    page.goto = AsyncMock()
    page.click = AsyncMock()
    page.fill = AsyncMock()
    page.screenshot = AsyncMock(return_value=b"fake-screenshot")
    page.content = AsyncMock(return_value="<html>fake</html>")
    page.title = AsyncMock(return_value="Mock Page Title")
    page.set_default_timeout = MagicMock()
    page.set_default_navigation_timeout = MagicMock()
    page.add_init_script = AsyncMock()
    return page


@pytest.fixture
def mock_browser_context(mock_page):
    """Fully async-capable mocked BrowserContext (supports add_init_script + new_page)."""
    context = MagicMock()
    context.new_page = AsyncMock(return_value=mock_page)
    context.close = AsyncMock()
    context.add_init_script = AsyncMock()  # Critical for _apply_stealth
    return context


@pytest.fixture
def mock_browser(mock_browser_context):
    """Fully async-capable mocked Browser (works for both chromium.launch and connect_over_cdp)."""
    browser = MagicMock()
    browser.new_context = AsyncMock(return_value=mock_browser_context)
    browser.close = AsyncMock()
    return browser


# ─────────────────────────────────────────────────────────────
# Lightpanda-specific fixtures
# ─────────────────────────────────────────────────────────────


class FakeLightpandaProcess:
    """Fake object returned by lightpanda.serve() for testing."""

    def __init__(self, pid: int = 12345):
        self.pid = pid
        self.terminate_called = False
        self.kill_called = False
        self.wait_called = False

    def terminate(self):
        self.terminate_called = True

    def kill(self):
        self.kill_called = True

    def wait(self, timeout=None):
        self.wait_called = True
        return 0


@pytest.fixture
def fake_lightpanda_proc():
    """Returns a controllable fake lightpanda process."""
    return FakeLightpandaProcess()


@pytest.fixture
def mock_lightpanda_serve(fake_lightpanda_proc):
    """Patches lightpanda.serve to return a fake process."""
    with patch("lightpanda.serve", return_value=fake_lightpanda_proc) as mock_serve:
        yield mock_serve, fake_lightpanda_proc


@pytest.fixture
def mock_connect_over_cdp(mock_browser):
    """Patches playwright.chromium.connect_over_cdp."""
    with patch("playwright.async_api.Playwright.chromium") as mock_chromium:
        mock_chromium.connect_over_cdp = AsyncMock(return_value=mock_browser)
        yield mock_chromium
