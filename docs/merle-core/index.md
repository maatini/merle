# merle-core

`merle-core` ist das **zentrale, wiederverwendbare Python-Package** für alle Merle-Bots.

Es kapselt wiederkehrende Infrastruktur (Resilienz, Observability, Secrets, Browser-Steuerung, NATS-Kommunikation), sodass Entwickler sich fast ausschließlich auf die fachliche Business-Logik konzentrieren können.

## Verfügbare Bausteine

![merle-core Komponenten](../assets/images/architecture/merle-core-components.jpg)

## Schnellstart

```bash
uv add merle-core                           # Basis (BaseTask, Retry, Logging, HTTP)
uv add merle-core[playwright]               # + Playwright + Chromium
uv add merle-core[lightpanda]               # + Lightpanda (Zig, CDP, ressourcenschonend)
uv add merle-core[observability]            # + OpenTelemetry
uv add merle-core[azure]                    # + Azure Key Vault + pydantic-settings
uv add merle-core[nats]                     # + NATS Client (Phase-4 Foundation)
uv add merle-core[data]                     # + pandas, openpyxl, pdfplumber
```

## Kern-Module

| Modul                  | Beschreibung                                            | Dokumentation                     |
| ---------------------- | ------------------------------------------------------- | --------------------------------- |
| **BaseBot & BaseTask** | Grundgerüst für alle Bots und Tasks                     | [Base Classes](base-classes.md)   |
| **Retry & Resilienz**  | `@with_retry` + vordefinierte Policies                  | [Retry](retry.md)                 |
| **Observability**      | Loguru + OpenTelemetry (Traces, Metrics, Logs)          | [Observability](observability.md) |
| **Playwright Wrapper** | Browser-Automatisierung (Chromium + Lightpanda via CDP) | [Playwright](playwright.md)       |
| **Secrets**            | Azure Key Vault + pydantic-settings                     | [Secrets](secrets.md)             |
| **NATS Client**        | Publish/Subscribe + Request/Reply (Phase 4)             | [NATS](nats.md)                   |

---

**Aktuelle Version**: Wird aus `packages/merle-core/` als installierbares Package gebaut.
