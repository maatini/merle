# Devbox-Entwicklungsumgebung für Merle

**Devbox + direnv ist die offizielle und standardmäßige Entwicklungsumgebung** für das Merle-Projekt.

Sie stellt sicher, dass alle Entwickler (und alle AI-Agenten) exakt dieselben Tool-Versionen verwenden wie in der CI-Pipeline:

- **Python 3.11**
- **uv 0.11.8**
- **pre-commit**
- **Node.js 20** (für Prettier)
- **Copier** (für Bot-Generierung)

---

## Warum Devbox?

| Problem ohne Devbox                  | Lösung mit Devbox                          |
|--------------------------------------|--------------------------------------------|
| "Funktioniert bei mir"               | Exakt gleiche Versionen wie im Team + CI   |
| Konflikte mit globalem Python/uv     | Vollständig isolierte Umgebung             |
| Fehlende Tools (copier, pre-commit)  | Alles ist sofort verfügbar                 |
| Unterschiedliche Node-Versionen      | Node 20 ist fest gepinnt                   |
| Aufwändiges Onboarding               | `direnv allow .` → alles läuft             |

Devbox basiert auf Nix und ist deutlich leichter als ein voller Docker-Dev-Container, aber trotzdem reproduzierbar und Linux-Container-kompatibel — perfekt passend zur Merle-Philosophie.

---

## Einrichtung (einmalig)

### 1. Devbox + direnv installieren

```bash
# macOS
brew install devbox direnv

# Linux (Beispiel Debian/Ubuntu)
curl -fsSL https://get.jetify.com/devbox | bash
# direnv über Paketmanager installieren

# WSL / andere Systeme
# Siehe https://www.jetify.com/devbox/docs/install/
```

### 2. direnv in deine Shell integrieren

Füge am Ende deiner `~/.zshrc` (oder `~/.bashrc`) hinzu:

```bash
eval "$(direnv hook zsh)"   # bei zsh
# oder
eval "$(direnv hook bash)"
```

Danach Shell neu starten.

### 3. Projekt klonen und Devbox aktivieren

```bash
git clone https://github.com/maatini/merle.git
cd merle

# Einmalig erlauben – danach wird Devbox automatisch beim Betreten des Verzeichnisses geladen
direnv allow .
```

Du solltest jetzt eine Willkommensnachricht sehen:

```
✅ Merle Devbox + direnv aktiviert (Python 3.11 + uv + pre-commit + Node 20)
```

---

## Tägliche Arbeit

### Automatische Umgebung (empfohlen)

Einfach ins Verzeichnis wechseln:

```bash
cd /path/to/merle
# Devbox ist sofort aktiv
which python   # → zeigt die Devbox-Python 3.11
which uv       # → zeigt die Devbox-uv 0.11.8
```

### Manuell (ohne direnv)

```bash
devbox shell          # Betritt die isolierte Umgebung
exit                  # Verlässt sie wieder
```

Oder einzelne Befehle ausführen, ohne die Shell zu betreten:

```bash
devbox run python --version
devbox run uv sync --group dev --all-packages
```

---

## Verfügbare Komfort-Skripte

In `devbox.json` sind folgende Skripte vordefiniert:

| Befehl                    | Was passiert                                      |
|---------------------------|---------------------------------------------------|
| `devbox run setup`        | `uv sync --group dev --all-packages` + Pre-Commit-Hooks installieren |
| `devbox run lint`         | `ruff check + ruff format --check`                |
| `devbox run test`         | `pytest -q`                                       |
| `devbox run new-bot`      | Kurzbefehl für `uv run merle new-bot ...`         |

Beispiel:

```bash
devbox run setup
devbox run new-bot rechnungsverarbeitung --playwright --pandas
devbox run lint
devbox run test
```

---

## Integration mit OpenCode & AI-Agenten (RPA-Hybrid-Architekt)

Der **Merle RPA-Hybrid-Architekt** kennt die Devbox-Umgebung als **Regel 0** und hat einen dedizierten Skill:

- Skill: `devbox-environment`
- Datei: `.opencode/skills/devbox-environment/SKILL.md`

**Verhalten des Agenten:**
- Bevor er Shell-Befehle, `uv`, `ruff`, `pytest` oder `merle` ausführt, stellt er sicher, dass die Devbox aktiv ist.
- Er verwendet bevorzugt `devbox run <befehl>`, wenn er nicht in einer interaktiven `devbox shell` arbeitet.
- Du kannst jederzeit `load_skill devbox-environment` aufrufen, wenn du detaillierte Anweisungen brauchst.

**Tipp für OpenCode-Nutzer:**
Starte einfach `opencode` im Merle-Root. Der Agent arbeitet automatisch in der korrekten Devbox-Umgebung.

---

## Wichtige Dateien

| Datei                    | Bedeutung                                      |
|--------------------------|------------------------------------------------|
| `devbox.json`            | Definition der Pakete, Environment-Variablen, Skripte und Init-Hooks |
| `devbox.lock`            | Gesperrte exakte Paket-Versionen (muss committet werden) |
| `.envrc`                 | direnv-Konfiguration (`use devbox`)            |
| `.opencode/skills/devbox-environment/SKILL.md` | Anleitung für AI-Agenten |
| `docs/development/devbox.md` | Diese Datei                                    |

---

## Troubleshooting

### "Virtual environment doesn't use Devbox Python"

Das passiert, wenn du bereits eine `.venv` mit einer anderen Python-Version (z. B. system Python 3.14) angelegt hast.

**Lösung:**

```bash
rm -rf .venv
devbox run setup
```

### direnv zeigt keine Willkommensnachricht

```bash
direnv reload
```

### Ich will Devbox temporär verlassen

```bash
direnv deny .
# oder einfach das Verzeichnis verlassen
```

### Ich arbeite auf einem Server ohne direnv

Dann einfach immer mit `devbox shell` oder `devbox run ...` arbeiten.

---

## Verwandte Dokumente

- [Entwicklungsumgebung einrichten](setup.md)
- [Contributing Guidelines](contributing.md)
- [AGENTS.md](../../AGENTS.md) (Regel 0 + Skill-Referenz)
- [Schnellstart](../getting-started/quickstart.md)

---

**Merle Devbox ist nicht optional — sie ist der Standard.**

Alle Pull Requests und lokalen Entwicklungsarbeiten sollten in einer aktiven Devbox-Umgebung erfolgen.