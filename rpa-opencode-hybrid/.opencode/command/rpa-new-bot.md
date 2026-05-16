---
description: Neuen RPA Bot mit dem offiziellen Merle-Template erstellen
model: opencode/gpt-5.4
subtask: false
---

Erstelle einen neuen RPA Python-Bot nach dem **verbindlichen Merle-Standard** (Copier-Template + merle-core).

## Vor dem Start
1. Frage den Bot-Namen ab (Format: `<domain>_<action>`, z.B. `invoice_processor`)
2. Frage den Zweck des Bots ab (1-2 Sätze)
3. Validiere, dass `python_bots/<bot_name>/` noch nicht existiert

## Empfohlener Weg (Phase 1+)
Verwende **immer** eine der folgenden Methoden:

### Variante A – Merle CLI (empfohlen)
```bash
merle new-bot <bot_name> --playwright --pandas
```

### Variante B – Copier direkt
```bash
copier copy templates/bot python_bots/<bot_name>
```

Danach:
- `uv sync --group dev` ausführen
- `config.py` um projektspezifische Felder erweitern
- Eigene Tasks in `tasks/` als Klassen von `BaseTask` implementieren
- `main.py` mit `configure_observability()` und Task-Orchestrierung anpassen
- Tests schreiben
- `.env.example` und `README.md` aktualisieren

## Wichtige Regeln (Phase 3+)
- **Immer** `merle new-bot` oder Copier verwenden (kein manuelles `cp -r`)
- **Immer** von `BaseTask` (nicht nur plain classes) erben wo sinnvoll
- **Immer** `configure_observability()` in `main.py` aufrufen
- **Immer** `merle-core` als Dependency nutzen (`merle-core[observability]` oder mehr)
- NIE hartcodierte Werte → pydantic-settings + Key Vault wo möglich
- IMMER loguru + tenacity aus `merle-core`
- IMMER Type-Hints und async/await

## Nach der Erstellung
1. `governance-validator` Skill laden und Bot validieren
2. `/rpa-validate <bot_name>` ausführen
3. Entscheidung (falls UiPath involviert) in `docs/decisions/` dokumentieren
