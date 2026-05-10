# Merle-Strategie: Python-First

## Strategische Ausrichtung

Dieses Dokument definiert die technologische Strategie für das **Merle-Framework** (Modern Enterprise RPA Leadership Environment).  
Es ist die normative Grundlage für **alle** Architekturentscheidungen in Automatisierungsprojekten.

### Leitsatz

> **Python ist der Default. UiPath ist die begründungspflichtige Ausnahme.**

Wir wollen 80–90 % aller Automatisierungen in modernem, Python-basiertem Code umsetzen.  
UiPath wird nur dann eingesetzt, wenn ein **nachgewiesener qualitativer oder architektonischer Vorteil** besteht, der mit Python nicht oder nur mit unverhältnismäßigem Aufwand erreichbar ist.

---

## Warum Python-First?

### Technische Vorteile

| Kriterium | Python | UiPath |
|-----------|--------|--------|
| **Wartbarkeit** | Klarer Code, Git-diff-fähig, Review-fähig | Visuelle Workflows, schwer diff-bar, kein Standard-Review |
| **Testbarkeit** | pytest, CI/CD-integrierbar, Unit/Integration/E2E | Eingeschränkt (Test Manager, begrenzte Mock-Möglichkeiten) |
| **Plattformunabhängigkeit** | Linux, macOS, Windows, Container | Windows only (Studio + Robot) |
| **CI/CD-Integration** | Native Git-Workflows, GitHub Actions, Jenkins | Orchestrator-gebunden, komplexe CI/CD-Pipelines |
| **Kosteneffizienz** | Open Source, keine Lizenzkosten pro Runtime | Pro-Robot-Lizenzierung, Studio-Lizenzen |
| **Skalierbarkeit** | Container-basiert, Kubernetes, Prefect | Orchestrator-basiert, begrenzte horizontale Skalierung |
| **AI/ML-Integration** | Direkt: LangChain, HuggingFace, llama-cpp | Nur über Activities/Connectors, hohe Abstraktion |
| **Entwicklergeschwindigkeit** | Standard-Tooling, IDE-Freiheit, schnelle Iteration | Proprietäre Studio-Umgebung, langsamere Dev-Schleifen |

### Organisatorische Vorteile

1. **Größerer Talent-Pool**: Python-Entwickler sind breiter verfügbar und günstiger als UiPath-zertifizierte Entwickler.
2. **Kein Vendor-Lock-in**: Volle Kontrolle über Abhängigkeiten und Deployment.
3. **Knowledge-Sharing**: Patterns und Libraries sind über Projekte hinweg wiederverwendbar.
4. **Future-Proofing**: Python ist die dominierende Sprache für KI/Automatisierung und wächst weiter.

---

## Die 80/90-Regel im Detail

### Python-Domäne (80–90 % der Fälle)

**Web-Automatisierung**
- Playwright ist stabiler, schneller und wartbarer als UiPath-Browser-Automation
- Moderne Web-Apps (React, Angular, Vue) werden besser unterstützt
- Headless-Betrieb für Server-/Container-Deployment

**API-Integrationen**
- REST, GraphQL, SOAP: Python hat überlegene HTTP-Client-Bibliotheken (httpx, requests)
- Async-fähig (asyncio, aiohttp) für hohe Durchsätze
- OpenAPI/Swagger-Codegen direkt nutzbar

**Datenverarbeitung**
- Excel, CSV, PDF: pandas, openpyxl, reportlab, pdfplumber
- Datenbanken: SQLAlchemy, direkte DBAPI-Treiber
- ETL-Pipelines: Prefect, Apache Airflow

**Business-Logik**
- Komplexe Regeln, Berechnungen, Validierungen
- Zustandsautomaten und Workflows
- Integration mit externen KI-Diensten

**Datei- und Systemoperationen**
- pathlib, shutil, watchdog für Dateisystem-Monitoring
- SFTP/FTPS über paramiko
- E-Mail-Verarbeitung (IMAP, SMTP, MS Graph)

### UiPath-Domäne (10–20 %, nur bei zwingendem Bedarf)

**Legacy-Desktop-UI-Automatisierung**
- Sehr komplexe, dynamische Win32-Apps (alte SAP GUI, Citrix)
- Hochdynamische UI-Elemente, die mit Accessibility-APIs schwer greifbar sind
- Begründung: UiPath-Selectors sind in diesen Szenarien oft robuster

