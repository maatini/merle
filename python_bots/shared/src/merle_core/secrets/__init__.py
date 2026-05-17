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

from .base import SecretProvider
from .azure import AzureKeyVaultProvider
from .pydantic import AzureKeyVaultSettings
from merle_core.exceptions import SecretNotFoundError

__all__ = [
    "SecretProvider",
    "AzureKeyVaultProvider",
    "AzureKeyVaultSettings",
    "SecretNotFoundError",
]
