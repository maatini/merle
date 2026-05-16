# Merle Examples

In diesem Ordner findest du vollständige, lauffähige Beispiele für typische RPA-Szenarien.

## Verfügbare Beispiele

| Beispiel                | Technologien                     | Beschreibung |
|-------------------------|----------------------------------|------------|
| `web-automation/`       | Playwright + merle-core          | Robustes Web-Scraping / UI-Automatisierung |
| `excel-processing/`     | pandas + openpyxl + merle-core   | Excel-Dateien einlesen, verarbeiten, schreiben |
| `uipath-hybrid/`        | Python + UiPath Orchestrator     | Queue-Items aus UiPath mit Python verarbeiten |

## Alle Beispiele starten

```bash
cd examples/web-automation
uv sync
uv run python main.py
```

Die Beispiele sind bewusst klein gehalten, demonstrieren aber die empfohlenen Patterns aus Phase 2:

- Verwendung von `BaseTask`
- `configure_observability()`
- `launch_robust_browser()` (im Web-Beispiel)
- Saubere Struktur + Logging

## Nächste Schritte

In realen Projekten würdest du diese Beispiele als Basis nehmen und mit domänenspezifischer Logik erweitern.
