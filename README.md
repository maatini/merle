# Merle

[![License](https://img.shields.io/badge/license-proprietary-red)](./LICENSE)
[![Version](https://img.shields.io/badge/version-1.1-blue)](https://github.com/maatini/merle)
[![Python](https://img.shields.io/badge/python-3.11%2B-3776AB?logo=python&logoColor=white)](https://python.org)
[![Strategy](https://img.shields.io/badge/strategy-python--first-success)](./docs/01_Strategie.md)
[![Status](https://img.shields.io/badge/status-active-brightgreen)](https://github.com/maatini/merle)
[![Roadmap](https://img.shields.io/badge/roadmap-orchestration--vision-orange)](./README.md#vision--zukünftige-erweiterungen)

<p align="center">
  <img src="merle.png" alt="Merle — Modern Enterprise RPA Leadership Environment" width="600">
</p>

**Modern Enterprise RPA Leadership Environment**  
Python-First Framework für hybride RPA-Entwicklung.  
Wartbare, testbare und kosteneffiziente Automatisierung — 80–90 % Python, UiPath nur bei nachgewiesenem Vorteil.  
**Zukünftig: Granulare, NATS-basierte Orchestrierung mit KI-Executor und BPMN-Transparenz.**

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

## Vision & Zukünftige Erweiterungen

Merle entwickelt sich schrittweise zu einer hochskalierbaren, intelligenten und kosteneffizienten Enterprise-RPA-Orchestrierungsplattform. Die folgenden Erweiterungen sind als zentrale Roadmap-Bausteine geplant:

- **Aufteilung von RPA-Tasks in kleinere abgeschlossene Teil-Tasks**  
  Komplexe RPA-Prozesse werden in feingranulare, eigenständig ausführbare und versionierbare Teil-Tasks zerlegt. Dies ermöglicht bessere Parallelisierung, isolierte Fehlerbehandlung, einfacheres Testing, Wiederverwendbarkeit und eine höhere Gesamt-Resilienz des Systems.

- **Speicherung der Teil-Tasks in NATS (Message Broker)**  
  Alle Teil-Tasks, deren Status und Metadaten werden über den hochperformanten, cloud-nativen Message Broker **[NATS (cobra-nats)](https://github.com/maatini/cobra-nats)** verwaltet. NATS bietet persistente Queues, JetStream, Pub/Sub, Request-Reply und exzellente Skalierbarkeit – die ideale Grundlage für eine lose gekoppelte, event-getriebene Architektur.

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

Für Merle wird eine speziell angepasste OpenCode-Version erstellt. Diese ist im Verzeichnis `rpa-opencode-hybrid/` enthalten und explizit als *RPA-Hybrid-Architekt* für das Merle-Framework konfiguriert. Er kennt unsere Leitplanken, Templates und die Systemarchitektur im Detail.

### Cloud-Native RPA im Azure AKS
Da unsere Software-Roboter nicht lokal auf Desktops, sondern **zentral und hochskalierbar in der Cloud (z. B. Azure AKS Cluster)** ausgeführt werden, gelten besondere Anforderungen an den Code. OpenCode unterstützt das Entwicklungsteam gezielt bei der Umsetzung dieser Cloud-Native-Paradigmen:

- **Container-Readiness:** Automatisierte Erstellung von Headless-fähigem Code (Playwright, Linux-kompatible Bibliotheken), der ohne Windows-Abhängigkeiten in Docker-Containern und Pods läuft.
- **Stateless & Robust:** Erzwingung von Retry-Mechanismen (Tenacity) und strukturiertem Logging (Loguru) für resiliente Bot-Ausführungen in flüchtigen Cloud-Umgebungen.
- **NATS & Orchestrierung:** Direkte Unterstützung bei der Anbindung an unseren NATS Message Broker für ereignisgesteuerte, verteilte Task-Bearbeitung.

### Integrierte Governance & Tools
Der OpenCode-Agent agiert als strikter Wächter der [Entscheidungsmatrix](docs/02_Wann_Python_vs_UiPath.md) und der Projekt-Governance. Dazu greift er auf unsere spezifischen Tools und Skills im `.opencode/`-Verzeichnis zurück:

1. **`rpa-context` (MCP Tool):** Lädt Projekt-Dokumentationen dynamisch und stellt sicher, dass Architekturentscheidungen immer auf dem neuesten Stand des Frameworks basieren.
2. **`rpa-bot-generator` (Skill):** Erzeugt neue Python-Bots ausschließlich auf Basis des verbindlichen Templates (`python_bots/template/`) – ein Start "von der grünen Wiese" ist ausgeschlossen.
3. **`governance-validator` (Skill):** Prüft Code auf hardcodierte Pfade, fehlendes Error Handling und Container-Kompatibilität, bevor er in den AKS-Cluster deployed wird.

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
│   ├── template/             # ✨ Verbindliches Bot-Template
│   └── shared/               # Gemeinsame Utilities
├── integration_examples/     # Python ↔ UiPath Muster
├── uipath_templates/         # UiPath-Templates (nur Ausnahmen)
├── agent/
│   └── CLAUDE.md             # Merle RPA-Hybrid-Architekt
├── AGENTS.md                 # AI-Agenten Kontext
└── README.md                 # Diese Datei
```

> **Hinweis zur Roadmap**: Zukünftige Verzeichnisse wie `orchestrator/`, `workers/`, `nats/`, `scheduler/` und `dashboards/` werden bei der Umsetzung der Vision ergänzt.

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

## Lizenz

Internes Framework — alle Rechte vorbehalten.

## Version

1.1 — Mai 2026 (inkl. detaillierter Orchestrierungs-Vision)
