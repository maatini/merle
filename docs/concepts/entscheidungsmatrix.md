# Entscheidungsmatrix: Python vs. UiPath

## Zweck

Diese Matrix ist das **zentrale Werkzeug** für die Entscheidung, ob ein Automatisierungsvorhaben mit Python oder UiPath umgesetzt wird. Sie muss bei **jedem** neuen Automatisierungsprojekt und bei **jeder** signifikanten Erweiterung konsultiert und dokumentiert werden.

## Entscheidungslogik

Der folgende Entscheidungsfluss ist das **zentrale Steuerungsinstrument** für alle Technologieentscheidungen im Merle-Framework.

![Python vs. UiPath Entscheidungsfluss](assets/images/decisions/python-vs-uipath-decision-flow.jpg)

> **Tipp für Reviews**: Drucke dieses Diagramm aus oder pinne es in deinem Chat. Jede Technologieentscheidung sollte sich an diesem Fluss orientieren und in einem ADR (`docs/decisions/`) dokumentiert werden.

### Kurze Zusammenfassung der Logik

1. **Python-Domäne?** → Web, API, Daten, Business-Logik, Reporting → **Default: Python**
2. **UiPath-Ausnahmekategorie?** → Nur bei Legacy Desktop, sehr hohem Document Understanding Volumen oder zwingendem HITL
3. **Vorteil nachweisbar?** → Prototyp + Messung + Begründung erforderlich

**Niemals ausreichend als Begründung:**
- „Das Team kennt nur UiPath“
- „UiPath hat dafür eine Activity“
- „Das haben wir schon immer so gemacht“

---

**Merke**: 80–90 % aller Automatisierungen sollten mit Python umgesetzt werden. UiPath nur bei **nachgewiesenem** qualitativen oder architektonischen Vorteil.

## Domänen-Matrix

### Python-Domäne (Default)

| Domäne | Beispiele | Technologie |
|--------|-----------|-------------|
| **Web-Automatisierung** | SAP Fiori, Salesforce, beliebige Webportale, Shop-Systeme | Playwright (via rpaframework.Browser) |
| **API-Integration** | REST, GraphQL, SOAP, MS Graph, OData | httpx, zeep (SOAP) |
| **Datenverarbeitung** | Excel-Reports, CSV-Konvertierung, PDF-Extraktion, Datenbank-ETL | pandas, openpyxl, pdfplumber, SQLAlchemy |
| **E-Mail-Verarbeitung** | Posteingangs-Monitoring, Anhang-Extraktion, Auto-Reply | imaplib, MS Graph API, exchangelib |
| **Datei-Operationen** | SFTP-Transfer, Dateisystem-Monitoring, Archivierung | paramiko, watchdog, pathlib |
| **Business-Logik** | Validierungsregeln, Berechnungen, Workflow-Steuerung | Vanilla Python, Prefect |
| **AI/ML-Integration** | Dokument-Klassifikation, NLP, Bilderkennung | transformers, LangChain, OpenCV |
| **Reporting** | Excel-Generierung, PDF-Berichte, Dashboards | openpyxl, reportlab, streamlit |
| **Scheduling/Orchestrierung** | Zeitpläne, Abhängigkeiten, Retries | Prefect 3.x, APScheduler |

### UiPath-Ausnahmekategorien (begründungspflichtig)

| Kategorie | Kriterien für UiPath | Nachweis erforderlich |
|-----------|---------------------|----------------------|
| **Legacy-Desktop-UI** | Win32-Apps mit dynamischen Controls, Citrix, alte SAP GUI | Prototyp mit pywinauto/pywinctl gescheitert ODER nachgewiesene Selektoren-Probleme |
| **Document Understanding (High-End)** | >10k Dokumente/Tag, komplexe Layouts, sehr hohe Genauigkeit (>98 %) | Benchmark UiPath DU vs. Python-Lösung (LayoutLM, Donut) |
| **Enterprise-Orchestrierung + HITL** | Action Center, Attended/Unattended-Queues, komplexe Eskalation | Anforderungsanalyse: Ohne Orchestrator nativ nicht umsetzbar |
| **Citizen-Developer-Team** | >5 Nicht-Entwickler als Bot-Autoren, nicht-geschäftskritisch | Team-Skills-Assessment |

