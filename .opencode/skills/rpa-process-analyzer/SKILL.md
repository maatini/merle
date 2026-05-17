# RPA Process Analyzer

## Purpose

Analysiert eine Prozessbeschreibung und gibt eine **fundierte, datenbasierte
Python-vs-UiPath-Empfehlung** mit ausführlicher Begründung.

## When to Use

- Immer wenn ein neuer Automatisierungsprozess beschrieben wird
- Bei Unsicherheit, ob Python oder UiPath die richtige Wahl ist
- Als erster Schritt vor der Bot-Entwicklung

## Process

### 1. Prozess verstehen

Lies die Prozessbeschreibung und extrahiere:

- **Systeme**: Welche Anwendungen/Systeme sind involviert?
- **Schnittstellen**: Web, API, Desktop-UI, Dateien, E-Mail?
- **Daten**: Welche Daten fließen? Welche Formate?
- **Frequenz**: Wie oft läuft der Prozess? Welches Volumen?
- **Komplexität**: Gibt es komplexe Entscheidungslogik?
- **Fehlertoleranz**: Wie kritisch sind Fehler? Welche SLAs?

### 2. Domäne klassifizieren

Ordne den Prozess einer Domäne zu:

**Python-Domäne:**

- Web-Automatisierung (moderne Web-Apps, SAP Fiori, Salesforce)
- API-Integration (REST, GraphQL, SOAP, OData)
- Datenverarbeitung (Excel, CSV, PDF, Datenbanken)
- E-Mail-Verarbeitung (IMAP, MS Graph, Exchange)
- Datei-Operationen (SFTP, Dateisystem-Monitoring)
- Business-Logik (Validierungen, Berechnungen, Workflows)
- AI/ML-Integration (Dokument-Klassifikation, NLP)
- Reporting (Excel-Generierung, PDF-Berichte)

**UiPath-Ausnahmekategorien (nur wenn zwingend):**

- Legacy-Desktop-UI (alte Win32-Apps, Citrix, SAP GUI)
- High-End Document Understanding (>10k Dokumente/Tag, >98 % Genauigkeit)
- Enterprise-Orchestrierung + HITL
- Citizen-Developer-Teams

### 3. Entscheidungslogik anwenden

```
1. Fällt der Prozess klar in die Python-Domäne?
   → JA: Empfehlung PYTHON. Begründung basierend auf Domäne.

2. Fällt er in eine UiPath-Ausnahmekategorie?
   → NEIN: Empfehlung PYTHON. Begründung: Keine UiPath-Ausnahme.
   → JA: Weiter zu Schritt 4.

3. Ist der UiPath-Vorteil NACHWEISBAR?
   → NEIN: Empfehlung PYTHON. Begründung: Kein nachweisbarer Vorteil.
   → JA: Empfehlung UIPATH mit detaillierter Begründung.
```

### 4. Scoring bei unklaren Fällen

Bewerte jedes Kriterium von 1 (UiPath) bis 5 (Python):

| Kriterium                                    | Gewicht |
| -------------------------------------------- | ------- |
| Wartbarkeit (Code-Review, Diff, Refactoring) | 30 %    |
| Testbarkeit (Unit/Integration/E2E, CI)       | 20 %    |
| Plattformfreiheit (Linux-Container)          | 15 %    |
| Entwicklungsgeschwindigkeit (Time-to-MVP)    | 15 %    |
| Kosteneffizienz (Lizenzen, Infrastruktur)    | 10 %    |
| Skills-Verfügbarkeit (Team)                  | 10 %    |

- Score ≥ 3,5 → Python
- Score 2,5–3,5 → Einzelfallprüfung
- Score < 2,5 → UiPath

### 5. Empfehlung ausgeben

Formatiere die Ausgabe als:

```markdown
## Prozessanalyse: [Name]

**Empfehlung**: 🐍 Python / 🔷 UiPath
**Score**: X.X / 5.0 (falls Scoring angewendet)
**Konfidenz**: Hoch / Mittel / Niedrig

### Begründung

- [Konkreter Grund 1 mit Verweis auf Domäne]
- [Konkreter Grund 2 mit Technologie-Vergleich]

### Technologie-Mapping

| Komponente     | Empfohlene Technologie | Begründung |
| -------------- | ---------------------- | ---------- |
| [Komponente 1] | [Tech]                 | [Warum]    |

### Risiken und Mitigation

- [Risiko 1] → [Gegenmaßnahme]

### Alternativen geprüft

- [Alternative]: [Warum verworfen]

### Nächste Schritte

1. [Konkreter nächster Schritt]
2. [Weiterer Schritt]
```

### 6. Bei UiPath-Empfehlung

- **Immer** eine Python-Alternative nennen
- Konkrete Nachteile der Python-Alternative beschreiben
- ADR-Vorlage für `docs/decisions/` bereitstellen

## Anti-Patterns

- ❌ UiPath empfehlen, weil „das Team es kennt"
- ❌ UiPath empfehlen, ohne Python-Alternative geprüft zu haben
- ❌ Vage Begründungen wie „UiPath ist besser für Desktop"
- ❌ Die Entscheidungsmatrix ignorieren

## References

- `docs/02_Wann_Python_vs_UiPath.md` — Vollständige Entscheidungsmatrix
- `docs/01_Strategie.md` — Strategie und Architekturprinzipien
