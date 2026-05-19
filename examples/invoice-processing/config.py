"""
Configuration for the Invoice Processing Bot.

Uses pydantic-settings (via merle-core) + environment variables.
"""

from __future__ import annotations

from pathlib import Path
from typing import Literal

from pydantic import Field
from pydantic_settings import BaseSettings


class InvoiceBotSettings(BaseSettings):
    """All configuration for the invoice processing bot."""

    # Identity (required by BaseBot governance)
    bot_name: str = Field(default="invoice-processing", validation_alias="BOT_NAME")

    # Environment
    environment: Literal["dev", "staging", "prod"] = Field(default="dev", validation_alias="ENVIRONMENT")

    # Paths
    input_dir: Path = Field(default=Path("./data/invoices"), validation_alias="INPUT_DIR")
    output_dir: Path = Field(default=Path("./data/reports"), validation_alias="OUTPUT_DIR")
    archive_dir: Path = Field(default=Path("./data/archive"), validation_alias="ARCHIVE_DIR")

    # Business rules
    min_invoice_amount: float = Field(default=0.0, validation_alias="MIN_INVOICE_AMOUNT")
    default_currency: str = Field(default="EUR", validation_alias="DEFAULT_CURRENCY")

    # Observability
    enable_tracing: bool = Field(default=True, validation_alias="ENABLE_TRACING")
    otlp_endpoint: str | None = Field(default=None, validation_alias="OTLP_ENDPOINT")

    # Retry / Resilience
    max_retries: int = Field(default=3, validation_alias="MAX_RETRIES")
    retry_base_delay: float = Field(default=1.0, validation_alias="RETRY_BASE_DELAY")

    # Email / Notification (example)
    notification_email: str | None = Field(default=None, validation_alias="NOTIFICATION_EMAIL")

    # IMAP / Email settings
    imap_host: str = Field(default="", validation_alias="IMAP_HOST")
    imap_port: int = Field(default=993, validation_alias="IMAP_PORT")
    imap_username: str = Field(default="", validation_alias="IMAP_USERNAME")
    imap_password: str = Field(default="", validation_alias="IMAP_PASSWORD")
    simulated_mode: bool = Field(default=True, validation_alias="SIMULATED_MODE")

    model_config = {
        "env_file": ".env",
        "env_file_encoding": "utf-8",
        "extra": "ignore",
    }


settings = InvoiceBotSettings()
