# Python Scope Activity (UiPath → Python)

## Zweck
Dokumentiert das Setup für UiPath's Python Scope Activity, mit der UiPath-Workflows Python-Code ausführen können.

## Setup

### 1. Python-Installation auf dem UiPath-Roboter
- Python 3.11+ installieren (Systemweit oder in Virtual Environment)
- Pfad in der UiPath Activity konfigurieren

### 2. Benötigte Pakete
```bash
pip install rpaframework pandas httpx
```

### 3. UiPath Activity konfigurieren
- **Python Path**: `C:\Python311\python.exe` (oder Pfad zur venv)
- **Python Module**: Das zu importierende Python-Modul
- **Input/Output**: Über UiPath-Argumente mappen

## Best Practice
- Python-Code in eigene `.py`-Dateien auslagern, nicht inline in UiPath
- Python-Module in Git versionieren (separat vom UiPath-Projekt)
- Klare Input/Output-Verträge definieren
