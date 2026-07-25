"""
Configuration for the UiPath Hybrid example.

Uses pydantic-settings + environment variables (12-factor).
Simulate mode is the default — no real UiPath credentials required for local/CI.
"""

from __future__ import annotations

from typing import Literal

from pydantic import Field
from pydantic_settings import BaseSettings


class UiPathHybridSettings(BaseSettings):
    """All configuration for the UiPath hybrid bot."""

    bot_name: str = Field(default="uipath-hybrid", validation_alias="BOT_NAME")
    environment: Literal["dev", "staging", "prod"] = Field(
        default="dev",
        validation_alias="ENVIRONMENT",
    )

    # When True (default), no real Orchestrator HTTP calls are made.
    # Set SIMULATE=false and provide credentials for production path.
    simulate: bool = Field(default=True, validation_alias="SIMULATE")

    # Queue names
    queue_name: str = Field(default="InvoiceQueue", validation_alias="UIPATH_QUEUE_NAME")
    result_queue_name: str = Field(
        default="InvoiceResultsQueue",
        validation_alias="UIPATH_RESULT_QUEUE_NAME",
    )

    # Optional: start a UiPath job after queue processing (real mode only)
    process_key: str | None = Field(default=None, validation_alias="UIPATH_PROCESS_KEY")

    # Orchestrator credentials (required when simulate=False)
    uipath_client_id: str = Field(default="", validation_alias="UIPATH_CLIENT_ID")
    uipath_client_secret: str = Field(default="", validation_alias="UIPATH_CLIENT_SECRET")
    uipath_tenant: str = Field(default="Default", validation_alias="UIPATH_TENANT")
    uipath_base_url: str = Field(
        default="https://cloud.uipath.com",
        validation_alias="UIPATH_BASE_URL",
    )

    # Observability
    enable_tracing: bool = Field(default=False, validation_alias="ENABLE_TRACING")
    otlp_endpoint: str | None = Field(default=None, validation_alias="OTLP_ENDPOINT")

    model_config = {
        "env_file": ".env",
        "env_file_encoding": "utf-8",
        "extra": "ignore",
        "populate_by_name": True,
    }


settings = UiPathHybridSettings()
