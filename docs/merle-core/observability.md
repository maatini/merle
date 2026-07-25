# Observability

Merle integriert **OpenTelemetry** + **loguru** für strukturierte Logs, Traces und Metrics.

## Schnellstart

```python
from merle_core.observability import configure_observability

configure_observability(service_name="rechnungsverarbeitung", environment="production")
```

## Was wird automatisch erfasst?

- Strukturierte Logs (JSON in Produktion)
- HTTP-Requests (via httpx Instrumentierung)
- Playwright-Aktionen (bei Verwendung des Wrappers)
- Task-Ausführungszeiten
- Fehler + Stacktraces

## Export

Standardmäßig wird nach:

- **OTLP** (OpenTelemetry Protocol) → z. B. Grafana Tempo / Loki / Prometheus

## Nützliche Funktionen

```python
from merle_core.observability import get_tracer, get_meter

tracer = get_tracer()
meter = get_meter()
```

---

**Ziel**: Jeder Bot liefert ohne zusätzlichen Aufwand production-grade Observability. Dies ist Teil von **Governance-Regel 4**.
