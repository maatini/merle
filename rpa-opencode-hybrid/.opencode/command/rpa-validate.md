---
description: Governance-Validierung eines Bots
model: opencode/gpt-5.4
subtask: false
---

Validiere den angegebenen Bot auf Einhaltung aller 10 Governance-Regeln.

## Prüfung

### Regel 1: Python-First
- [ ] Technologieentscheidung dokumentiert?

### Regel 2: Template-Pflicht
- [ ] Alle Template-Dateien vorhanden? (main.py, config.py, tasks/, tests/, Dockerfile, .env.example, README.md)

### Regel 3: Keine hartcodierten Werte
!`grep -rn "api_key\s*=\s*['\"]" python_bots/ 2>/dev/null || echo "OK - keine hartcodierten API-Keys"`
!`grep -rn "C:\\\\" python_bots/ 2>/dev/null || echo "OK - keine Windows-Pfade"`

### Regel 4: Strukturiertes Logging
!`grep -rn "from loguru import logger" python_bots/ 2>/dev/null | head -20`
!`grep -rn "^[^#]*print\(" python_bots/ 2>/dev/null | grep -v "__pycache__" | head -10 || echo "OK - kein print()"`

### Regel 5: Retry-Mechanismen
!`grep -rn "from tenacity import\|@retry" python_bots/ 2>/dev/null | head -20`

### Regel 6: Tests
!`find python_bots/ -name "test_*.py" 2>/dev/null | sort`

### Regel 7: Linux-Container
!`grep -rn "powershell\|cmd\.exe" python_bots/ 2>/dev/null || echo "OK - keine Windows-Commands"`
!`ls python_bots/*/Dockerfile 2>/dev/null`

### Regel 8: Dokumentation
!`ls python_bots/*/README.md 2>/dev/null`

### Regel 9: Code-Review-Bereitschaft
Prüfe auf auskommentierte Code-Blöcke und TODOs ohne Referenz.

### Regel 10: Entscheidungsdokumentation
!`ls docs/decisions/*.md 2>/dev/null || echo "Keine ADRs gefunden"`

## Ergebnis
Gib eine strukturierte Bewertung aus:
- **Gesamtergebnis**: ✅ Bestanden / ⚠️ Mängel / ❌ Nicht bestanden
- **Score**: X/10
- **Kritische Mängel**: Liste mit Behebungsvorschlägen
- **Warnungen**: Liste mit Verbesserungsvorschlägen
