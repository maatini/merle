"""
Common test fixtures for merle-core.
"""

from __future__ import annotations

from collections.abc import Generator
from unittest.mock import AsyncMock, MagicMock

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
    """Mocked Playwright Page for playwright tests."""
    page = MagicMock()
    page.url = "https://example.com"
    page.goto = AsyncMock()
    page.click = AsyncMock()
    page.fill = AsyncMock()
    page.screenshot = AsyncMock(return_value=b"fake-screenshot")
    page.content = AsyncMock(return_value="<html>fake</html>")
    return page


@pytest.fixture
def mock_browser_context(mock_page):
    """Mocked BrowserContext."""
    context = MagicMock()
    context.new_page = AsyncMock(return_value=mock_page)
    context.close = AsyncMock()
    return context


@pytest.fixture
def mock_browser(mock_browser_context):
    """Mocked Browser."""
    browser = MagicMock()
    browser.new_context = AsyncMock(return_value=mock_browser_context)
    browser.close = AsyncMock()
    return browser
