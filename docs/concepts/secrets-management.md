# Secrets Management in Merle (Phase 2+)

## Ziel

Kein Secret (API-Keys, Passwörter, Connection Strings, Tokens) darf jemals im Code oder in `.env`-Dateien in Produktion liegen.

## Empfohlene Architektur

1. **Azure Key Vault** ist der primäre und verbindliche Secrets-Speicher für alle produktiven Umgebungen.
2. **Lokale Entwicklung**: Fallback auf `.env` + `pydantic-settings`.
3. **CI/CD**: Verwendung von Managed Identity / Workload Identity.

## Verwendung mit merle-core

```python
from merle_core.secrets import AzureKeyVaultProvider, AzureKeyVaultSettings
from pydantic_settings import BaseSettings, SettingsConfigDict

class BotSettings(AzureKeyVaultSettings, BaseSettings):
    model_config = SettingsConfigDict(
        env_prefix="BOT_",
        azure_keyvault_url="https://merle-prod.vault.azure.net/",
    )

    api_key: str
    db_connection_string: str
```

### Empfohlener Boot-Prozess

```python
# main.py
import asyncio
from merle_core.secrets import AzureKeyVaultProvider
from config import BotSettings

async def main():
    # Optional: Secrets vorab laden
    provider = AzureKeyVaultProvider("https://my-vault.vault.azure.net/")
    api_key = await provider.get_secret("my-bot-api-key")

    settings = await BotSettings.from_keyvault()
    ...
```

## Governance (Regel 3 + 10 + 11)

- **Nie** Secrets in Git committen.
- **Nie** `api_key = "..."` im Code.
- **Immer** Key Vault in produktiven Umgebungen verwenden.
- Der `governance-validator` wird zukünftig prüfen, ob `azure_keyvault_url` konfiguriert ist.

## Nächste Schritte (geplant)

- Bessere asynchrone Auflösung in `AzureKeyVaultSettings`
- Unterstützung für Secret-Rotation / Caching
- HashiCorp Vault als alternativer Provider

---

**Status**: Phase 2 – Grundlegende Integration verfügbar
