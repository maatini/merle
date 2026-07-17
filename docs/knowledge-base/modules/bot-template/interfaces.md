# Bot Template — Interface (copier.yml Schema)

Das `copier.yml` definiert die User-Questions, die bei `merle new-bot` (oder direktem `copier copy`) gestellt werden. Die Antworten werden zu Jinja2-Template-Variablen.

## Template-Variablen (vollständig)

| Variable                      | Typ    | Default         | Prompt                                                  |
| ----------------------------- | ------ | --------------- | ------------------------------------------------------- |
| `bot_name`                    | `str`  | —               | "Bot name (snake_case)"                                 |
| `bot_description`             | `str`  | `""`            | "Short description"                                     |
| `python_version`              | `str`  | `"3.11"`        | "Python version (3.11 or 3.12)"                         |
| `include_playwright`          | `bool` | `false`         | "Include Playwright for browser automation?"            |
| `browser_engine`              | `str`  | `"chromium"`    | "Browser engine (chromium or lightpanda)" (conditional) |
| `include_pandas`              | `bool` | `false`         | "Include pandas + openpyxl for Excel/data processing?"  |
| `include_pdf`                 | `bool` | `false`         | "Include pdfplumber for PDF parsing?"                   |
| `include_uipath_orchestrator` | `bool` | `false`         | "Include UiPath Orchestrator REST client?"              |
| `use_base_bot_class`          | `bool` | `true`          | "Inherit from BaseBot (merle-core)?"                    |
| `location`                    | `str`  | `"python_bots"` | "Target location (python_bots or standalone)"           |

## Conditional-Field: `browser_engine`

Die Frage nach `browser_engine` erscheint **nur**, wenn `include_playwright = true`:

```yaml
browser_engine:
  type: str
  default: "chromium"
  choices:
    - "chromium"
    - "lightpanda"
  when: "{{ include_playwright }}"
```

## Generierte Dateien (Output)

```
<target_dir>/               # python_bots/<bot_name>/  oder  <bot_name>/
├── .copier-answers.yml     # Auto-generiert von Copier (nicht im Template)
├── .dockerignore           # Generiert von .dockerignore.jinja oder kopiert .dockerignore
├── .env.example            # Kopiert (statisch)
├── Dockerfile              # Generiert von Dockerfile.jinja
├── README.md               # Generiert von README.md.jinja
├── pyproject.toml          # Generiert von pyproject.toml.jinja
├── config.py               # Generiert von config.py.jinja
├── main.py                 # Generiert von main.py.jinja
├── tasks/
│   ├── __init__.py         # Kopiert (statisch)
│   └── example_task.py     # Generiert von example_task.py.jinja
└── tests/
    ├── __init__.py         # Kopiert (statisch)
    ├── conftest.py         # Generiert von conftest.py.jinja
    ├── test_main.py        # Generiert von test_main.py.jinja
    └── test_tasks.py       # Generiert von test_tasks.py.jinja
```

## @tag:copier-template — Update-Mechanismus

Copier unterstützt `copier update` zum Aktualisieren bestehender Bots auf eine neue Template-Version:

```bash
cd python_bots/my_bot
copier update
```

Dies funktioniert nur, weil `.copier-answers.yml` die ursprünglichen Antworten speichert.
