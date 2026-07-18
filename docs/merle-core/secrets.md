# Secrets (Azure Key Vault + pydantic-settings)

`merle_core.secrets` stellt Secret-Provider und eine pydantic-settings-Integration bereit. Produktive Secrets gehören **nicht** in Git oder committed `.env`-Dateien (Governance-Regeln 3 + 10).

Konzeptuelle Policy und Governance: [docs/concepts/secrets-management.md](../concepts/secrets-management.md).  
Knowledge-Base (Gotchas): [docs/knowledge-base/modules/merle-core/gotchas.md](../knowledge-base/modules/merle-core/gotchas.md) (`@tag:secrets`).

## Extra installieren

Azure- und Settings-Abhängigkeiten sind **optional**:

```bash
uv add "merle-core[azure]"
# zieht: azure-identity, azure-keyvault-secrets, pydantic-settings
```

Ohne Extra: `ImportError` mit Hinweis auf `merle-core[azure]` beim ersten Key-Vault-Zugriff.

## Bausteine

| API                     | Rolle                                                        |
| ----------------------- | ------------------------------------------------------------ |
| `SecretProvider`        | Abstraktes Interface (`get_secret`, `get_secret_or_default`) |
| `AzureKeyVaultProvider` | Async-Client über `DefaultAzureCredential` + `SecretClient`  |
| `AzureKeyVaultSettings` | `BaseSettings`-Mixin / Factory `from_keyvault()`             |
| `SecretNotFoundError`   | Wenn ein Secret im Vault fehlt                               |

## Direkter Provider

```python
from merle_core.secrets import AzureKeyVaultProvider

async def load_api_key() -> str:
    provider = AzureKeyVaultProvider(
        vault_url="https://my-vault.vault.azure.net/",
    )
    try:
        return await provider.get_secret("my-api-key")
    finally:
        await provider.close()
```

- **Auth:** standardmäßig `DefaultAzureCredential` (Managed Identity, Azure CLI, Env, …). Eigenes Credential optional als `credential=` übergeben.
- **Fallback-Wert:** `await provider.get_secret_or_default(name, default)`.

## pydantic-settings Integration

```python
from pydantic_settings import BaseSettings, SettingsConfigDict
from merle_core.secrets import AzureKeyVaultSettings

class BotSettings(AzureKeyVaultSettings, BaseSettings):
    model_config = SettingsConfigDict(
        env_prefix="BOT_",
        azure_keyvault_url="https://my-vault.vault.azure.net/",
    )

    api_key: str
    target_url: str

# Empfohlener Boot (async):
settings = await BotSettings.from_keyvault()
```

`from_keyvault()`:

1. Instantiiert Settings aus Environment / `.env` (synchroner pydantic-settings-Pfad).
2. Für leere Felder (`None`, `""`, `"CHANGE_ME"`) versucht es, den **Feldnamen** als Secret-Namen aus dem Key Vault zu laden.
3. Ohne `azure_keyvault_url` in `model_config` bleibt es bei Env/`.env` (lokale Entwicklung).

## Empfohlene Fallback-Kette

1. **Produktion:** Azure Key Vault (Managed / Workload Identity)
2. **Lokal:** Environment-Variablen + `.env` (nicht committen)
3. **CI:** Pipeline-Secrets / Workload Identity — keine hardcodierten Werte

## Gotchas

- **Async-Factory:** Key-Vault-Laden ist async. Nicht erwarten, dass `BotSettings()` allein Vault-Secrets befüllt — `await BotSettings.from_keyvault()` nutzen. Details: KB `@tag:secrets`.
- **Extra fehlt:** Code importiert `merle_core.secrets` auch ohne Azure-Deps, scheitert aber beim Client-Aufbau mit klarer `ImportError`-Message.
- **Secret-Namen = Feldnamen:** `from_keyvault` mappt aktuell 1:1 auf Pydantic-Feldnamen. Abweichende Vault-Namen über `AzureKeyVaultProvider.get_secret("expliziter-name")` laden.
- **Nie Secrets loggen:** loguru-Debug meldet nur den Secret-**Namen**, nicht den Wert — so belassen.
- **Client schließen:** bei langlaufenden Prozessen `await provider.close()`.

## Verwandte Docs

- [merle-core Index](index.md)
- [Secrets Management (Konzepte)](../concepts/secrets-management.md)
- [merle-core Gotchas (KB)](../knowledge-base/modules/merle-core/gotchas.md)
- Package-README: `packages/merle-core/README.md`
