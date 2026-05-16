# Schnellstart

> **Neu im Team oder zum ersten Mal hier?**  
> Lies zuerst den **[Junior-Guide für Einsteiger](junior-guide.md)** – alles wird dort in ganz einfacher Sprache erklärt.

> **Hinweis:** Die empfohlene Entwicklungsumgebung ist **Devbox + direnv** (siehe [Entwicklungsumgebung einrichten](../development/setup.md)). Alle folgenden Befehle laufen idealerweise innerhalb der Devbox (`devbox run ...` oder `devbox shell`).

## 1. Voraussetzungen

- Devbox + direnv (empfohlen) **oder** Python 3.11+ + uv
- Git

## 2. Neuen Bot erstellen

### Variante A – Mit der merle CLI (empfohlen)

```bash
merle new-bot rechnungsverarbeitung --playwright --pandas
# Für hochvolumige / kostensensitive Web-Bots:
# merle new-bot high_volume_scraper --playwright --lightpanda   # oder --browser-engine lightpanda
cd python_bots/rechnungsverarbeitung
```

### Variante B – Mit Copier

```bash
copier copy templates/bot python_bots/rechnungsverarbeitung
cd python_bots/rechnungsverarbeitung
```

## 3. Abhängigkeiten installieren

```bash
uv sync --group dev
```

## 4. Bot starten

```bash
uv run python main.py
```

## 5. Tests ausführen

```bash
uv run pytest -v
```

## Nächste Schritte

- `config.py` anpassen
- Eigene Tasks unter `tasks/` anlegen (von `BaseTask` erben)
- `configure_observability()` in `main.py` aktivieren
- `.env` mit echten Werten befüllen (niemals committen!)

---

## Wichtige Visuals zum Verständnis

Bevor du startest, solltest du dir diese drei Diagramme anschauen — sie ersetzen viele Seiten Text:

- [Python vs. UiPath Entscheidungsfluss](../concepts/entscheidungsmatrix.md)
- [Die 10 Governance-Regeln (Poster)](../concepts/governance.md)
- [Merle Bot Lifecycle](../concepts/entwicklungsleitfaden.md)

---

## KI-gestützte Entwicklung mit OpenCode (empfohlen)

Im Merle-Root einfach `opencode` starten:

```bash
opencode
```

Du erhältst sofort den **Merle RPA-Hybrid-Architekt** als Primary Agent mit:
- Vollständiger Kenntnis der Entscheidungsmatrix und aller 10 Governance-Regeln
- Skills: `rpa-process-analyzer`, `rpa-bot-generator`, `governance-validator`
- Commands: `/rpa-new-bot`, `/rpa-validate`
- Tool: `load_rpa_context` für On-Demand-Dokumentation

Der Agent achtet strikt auf Template-Konformität (`templates/bot/` + `merle new-bot`), merle-core-Nutzung und Linux-Container-Fähigkeit.