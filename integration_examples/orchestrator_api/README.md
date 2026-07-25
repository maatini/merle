# Orchestrator API Integration

## Zweck

Zeigt, wie Python-Bots die UiPath Orchestrator REST API nutzen, um UiPath-Jobs zu starten und zu überwachen.

## SSOT (Single Source of Truth)

> **Die kanonische Client-Implementierung liegt in `merle_core.uipath`.**
>
> - `UiPathOrchestratorClient` — OAuth 2.0, `start_job`, `get_job_status`
> - `UiPathQueueHelper` — `add_queue_item`, `get_queue_items`
>
> `example.py` in diesem Ordner ist ein **dünner Demo-Einstieg** (Re-Export + env-basiertes main).
> Für einen vollständigen Bot mit `BaseBot` / `BaseTask` und **SIMULATE-Default** siehe:
> [`examples/uipath-hybrid/`](../../examples/uipath-hybrid/).

```python
from merle_core.uipath import UiPathOrchestratorClient, UiPathQueueHelper
```

## Einsatzbereich

- Nur in den 10–20 % der Fälle, in denen UiPath zum Einsatz kommt
- Zur Integration von Python-Orchestrierung mit UiPath-Jobs
- Zur Überwachung und Steuerung von UiPath-Robotern aus Python

## Authentifizierung

- OAuth 2.0 Client Credentials Grant
- Benötigt: Client ID + Client Secret aus dem Orchestrator

## Umgebungsvariablen

| Variable               | Default                    | Beschreibung                               |
| ---------------------- | -------------------------- | ------------------------------------------ |
| `SIMULATE`             | `true`                     | Kein HTTP wenn true / fehlende Credentials |
| `UIPATH_CLIENT_ID`     | —                          | OAuth client id (live)                     |
| `UIPATH_CLIENT_SECRET` | —                          | OAuth client secret (live)                 |
| `UIPATH_TENANT`        | `Default`                  | Tenant name header                         |
| `UIPATH_BASE_URL`      | `https://cloud.uipath.com` | Orchestrator base URL                      |
| `UIPATH_QUEUE_NAME`    | `InvoiceQueue`             | Queue for demo add                         |
| `UIPATH_PROCESS_KEY`   | —                          | Optional release key for `start_job`       |

## API-Endpunkte (Auswahl)

- `POST /odata/Jobs/UiPath.Server.Configuration.OData.StartJobs` — Job starten
- `GET /odata/Jobs({id})` — Job-Status
- `POST /odata/QueueItems` — Queue-Item hinzufügen

## Ausführen

```bash
# Smoke (default, no network)
uv run python integration_examples/orchestrator_api/example.py

# Live (real Orchestrator)
export SIMULATE=false
export UIPATH_CLIENT_ID=...
export UIPATH_CLIENT_SECRET=...
uv run python integration_examples/orchestrator_api/example.py
```
