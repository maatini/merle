# Integration Examples: Python ↔ UiPath

Dieses Verzeichnis enthält **bewährte Muster** für die Integration zwischen Python-Bots und UiPath-Komponenten. Alle Muster folgen dem Prinzip des **Loose Coupling**: Die Integration erfolgt nur über wohldefinierte Schnittstellen.

## Enthaltene Muster

### 1. Orchestrator API (`orchestrator_api/`)
Python ruft UiPath Orchestrator REST API auf, um Jobs zu starten, Queues zu befüllen oder Status abzufragen.

### 2. Python Scope Activity (`python_scope/`)
UiPath ruft Python-Code über die Python Scope Activity auf. Dokumentation des Setups.

### 3. File-Based Integration (`file_based_integration/`)
Python und UiPath tauschen Daten über geteilte Dateien (CSV, JSON) oder Message Queues aus.

## Wichtiger Hinweis
Diese Muster sind für die **10–20 % der Fälle**, in denen UiPath tatsächlich zum Einsatz kommt. In den meisten Projekten wird ausschließlich Python verwendet.
