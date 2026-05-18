# ADR-0005: merle-core v0.2 – Architektur, Observability und zentrale Patterns

**Status:** Akzeptiert  
**Datum:** 2026-05-16  
**Betroffene Komponente:** `merle-core` (packages/merle-core)

---

## 1. Kontext

Nach Phase 0/1 ist `merle-core` noch sehr schlank (BaseBot, RpaHttpClient, setup_logging).  
Die Vision des Projekts (siehe `docs/concepts/strategie.md`) fordert jedoch starke Observability, einheitliche Resilienz und Vermeidung von Boilerplate in den Bots.

In Phase 2 soll `merle-core` zum echten wiederverwendbaren Framework ausgebaut werden, das:

- OpenTelemetry (Tracing + Metrics) nativ unterstützt
- Playwright-Robustheit, Excel/PDF, UiPath-Queue und Secrets-Management zentral anbietet
- `BaseTask` als Gegenstück zu `BaseBot` etabliert
- Error-Handling und Retry-Patterns zentralisiert

## 2. Entscheidung

Wir bauen `merle-core` auf Version **0.2.0** massiv aus mit folgender modularer Struktur:

```
merle_core/
├── base.py                 # BaseBot + BaseTask (erweitert mit Metrics & Self-Healing)
├── http.py
├── logging.py              # + OTEL Sink
├── exceptions.py           # Merle-spezifische Exceptions
├── retry.py                # Zentrale Policies + Dekoratoren
├── observability/          # Metrics, Tracing, Health
├── playwright/             # Robust Wrapper (stealth, auto-screenshot, proxy)
├── data/                   # Excel, PDF, Email
├── uipath/                 # Orchestrator Queue & Job Client
└── secrets/                # Azure Key Vault + Pydantic-Integration
```

**Wichtige Prinzipien:**

- Kern bleibt leicht (`loguru`, `tenacity`, `httpx`, `pydantic-settings`)
- Alles Weitere kommt über **optionale Extras** (`playwright`, `azure`, `observability`, `data`)
- Jede neue Basisklasse (`BaseTask`, RobustPlaywright etc.) emittiert automatisch Metriken und Traces
- Secrets werden nie mehr direkt aus `.env` in Produktion gelesen (Key Vault first)

## 3. Neue Governance-Regel (Regel 10)

**Regel 10 – Merle-Core-Pflicht**  
Jeder neue Python-Bot **muss** `merle-core` als Abhängigkeit deklarieren und die zentralen Basisklassen sowie Utilities verwenden.  
Manuelles Nachimplementieren von Logging, Retry, Browser-Handling oder Secrets-Handling ist nicht mehr zulässig.

## 4. Technische Umsetzung

- Verwendung von OpenTelemetry (OTLP) als Standard für Tracing + Metrics
- Loguru wird um einen OTEL-Sink erweitert (Trace-ID/Span-ID werden automatisch injiziert)
- Azure Key Vault wird als primärer Secrets-Provider etabliert (mit Fallback auf .env für lokale Entwicklung)
- Playwright-Wrapper kapselt Stealth, Error-Screenshots und Proxy-Handling

## 5. Konsequenzen

**Positiv:**

- Starke Reduktion von Duplizierung und Fehlerquellen
- Einheitliche Observability über alle Bots (Grafana/Loki/Tempo ready)
- Bessere Self-Healing-Fähigkeit von Bots

**Negativ / Risiken:**

- Erhöhter Initialaufwand beim Aufbau von `merle-core`
- Lernkurve für Entwickler (neue Imports und Patterns)
- Komplexität durch optionale Extras

## 6. Umsetzung

Siehe separaten Phase-2-Plan (`docs/plans/phase2-merle-core-observability.md`).

Die Umsetzung erfolgt schrittweise über 2 Wochen, beginnend mit Retry-Patterns, BaseTask und Observability-Grundgerüst.

---

**Entscheidungsträger:** Merle RPA-Hybrid-Architekt
**Review:** Engineering-Team + DevOps (wegen Observability-Stack)
