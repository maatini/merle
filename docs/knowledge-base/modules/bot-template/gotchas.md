# Bot Template — Gotchas & Pitfalls

## `.jinja`-Dateien gewinnen gegen statische Dateien

**Problem:** Copier's Regel: Wenn sowohl `README.md` als auch `README.md.jinja` existieren, wird **nur** `README.md.jinja` verwendet (gerendert nach `README.md`). Die statische `README.md` wird ignoriert.

Das ist der Grund, warum die statische `README.md` (Template-Dokumentation) im `templates/bot/` liegt aber NICHT in den generierten Bot kopiert wird — das `.jinja`-File überschreibt sie.

**Konsequenz:** Wenn du eine neue statische Datei ins Template legst, die auch als `.jinja`-Version existiert, wird die statische ignoriert. Entweder `.jinja` weglassen oder in der `.jinja`-Version die statischen Inhalte via `{% raw %}...{% endraw %}` einbetten.

## `.dockerignore` vs `.dockerignore.jinja`

**Problem:** Es existieren BEIDE Dateien:

- `.dockerignore` — statisch, einfacher Fallback
- `.dockerignore.jinja` — dynamisch, mit Monorepo-Logik

Copier wird `.dockerignore.jinja` rendern und nach `.dockerignore` ausgeben — die statische `.dockerignore` wird überschrieben.

Die statische Version existiert als Fallback für den unwahrscheinlichen Fall, dass jemand Copier ohne Jinja2-Rendering nutzt. In der Praxis irrelevant, aber nicht löschen (könnte Verwirrung stiften, wenn sie fehlt).

## Docker: Monorepo-Build nur vom Repo-Root

**Problem:** Das generierte `Dockerfile` enthält `COPY packages/merle-core ./packages/merle-core`. Dieser Befehl funktioniert nur, wenn der Docker-Build-Kontext das Merle-Repo-Root ist:

```bash
# ✅ Korrekt:
cd /path/to/merle
docker build -f python_bots/my_bot/Dockerfile .

# ❌ Falsch:
cd /path/to/merle/python_bots/my_bot
docker build .
# COPY packages/merle-core → kein solches Verzeichnis im Kontext!
```

Das `.dockerignore.jinja` ist so konfiguriert, dass im Monorepo-Modus `packages/merle-core/` **nicht** ignoriert wird (via `!packages/merle-core/`). Alle anderen `python_bots/` werden ignoriert.

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

## `location: standalone` noch nicht vollständig getestet

**Problem:** Der Standalone-Modus (`--location standalone`) geht davon aus, dass `merle-core` als Package von einem (internen) PyPI installiert werden kann. Dies ist noch **nicht produktiv getestet**. Der Monorepo-Modus (`python_bots`) ist der einzig aktiv genutzte Pfad.
