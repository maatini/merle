# ⚠️ LEGACY – Deprecated (seit Professional Foundation v0.2 / Phase 1)

**Dieses Verzeichnis (`python_bots/template/`) ist veraltet und wird nicht mehr gepflegt.**

Es ist eine statische Snapshot-Kopie aus der frühen Phase des Projekts und führt zu **Drift** gegenüber dem offiziellen, feature-flag-fähigen Copier-Template.

---

## ✅ Verbindlicher Weg (2026+)

```bash
# Beste DX: just (empfohlen)
just new-bot mein_bot --playwright --pandas

# Oder direkt
uv run merle new-bot mein_bot --playwright --pandas
# oder
copier copy templates/bot python_bots/mein_bot
```

**Die Quelle der Wahrheit ist ausschließlich:**

- `templates/bot/` + `copier.yml` + Jinja-Templates + `hooks/post_gen_project.py`
- `tools/merle/` (die `merle` CLI, als uv-Workspace-Member installiert)

---

## Warum du dieses Verzeichnis **nicht** mehr verwenden darfst

- Keine Feature-Flags (Playwright, pandas, PDF, UiPath-Orchestrator, browser_engine etc.)
- Kein modernes `merle-core` (BaseBot, Observability, NATS-Client, Self-Healing)
- Kein Post-Generation-Hook (uv sync + ruff auto-fix)
- Führt langfristig zu inkonsistenten, nicht wartbaren Bots
- Wird in CI/ADR/Dokumentation nicht mehr berücksichtigt

---

## Migration bestehender Bots

Falls du Bots hast, die per `cp -r python_bots/template/` erstellt wurden:

1. Erzeuge einen frischen Bot mit `just new-bot <name> --<flags>`
2. Kopiere deine fachliche Logik (`tasks/`, Business-Code) in den neuen Bot
3. Passe `config.py` und `pyproject.toml` an (merle-core Dependency ist bereits korrekt)
4. Lösche den alten Bot-Ordner oder markiere ihn als `legacy/`

Die manuelle `cp -r`-Methode wird **nicht mehr supported**.

---

**Weiterführend:**

- `just --list` (zeigt `new-bot`)
- `uv run merle new-bot --help`
- [templates/bot/README.md](../templates/bot/README.md)
- ADR 0004 (Copier-Bot-Scaffolding) + 0005 (merle-core Architecture)
- `docs/getting-started/quickstart.md`

---

**Governance-Hinweis für Agenten:**  
Siehe AGENTS.md und agent/CLAUDE.md – Template-First bedeutet **immer** den Copier-Weg.
