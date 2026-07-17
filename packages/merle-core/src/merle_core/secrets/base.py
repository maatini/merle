"""
Abstrakte Basis für Secret Provider.
"""

from __future__ import annotations

from abc import ABC, abstractmethod


class SecretProvider(ABC):
    """Interface für alle Secret-Backends (Key Vault, HashiCorp, etc.)."""

    @abstractmethod
    async def get_secret(self, name: str) -> str:
        """Holt ein Secret als String."""
        ...

    @abstractmethod
    async def get_secret_or_default(self, name: str, default: str) -> str:
        """Holt ein Secret oder gibt den Default zurück."""
        ...
