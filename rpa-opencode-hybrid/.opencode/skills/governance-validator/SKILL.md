# Governance Validator

## Purpose
Validiert Code und Projektstruktur auf **vollständige Einhaltung** aller
Governance-Regeln des RPA Hybrid Development Kit.

## When to Use
- Nach der Bot-Erstellung (vor Code-Review)
- Vor dem Merge in `main`
- Bei quartalsweisen Audits
- Bei Verdacht auf Regelverstöße
- Auf Anforderung: „Validiere den Bot <name>"

## Process

### 1. Ziel bestimmen
- Einzelner Bot: `python_bots/<bot_name>/`
- Alle Bots: `python_bots/*/`
- Gesamtes Repository: `.`

### 2. Regel-Checks durchführen

#### Regel 1: Python-First
- [ ] Technologieentscheidung dokumentiert? (ADR in `docs/decisions/`)
- [ ] Bei UiPath: Begründung gemäß Entscheidungsmatrix?
- [ ] Bei UiPath: Python-Alternative geprüft?

#### Regel 2: Template-Pflicht
- [ ] Bot-Verzeichnis enthält alle Template-Dateien?
  - `main.py`
  - `config.py`
  - `tasks/` (mit __init__.py und mindestens einer Task)
  - `tests/` (mit __init__.py, conftest.py, mindestens einem Test)
  - `requirements.txt`
  - `Dockerfile`
  - `.env.example`
  - `README.md`

#### Regel 3: Keine hartcodierten Werte
- [ ] Keine URLs im Code (außer Defaults in Settings-Klasse)
- [ ] Keine API-Keys, Passwörter, Tokens im Code
- [ ] Keine absoluten Windows-Pfade (`C:\...`)
- [ ] Alle Umgebungsvariablen in `.env.example` dokumentiert
- [ ] `.env` in `.gitignore`

Prüf-Befehl:
```bash
grep -rn "api_key\s*=\s*['\"]" python_bots/  # Sollte LEER sein
grep -rn "password\s*=\s*['\"]" python_bots/  # Sollte LEER sein
grep -rn "C:\\\\" python_bots/                  # Sollte LEER sein
```

#### Regel 4: Strukturiertes Logging
- [ ] loguru wird importiert und verwendet (`from loguru import logger`)
- [ ] Kein `print()` für Logging-Zwecke
- [ ] Logger-Instanz pro Bot/Task mit `bind()`
- [ ] JSON-Logging-Option in Produktion (`BOT_LOG_JSON`)

Prüf-Befehl:
```bash
grep -rn "from loguru import logger" python_bots/  # Sollte in jeder .py-Datei sein
grep -rn "^[^#]*print\(" python_bots/               # Sollte minimal sein
```

#### Regel 5: Retry-Mechanismen
- [ ] `from tenacity import retry` in Dateien mit externen Aufrufen
- [ ] `@retry`-Dekorator auf HTTP-Calls, DB-Zugriffen, Datei-I/O
- [ ] Exponentielles Backoff konfiguriert
- [ ] Maximale Anzahl Versuche definiert (3-5)

#### Regel 6: Tests
- [ ] `tests/`-Verzeichnis mit mindestens einer Test-Datei
- [ ] Unit-Tests für Business-Logik (`test_*.py`)
- [ ] Mock für externe Abhängigkeiten verwendet (nicht echte Aufrufe)
- [ ] `pytest` in `requirements.txt`

Prüf-Befehl:
```bash
find python_bots/*/tests -name "test_*.py" | wc -l  # Sollte > 0 sein
```

#### Regel 7: Linux-Container-Kompatibilität
- [ ] `Dockerfile` vorhanden
- [ ] Basis-Image ist Linux (`python:3.11-slim` oder ähnlich)
- [ ] Keine Windows-only-Befehle (`powershell`, `cmd`, `reg`)
- [ ] Keine Windows-Pfade (`C:\`, `\\server\share`)
- [ ] Playwright-Abhängigkeiten installiert (wenn Playwright verwendet)

Prüf-Befehl:
```bash
grep -rn "powershell\|cmd\.exe\|reg\.exe" python_bots/  # Sollte LEER sein
```

#### Regel 8: Dokumentation
- [ ] `README.md` im Bot-Verzeichnis
- [ ] Enthält: Zweck, Konfiguration, Entwicklung, Docker, Betrieb
- [ ] Bei UiPath: ADR in `docs/decisions/`

#### Regel 9: Code-Review-Bereitschaft
- [ ] Keine auskommentierten Code-Blöcke (> 3 Zeilen)
- [ ] Keine TODO/FIXME ohne Issue-Referenz
- [ ] Gitignore vollständig (`.env`, `__pycache__`, `logs/`)

#### Regel 10: Entscheidungsdokumentation
- [ ] Bei UiPath-Nutzung: ADR vorhanden mit Begründung, Alternativen, Risiken

### 3. Bewertung ausgeben

```markdown
## Governance-Validierung: [Bot-Name]

**Gesamtergebnis**: ✅ Bestanden / ⚠️ Mängel / ❌ Nicht bestanden
**Score**: X/10 Regeln erfüllt

### Detail-Ergebnisse

| Regel | Status | Anmerkung |
|-------|--------|-----------|
| 1. Python-First | ✅ | ADR vorhanden |
| 2. Template | ✅ | Alle Dateien vorhanden |
| 3. Keine Hardcoding | ⚠️ | Zeile 42: URL hartcodiert |
| ... | ... | ... |

### Kritische Mängel (müssen behoben werden)
- [ ] [Mangel 1] → [Konkrete Behebungsanleitung]
- [ ] [Mangel 2] → [Konkrete Behebungsanleitung]

### Warnungen (sollten behoben werden)
- [ ] [Warnung 1] → [Verbesserungsvorschlag]
```

### 4. Schweregrade
- **❌ Kritisch**: Regel 1-3, 7 verletzt → Deployment-Blocker
- **⚠️ Warnung**: Regel 4-6, 8-10 teilweise verletzt → Vor Merge beheben
- **💡 Hinweis**: Kleinere Verbesserungsmöglichkeiten

## Hard Constraints
- IMMER alle 10 Regeln prüfen
- IMMER konkrete Zeilennummern und Behebungsvorschläge nennen
- NIE „Bestanden" melden, wenn kritische Mängel vorliegen

## References
- `docs/03_Governance.md` — Vollständige Governance-Regeln
- `docs/05_Entwicklungsleitfaden.md` — Abschnitt „Checkliste für Bot-Fertigstellung"
