---
description: Neuen RPA Bot aus Template erstellen
model: opencode/gpt-5.4
subtask: false
---

Erstelle einen neuen RPA Python-Bot nach dem Template.

## Vor dem Start
1. Frage den Bot-Namen ab (Format: `<domain>_<action>`, z.B. `invoice_processor`)
2. Frage den Zweck des Bots ab (1-2 Sätze)
3. Validiere, dass `python_bots/<bot_name>/` noch nicht existiert

## Dann
1. Klone das Template: `cp -r python_bots/template/ python_bots/<bot_name>/`
2. Passe `config.py` an:
   - `bot_name` auf den neuen Namen setzen
   - Projektspezifische Settings-Felder hinzufügen
3. Erstelle Task-Module in `tasks/`:
   - `example_task.py` löschen
   - Neue Tasks mit loguru, tenacity, async/await
4. Passe `main.py` an:
   - Neue Tasks importieren
   - Workflow-Logik implementieren
5. Schreibe Tests in `tests/test_main.py`
6. Aktualisiere `.env.example`
7. Schreibe `README.md` mit Zweck, Konfiguration, Betrieb
8. Führe Governance-Check durch (siehe Checkliste)

## Wichtige Regeln
- NIE Template-Dateien löschen, nur anpassen
- NIE Werte hartcodieren → immer pydantic-settings
- IMMER loguru statt print()
- IMMER tenacity-Retry für externe Aufrufe
- IMMER async/await
- IMMER Type-Hints
