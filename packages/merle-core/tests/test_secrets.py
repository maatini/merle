"""
Mocked tests for the Secrets module (Azure Key Vault + pydantic-settings).
"""

from __future__ import annotations

from typing import ClassVar
from unittest.mock import AsyncMock, MagicMock, patch

import pytest
from pydantic_settings import SettingsConfigDict

from merle_core.exceptions import SecretNotFoundError
from merle_core.secrets import AzureKeyVaultProvider, AzureKeyVaultSettings


# ─────────────────────────────────────────────────────────────
# AzureKeyVaultProvider
# ─────────────────────────────────────────────────────────────


@pytest.mark.asyncio
async def test_azure_key_vault_provider_get_secret_success() -> None:
    provider = AzureKeyVaultProvider("https://test.vault.azure.net/")

    with patch.object(provider, "_get_client", new_callable=AsyncMock) as mock_client:
        mock_secret = AsyncMock()
        mock_secret.value = "super-secret-value"
        mock_client.return_value.get_secret = AsyncMock(return_value=mock_secret)

        value = await provider.get_secret("my-api-key")
        assert value == "super-secret-value"


@pytest.mark.asyncio
async def test_azure_key_vault_provider_raises_on_missing_secret() -> None:
    provider = AzureKeyVaultProvider("https://test.vault.azure.net/")

    with patch.object(provider, "_get_client", new_callable=AsyncMock) as mock_client:
        mock_client.return_value.get_secret.side_effect = Exception("Secret not found")

        with pytest.raises(SecretNotFoundError):
            await provider.get_secret("non-existent-key")


@pytest.mark.asyncio
async def test_azure_key_vault_provider_raises_on_null_secret_value() -> None:
    provider = AzureKeyVaultProvider("https://test.vault.azure.net/")

    with patch.object(provider, "_get_client", new_callable=AsyncMock) as mock_client:
        mock_secret = MagicMock()
        mock_secret.value = None
        mock_client.return_value.get_secret = AsyncMock(return_value=mock_secret)

        with pytest.raises(SecretNotFoundError) as exc_info:
            await provider.get_secret("empty-secret")
        assert "keinen Wert" in str(exc_info.value)


@pytest.mark.asyncio
async def test_azure_key_vault_provider_get_secret_or_default() -> None:
    provider = AzureKeyVaultProvider("https://test.vault.azure.net/")

    with patch.object(provider, "get_secret", new_callable=AsyncMock) as mock_get:
        mock_get.side_effect = SecretNotFoundError("missing")
        value = await provider.get_secret_or_default("missing-key", "fallback")
        assert value == "fallback"

        mock_get.side_effect = None
        mock_get.return_value = "from-vault"
        value = await provider.get_secret_or_default("present-key", "fallback")
        assert value == "from-vault"


@pytest.mark.asyncio
async def test_azure_key_vault_provider_close() -> None:
    provider = AzureKeyVaultProvider("https://test.vault.azure.net/")
    mock_client = AsyncMock()
    provider._client = mock_client

    await provider.close()
    mock_client.close.assert_awaited_once()
    assert provider._client is None

    # Second close is a no-op
    await provider.close()


@pytest.mark.asyncio
async def test_azure_key_vault_provider_get_client_returns_cached() -> None:
    """Cached client is returned without re-importing Azure SDKs."""
    provider = AzureKeyVaultProvider("https://test.vault.azure.net/")
    fake_client = MagicMock()
    provider._client = fake_client

    client = await provider._get_client()
    assert client is fake_client


# ─────────────────────────────────────────────────────────────
# AzureKeyVaultSettings
# ─────────────────────────────────────────────────────────────


class _SampleSettings(AzureKeyVaultSettings):
    """Minimal settings subclass for from_keyvault tests."""

    model_config = SettingsConfigDict(
        env_prefix="MERLE_TEST_SECRETS_",
        extra="ignore",
    )
    azure_keyvault_url: ClassVar[str | None] = "https://test.vault.azure.net/"

    api_key: str = "CHANGE_ME"
    target_url: str = "https://example.com"


@pytest.mark.asyncio
async def test_from_keyvault_fills_empty_fields() -> None:
    # Reset class-level provider cache between tests
    _SampleSettings._keyvault_provider = None

    mock_provider = AsyncMock(spec=AzureKeyVaultProvider)
    mock_provider.get_secret = AsyncMock(return_value="kv-secret-value")

    with patch.object(_SampleSettings, "_get_keyvault_provider", return_value=mock_provider):
        settings = await _SampleSettings.from_keyvault()

    assert settings.api_key == "kv-secret-value"
    # target_url has a real default — not replaced
    assert settings.target_url == "https://example.com"
    mock_provider.get_secret.assert_awaited_with("api_key")


@pytest.mark.asyncio
async def test_from_keyvault_without_provider_returns_instance() -> None:
    _SampleSettings._keyvault_provider = None

    with patch.object(_SampleSettings, "_get_keyvault_provider", return_value=None):
        settings = await _SampleSettings.from_keyvault(api_key="from-override")

    assert settings.api_key == "from-override"


@pytest.mark.asyncio
async def test_from_keyvault_swallows_missing_secrets() -> None:
    _SampleSettings._keyvault_provider = None

    mock_provider = AsyncMock(spec=AzureKeyVaultProvider)
    mock_provider.get_secret = AsyncMock(side_effect=SecretNotFoundError("nope"))

    with patch.object(_SampleSettings, "_get_keyvault_provider", return_value=mock_provider):
        settings = await _SampleSettings.from_keyvault()

    # Falls back to model default when vault lookup fails
    assert settings.api_key == "CHANGE_ME"


@pytest.mark.asyncio
async def test_load_secrets_noop_without_provider() -> None:
    _SampleSettings._keyvault_provider = None

    with patch.object(_SampleSettings, "_get_keyvault_provider", return_value=None):
        await _SampleSettings.load_secrets()  # should not raise


def test_get_keyvault_provider_creates_once() -> None:
    _SampleSettings._keyvault_provider = None

    with patch(
        "merle_core.secrets.pydantic.AzureKeyVaultProvider",
    ) as mock_cls:
        mock_cls.return_value = MagicMock(spec=AzureKeyVaultProvider)
        p1 = _SampleSettings._get_keyvault_provider()
        p2 = _SampleSettings._get_keyvault_provider()
        assert p1 is p2
        mock_cls.assert_called_once()

    _SampleSettings._keyvault_provider = None


def test_get_keyvault_provider_none_without_url() -> None:
    class _NoVaultSettings(AzureKeyVaultSettings):
        azure_keyvault_url: ClassVar[str | None] = None
        _keyvault_provider: ClassVar[AzureKeyVaultProvider | None] = None

    assert _NoVaultSettings._get_keyvault_provider() is None