## Bewertungskriterien (Scoring-Modell)

Bei unklaren Fällen: Jedes Kriterium 1 (UiPath) bis 5 (Python) bewerten.

| Kriterium | Gewicht | Beschreibung |
|-----------|---------|--------------|
| Wartbarkeit | 30 % | Code-Review, Diff, Refactoring-Fähigkeit |
| Testbarkeit | 20 % | Unit/Integration/E2E-Tests, CI-Integration |
| Plattformfreiheit | 15 % | Linux-Container-Fähigkeit |
| Entwicklungsgeschwindigkeit | 15 % | Time-to-MVP, Iterationsgeschwindigkeit |
| Kosteneffizienz | 10 % | Lizenzen, Infrastruktur, Wartung |
| Skills-Verfügbarkeit | 10 % | Verfügbare Entwickler im Team/Markt |

**Auswertung:**
- Score ≥ 3,5 → **Python**
- Score 2,5–3,5 → Detaillierte Einzelfallprüfung
- Score < 2,5 → UiPath (mit Begründung)

## Entscheidungsdokumentation

Jede Entscheidung MUSS dokumentiert werden:

```markdown
### Entscheidung: [Projektname] — [Datum]

**Empfehlung**: Python / UiPath
**Score**: X.X / 5.0 (falls Scoring-Modell angewendet)

**Begründung**:
- [Konkreter Grund 1]
- [Konkreter Grund 2]

**Alternativen geprüft**:
- [Alternative 1]: [Warum verworfen]
- [Alternative 2]: [Warum verworfen]

**Risiken**:
- [Risiko 1] → [Mitigation]

**Entscheider**: [Name/Rolle]
**Genehmigt durch**: [Merle RPA-Hybrid-Architekt]
```

## Fallbeispiele

### Beispiel 1: Rechnungsverarbeitung (Web-Portal + SAP Fiori)

**Analyse**: Web-basierte Rechnungserfassung in SAP Fiori + PDF-Extraktion + Excel-Export
**Domäne**: Web-Automatisierung + Datenverarbeitung
**Empfehlung**: **Python** (rpaframework + Playwright + pdfplumber)
**Begründung**: Moderne Web-App, keine Legacy-Desktop-UI. PDF-Extraktion mit Python gleichwertig oder besser.

### Beispiel 2: Alte Win32-Lagerverwaltung mit dynamischen Fenstern

**Analyse**: 20 Jahre alte Lagerverwaltungssoftware, keine API, dynamische Fensterstruktur
**Domäne**: Legacy-Desktop-UI
**Empfehlung**: **UiPath** (nach gescheitertem pywinauto-Prototypen)
**Begründung**: Fenster-Titel und Control-IDs ändern sich dynamisch. UiPath-Selectors mit Fuzzy-Matching und Anchoring robuster. Python-Prototyp (pywinauto) produzierte 30 % Fehlerrate.

### Beispiel 3: HR-Onboarding mit Genehmigungsworkflow

**Analyse**: Formular-basierte Datenerfassung + mehrstufige Genehmigungen + Active-Directory-Integration
**Domäne**: Business-Logik + API + Web
**Empfehlung**: **Python** (Prefect für Workflow + Playwright für Web + ldap3 für AD)
**Begründung**: Alle Komponenten Python-nativ abbildbar. Prefect bietet überlegene Workflow-Steuerung mit Retries, Timeouts und Observability.

## Anti-Patterns

Diese Begründungen sind **nicht** ausreichend für UiPath:

- ❌ „Das Team kennt nur UiPath" → Weiterbildung investieren
- ❌ „UiPath hat eine Activity dafür" → Python hat eine Library dafür
- ❌ „Das haben wir schon immer mit UiPath gemacht" → Technische Schuld abbauen
- ❌ „UiPath ist schneller für einfache Sachen" → Template und Skills beschleunigen Python
- ❌ „Der Kunde verlangt UiPath" → Beratungskompetenz: Python-Vorteile aufzeigen

## Revision

| Version | Datum | Änderung | Autor |
|---------|-------|----------|-------|
| 1.0 | 2026-05-10 | Initiale Version | Merle RPA-Hybrid-Architekt |
