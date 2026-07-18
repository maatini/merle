"""
Configuration for the NATS Task Communication example.
"""

from __future__ import annotations

from typing import Literal

from pydantic import Field
from pydantic_settings import BaseSettings


class NatsExampleSettings(BaseSettings):
    """Settings for the NATS producer/consumer demo."""

    bot_name: str = Field(default="nats-task-communication", validation_alias="BOT_NAME")
    environment: Literal["dev", "staging", "prod"] = Field(default="dev", validation_alias="ENVIRONMENT")

    nats_url: str = Field(default="nats://localhost:4222", validation_alias="NATS_URL")
    nats_name: str = Field(default="nats-demo", validation_alias="NATS_NAME")
    subject: str = Field(default="tasks.web_scrape", validation_alias="NATS_SUBJECT")

    # When False, main.py refuses to start without a reachable NATS server
    require_live_nats: bool = Field(default=True, validation_alias="REQUIRE_LIVE_NATS")

    model_config = {
        "env_file": ".env",
        "env_file_encoding": "utf-8",
        "extra": "ignore",
        "populate_by_name": True,
    }


settings = NatsExampleSettings()
