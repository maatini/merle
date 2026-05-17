# ADR-0007: Lightpanda als optionale Browser-Engine in Merle

**Status:** Akzeptiert  
**Datum:** 2026-05-17  
**Betroffene Komponente:** `merle-core.playwright`, Copier-Template, CLI (`merle new-bot`), Docker-Images

---

## 1. Kontext

Merle ist ein **Python-First, Cloud-Native, Container-First** RPA-Framework. Web-Automatisierung erfolgt ausschließlich über den robusten Playwright-Wrapper in `merle_core.playwright` (`launch_robust_browser`, `RobustBrowser`, Stealth, automatische Failure-Artifacts).

Bisher wurde ausschließlich **Chromium** (via `playwright`) unterstützt. Für hochvolumige, parallele, kostensensitive Automatisierungen (typisch für Cloud / Kubernetes / Serverless) entsteht jedoch ein Problem:

- Chromium ist ressourcenintensiv (hoher Memory-Footprint, langsame Starts).
- Viele moderne RPA-/Agenten-Workloads benötigen **kein** visuelles Rendering, keine pixel-perfekten Screenshots und keine PDF-Generierung aus dem Browser.

Im Mai 2026 hat sich **Lightpanda** (vollständig in Zig neu implementierte, headless-first Browser-Engine mit CDP-Server) als ernstzunehmende, produktiv einsetzbare Alternative etabliert:

- 9–11× schnellere Ausführung
- 10–16× geringerer Memory-Verbrauch
- Volle CDP-Kompatibilität → nutzbar über `playwright-core` + `connect_over_cdp`

## 2. Entscheidung

Wir integrieren **Lightpanda** als **erste klassengleiche alternative Browser-Engine** neben Chromium.

### Kern-Entscheidungen im Detail

| Aspekt                   | Entscheidung                                                                           |
| ------------------------ | -------------------------------------------------------------------------------------- |
| **API**                  | Einheitlicher Einstiegspunkt: `launch_robust_browser(engine="lightpanda"\|"chromium")` |
| **Abhängigkeiten**       | Neues Extra `merle-core[lightpanda]` (`lightpanda-py` + `playwright-core`)             |
| **Default**              | `chromium` (maximale Kompatibilität + visuelle Features)                               |
| **Template-Integration** | Neues Copier-Feld `browser_engine` (wird nur bei `include_playwright` angeboten)       |
| **Docker**               | Engine-spezifische Runtime-Layer (Chromium = schwer, Lightpanda = minimal)             |
| **CLI**                  | `merle new-bot ... --lightpanda` oder `--browser-engine lightpanda`                    |
| **Dokumentation**        | Explizite Entscheidungsmatrix-Erweiterung + neuer Abschnitt im Entwicklungsleitfaden   |

## 3. Begründung

### Warum Lightpanda?

- Passt exakt zur Merle-Strategie (kosteneffizient, skalierbar, cloud-native, resilient).
- CDP-Kompatibilität ermöglicht **nahezu identische** Nutzung der bestehenden `RobustBrowser`- und Helper-APIs.
- Deutliche Vorteile bei parallelen Workloads (typisch für NATS-orchestrierte oder Prefect-basierte Bot-Farmen).
- Reduziert Container-Größe und Infrastrukturkosten signifikant.

### Warum nicht nur Lightpanda?

- Lightpanda ist (Stand Mai 2026) noch Beta/early Production.
- Keine vollständige visuelle Rendering-Pipeline → `page.screenshot()`, `page.pdf()` und bestimmte visuelle Verifikationen funktionieren nicht oder nur eingeschränkt.
- Einige komplexe SPAs oder sehr dynamische Sites können noch Instabilitäten zeigen.

→ Deshalb **optionale, rückwärtskompatible Ergänzung**, kein Ersatz.

## 4. Konsequenzen

### Positive

- Bots mit hohem Durchsatz können bei gleicher Hardware 5–10× mehr Instanzen fahren.
- Deutlich kleinere und schnellere Docker-Images für Lightpanda-Bots.
- Zukunftssicher: Der Wrapper ist jetzt engine-agnostisch und kann später weitere CDP-fähige Engines aufnehmen.

### Negative / Trade-offs

- Etwas höhere Komplexität im `browser.py`-Wrapper (zwei Code-Pfade).
- Für Bots, die Screenshots für Audit/HITL brauchen, bleibt Chromium Pflicht (explizit dokumentiert).
- Leicht erhöhte Einarbeitung für Entwickler (müssen Engine bewusst wählen).

### Risiken & Gegenmaßnahmen

- **Lightpanda-Stabilität**: Canary-Deployments + automatische Fallback-Logik (Phase 4) vorgesehen.
- **Screenshot-Failure**: `RobustBrowser._capture_failure_artifacts` behandelt Fehler bei Lightpanda graceful (Warning + HTML-Dump nur).
- **Wartung**: Lightpanda-Extra wird separat versioniert. Bei Problemen kann der Bot per Config sofort auf Chromium umgestellt werden.

## 5. Umsetzung

- `merle-core` v0.3.x: `launch_robust_browser(engine=...)` + `BrowserEngine` Type + Readiness-Poller
- Copier Template + `merle` CLI: `browser_engine` als First-Class-Option
- Neue ADR- und Dokumentations-Updates (diese Datei + `entscheidungsmatrix.md` + `entwicklungsleitfaden.md`)
- Beispiel-Bot `examples/lightpanda-scraping` (geplant)

## 6. Alternativen, die verworfen wurden

| Alternative                                                | Warum verworfen?                                                                                         |
| ---------------------------------------------------------- | -------------------------------------------------------------------------------------------------------- |
| Nur Chromium behalten                                      | Ignoriert massive Kostensenkungs-Potenziale und die strategische Ausrichtung "cloud-native & skalierbar" |
| Lightpanda als separater Wrapper (`merle_core.lightpanda`) | Verletzt das Ziel eines einheitlichen RPA-Browser-Erlebnisses; dupliziert viel Code                      |
| Automatischer Fallback im Code                             | Zu magic; Entwickler sollen die Engine bewusst wählen (Governance)                                       |
| Puppeteer statt Playwright                                 | Merle ist Playwright-basiert; Wechsel würde zu viele Breaking Changes erzeugen                           |

## 7. Referenzen

- Lightpanda: https://lightpanda.io/ + https://github.com/lightpanda-io/browser
- `lightpanda-py`: https://github.com/tclesius/lightpanda-py
- Bestehende `merle_core.playwright` Implementierung (browser.py)
- ADR-0001 (Python-First) und ADR-0005 (merle-core Architektur)

---

**Entscheidungsträger:** Merle Core Maintainers + RPA-Hybrid-Architektur-Board  
**Nächste Review:** Q3 2026 (nach 3–6 Monaten produktivem Einsatz von Lightpanda-Bots)
