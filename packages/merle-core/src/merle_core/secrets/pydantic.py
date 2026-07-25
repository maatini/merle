"""
Azure Key Vault Integration für pydantic-settings.

Ermöglicht, dass Konfigurationswerte automatisch aus Azure Key Vault
geladen werden können, mit sauberer Fallback-Kette.
"""

from __future__ import annotations

from typing import Any, ClassVar, TypeVar, cast

from loguru import logger
from pydantic_settings import BaseSettings

from .azure import AzureKeyVaultProvider

T = TypeVar("T", bound="AzureKeyVaultSettings")


class AzureKeyVaultSettings(BaseSettings):
    """
    Mixin für pydantic-settings, das Azure Key Vault als Secret-Quelle unterstützt.

    Verwendung:

        from pydantic_settings import SettingsConfigDict
        from merle_core.secrets import AzureKeyVaultSettings

        class BotSettings(AzureKeyVaultSettings, BaseSettings):
            model_config = SettingsConfigDict(
                env_prefix="BOT_",
                azure_keyvault_url="https://my-vault.vault.azure.net/",
            )

            api_key: str          # Wird zuerst aus Key Vault versucht
            target_url: str
    """

    # Custom keys are read via getattr on model_config; stored as ClassVars
    # so they do not collide with SettingsConfigDict TypedDict keys.
    azure_keyvault_url: ClassVar[str | None] = None
    azure_keyvault_credential: ClassVar[Any | None] = None

    _keyvault_provider: ClassVar[AzureKeyVaultProvider | None] = None

    @classmethod
    def _get_keyvault_provider(cls) -> AzureKeyVaultProvider | None:
        vault_url = cast(
            str | None,
            cls.model_config.get("azure_keyvault_url", cls.azure_keyvault_url),
        )
        if not vault_url:
            return None

        if cls._keyvault_provider is None:
            credential = cls.model_config.get("azure_keyvault_credential", cls.azure_keyvault_credential)
            cls._keyvault_provider = AzureKeyVaultProvider(
                vault_url=str(vault_url),
                credential=credential,
            )
        return cls._keyvault_provider

    @classmethod
    async def load_secrets(cls) -> None:
        """
        Lädt alle als Secret markierten Werte aus Key Vault in die Umgebung.
        Sollte früh im Boot-Prozess aufgerufen werden.
        """
        provider = cls._get_keyvault_provider()
        if provider is None:
            return

        # Hier könnte man später eine Liste von Secret-Namen konfigurieren
        # Für den Anfang: Wir lassen pydantic-settings die Werte ziehen,
        # wenn sie mit dem Prefix "kv:" oder ähnlich markiert sind.
        # Eine einfachere und robustere Lösung ist, den Provider global zu setzen.
        pass

    @classmethod
    async def from_keyvault(cls: type[T], **overrides: Any) -> T:
        """
        Erstellt die Settings und versucht, fehlende Werte aus Azure Key Vault zu laden.

        Empfohlene Nutzung:
            settings = await BotSettings.from_keyvault()
        """
        provider = cls._get_keyvault_provider()

        # Zuerst normale Initialisierung (aus Env + .env)
        instance = cls(**overrides)

        if provider is None:
            return instance

        # Für alle Felder, die noch leer sind, aus Key Vault versuchen
        for field_name, _field_info in instance.model_fields.items():
            current_value = getattr(instance, field_name, None)
            if current_value in (None, "", "CHANGE_ME"):
                try:
                    secret_value = await provider.get_secret(field_name)
                    setattr(instance, field_name, secret_value)
                    logger.info("Secret '{}' aus Key Vault geladen", field_name)
                except Exception:
                    pass  # Bleibt bei Default / leer

        return instance
