# Phase 2 Plan: merle-core v0.2 – Core Framework & Observability

**Zeitraum:** Wochen 3–4  
**Ziel:** `merle-core` wird zum echten wiederverwendbaren Powerhouse für alle Merle-Bots.

---

## 1. Vision & Erfolgsmetriken

**Vision:**  
Jeder neue Merle-Bot startet mit einem starken, beobachtbaren, resilienten Fundament aus `merle-core`. Entwickler schreiben fast nur noch Business-Logik, nicht mehr Infrastruktur (Retry, Logging, Secrets, Browser-Steuerung, Monitoring).

**Erfolgsmetriken (Phase 2):**

- `merle-core` v0.2 enthält **mindestens 8–10** hochwertige, getestete Module
- Jeder Bot kann mit `uv add merle-core[playwright,azure,observability]` ein vollständiges Observability- und Resilience-Stack bekommen
- Neue Governance-Regel: **„Jeder Bot muss merle-core verwenden“**
- OpenTelemetry + Loguru-Integration ist produktionsreif (OTLP → Grafana Stack)
- Azure Key Vault Integration funktioniert nahtlos über `pydantic-settings`

---

## 2. Aktueller Stand (nach Phase 0 + 1)

- `merle-core` (in `python_bots/shared/src/merle_core/`) hat derzeit nur:
  - `BaseBot`
  - `RpaHttpClient`
  - `setup_logging`
- Keine Observability, keine Playwright-Wrapper, keine Secrets-Lösung, keine zentralen Retry-Patterns, kein `BaseTask`

---

## 3. Vorgeschlagene Modulstruktur für v0.2

```python
merle_core/
├── __init__.py
├── base.py                 # BaseBot + BaseTask (neue zentrale Klassen)
├── http.py                 # RpaHttpClient (verbessert)
├── logging.py              # setup_logging + OTEL-Sink
├── exceptions.py           # Merle-spezifische Exception-Hierarchie
├── retry.py                # Zentrale Retry-Policies + dekoratoren
│
├── observability/
│   ├── __init__.py
│   ├── metrics.py          # OTEL + Prometheus Metrics
│   ├── tracing.py          # Distributed Tracing (Spans)
│   └── health.py           # Erweiterte Health-Checks
│
├── playwright/
│   ├── __init__.py
│   ├── browser.py          # RobustPlaywright (Context + Page Factory)
│   ├── stealth.py          # Stealth-Plugin, User-Agent Rotation
│   ├── utils.py            # auto_screenshot_on_failure, proxy support
│   └── exceptions.py
│
├── data/
│   ├── __init__.py
│   ├── excel.py            # ExcelReader/Writer mit openpyxl + pandas
│   ├── pdf.py              # PDFExtractor (pdfplumber)
│   └── email.py            # IMAP/SMTP + Outlook Graph (optional)
│
├── uipath/
│   ├── __init__.py
│   ├── orchestrator.py     # UiPath Orchestrator REST Client
│   └── queue.py            # QueueItem add/get/set/transaction
│
└── secrets/
    ├── __init__.py
    ├── base.py
    ├── azure.py            # Azure Key Vault Provider
    └── pydantic.py         # AzureKeyVaultSettings (Mixin für BaseSettings)
```

Das ergibt **ca. 10–12 logische Module**, gruppiert in sinnvolle Namespaces.

---

## 4. Technische Schlüsselentscheidungen

### 4.1 OpenTelemetry + Loguru

- Verwende `opentelemetry-api` + `opentelemetry-sdk`
- Exporter: `opentelemetry-exporter-otlp-proto-grpc` (empfohlen für Grafana Tempo + Loki)
- Loguru → OTEL: Eigenen Sink schreiben (`OTELLogSink`), der `logger.add()` mit structurierten Attributen unterstützt
- Automatische Injection von Trace-ID / Span-ID in Loguru-Logs

**Extra:** `observability`

### 4.2 Playwright Robust Wrapper (sehr wichtiges Modul)

Ziel: Kein Bot schreibt mehr rohes Playwright.

Features:

- `RobustBrowser` Context Manager
- Stealth (playwright-stealth oder eigene Implementierung)
- Automatisches Screenshot + HTML-Dump bei Fehlern (in `logs/failures/`)
- Proxy-Support (pro Bot konfigurierbar)
- Retry + Circuit Breaker um Browser-Operationen
- Page Object Factory Pattern

**Extra:** `playwright`

### 4.3 Secrets Management (Azure Key Vault)

- Neuer `AzureKeyVaultProvider`
- Integration in `pydantic-settings` via custom `AzureKeyVaultSettings` Base-Klasse
- Fallback-Kette: Key Vault → .env → Umgebungsvariable
- Guideline-Dokument (`docs/concepts/secrets-management.md`)

