# Merle Bot Template (Copier)

Dies ist das **offizielle, verbindliche Template** für alle neuen Python-Bots im Merle-Framework (ab Phase 1).

## Verwendung

### Mit der merle CLI (empfohlen)
```bash
merle new-bot invoice_processor --playwright --description "Rechnungen aus E-Mail verarbeiten"
```

### Direkt mit Copier
```bash
copier copy templates/bot python_bots/invoice_processor
```

Copier stellt interaktive Fragen (Features, Beschreibung, etc.).

## Feature-Flags

| Flag                        | Was wird generiert                          | Wann sinnvoll?                     |
|----------------------------|---------------------------------------------|------------------------------------|
| `include_playwright`       | playwright + Beispiel-Task                  | Web-Portale, moderne UIs           |
| `include_pandas`           | pandas + openpyxl                           | Excel, Reporting, Massendaten      |
| `include_pdf`              | pdfplumber                                  | PDF-Parsing                        |
| `include_uipath_orchestrator` | Einfacher Orchestrator-Client            | Nur bei nachgewiesenem Bedarf      |
| `use_base_bot_class`       | `class MeinBot(BaseBot)` Beispiel           | Empfohlen für neue Bots            |

## Nach der Generierung

```bash
cd python_bots/<bot_name>
uv sync --group dev
uv run python main.py
```

Der Post-Hook führt automatisch `uv sync` + Linting aus (wenn aktiviert).

## Entwicklung des Templates

- Alle Dateien unter `{{ bot_name }}/` sind Jinja2-Templates.
- Bedingungen mit `{% if include_playwright %}` etc.
- `hooks/post_gen_project.py` für automatisierte Nachbearbeitung.

## Governance

Jeder über dieses Template erzeugte Bot erfüllt automatisch:
- ADR-0004 + ADR-0002
- Merle Governance (docs/03_Governance.md)
- uv + merle-core + strukturierte Qualität

---

**Single Source of Truth** für neue RPA-Bots seit Mai 2026.
