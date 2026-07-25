# Retry & Resilienz

Merle verwendet **tenacity** als Basis und stellt vordefinierte, RPA-freundliche Retry-Policies bereit.

## Verwendung

```python
from merle_core.retry import with_retry, default_http_retry


@with_retry(policy=default_http_retry)
async def call_external_api(url: str): ...
```

## Verfügbare Policies

| Policy                      | Zweck                 | Empfohlene Anwendung                          |
| --------------------------- | --------------------- | --------------------------------------------- |
| `default_http_retry`        | HTTP 5xx + Timeouts   | API-Aufrufe                                   |
| `browser_retry`             | Playwright-spezifisch | Browser-Automatisierung                       |
| `sensitive_operation_retry` | Konservativ           | Finanz- oder Compliance-kritische Operationen |
| `aggressive_retry`          | Viele Versuche        | Hintergrund-Jobs                              |

## Eigene Policies definieren

```python
from tenacity import retry, stop_after_attempt, wait_exponential

custom_retry = retry(stop=stop_after_attempt(5), wait=wait_exponential(multiplier=1, min=2, max=30), reraise=True)
```

---

**Merke**: Jede externe Abhängigkeit (HTTP, Datenbank, Browser, Dateisystem) sollte mit `@with_retry` geschützt werden. Dies ist Teil von **Governance-Regel 5**.
