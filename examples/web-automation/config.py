"""
Configuration for the Web Automation Bot.

Uses pydantic-settings + environment variables (12-factor).
"""

from __future__ import annotations

from pathlib import Path
from typing import Literal

from pydantic import Field
from pydantic_settings import BaseSettings


class WebBotSettings(BaseSettings):
    """All configuration for the web automation bot."""

    bot_name: str = Field(default="web-automation", validation_alias="BOT_NAME")
    environment: Literal["dev", "staging", "prod"] = Field(default="dev", validation_alias="ENVIRONMENT")

    # Target page
    target_url: str = Field(
        default="https://httpbin.org/html",
        validation_alias="TARGET_URL",
    )

    # Browser
    headless: bool = Field(default=True, validation_alias="HEADLESS")
    stealth: bool = Field(default=True, validation_alias="STEALTH")
    screenshot_on_failure: bool = Field(default=True, validation_alias="SCREENSHOT_ON_FAILURE")
    failure_dir: Path = Field(
        default=Path("./logs/failures"),
        validation_alias="FAILURE_DIR",
    )

    # Observability
    enable_tracing: bool = Field(default=False, validation_alias="ENABLE_TRACING")
    otlp_endpoint: str | None = Field(default=None, validation_alias="OTLP_ENDPOINT")

    # Retry
    max_retries: int = Field(default=3, validation_alias="MAX_RETRIES")

    model_config = {
        "env_file": ".env",
        "env_file_encoding": "utf-8",
        "extra": "ignore",
        "populate_by_name": True,
    }


settings = WebBotSettings()
