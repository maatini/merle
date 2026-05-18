# Governance Validator (Phase 3+)

## Purpose

Validiert Code und Projektstruktur auf **vollständige Einhaltung** aller
Governance-Regeln des Merle RPA Frameworks (inkl. Rule 10: Merle-Core-Pflicht).

## When to Use

- Nach Bot-Erstellung (vor Code-Review)
- Vor Merge nach `main`
- Bei Audits
- Auf Anfrage: "Validiere den Bot <name>"

## Process

### 1. Ziel bestimmen

- Einzelner Bot: `python_bots/<bot_name>/`
- Gesamtes Repository: `.`

### 2. Regel-Checks durchführen (alle 10 Regeln)

#### Regel 1: Python-First

- Technologieentscheidung dokumentiert (ADR)?
- Bei UiPath: Begründung gemäß Entscheidungsmatrix?

#### Regel 2: Template-Pflicht (aktualisiert)

- Wurde der Bot mit `merle new-bot` oder Copier (`templates/bot/`) erstellt?
- Oder zumindest: Enthält er alle notwendigen Dateien?

#### Regel 3: Keine hartcodierten Werte

- Keine API-Keys, URLs, Pfade im Code
- Alle Werte in `config.py` (pydantic-settings)

#### Regel 4: Strukturiertes Logging

- `loguru` wird verwendet
- `configure_observability()` in `main.py` vorhanden?

#### Regel 5: Retry-Mechanismen

- `@with_retry` oder Policies aus `merle_core.retry` werden genutzt

#### Regel 6: Tests

- `tests/` vorhanden mit sinnvollen Tests

#### Regel 7: Linux-Container-fähig

- `Dockerfile` vorhanden und Linux-basiert

#### Regel 8: Dokumentation

- `README.md` vorhanden und aktuell

#### Regel 9: Code-Review-Bereitschaft

#### Regel 10: Merle-Core-Pflicht (neu)

- Wird `merle-core` als Dependency verwendet?
- Werden `BaseTask`, `TaskSpec`, Observability-Funktionen genutzt?
- Werden Helfer aus `merle_core.nats`, `merle_core.playwright` etc. verwendet?

### 3. Bewertung ausgeben

```markdown
## Governance-Validierung: <Bot-Name>

**Gesamtergebnis**: ✅ Bestanden / ⚠️ Mängel / ❌ Nicht bestanden
**Score**: X/10 Regeln erfüllt

### Kritische Mängel (Deployment-Blocker)

- ...

### Empfohlene Verbesserungen

- ...
```

## Hard Constraints

- IMMER alle 10 Regeln prüfen
- Besonders auf Rule 10 (Merle-Core) achten
- Konkrete Beispiele und Verbesserungsvorschläge liefern

## References

- `docs/concepts/governance.md`
- `docs/concepts/entwicklungsleitfaden.md`
- `merle_core/` (v0.3+)
