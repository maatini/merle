# Bot Template — Gotchas & Pitfalls

## `.jinja`-Dateien gewinnen gegen statische Dateien

**Problem:** Copier's Regel: Wenn sowohl `README.md` als auch `README.md.jinja` existieren, wird **nur** `README.md.jinja` verwendet (gerendert nach `README.md`). Die statische `README.md` wird ignoriert.

Das ist der Grund, warum die statische `README.md` (Template-Dokumentation) im `templates/bot/` liegt aber NICHT in den generierten Bot kopiert wird — das `.jinja`-File überschreibt sie.

**Konsequenz:** Wenn du eine neue statische Datei ins Template legst, die auch als `.jinja`-Version existiert, wird die statische ignoriert. Entweder `.jinja` weglassen oder in der `.jinja`-Version die statischen Inhalte via `{% raw %}...{% endraw %}` einbetten.

## `.dockerignore` vs `.dockerignore.jinja`

**Problem:** Es existieren BEIDE Dateien im Template:

- `.dockerignore` — statisch, einfacher Fallback
- `.dockerignore.jinja` — gerendert (gewinnt bei Copier)

Copier rendert `.dockerignore.jinja` → `.dockerignore` im generierten Bot. Diese Datei gilt nur, wenn der Build-**Kontext** das Bot-Verzeichnis ist.

**Monorepo-Builds** nutzen die **Root-`.dockerignore`** (Kontext = Repo-Root). Das Bot-`.dockerignore` ist dann irrelevant.

## Docker: Monorepo-Build nur vom Repo-Root

**Problem:** Das generierte `Dockerfile` erwartet Build-Kontext = Merle-Repo-Root und kopiert explizit `packages/merle-core` sowie `${BOT_PATH}` (Default: `python_bots/<bot_name>`).

```bash
# ✅ Korrekt (Repo-Root):
docker build -f python_bots/my_bot/Dockerfile \
  --build-arg BUILD_MODE=monorepo \
  --build-arg BOT_PATH=python_bots/my_bot \
  -t my_bot:latest .

# ✅ Convenience:
just docker-bot my_bot

# ❌ Falsch (Kontext = Bot-Verzeichnis):
cd python_bots/my_bot && docker build .
# COPY packages/merle-core → fehlt im Kontext
```

**Layout im Builder:** Die Pfad-Dependency `../../packages/merle-core` aus dem Bot-`pyproject.toml` wird gespiegelt unter `/src/python_bots/<bot>` + `/src/packages/merle-core`. Runtime enthält nur `.venv` + App-Quellen unter `/app`.

**Root-`.dockerignore`:** Darf `python_bots/*/` **nicht** pauschal ausschließen (sonst schlägt `COPY ${BOT_PATH}` fehl). Nur Caches/Tests/Logs unter `python_bots/` ignorieren. `*.md` braucht Exceptions für `python_bots/*/README.md` und `packages/merle-core/README.md`.

**Standalone `BUILD_MODE`:** Mit Monorepo-Kontext wird `merle-core` als Wheel gebaut und via `uv sync --no-sources --find-links` installiert (kein privates PyPI nötig). Reines Standalone ohne `packages/` im Kontext ist noch nicht produktiv.

## `uv sync` im Post-Hook kann fehlschlagen

**Problem:** Der Post-Generation-Hook führt `uv sync --group dev` aus. Wenn:

- `uv` nicht installiert ist
- Das Netzwerk nicht erreichbar ist
- `merle-core` nicht als Pfad aufgelöst werden kann (Monorepo, falsches CWD)

...dann schlägt der Hook fehl und der Bot hat keine installierten Dependencies.

Der Fehler wird in der Copier-Ausgabe sichtbar, aber der Bot ist trotzdem generiert (nur nicht lauffähig). Manuelles `cd python_bots/<name> && uv sync --group dev` behebt das.

## `copier update` — Nicht alle Änderungen sind gemerged

**Problem:** `copier update` kann strukturelle Template-Änderungen mergen, aber **Änderungen im generierten Code überschreiben** (wenn der Nutzer sie nicht via `.copier-answers.yml` geschützt hat).

Beispiel: Wenn das Template `main.py.jinja` ändert und der Nutzer `main.py` manuell angepasst hat, wird Copier einen Merge-Konflikt erzeugen. Es gibt kein automatisches 3-Way-Merge für generierte Dateien.

## Browser-Engine-Wechsel erfordert Docker-Neubau

**Problem:** Der Wechsel von `chromium` zu `lightpanda` (oder umgekehrt) ändert:

- `pyproject.toml` (anderes merle-core-Extra)
- `config.py` (andere Browser-Konfiguration)
- `Dockerfile` (andere System-Dependencies)

Ein bestehender Bot muss nach dem Engine-Wechsel **komplett neu generiert** werden — ein einfaches `copier update` reicht nicht, da die Docker-System-Dependencies tief in der Image-Struktur liegen.

## `location: standalone` / reines External-Standalone noch limitiert

**Problem:** Der Copier-`location=standalone` schreibt `merle-core >= 0.1.0` ohne Path-Source. Ohne internes PyPI schlägt `uv sync` lokal fehl.

**Was CI smoke-testet:** `BUILD_MODE=standalone` **mit Monorepo-Kontext** (Wheel aus `packages/merle-core`). Das validiert die Packaging-Pipeline, nicht „Bot-Ordner allein auf einem fremden Host“.

**Noch nicht produktiv:** Reines External-Standalone (`BOT_PATH=.`, Kontext = nur Bot-Dir, ohne `packages/merle-core`). Dafür später: veröffentlichtes `merle-core` oder vendored wheel.