**Hochvolumige Document Understanding mit höchsten Genauigkeitsanforderungen**
- >10.000 Dokumente/Tag mit komplexen Layouts
- Wenn UiPath DU nachweislich bessere Extraktionsgenauigkeit liefert
- Begründung: UiPath DU ist ein ausgereiftes, vortrainiertes System

**Starkes Enterprise-Orchestrierung + Human-in-the-Loop (HITL)**
- Wenn Action Center, Queues und Attended/Unattended-Orchestrierung zwingend benötigt werden
- Wenn HITL-Prozesse mit komplexen Eskalations-Workflows
- Begründung: UiPath Orchestrator bietet hier integrierte Lösungen

**Citizen-Developer-Teams**
- Wenn viele Nicht-Programmierer Bots bauen sollen
- Nur für klar abgegrenzte, nicht-geschäftskritische Module
- Begründung: Visuelle Low-Code-Entwicklung senkt die Einstiegshürde

---

## Architekturprinzipien

### 1. Loose Coupling
Python- und UiPath-Komponenten kommunizieren nur über wohldefinierte Schnittstellen:
- REST APIs (Orchestrator API, eigene Microservices)
- Message Queues (RabbitMQ, Redis)
- Dateibasierte Integration (CSV, JSON, XML über geteilte Pfade)

### 2. Container-First
Jeder Python-Bot muss in einem Linux-Container lauffähig sein:
- Dockerfile im Template
- Keine Windows-only-Abhängigkeiten
- Umgebungsvariablen für Konfiguration (12-Factor-App)

### 3. Observability
Jeder Bot muss beobachtbar sein:
- Strukturiertes Logging (loguru, JSON-Format)
- Metriken (Prometheus-Format)
- Health-Checks
- Fehler-Reporting (Sentry oder ähnlich)

### 4. Testbarkeit
Jeder Bot muss testbar sein:
- Unit-Tests für Business-Logik
- Integration-Tests mit Mocks für externe Systeme
- E2E-Tests für kritische Pfade (mit Playwright)

### 5. GitOps
Alles ist Code, alles ist versioniert:
- Bot-Code in Git
- Konfiguration in Git (pydantic-settings, .env.example)
- Infrastruktur als Code (Docker Compose, Terraform wenn nötig)

---

## Rollen und Verantwortlichkeiten

| Rolle | Verantwortung |
|-------|---------------|
| **Merle RPA-Hybrid-Architekt** | Entscheidet Python vs. UiPath, reviewt Architektur, setzt Governance durch |
| **Python-RPA-Entwickler** | Entwickelt Python-Bots nach Template, schreibt Tests |
| **UiPath-Entwickler** | Entwickelt UiPath-Komponenten nur bei freigegebenen Ausnahmen |
| **DevOps/Automation Engineer** | CI/CD-Pipelines, Container-Deployment, Monitoring |

---

## Technologie-Stack (verbindlich)

### Python (Default)
- **Runtime**: Python 3.11+
- **RPA-Framework**: rpaframework >= 28.0
- **Web-Automation**: Playwright (via rpaframework oder direkt)
- **Daten**: pandas >= 2.0, openpyxl, pdfplumber
- **HTTP**: httpx (async-first)
- **Config**: pydantic-settings
- **Logging**: loguru
- **Retry/Resilience**: tenacity
- **Orchestrierung**: Prefect 3.x
- **Testing**: pytest, pytest-playwright, pytest-asyncio
- **Container**: Docker, docker-compose

### UiPath (Ausnahme)
- **Studio**: Aktuelle LTS-Version
- **Integration**: Orchestrator REST API, Python Scope Activity
- **Deployment**: Orchestrator-basiert

---

## Messung des Erfolgs

### KPIs für die Hybrid-Strategie
1. **Python-Anteil**: Ziel > 80 % aller neuen Automatisierungen
2. **UiPath-Begründungsquote**: Jede UiPath-Nutzung hat dokumentierte Begründung
3. **Template-Adhärenz**: > 95 % der Python-Bots nutzen das Template
4. **Testabdeckung**: > 70 % für Python-Bots
5. **Container-Fähigkeit**: 100 % der Python-Bots sind Docker-fähig
6. **Time-to-First-Automation**: Reduktion durch Template-Wiederverwendung

---

## Revision

| Version | Datum | Änderung | Autor |
|---------|-------|----------|-------|
| 1.0 | 2026-05-10 | Initiale Version | Merle RPA-Hybrid-Architekt |