**Extra:** `azure`

### 4.4 BaseTask + erweitertes BaseBot

- `BaseTask` als Pendant zu `BaseBot` für feingranulare Tasks
- Beide bekommen:
  - Automatische Metrik-Emission (execution_time, success_rate, error_count)
  - Self-Healing Hooks (`on_failure`, `on_retry_exhausted`, `fallback`)
  - Automatisches Tracing (OTEL Span pro `run()` / `execute()`)

### 4.5 Zentrales Retry-Modul

- `retry.py` enthält vordefinierte Policies:
  - `default_http_retry`
  - `aggressive_browser_retry`
  - `sensitive_operation_retry`
- Dekoratoren: `@with_retry(policy=...)`
- Integration mit OTEL (Retry-Count als Span-Attribute)

---

## 5. Packaging & Versionierung

- `merle-core` wird auf **0.2.0** gehoben
- Verwendung von PEP 621 Extras:

```toml
[project.optional-dependencies]
playwright = ["playwright>=1.40"]
azure = ["azure-identity>=1.16", "azure-keyvault-secrets>=4.8"]
observability = [
    "opentelemetry-api>=1.25",
    "opentelemetry-sdk>=1.25",
    "opentelemetry-exporter-otlp>=1.25",
]
data = ["pandas>=2.0", "openpyxl>=3.1", "pdfplumber>=0.10"]
```

- `merle-core` bleibt weiterhin leicht (Core-Deps: loguru, tenacity, httpx, pydantic)

---

## 6. Neue Governance-Regel (Regel 10)

**Regel 10: Merle-Core-Pflicht**

**Regel**: Jeder Python-Bot **muss** `merle-core` als Abhängigkeit verwenden und die bereitgestellten Basisklassen (`BaseBot`, `BaseTask`) sowie zentralen Utilities nutzen.  
**Begründung**: Vermeidung von Duplizierung, garantierte Observability, einheitliche Fehlerbehandlung und Secrets-Handhabung.  
**Durchsetzung**: `governance-validator` + `rpa-bot-generator` Skill prüfen auf Import von `merle_core`.

---

## 7. Umsetzungsreihenfolge (empfohlen)

**Woche 3 – Fundament & Observability**

1. `exceptions.py` + `retry.py` (zentral)
2. Erweiterung von `BaseBot` + Einführung von `BaseTask`
3. `observability/` Paket (Metrics + Tracing)
4. `logging.py` mit OTEL-Sink
5. ADR-0005 schreiben

**Woche 4 – Power-Features** 6. `playwright/` Wrapper (hoher Wert) 7. `secrets/` + Azure Key Vault + Pydantic Integration 8. `uipath/` Queue Helpers (basiert auf bestehendem Beispiel) 9. `data/` (Excel + PDF) – priorisiert nach Bedarf 10. Neue Governance-Regel + Guideline-Dokument `docs/concepts/secrets-management.md` 11. Update des Templates (`templates/bot/`) auf `merle-core>=0.2`

---

## 8. Offene Fragen an den User

1. **Priorisierung der Module**  
   Welche 3–4 Module sind in den nächsten 2 Wochen **am wichtigsten**?

   - Playwright Wrapper?
   - Azure Key Vault + Secrets?
   - OpenTelemetry Observability?
   - UiPath Queue Helpers?

2. **OpenTelemetry Stack**  
   Sollen wir konkret auf **Grafana Stack** (Loki + Tempo + Prometheus) ausrichten, oder allgemein OTLP halten?

3. **Self-Healing Pattern**  
   Wie weit soll das gehen? Nur Retry + Fallback, oder auch einfache "Circuit Breaker" + "Bulkhead" Patterns?

4. **Playwright Stealth**  
   Wollen wir `playwright-stealth` als Dependency nehmen oder eine eigene, wartbare Lösung bauen?

5. **Abhängigkeit von `merle-core` erzwingen**  
   Ab wann soll der `governance-validator` und der Bot-Generator **zwingend** `merle-core` voraussetzen?

---

## 9. Risiken

- Zu viele optionale Extras → Komplexität im Packaging
- OTEL + Loguru Bridging kann tricky sein (besonders mit strukturierten Logs)
- Azure SDKs sind relativ schwer

**Gegenmaßnahme**: Modulare Extras + klare Dokumentation + schrittweise Einführung.

---

**Nächster Schritt nach Freigabe:**  
Ich beginne mit der Erstellung von ADR-0005 + der Kernstruktur (`retry`, `exceptions`, `BaseTask`, Observability-Grundgerüst).

Bereit für dein Feedback zu Priorisierung und Scope.
