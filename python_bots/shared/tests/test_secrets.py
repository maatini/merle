"""
Mocked tests for the Secrets module (Azure Key Vault).
"""

from unittest.mock import AsyncMock, patch

import pytest

from merle_core.secrets import AzureKeyVaultProvider
from merle_core.exceptions import SecretNotFoundError


@pytest.mark.asyncio
async def test_azure_key_vault_provider_get_secret_success():
    provider = AzureKeyVaultProvider("https://test.vault.azure.net/")

    with patch.object(provider, "_get_client", new_callable=AsyncMock) as mock_client:
        mock_secret = AsyncMock()
        mock_secret.value = "super-secret-value"
        mock_client.return_value.get_secret = AsyncMock(return_value=mock_secret)

        value = await provider.get_secret("my-api-key")
        assert value == "super-secret-value"


@pytest.mark.asyncio
async def test_azure_key_vault_provider_raises_on_missing_secret():
    provider = AzureKeyVaultProvider("https://test.vault.azure.net/")

    with patch.object(provider, "_get_client", new_callable=AsyncMock) as mock_client:
        mock_client.return_value.get_secret.side_effect = Exception("Secret not found")

        with pytest.raises(SecretNotFoundError):
            await provider.get_secret("non-existent-key")
