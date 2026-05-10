"""
Test-Konfiguration und gemeinsame Fixtures.
"""

from __future__ import annotations

from collections.abc import Generator

import pytest

from config import BotSettings


@pytest.fixture
def settings() -> Generator[BotSettings, None, None]:
    """Basis-Settings für Tests (keine echten Secrets)."""
    yield BotSettings(
        bot_name="test_bot",
        environment="testing",
        log_level="DEBUG",
        target_url="https://test.example.com/api",
        api_key="test-key",
    )
