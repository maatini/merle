# RPA Hybrid Development Kit

**Python-First Framework für hybride RPA-Entwicklung**  
Wartbare, testbare und kosteneffiziente Automatisierung — 80–90 % Python, UiPath nur bei nachgewiesenem Vorteil.

---

## Schnellstart

```bash
# Neuen Python-Bot erstellen
cp -r python_bots/template/ python_bots/mein_bot/
cd python_bots/mein_bot/

# Entwicklung
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
python main.py

# Tests
pytest tests/ -v

# Docker
docker build -t mein-bot .
docker run --env-file .env mein-bot
```

---

## Philosophie

| Prinzip | Beschreibung |
|----------|-------------|
| **Python-First** | Python ist der Default für alle Automatisierungen |
| **UiPath nur begründet** | UiPath kommt nur bei nachgewiesenem Vorteil zum Einsatz |
| **Template-First** | Alle Bots entstehen aus dem professionellen Template |
| **Container-Fähig** | Jeder Bot läuft im Linux-Container |
| **Testgetrieben** | Unit-Tests, Integration-Tests, CI/CD |
| **Governance** | Klare Regeln, Entscheidungsmatrix, ADRs |

---

## Repository-Struktur

```
.
├── docs/                     # Strategie, Governance, Leitfäden
│   ├── 01_Strategie.md       # Python-First Strategie
│   ├── 02_Wann_Python_vs_UiPath.md  # Entscheidungsmatrix
│   ├── 03_Governance.md      # Governance-Regeln
│   ├── 04_Projektstruktur.md # Projektstruktur & Konventionen
│   ├── 05_Entwicklungsleitfaden.md  # Entwicklungsleitfaden
│   └── decisions/            # ADR-Archiv
├── python_bots/
│   ├── template/             # ✨ Verbindliches Bot-Template
│   └── shared/               # Gemeinsame Utilities
├── integration_examples/     # Python ↔ UiPath Muster
├── uipath_templates/         # UiPath-Templates (nur Ausnahmen)
├── agent/
│   └── CLAUDE.md             # RPA-Hybrid-Architekt Agent
├── AGENTS.md                 # AI-Agenten Kontext
└── README.md                 # Diese Datei
```

---

## Dokumentation

| Dokument | Inhalt |
|----------|--------|
| [Strategie](docs/01_Strategie.md) | Warum Python-First, Architekturprinzipien, KPIs |
| [Entscheidungsmatrix](docs/02_Wann_Python_vs_UiPath.md) | Wann Python, wann UiPath — mit Fallbeispielen |
| [Governance](docs/03_Governance.md) | 10 verbindliche Regeln für alle Bots |
| [Projektstruktur](docs/04_Projektstruktur.md) | Repository-Layout, Konventionen |
| [Entwicklungsleitfaden](docs/05_Entwicklungsleitfaden.md) | Schritt-für-Schritt zur Bot-Entwicklung |

---

## Technologie-Stack

### Python (Default)
- **RPA**: rpaframework ≥ 28.0
- **Web**: Playwright
- **Daten**: pandas, openpyxl, pdfplumber
- **HTTP**: httpx (async)
- **Config**: pydantic-settings
- **Logging**: loguru
- **Retry**: tenacity
- **Orchestrierung**: Prefect 3.x
- **Testing**: pytest
- **Container**: Docker

### UiPath (Ausnahme)
- Integration über Orchestrator REST API
- Lose Kopplung (APIs, Queues, Dateien)

---

## Governance

**10 Regeln für jeden Bot:**
1. Python-First (Default)
2. Template verwenden
3. Keine hartcodierten Werte
4. Strukturiertes Logging
5. Retry-Mechanismen
6. Tests schreiben
7. Linux-Container-fähig
8. Dokumentation
9. Code-Review
10. Entscheidungen dokumentieren

Details: [Governance-Regeln](docs/03_Governance.md)

---

## Für AI-Agenten

Wenn du ein AI-Agent (Claude, DeepSeek, etc.) in diesem Repository arbeitest:
- Lies `AGENTS.md` für deinen System-Kontext
- Lies `agent/CLAUDE.md` für deine Persona als RPA-Hybrid-Architekt
- Befolge die Governance-Regeln strikt
- Denke Python-first

---

## Lizenz

Internes Framework — alle Rechte vorbehalten.

## Version

1.0 — Mai 2026
