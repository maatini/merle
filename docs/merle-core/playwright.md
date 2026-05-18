# Playwright Wrapper in merle-core

`merle_core.playwright` bietet einen **robust, stealth-fähigen und engine-agnostischen** Browser-Wrapper für alle Web-Automatisierungen in Merle-Bots.

Seit Version 0.3 unterstützt der Wrapper **zwei Browser-Engines** über eine einheitliche API:

- **`chromium`** (Default) – volle Playwright-Kompatibilität
- **`lightpanda`** – Zig-basierte, hochperformante CDP-Alternative (siehe ADR-0007)

## Installation

```bash
# Für Chromium (maximale Kompatibilität)
uv add "merle-core[playwright]"

# Für Lightpanda (empfohlen bei hohem Volumen / Kosten-Sensitivität)
uv add "merle-core[lightpanda]"
```

## Verwendung

```python
from merle_core.playwright import launch_robust_browser

async with launch_robust_browser(
    engine="lightpanda",           # oder "chromium"
    headless=True,
    stealth=True,
    screenshot_on_failure=True,
    lightpanda_host="127.0.0.1",
    lightpanda_port=9222,
) as browser:
    page = await browser.new_page()
    await page.goto("https://example.com")
    title = await page.title()
```

### Wichtige Parameter

| Parameter               | Bedeutung                                  | Chromium | Lightpanda    |
| ----------------------- | ------------------------------------------ | -------- | ------------- |
| `engine`                | `"chromium"` (Default) oder `"lightpanda"` | —        | —             |
| `stealth`               | Anti-Detection JavaScript-Injection        | ✅       | ✅            |
| `screenshot_on_failure` | Automatische Failure-Artifacts             | ✅       | ⚠️ (nur HTML) |
| `proxy`                 | HTTP-Proxy                                 | ✅       | ✅            |
| `lightpanda_*`          | Host/Port/Log-Level für CDP-Server         | —        | ✅            |

## RobustBrowser Features

- Automatisches `new_page()` mit RPA-freundlichen Timeouts
- `screenshot_on_failure=True` → Screenshot + vollständiges HTML bei Exceptions
- Sauberes Cleanup auch bei Fehlern
- Stealth-Techniken (webdriver-Flag, permissions, cdc-Variablen)

## Lightpanda – Besonderheiten (2026)

- Sehr geringer Memory-Footprint (typisch 80–150 MB statt 1–2 GB)
- Extrem schneller Start → ideal für kurzlebige Container
- Keine vollwertige visuelle Rendering-Pipeline → `page.screenshot()` und `page.pdf()` funktionieren derzeit nicht oder nur eingeschränkt
- Empfehlung: Lightpanda für reine Datengewinnung / Agenten-Workflows, Chromium bei Audit-Pflicht oder visueller Verifikation

## Nächste Schritte / Best Practices

1. In `config.py` immer `browser_engine` + `lightpanda_*` Felder definieren (wird vom Template automatisch gemacht).
2. Bei der Bot-Erstellung bewusst entscheiden:
   ```bash
   merle new-bot mein_bot --playwright --lightpanda
   ```
3. Bei Unsicherheit immer `chromium` als Default belassen (Governance).

## Weiterführende Dokumente

- [ADR-0007: Lightpanda als optionale Browser-Engine](../decisions/0007-lightpanda-als-optionale-browser-engine.md)
- [Entscheidungsmatrix](../concepts/entscheidungsmatrix.md#browser-engine-innerhalb-von-python-chromium-vs-lightpanda)
- [Entwicklungsleitfaden](../concepts/entwicklungsleitfaden.md)
- [merle-core Index](index.md)

---

**Hinweis für Contributor**: Der Wrapper lebt in  
`packages/merle-core/src/merle_core/playwright/browser.py`  
Alle Änderungen an der Engine-Logik müssen im zugehörigen ADR und in den Template-Dateien nachgezogen werden.
