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

## OpenCode und die Entwicklung von RPA – eine klare Erklärung

OpenCode ist ein **open-source KI-Coding-Agent**. Das bedeutet: Es ist ein kostenloses, frei einsehbares Programm, das Entwicklern beim Schreiben von Code hilft. Es läuft direkt im Terminal, in der Entwicklungsumgebung (IDE) oder als Desktop-App. 

Die **Spezialisierung** von OpenCode liegt darin, dass es genau auf Programmieraufgaben zugeschnitten ist. Es versteht Code sehr gut (dank LSP-Unterstützung), kann mit über 75 verschiedenen KI-Modellen arbeiten (z. B. Claude, GPT, Gemini oder sogar komplett lokale Modelle auf dem eigenen Rechner) und lässt sich mit eigenen Tools und „Agenten“ erweitern. Es ist nicht an einen einzigen Anbieter gebunden und kann komplett offline laufen.

### Warum das die RPA-Entwicklung stark verbessert

**RPA** (Robotic Process Automation) bedeutet: Man baut Software-Roboter, die am Computer genau das machen, was sonst ein Mensch von Hand erledigt – zum Beispiel Daten aus Excel in ein altes Fachverfahren kopieren, Rechnungen prüfen oder Formulare ausfüllen. 

Dafür braucht man oft **viel Code** (in Python, C#, JavaScript oder PowerShell). Dieser Code muss mit Benutzeroberflächen umgehen, Wartezeiten einplanen, Fehler abfangen und mit vielen verschiedenen Programmen zusammenarbeiten. Das Schreiben, Testen und Pflegen dieses Codes ist normalerweise zeitaufwendig, teuer und fehleranfällig.

Hier kommt die Spezialisierung von OpenCode ins Spiel – und das macht einen großen Unterschied:

1. **Viel schneller Code schreiben**  
   Du sagst in normaler Sprache, was der Roboter tun soll: „Erstelle ein Python-Skript, das sich bei SAP anmeldet, die offenen Bestellungen sucht und als Excel-Datei speichert.“ OpenCode schreibt dir den passenden Code vor, ergänzt fehlende Teile oder schlägt bessere Lösungen vor. Statt stundenlang zu tippen, brauchst du oft nur noch kleine Anpassungen.

2. **Bessere und stabilere Roboter**  
   RPA-Code muss sehr zuverlässig sein – sonst bricht der Roboter bei jeder kleinen Änderung in der Benutzeroberfläche ab. OpenCode kennt typische RPA-Muster (z. B. wie man auf Elemente klickt, auf das Erscheinen von Fenstern wartet oder mit Fehlermeldungen umgeht). Die KI hilft dabei, robusten Code zu erzeugen und häufige Fehler schon beim Schreiben zu vermeiden.

3. **Unterstützt genau die Techniken, die in RPA gebraucht werden**  
   Viele RPA-Lösungen nutzen Python mit Bibliotheken wie Playwright, Selenium oder pywinauto, oder sie erweitern OpenRPA und ähnliche Tools. OpenCode versteht all diese Sprachen und Frameworks sehr gut und kann Code dafür gezielt verbessern oder erklären.

4. **Datenschutz und Unabhängigkeit (besonders wichtig in Firmen und Behörden)**  
   Weil OpenCode komplett open-source ist und lokale KI-Modelle unterstützt, muss man sensible Daten oder internen Code nicht in die Cloud schicken. Man kann alles auf dem eigenen Rechner oder Server laufen lassen. Das ist ein großer Vorteil gegenüber reinen Cloud-KI-Tools, wenn es um vertrauliche Prozesse geht.

5. **Einfacher erweiterbar für RPA-spezifische Aufgaben**  
   Man kann eigene „Skills“ oder Zusatz-Tools bauen. Zum Beispiel einen Agenten, der automatisch RPA-Skripte testet, Dokumentation schreibt oder sich mit einem RPA-Orchestrierer (z. B. OpenFlow oder UiPath Orchestrator) verbindet. So wird aus einem reinen Coding-Helfer ein echtes Automatisierungs-Werkzeug.

6. **Weniger Einstiegshürde und bessere Zusammenarbeit**  
   Auch Entwickler, die RPA noch nicht so gut kennen, werden mit OpenCode schneller gut. Die KI erklärt, warum etwas so gemacht wird. Teams können eigene Prompts, Tools oder ganze Agenten teilen und gemeinsam weiterentwickeln – Wissen bleibt im Unternehmen und geht nicht verloren.

### Das große Ganze

Durch die Spezialisierung von OpenCode als flexibler, offener und mächtiger KI-Coding-Assistent wird die Entwicklung von RPA-Lösungen:
- **schneller** (weniger Zeit für Routine-Code),
- **günstiger** (weniger Entwicklerstunden),
- **sicherer** (besserer Code + volle Kontrolle über Daten),
- **zugänglicher** (auch für Teams mit weniger RPA-Erfahrung) und
- **zukunftssicherer** (keine Abhängigkeit von einem einzigen KI-Anbieter).

Kurz gesagt: OpenCode nimmt den Entwicklern den mühsamen Teil der RPA-Programmierung ab und lässt sie sich auf das Wesentliche konzentrieren – nämlich die Geschäftsprozesse wirklich gut zu automatisieren. Gleichzeitig bleibt alles transparent, anpassbar und unter eigener Kontrolle.

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
