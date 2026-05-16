---
description: Governance-Validierung eines Bots (Phase 3+)
model: opencode/gpt-5.4
subtask: false
---

Validiere den angegebenen Bot auf Einhaltung aller 10 Governance-Regeln (inkl. Rule 10: Merle-Core-Pflicht).

## Prüfung

### Regel 1: Python-First
- Technologieentscheidung dokumentiert?

### Regel 2: Template-Pflicht
- Wurde `merle new-bot` oder Copier verwendet?
- Moderne Struktur vorhanden?

### Regel 3: Keine hartcodierten Werte
- Keine Secrets, URLs, Pfade im Code?

### Regel 4-5: Logging + Retry
- `configure_observability()` vorhanden?
- `@with_retry` oder `merle_core.retry` wird genutzt?

### Regel 6: Tests
- Sinnvolle Tests vorhanden?

### Regel 7: Linux-Container
- Dockerfile Linux-basiert?

### Regel 8-9: Dokumentation & Review

### Regel 10: Merle-Core-Pflicht (kritisch)
- `merle-core` als Dependency?
- `BaseTask` wird verwendet?
- Observability aktiviert?

## Ausgabe
Strukturiertes Ergebnis mit Score, kritischen Mängeln und Verbesserungsvorschlägen.