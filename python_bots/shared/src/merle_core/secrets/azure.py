"""
Azure Key Vault Integration für Merle.

Verwendet Managed Identity / DefaultAzureCredential wo möglich.
"""

from __future__ import annotations

import os
from typing import Any

from loguru import logger

from .base import SecretProvider, SecretNotFoundError


class AzureKeyVaultProvider(SecretProvider):
    """
    Secret Provider für Azure Key Vault.

    Beispiel:
        provider = AzureKeyVaultProvider(
            vault_url="https://my-vault.vault.azure.net/"
        )
        api_key = await provider.get_secret("my-api-key")
    """

    def __init__(self, vault_url: str, credential: Any | None = None):
        self.vault_url = vault_url.rstrip("/")
        self._credential = credential
        self._client = None

    async def _get_client(self):
        if self._client is not None:
            return self._client

        try:
            from azure.identity.aio import DefaultAzureCredential
            from azure.keyvault.secrets.aio import SecretClient
        except ImportError as e:
            raise ImportError(
                "Azure Key Vault Support erfordert die Extras: "
                "uv add 'merle-core[azure]'"
            ) from e

        if self._credential is None:
            self._credential = DefaultAzureCredential()

        self._client = SecretClient(vault_url=self.vault_url, credential=self._credential)
        return self._client

    async def get_secret(self, name: str) -> str:
        client = await self._get_client()
        try:
            secret = await client.get_secret(name)
            logger.debug("Secret '{}' erfolgreich aus Key Vault geladen", name)
            return secret.value
        except Exception as exc:
            logger.error("Secret '{}' konnte nicht aus Key Vault geladen werden: {}", name, exc)
            raise SecretNotFoundError(f"Secret '{name}' nicht in Key Vault gefunden") from exc

    async def get_secret_or_default(self, name: str, default: str) -> str:
        try:
            return await self.get_secret(name)
        except SecretNotFoundError:
            return default

    async def close(self):
        """Schließt den Client (wichtig bei async)."""
        if self._client:
            await self._client.close()
            self._client = None
