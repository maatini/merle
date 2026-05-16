# Merle

[![License](https://img.shields.io/badge/license-proprietary-red)](./LICENSE)
[![Version](https://img.shields.io/badge/version-0.2.0-blue)](https://github.com/maatini/merle)
[![Python](https://img.shields.io/badge/python-3.11%2B-3776AB?logo=python&logoColor=white)](https://python.org)
[![uv](https://img.shields.io/badge/uv-0.11+-8A2BE2?logo=python)](https://docs.astral.sh/uv/)
[![Strategy](https://img.shields.io/badge/strategy-python--first-success)](./docs/01_Strategie.md)
[![Status](https://img.shields.io/badge/status-active-brightgreen)](https://github.com/maatini/merle)
[![Roadmap](https://img.shields.io/badge/roadmap-orchestration--vision-orange)](./README.md#vision--zukünftige-erweiterungen)

> **⚠️ INTERNAL USE ONLY** — Dieses Repository enthält proprietären Code der Antigravity GmbH.  
> Jegliche unautorisierte Nutzung, Weitergabe oder externe Verwendung ist strengstens untersagt. Siehe [LICENSE](./LICENSE).

<p align="center">
  <img src="merle.png" alt="Merle — Modular Enterprise RPA Lifecycle Engine" width="600">
</p>

**Modular Enterprise RPA Lifecycle Engine**  
Python-First Framework für hybride RPA-Entwicklung.  
Wartbare, testbare und kosteneffiziente Automatisierung — 80–90 % Python, UiPath nur bei nachgewiesenem Vorteil.  
**Zukünftig: Granulare, NATS-basierte Orchestrierung mit KI-Executor und BPMN-Transparenz.**

---

## Schnellstart (uv)

```bash
# 1. Repository klonen & Workspace initialisieren (einmalig)
git clone <repo>
cd merle
uv sync --group dev

# 2. Neuen Python-Bot erstellen (Template)
cp -r python_bots/template/ python_bots/mein_bot/
cd python_bots/mein_bot/

# 3. Bot entwickeln (uv managed)
uv run python main.py

# Linting & Type-Check (am Root oder im Bot-Verzeichnis)
uv run ruff check .
uv run ruff format .
uv run mypy .

# Tests
uv run pytest python_bots -v

# Docker (Template)
docker build -t mein-bot python_bots/template
docker run --env-file .env mein-bot
```

> **Hinweis**: Mit `uv` als Package-Manager werden alle Abhängigkeiten (inkl. `merle-core` aus dem Workspace) automatisch und reproduzierbar verwaltet. Das alte `requirements.txt` + venv-Setup wird schrittweise abgelöst.

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

## Vision & Zukünftige Erweiterungen

Merle entwickelt sich schrittweise zu einer hochskalierbaren, intelligenten und kosteneffizienten Enterprise-RPA-Orchestrierungsplattform. Die folgenden Erweiterungen sind als zentrale Roadmap-Bausteine geplant:

- **Aufteilung von RPA-Tasks in kleinere abgeschlossene Teil-Tasks**  
  Komplexe RPA-Prozesse werden in feingranulare, eigenständig ausführbare und versionierbare Teil-Tasks zerlegt. Dies ermöglicht bessere Parallelisierung, isolierte Fehlerbehandlung, einfacheres Testing, Wiederverwendbarkeit und eine höhere Gesamt-Resilienz des Systems.

- **Speicherung der Teil-Tasks in NATS (Message Broker)**  
  Alle Teil-Tasks, deren Status und Metadaten werden über den hochperformanten, cloud-nativen Message Broker **NATS** verwaltet. NATS bietet persistente Queues, JetStream, Pub/Sub, Request-Reply und exzellente Skalierbarkeit – die ideale Grundlage für eine lose gekoppelte, event-getriebene Architektur. Zur Einsicht und Verwaltung der Streams und Nachrichten nutzen wir die UI **[Cobra-NATS](https://github.com/maatini/cobra-nats)**.

- **Intelligenter Orchestrator verteilt Teil-Tasks auf Rechen-Ressourcen**  
  Ein zentraler, hochverfügbarer Orchestrator übernimmt das Scheduling und Routing der Teil-Tasks auf die verfügbaren Worker-Ressourcen (Docker-Container, Kubernetes-Pods, On-Prem-Server, Cloud-Instanzen). Die Verteilung erfolgt dynamisch und unter Berücksichtigung von Echtzeit-Metriken.

- **Anforderungsprofile für Tasks (UiPath, Python, GPU, RAM+HDD etc.)**  
  Jeder Task und Teil-Task kann ein detailliertes Anforderungsprofil deklarieren:
  - Technologie-Stack: `UiPath`, `Python`, `Path` (andere RPA-Tools)
  - Hardware-Ressourcen: GPU (für ML/CV), CPU-Kerne, RAM, HDD/SSD-Kapazität, Netzwerk-Bandbreite
  Der Orchestrator matched diese Anforderungen automatisch an passende Worker-Nodes (z. B. dedizierte UiPath-Lizenz-Worker oder GPU-beschleunigte Nodes).

- **Prioritäten für Tasks**  
  Tasks und Teil-Tasks erhalten Prioritäten (z. B. `critical`, `high`, `normal`, `low` oder numerisch). Der Orchestrator berücksichtigt diese Prioritäten bei der Scheduling-Entscheidung, um geschäftskritische Prozesse bevorzugt und termingerecht auszuführen (SLA-Support).

- **Ressourcen-Optimierung zur Kosten-Minimierung**  
  Durch intelligente Algorithmen (Predictive Scaling, Workload-Konsolidierung, bevorzugte Nutzung von Spot/Preemptible Instances, Auto-Hibernation nicht ausgelasteter Ressourcen) wird die Ressourcenauslastung optimiert. Ziel ist die nachhaltige Senkung der Betriebskosten bei gleichbleibender oder höherer Durchsatzleistung. Relevante KPIs: Cost-per-Execution, Resource Utilization, Idle-Time.

- **KI als möglicher Executor**  
  Zukünftig können KI-Komponenten (LLM-basierte Agenten, spezialisierte ML-Modelle, Vision-Modelle etc.) als vollwertige Executor für geeignete Teil-Tasks eingesetzt werden. Anwendungsfälle: intelligente Dokumentenklassifikation & -extraktion, kontextbezogene Entscheidungsfindung, Self-Healing bei Fehlern, generative Erstellung von Teil-Logik oder sogar vollständige KI-gestützte Prozessautomatisierung.

- **Transparente Orchestrierung analog BPMN**  
  Die gesamte Task-Orchestrierung, Abhängigkeiten, Datenflüsse, Status-Übergänge und Ausführungshistorie sollen visuell transparent und nachvollziehbar dargestellt werden – angetrieben von der **[BPMNinja Engine](https://github.com/maatini/bpmninja)**. Dies ermöglicht:
  - Einfaches Auditing & Compliance
  - Prozessoptimierung durch Fachabteilungen
  - Bessere Zusammenarbeit zwischen Citizen Developers und RPA-Experten
  - Visuelle Dashboards und Drill-Down-Analysen

Diese Erweiterungen bauen auf dem bestehenden Python-First-Ansatz, Prefect 3.x, Docker und der bestehenden Governance auf. Sie führen Merle schrittweise in Richtung einer vollständig hybriden, KI-gestützten, kostenoptimierten und vollständig transparenten Enterprise-RPA-Plattform.

---

## OpenCode in Merle: RPA-Hybrid-Architekt

Merle bringt eine **projekt-lokale OpenCode-Konfiguration** mit (`/.opencode/`). Sobald du `opencode` im Root des Merle-Repositories startest, ist automatisch der **RPA-Hybrid-Architekt** als Primary Agent aktiv. Er kennt die Entscheidungsmatrix, alle Governance-Regeln, Templates und die Cloud-Native-Architektur im Detail.

### Einfache Nutzung
```bash
# Im Merle-Root
opencode
# → rpa-hybrid Agent ist sofort verfügbar
# → Skills: rpa-process-analyzer, rpa-bot-generator, governance-validator
# → Command: /rpa-new-bot, /rpa-validate
# → Tool: load_rpa_context (MCP)
```

### Cloud-Native RPA im Azure AKS
Da unsere Software-Roboter nicht lokal auf Desktops, sondern **zentral und hochskalierbar in der Cloud (z. B. Azure AKS Cluster)** ausgeführt werden, gelten besondere Anforderungen an den Code. Der RPA-Hybrid-Architekt unterstützt das Entwicklungsteam gezielt bei der Umsetzung dieser Cloud-Native-Paradigmen:

- **Container-Readiness:** Automatisierte Erstellung von Headless-fähigem Code (Playwright, Linux-kompatible Bibliotheken), der ohne Windows-Abhängigkeiten in Docker-Containern und Pods läuft.
- **Stateless & Robust:** Erzwingung von Retry-Mechanismen (Tenacity) und strukturiertem Logging (Loguru) für resiliente Bot-Ausführungen in flüchtigen Cloud-Umgebungen.
- **NATS & Orchestrierung:** Direkte Unterstützung bei der Anbindung an unseren NATS Message Broker für ereignisgesteuerte, verteilte Task-Bearbeitung.

### Integrierte Governance & Tools
Der Agent agiert als strikter Wächter der [Entscheidungsmatrix](docs/02_Wann_Python_vs_UiPath.md) und der Projekt-Governance. Dazu stehen folgende Erweiterungen im `.opencode/`-Verzeichnis zur Verfügung:

1. **`rpa-context` (MCP Tool):** Lädt Projekt-Dokumentationen dynamisch (`load_rpa_context strategy`, `dev-guide`, `governance` …).
2. **`rpa-bot-generator` (Skill):** Erzeugt neue Python-Bots **ausschließlich** auf Basis des verbindlichen Copier-Templates (`templates/bot/`) via `merle new-bot` oder Copier.
3. **`governance-validator` (Skill):** Prüft Code auf Einhaltung aller 10 Governance-Regeln (inkl. Rule 10: merle-core + BaseTask).
4. **Commands:** `/rpa-new-bot` und `/rpa-validate` für schnelle Workflows.

**Hinweis zur Fork-Version:** Das Verzeichnis `rpa-opencode-hybrid/` enthält einen vollständigen OpenCode-Fork und ist **nur** relevant, wenn du selbst Änderungen am OpenCode-Core entwickeln oder eine komplett angepasste Desktop-App bauen möchtest. Für die tägliche Bot-Entwicklung reicht die leichte `.opencode/`-Integration im Root.

Durch diese tiefe Integration verringert OpenCode nicht nur die Entwicklungszeit, sondern garantiert vor allem die **architektonische Integrität** und **Betriebsstabilität** aller Bots in unserer Cloud-Umgebung.

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
│   ├── template/             # Legacy Template (nur noch für alte Bots)
│   └── shared/               # merle-core (installierbares Package, src-layout)
├── templates/
│   └── bot/                  # ✨ Offizielles Copier-Template (merle new-bot)
│       ├── pyproject.toml
│       ├── src/merle_core/
│       │   ├── __init__.py   # BaseBot, RpaHttpClient, setup_logging
│       │   └── ...
│       └── README.md
├── integration_examples/     # Python ↔ UiPath Muster
├── uipath_templates/         # UiPath-Templates (nur Ausnahmen)
├── agent/
│   └── CLAUDE.md             # Merle RPA-Hybrid-Architekt
├── .opencode/                # OpenCode RPA-Erweiterungen (rpa-hybrid Agent, Skills, rpa-context Tool)
│   ├── agent/rpa-hybrid.md   # Primary Agent (automatisch aktiv bei `opencode`)
│   ├── skills/               # rpa-process-analyzer, rpa-bot-generator, governance-validator
│   ├── tool/rpa-context.ts   # MCP-Tool: load_rpa_context
│   └── command/              # /rpa-new-bot, /rpa-validate
├── AGENTS.md                 # AI-Agenten Kontext (DeepSeek-TUI etc.)
└── README.md                 # Diese Datei
```

> **Hinweis zur Roadmap**: Zukünftige Verzeichnisse wie `orchestrator/`, `workers/`, `nats/`, `scheduler/` und `dashboards/` werden bei der Umsetzung der Vision ergänzt.

---

## Dokumentation

Die vollständige Dokumentation findest du unter:

- **MkDocs Material** (empfohlen): `uv run mkdocs serve`
- Online (geplant): docs.merle.example.com

Wichtige Dokumente:
- [Architektur](docs/concepts/architecture.md) (inkl. C4-Diagramme)
- [Governance](docs/03_Governance.md)
- [merle-core](docs/merle-core/index.md) (ab v0.2)
- [Beispiele](examples/README.md) (Web, Excel, UiPath-Hybrid)

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
- **Orchestrierung**: Prefect 3.x (aktuell) → zukünftig NATS + eigener Orchestrator
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

Wenn du als AI-Agent (Claude, DeepSeek, etc.) in diesem Repository arbeitest:
- Lies `AGENTS.md` für deinen System-Kontext
- Lies `agent/CLAUDE.md` für deine Persona als Merle RPA-Hybrid-Architekt
- Befolge die Governance-Regeln strikt
- Denke Python-first
- Berücksichtige bei zukünftigen Erweiterungen die Vision der granularen, NATS-basierten und KI-gestützten Orchestrierung

---

## Contributing

Beiträge zum Merle-Framework erfolgen ausschließlich durch autorisierte Mitarbeiter und Partner.

### Workflow für interne Entwickler

1. **Branch erstellen**: `feature/<kurzbeschreibung>` oder `fix/<issue>`
2. **Code-Qualität**:
   - `uv run ruff check --fix . && uv run ruff format .`
   - `uv run mypy python_bots/shared/src/merle_core`
   - `uv run pytest python_bots -v`
3. **pre-commit Hooks** (empfohlen):
   ```bash
   uv run pre-commit install
   ```
4. **PR erstellen** gegen `develop` (oder `main` für Hotfixes)
5. **Review**: Mindestens ein Senior RPA-Architekt + automatisierte CI (Ruff, Mypy, Tests, Trivy)

### Wichtige Regeln

- **Kein Code ohne Template**: Jeder neue Bot startet aus `python_bots/template/`
- **merle-core** (`python_bots/shared/`) nur bei echter Wiederverwendbarkeit erweitern
- **Keine hartcodierten Secrets/Pfade**
- **Linux-Container-Kompatibilität** ist Pflicht
- Änderungen an der Architektur oder Governance → ADR in `docs/decisions/`

### Fragen?

- Technische Fragen → `#rpa-engineering` (Slack/Teams)
- Architektur-Entscheidungen → `docs/03_Governance.md` + `agent/CLAUDE.md`

## Lizenz

**PROPRIETARY — INTERNAL USE ONLY**

Dieses Repository und alle darin enthaltenen Artefakte sind ausschließlich für den internen Gebrauch bei Antigravity bestimmt. Siehe [LICENSE](./LICENSE) für die vollständige Lizenz.

## Version

**0.2.0** — Phase 0 Foundations (uv + merle-core + CI/CD + pre-commit) — Mai 2026

Frühere Versionen:
- 1.1 — Mai 2026 (initiale Vision & Template)
- 1.0 — Initiales Python-First Framework
