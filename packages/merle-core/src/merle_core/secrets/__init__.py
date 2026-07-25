"""
merle_core.secrets

Secrets Management für Merle-Bots mit Fokus auf Azure Key Vault.

Bietet:
- AzureKeyVaultProvider
- Integration mit pydantic-settings (AzureKeyVaultSettings)
- Klare Fallback-Kette: Key Vault → Environment → .env

Verwendung:
    from merle_core.secrets import AzureKeyVaultProvider, AzureKeyVaultSettings
"""

from merle_core.exceptions import SecretNotFoundError

from .azure import AzureKeyVaultProvider
from .base import SecretProvider
from .pydantic import AzureKeyVaultSettings

__all__ = [
    "AzureKeyVaultProvider",
    "AzureKeyVaultSettings",
    "SecretNotFoundError",
    "SecretProvider",
]
