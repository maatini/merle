# Examples — Gotchas & Pitfalls

## invoice-processing: Simulate-Modus liest lokale Testdaten

**Problem:** Der Simulate-Modus (`settings.simulate = True`) liest `.eml`-Dateien aus einem lokalen Verzeichnis statt echtem IMAP. Fehlen die Dateien, schlägt der Bot fehl.

**Stand im Repo:** `examples/invoice-processing/data/` enthält Sample-Daten:

- `data/simulated_mail_inbox/` — `.eml` (z.B. `INV-2025-0042.eml` …)
- `data/invoices/` — gepaarte `.pdf` + `.json` Samples
- `data/reports/` — Beispiel-Excel-Reports

Pfad und Dateinamen müssen zur Config des Bots passen; eigene Szenarien erfordern zusätzliche Dateien.

## nats-task-communication: NATS-Server muss laufen

**Problem:** Das @tag:nats Beispiel benötigt einen laufenden NATS-Server auf `localhost:4222`. Ohne diesen crasht der `async with NatsClient() as client:` Block.

```bash
# Vor Ausführung:
docker run -d -p 4222:4222 nats:latest
```

## uipath-hybrid: Simulate vs. echte Orchestrator-API

**Stand:** `examples/uipath-hybrid/` nutzt `merle_core.uipath` (`UiPathOrchestratorClient`, `UiPathQueueHelper`) — kein Platzhalter mehr.

**Falle:** Default ist `SIMULATE=true` (keine Credentials, keine HTTP-Calls). Für echte Queues:

```bash
export SIMULATE=false
export UIPATH_CLIENT_ID=...
export UIPATH_CLIENT_SECRET=...
# optional: UIPATH_TENANT, UIPATH_BASE_URL, UIPATH_PROCESS_KEY
```

Ohne Credentials und mit `SIMULATE=false` schlägt der Bot bei Auth fehl.

## integration_examples/orchestrator_api: dünner SSOT-Wrapper

**Status:** `integration_examples/orchestrator_api/example.py` ist ein dünner Demo-Wrapper um `merle_core.uipath` (SSOT). Vollständiger Bot: `examples/uipath-hybrid/`.

Neue Bots sollen **nur** `merle_core.uipath` nutzen, nicht eigene Orchestrator-Clients bauen.

## web-automation: Lightpanda benötigt separaten Prozess

**Problem:** Das Beispiel nutzt Chromium (Default). Ein Wechsel zu `engine="lightpanda"` erfordert einen **separat gestarteten** Lightpanda-Prozess auf `localhost:9222` vor dem Bot-Start.

## Testdaten in Examples sind ungleichmäßig

**Problem:** Nicht alle Examples bringen Sample-Daten mit.

- **invoice-processing:** hat Sample-`.eml`/`.pdf`/`.json` unter `data/` (siehe oben)
- **web-automation, nats-task-communication, uipath-hybrid:** typischerweise gemockt / ohne vollständige Fixtures; E2E braucht eigene Umgebung (Browser, NATS, Orchestrator)

Unit-Tests in den Examples bleiben oft gemockt, auch wenn Sample-Dateien existieren.

## invoice-processing: Self-Healing ist demonstrativ

**Problem:** `_attempt_self_healing()` im Invoice-Processing-Bot ist ein **Demo-Hook**. Er loggt nur die Fehlerursache und versucht keine echte automatische Reparatur. In Produktion müsste dieser Hook mit echter Recovery-Logik gefüllt werden (z.B. OCR-Fallback, manuelles Review-Queueing).
