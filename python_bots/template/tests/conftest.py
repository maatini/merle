"""
Test-Konfiguration und gemeinsame Fixtures.
"""

import pytest
from config import BotSettings


@pytest.fixture
def settings() -> BotSettings:
    """Basis-Settings für Tests (keine echten Secrets)."""
    return BotSettings(
        bot_name="test_bot",
        environment="testing",
        log_level="DEBUG",
        target_url="https://test.example.com/api",
        api_key="test-key",
    )
