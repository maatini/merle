"""
Zentrale Konfiguration für den Bot.

Verwendet pydantic-settings für typsichere Konfiguration
aus Umgebungsvariablen und .env-Dateien.
"""

from pydantic_settings import BaseSettings, SettingsConfigDict


class BotSettings(BaseSettings):
    """Bot-Konfiguration — Werte werden automatisch aus Umgebungsvariablen geladen."""

    model_config = SettingsConfigDict(
        env_prefix="BOT_",
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",  # Ignoriere unbekannte Umgebungsvariablen
    )

    # --- Allgemeine Settings ---
    bot_name: str = "template_bot"
    environment: str = "development"  # development, staging, production

    # --- Logging ---
    log_level: str = "INFO"
    log_json: bool = False  # JSON-Format für Produktion

    # --- Retry & Timeout ---
    max_retries: int = 3
    request_timeout: float = 30.0

    # --- Zielsystem (projektspezifisch) ---
    target_url: str = "https://example.com/api"
    api_key: str = ""

    # --- UiPath Orchestrator (optional) ---
    orchestrator_url: str = ""
    orchestrator_tenant: str = "Default"
    orchestrator_client_id: str = ""
    orchestrator_client_secret: str = ""
