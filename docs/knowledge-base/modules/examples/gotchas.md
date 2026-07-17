# Examples — Gotchas & Pitfalls

## invoice-processing: Simulate-Modus benötigt `.eml`-Dateien

**Problem:** Der Simulate-Modus (`settings.simulate = True`) liest `.eml`-Dateien aus einem lokalen Verzeichnis statt echtem IMAP. Ohne diese Dateien schlägt der Bot fehl.

**Lösung:** `.eml`-Testdateien müssen manuell bereitgestellt werden. Das Beispiel enthält keine Testdaten.

## nats-task-communication: NATS-Server muss laufen

**Problem:** Das @tag:nats Beispiel benötigt einen laufenden NATS-Server auf `localhost:4222`. Ohne diesen crasht der `async with NatsClient() as client:` Block.

```bash
# Vor Ausführung:
docker run -d -p 4222:4222 nats:latest
```

## uipath-hybrid: Platzhalter-Code

**Problem:** `examples/uipath-hybrid/` ist ein Platzhalter. Der Code referenziert `merle_core.uipath`, das zum Zeitpunkt der Beispiel-Erstellung noch nicht vollständig implementiert war.

**Aktueller Stand:** Die echte UiPath-Integration liegt in:

- `integration_examples/orchestrator_api/example.py` (httpx-basierter Client)
- `packages/merle-core/src/merle_core/uipath/orchestrator.py` (merle-core UiPath Client)

## integration_examples/orchestrator_api: Wird durch merle_core.uipath ersetzt

**Problem:** Der `OrchestratorClient` in `integration_examples/` dupliziert Funktionalität, die jetzt in `merle_core.uipath.UiPathOrchestratorClient` liegt. Langfristig wird das Integration-Example auf den merle-core-Client migriert.

**Übergangsweise:** Beide Implementierungen existieren parallel. Neue Bots sollten `merle_core.uipath` nutzen.

## web-automation: Lightpanda benötigt separaten Prozess

**Problem:** Das Beispiel nutzt Chromium (Default). Ein Wechsel zu `engine="lightpanda"` erfordert einen **separat gestarteten** Lightpanda-Prozess auf `localhost:9222` vor dem Bot-Start.

## Keine Testdaten in Examples

**Problem:** Keines der Examples enthält reale Testdaten (`.eml`, `.xlsx`, `.pdf`). Alle Tests nutzen gemockte Daten oder Dummy-Werte. Für echte End-to-End-Tests müssen Testdaten manuell bereitgestellt werden.

## invoice-processing: Self-Healing ist demonstrativ

**Problem:** `_attempt_self_healing()` im Invoice-Processing-Bot ist ein **Demo-Hook**. Er loggt nur die Fehlerursache und versucht keine echte automatische Reparatur. In Produktion müsste dieser Hook mit echter Recovery-Logik gefüllt werden (z.B. OCR-Fallback, manuelles Review-Queueing).
