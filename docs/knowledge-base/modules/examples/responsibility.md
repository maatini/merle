# Examples — Verantwortlichkeiten

Jedes Beispiel demonstriert ein bestimmtes Pattern. Sie sind **Referenz-Code**, nicht Produktionscode.

---

## invoice-processing — Gold Standard

**Owns:** Die vollständigste Referenz-Implementierung. Zeigt ALLE empfohlenen Patterns in einer realen Pipeline.

| Aspekt                 | Details                                                                                         |
| ---------------------- | ----------------------------------------------------------------------------------------------- |
| **Pipeline**           | Download (IMAP) → Parse (PDF) → Enrich (Master Data) → Report (Excel)                           |
| **@tag:basebot**       | `InvoiceProcessingBot(BaseBot)` orchestriert 4 Tasks                                            |
| **@tag:basetask**      | 4 Tasks: `DownloadInvoicesTask`, `ParseInvoicesTask`, `EnrichDataTask`, `WriteReportTask`       |
| **@tag:retry**         | `@with_retry(policy=default_http_retry)` auf IMAP, `@sensitive_operation_retry` auf Master Data |
| **@tag:observability** | `configure_observability(service_name="invoice-processing")`                                    |
| **Self-Healing**       | `_attempt_self_healing()` Hook bei fehlgeschlagenem PDF-Parsing                                 |
| **Simulate Mode**      | Liest `.eml`-Dateien statt echtem IMAP (`settings.simulate = True`)                             |
| **Excel-Output**       | Multi-Sheet, Formeln, bedingte Formatierung, Auto-Fit-Columns                                   |

**Struktur:**

```
invoice-processing/
├── main.py                    # InvoiceProcessingBot(BaseBot)
├── config.py                  # pydantic-settings
├── pyproject.toml             # merle-core[data,observability]
├── tasks/
│   ├── download_invoices.py   # IMAP Download Task
│   ├── parse_pdfs.py          # pdfplumber Extraction Task
│   ├── enrich_data.py         # Master Data Lookup Task
│   └── write_report.py        # Excel Report Task
└── tests/
```

**Wann lesen?** Beim Schreiben eines neuen Bots mit mehreren Tasks, Datenverarbeitung und Observability. Dies ist das **erste Beispiel**, das ein Agent lesen sollte.

---

## web-automation — Browser-Steuerung

**Owns:** Demonstration von @tag:playwright mit Stealth-Mode und automatischen Fehler-Screenshots.

| Aspekt                  | Details                                                                |
| ----------------------- | ---------------------------------------------------------------------- |
| **@tag:basetask**       | `WebAutomationTask(BaseTask)` mit `@with_retry`                        |
| **@tag:playwright**     | `launch_robust_browser(engine="chromium", screenshot_on_failure=True)` |
| **Stealth**             | Automatisch via Browser-Launcher injiziert                             |
| **Screenshot-Handling** | `RobustBrowser.__aexit__` macht Screenshot + HTML-Dump bei Fehlern     |

---

## excel-processing — Datenverarbeitung

**Owns:** Minimales Beispiel für strukturierte Excel-Verarbeitung mit @tag:basetask.

| Aspekt            | Details                                               |
| ----------------- | ----------------------------------------------------- |
| **@tag:basetask** | `ExcelProcessingTask(BaseTask)`                       |
| **Data**          | Nutzt pandas + openpyxl (via merle-core `data` Extra) |

---

## uipath-hybrid — Orchestrator-Integration

**Owns:** Platzhalter für @tag:uipath-hybrid. Zeigt das Konzept, aber die Implementierung verweist auf das zukünftige `merle_core.uipath`-Modul.

**Status:** Noch nicht vollständig. Die tatsächliche Orchestrator-Integration liegt in `integration_examples/orchestrator_api/`.

---

## nats-task-communication — NATS PoC

**Owns:** Demonstration von @tag:nats Task-Kommunikation (Phase 4 Foundation).

| Aspekt             | Details                                                     |
| ------------------ | ----------------------------------------------------------- |
| **Pattern**        | Producer (`WebScraper`) → NATS → Consumer (`DataProcessor`) |
| **@tag:task-spec** | `TaskSpec` (Request) → `TaskResult` (Response)              |
| **@tag:nats**      | `NatsClient.publish_task()`, `NatsClient.request_task()`    |
| **Voraussetzung**  | `docker run -p 4222:4222 nats:latest`                       |

---

## Integration Patterns (integration_examples/)

### orchestrator_api — UiPath REST Client

**Owns:** Referenz-Implementierung für UiPath Orchestrator OAuth2 + OData API.

| Aspekt      | Details                                                                  |
| ----------- | ------------------------------------------------------------------------ |
| **Auth**    | OAuth2 Client Credentials Grant                                          |
| **Ops**     | Start Job, Get Status, Add Queue Item                                    |
| **HTTP**    | `httpx.AsyncClient`                                                      |
| **Secrets** | `UIPATH_CLIENT_ID`, `UIPATH_CLIENT_SECRET`, `UIPATH_TENANT` via env vars |

> **Hinweis:** Wird langfristig durch `merle_core.uipath.UiPathOrchestratorClient` ersetzt.

### file_based_integration — Dateibasierter Austausch

**Owns:** Pattern für lose Kopplung via Dateisystem (JSON/CSV).

| Aspekt        | Details                                               |
| ------------- | ----------------------------------------------------- |
| **Schreiben** | Python schreibt JSON → `shared_path/for_uipath/`      |
| **Lesen**     | Python liest CSV ← `shared_path/from_uipath/`         |
| **Archiv**    | Verarbeitete Dateien → `shared_path/archive/`         |
| **Trade-off** | Einfach, kein API nötig — aber kein Echtzeit-Feedback |

### python_scope — UiPath → Python

**Owns:** Dokumentation (README.md), kein Code. Beschreibt, wie UiPath Workflows Python via Python Scope Activity aufrufen.

- Python 3.11+ auf UiPath Robot installieren
- Code in `.py`-Dateien (nicht inline)
- Klare Input/Output-Verträge

---

## Was Examples **nicht** besitzen

- **Keine** Produktionsreife — Fehlerbehandlung ist demonstrativ, nicht exhaustiv
- **Keine** CI/CD-Integration (außer invoice-processing)
- **Keine** echten Secrets — alle Credentials sind env-vars oder simuliert
