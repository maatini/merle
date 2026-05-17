# Orchestrator API Integration

## Zweck

Zeigt, wie Python-Bots die UiPath Orchestrator REST API nutzen, um UiPath-Jobs zu starten und zu überwachen.

## Einsatzbereich

- Nur in den 10–20 % der Fälle, in denen UiPath zum Einsatz kommt
- Zur Integration von Python-Orchestrierung mit UiPath-Jobs
- Zur Überwachung und Steuerung von UiPath-Robotern aus Python

## Authentifizierung

- OAuth 2.0 Client Credentials Grant
- Benötigt: Client ID + Client Secret aus dem Orchestrator

## API-Endpunkte (Auswahl)

- `POST /odata/Jobs/StartJobs` — Job starten
- `GET /odata/Jobs({id})` — Job-Status
- `POST /odata/QueueItems` — Queue-Item hinzufügen
