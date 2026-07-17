# Junior-Guide für Merle – Dein Einstieg als Junior

**Willkommen im Team!**  
Dieser Guide erklärt dir **alles ganz einfach**, Schritt für Schritt. Du brauchst keine 5 Jahre Erfahrung. Du lernst hier, wie man bei Merle richtig gute RPA-Bots baut – verständlich, sicher und professionell.

> **Ziel dieses Guides:** Nach dem Lesen kannst du allein einen neuen Bot anlegen, verstehen, wie er aufgebaut ist, und kleine Änderungen machen.

---

## 1. Was ist Merle eigentlich? (ganz einfach erklärt)

Stell dir vor, ein **Bot** ist wie ein fleißiger, digitaler Mitarbeiter.

Er macht immer wieder dieselben langweiligen oder fehleranfälligen Aufgaben am Computer:

- Rechnungen aus E-Mails herunterladen
- Daten aus Web-Portalen kopieren
- Excel-Listen erstellen und versenden
- PDFs lesen und wichtige Zahlen herausziehen

**Merle** ist das "Rezeptbuch + Werkzeugkasten", mit dem wir diese digitalen Helfer **richtig gut** bauen.

### Warum Merle besonders ist

| Normalerweise...                  | Bei Merle machen wir es so...                        |
| --------------------------------- | ---------------------------------------------------- |
| Jeder baut irgendwie anders       | Alle Bots sehen gleich aus (dank Template)           |
| Wenn etwas kaputt geht → Chaos    | Der Bot versucht es automatisch nochmal (Retry)      |
| Niemand weiß, was im Bot passiert | Alles wird sauber protokolliert (Logging)            |
| Passwörter stehen im Code         | Passwörter kommen nie in den Code (Config + Secrets) |
| "Funktioniert bei mir"            | Funktioniert überall gleich (Devbox + Docker)        |

**Kurz gesagt:** Merle-Bots sind wie gute Software – nicht wie schnelle Skripte.

---

## 2. Die 5 wichtigsten Regeln (die du dir merken solltest)

Diese Regeln gelten für **jedes** Projekt. Sie sind nicht kompliziert:

1. **Python ist der Standard**  
   Fast alles machen wir mit Python (Playwright für Browser, pandas für Excel, etc.).  
   UiPath benutzen wir nur in ganz seltenen Ausnahmefällen (z. B. sehr alte SAP-Programme).  
   → Wenn du unsicher bist: Immer erst an Python denken.

2. **Immer mit dem offiziellen Template starten**  
   Nie von Null anfangen!  
   Du benutzt immer den Befehl `merle new-bot ...` oder `copier`.  
   Dadurch hat dein Bot von Anfang an Logging, Tests, Retry und alles Wichtige.

3. **Keine Geheimnisse im Code**  
   Passwörter, API-Keys, Datenbank-Links kommen **nie** direkt in den Python-Code.  
   Die kommen in eine `.env`-Datei (die nie ins Git kommt).

4. **Der Bot muss erklären, was er tut**  
   Jeder Bot schreibt in ein Logbuch (mit loguru).  
   Wenn etwas schiefgeht, sehen wir später genau, wo es passiert ist.

5. **Fehler? Der Bot versucht es nochmal**  
   Beim Zugriff auf Webseiten oder APIs kann mal etwas schiefgehen (kurzer Internet-Ausfall etc.).  
   Deshalb gibt es automatische Wiederholungen (mit tenacity).

Diese 5 Regeln machen später Reviews und Übergaben viel einfacher.

---

## 3. Deine Entwicklungsumgebung einrichten (Devbox)

**Die wichtigste Regel für den Anfang:**  
Wir arbeiten **nicht** mit dem normalen Python auf deinem Laptop. Wir benutzen **Devbox**.

Devbox sorgt dafür, dass bei dir, bei deinen Kollegen und in der Cloud **exakt dieselben Programme** laufen. Kein "Aber bei mir funktioniert es nicht".

### Schritt-für-Schritt Einrichtung (macOS)

1. **Devbox + direnv installieren**

   Öffne dein Terminal (Terminal.app oder iTerm) und gib ein:

   ```bash
   brew install devbox direnv
   ```

2. **direnv in deine Shell einbinden** (einmalig)

   ```bash
   # Für zsh (meistens der Fall)
   echo 'eval "$(direnv hook zsh)"' >> ~/.zshrc

   # Danach Shell neu starten oder:
   source ~/.zshrc
   ```

3. **Merle-Repository klonen**

   ```bash
   git clone <der-link-zum-merle-repository>
   cd merle
   ```

4. **Devbox aktivieren** (das Wichtigste!)

   ```bash
   direnv allow .
   ```

   Du solltest jetzt eine freundliche Nachricht sehen, z. B.:

   ```
   ✅ Merle Devbox + direnv aktiviert (Python 3.11 + uv + pre-commit + Node 20)
   ```

   Ab jetzt passiert beim Betreten des Ordners automatisch alles.

5. **Einrichtung abschließen**

   ```bash
   devbox run setup
   ```

   Das lädt alle benötigten Python-Pakete herunter und richtet Pre-Commit-Hooks ein.

**Tipp:** Ab jetzt musst du nie mehr `python` oder `uv` direkt tippen. Nutze immer `devbox run ...` oder arbeite in der Devbox-Shell.

---

## 4. Deinen allerersten Bot erstellen

Jetzt wird es spannend!

### So legst du einen neuen Bot an

Im Merle-Ordner (Devbox aktiv) gibst du ein:

```bash
devbox run new-bot mein_erster_bot --playwright --pandas --description "Mein allererster Test-Bot"
```

**Was bedeuten die Teile?**

- `mein_erster_bot` = Name deines Bots (klein geschrieben, mit Unterstrichen)
- `--playwright` = Wir wollen Browser-Automatisierung (Webseiten steuern)
- `--pandas` = Wir wollen später Excel-Dateien schreiben können
- `--description` = Kurze Beschreibung, was der Bot machen soll

Der Befehl erstellt automatisch einen kompletten, fertigen Ordner unter `python_bots/mein_erster_bot/`.

Danach:

```bash
cd python_bots/mein_erster_bot
uv run python main.py
```

Du solltest jetzt sehen, dass der Bot startet und etwas loggt.

**Herzlichen Glückwunsch!** Du hast gerade deinen ersten Merle-Bot erstellt.

---

## 5. Was ist eigentlich in einem Bot drin? (Dateien einfach erklärt)

Geh in den neuen Ordner und schau dir die Dateien an:

```
mein_erster_bot/
├── config.py          ← Hier stehen alle Einstellungen (z.B. URLs, Timeouts)
├── main.py            ← Der "Chef" – er sagt, in welcher Reihenfolge was passiert
├── pyproject.toml     ← Welche Python-Pakete wir brauchen
├── Dockerfile         ← Rezept, damit der Bot später im Container läuft
├── .env.example       ← Vorlage für deine geheimen Werte (niemals committen!)
├── tasks/
│   └── example_task.py ← Hier passiert die echte Arbeit (ein "Arbeitsschritt")
└── tests/
    └── test_main.py    ← Hier testen wir, ob der Bot richtig funktioniert
```

### Die wichtigsten Dateien – ganz einfach:

**main.py**  
Das ist der Dirigent. Er sagt:

> "Zuerst lade ich die Daten, dann verarbeite ich sie, dann schreibe ich einen Bericht."

Er benutzt dafür kleine Helfer-Klassen aus dem `tasks/`-Ordner.

**tasks/example_task.py**  
Hier steht die eigentliche Arbeit.  
Ein Bot besteht meist aus mehreren Tasks (z. B. "Daten herunterladen", "Daten prüfen", "Bericht schreiben").

Jeder Task kann einzeln getestet werden. Das ist super praktisch!

**config.py**  
Alle Einstellungen kommen hierher.  
Beispiel: Welche Webseite soll besucht werden? Wie oft soll bei Fehlern neu versucht werden?

**Wichtig:** Echte Passwörter kommen hier **nicht** rein. Die kommen in die `.env`-Datei.

---

## 6. Einen Task verstehen (das Herzstück)

Schau dir die Datei `tasks/example_task.py` an.

Du siehst dort ungefähr so etwas:

```python
class ExampleTask(BaseTask):
    @with_retry(policy=default_http_retry)
    async def _do_work(self):
        # Hier passiert die echte Arbeit
        self.logger.info("Ich hole jetzt Daten...")
        # ... dein Code ...
        return {"status": "erledigt"}
```

**Was bedeutet das?**

- `BaseTask` = Die Merle-Vorlage für Arbeitsschritte. Sie bringt automatisch Logging, Zeitmessung und Fehlerbehandlung mit.
- `@with_retry` = "Wenn etwas schiefgeht, versuche es bitte nochmal automatisch."
- `self.logger.info(...)` = Schreibe eine Nachricht ins Logbuch.

**Dein erster eigener Task:**

1. Kopiere `example_task.py` → `mein_erster_task.py`
2. Ändere den Namen der Klasse
3. Schreibe in `_do_work` deinen eigenen Code
4. Rufe den neuen Task in `main.py` auf

Fertig.

---

## 7. Wie du deinen Bot testest

Gute Bots haben Tests. Das klingt erstmal langweilig, spart aber später riesig Zeit.

Im Bot-Ordner einfach ausführen:

```bash
uv run pytest -v
```

Du siehst dann, welche Tests laufen und ob alles grün ist.

**Tipp für Juniors:**  
Schreibe zuerst einen Test für deinen neuen Task, bevor du den richtigen Code schreibst. Das nennt man "Test-Driven Development" und ist bei Merle gewünscht.

---

## 8. Was passiert, wenn etwas schiefgeht?

Das passiert ständig – und das ist okay!

Merle-Bots sind darauf vorbereitet:

- **Retry (Wiederholung):** Beim Zugriff auf eine Webseite oder API kann es zu einem kurzen Ausfall kommen. Der Bot wartet ein paar Sekunden und versucht es nochmal (bis zu 3–5 Mal).
- **Logging:** Jeder Versuch und jeder Fehler wird ins Log geschrieben. Du siehst später genau: "Um 14:32 hat der Login auf Seite X nicht funktioniert."
- **Self-Healing (in Zukunft):** Manche Tasks können sich sogar selbst "reparieren".

Deshalb siehst du überall im Code `@with_retry` und `logger.info()` / `logger.error()`.

---

## 9. Dein erstes Mini-Projekt – Jetzt baust du selbst!

Du hast jetzt viel gelesen. Zeit, dass **du selbst etwas baust**.

Dieses Mini-Projekt ist bewusst klein, aber richtig – genau so, wie echte Merle-Bots aussehen. Wenn du es schaffst, kannst du stolz sein: Du hast dann schon das Grundmuster eines professionellen RPA-Bots verstanden.

### Das Ziel

Wir bauen einen kleinen Bot, der **Zitate von einer Übungs-Webseite** sammelt:

- Seite: [https://quotes.toscrape.com/](https://quotes.toscrape.com/) (extra zum Üben gemacht, keine Tricks)
- Wir holen die ersten 5 Zitate + den Autor
- Wir speichern alles schön in einer Datei `data/quotes.json`
- Der Bot schreibt ordentlich ins Log, was er tut

**Warum gerade diese Aufgabe?**  
Du übst genau die Dinge, die in 80 % aller realen Web-Bots vorkommen:

- Browser starten
- Auf eine Seite gehen
- Mehrere Elemente finden
- Daten extrahieren
- Etwas damit machen (hier: speichern)

### Voraussetzungen

Du brauchst einen Bot, der mit `--playwright` erzeugt wurde (siehe Kapitel 4).

```bash
cd python_bots/mein_erster_bot
```

Falls du noch keinen `data/`-Ordner hast, lege ihn jetzt an:

```bash
mkdir -p data
```

### Schritt 1: Neuen Task anlegen

Erstelle eine neue Datei:

**`tasks/quotes_scraper.py`**

Kopiere den folgenden kompletten Code hinein:

```python
"""
QuotesScraperTask – Dein erster eigener Web-Task

Dieser Task zeigt dir das typische Muster eines Merle Playwright-Bots:
1. Browser starten (mit launch_robust_browser)
2. Auf Seite gehen
3. Daten extrahieren
4. Ergebnis zurückgeben
"""

from __future__ import annotations

from typing import Any

from config import BotSettings
from merle_core import BaseTask
from merle_core.playwright import launch_robust_browser
from merle_core.retry import with_retry, default_http_retry


class QuotesScraperTask(BaseTask):
    """Holt Zitate von quotes.toscrape.com und gibt sie als Liste zurück."""

    def __init__(self, settings: BotSettings) -> None:
        super().__init__(settings, name="QuotesScraperTask")

    @with_retry(policy=default_http_retry)
    async def _do_work(self) -> dict[str, Any]:
        """Die eigentliche Arbeit passiert hier."""
        self.logger.info("Starte Browser und hole Zitate...")

        quotes: list[dict[str, str]] = []

        # launch_robust_browser = Merles smarter Browser-Starter
        # headless=True → du siehst kein Fenster (gut für Server)
        # stealth=True  → die Seite merkt weniger, dass ein Bot kommt
        async with launch_robust_browser(
            headless=True,
            stealth=True,
            screenshot_on_failure=True,   # bei Fehler wird automatisch ein Screenshot gemacht
        ) as browser:
            page = await browser.new_page()

            # Zur Übungsseite gehen
            await page.goto("https://quotes.toscrape.com/")
            self.logger.info("Seite erfolgreich geladen")

            # Alle Zitat-Blöcke finden (.quote ist die CSS-Klasse auf der Seite)
            all_quotes = page.locator(".quote")
            count = await all_quotes.count()
            self.logger.info("{} Zitate auf der Seite gefunden", count)

            # Die ersten 5 verarbeiten
            limit = min(5, count)
            for i in range(limit):
                quote_element = all_quotes.nth(i)

                # Text und Autor extrahieren
                text = await quote_element.locator(".text").inner_text()
                author = await quote_element.locator(".author").inner_text()

                quotes.append({
                    "text": text.replace("“", "").replace("”", ""),  # Anführungszeichen weg
                    "author": author
                })

                self.logger.info("Zitat {} von {}: {} - {}", i + 1, limit, text[:60], author)

        self.logger.success("{} Zitate erfolgreich extrahiert", len(quotes))
        return {"quotes": quotes, "count": len(quotes)}

    async def execute(self) -> dict[str, Any]:
        """Wird von BaseTask.run() aufgerufen."""
        self.logger.info("QuotesScraperTask startet...")

        result = await self._do_work()

        # Ergebnis später noch als Datei speichern (siehe Schritt 3)
        return result

    def _on_success(self, result: dict[str, Any]) -> None:
        self.logger.success("Task erfolgreich abgeschlossen")
```

**Wichtige Zeilen kurz erklärt:**

- `launch_robust_browser(...)` → Startet Chromium (oder Lightpanda) mit guten Standard-Einstellungen
- `page.locator(".quote")` → Sucht alle Elemente mit der CSS-Klasse "quote"
- `.nth(i)` → Nimm das i-te Element
- `inner_text()` → Holt den sichtbaren Text
- `self.logger.info(...)` → Schreibt eine schöne Nachricht ins Log

### Schritt 2: main.py anpassen

Öffne `main.py` und ändere den Import und den Aufruf:

**Oben bei den Imports** ersetze die Beispiel-Task durch deine neue:

```python
from tasks.quotes_scraper import QuotesScraperTask
```

**Im `execute()`-Block** (bei `use_base_bot_class`):

```python
task = QuotesScraperTask(self.settings)
task_result = await task.run()
results["quotes"] = task_result
```

Falls du die einfache Variante ohne BaseBot hast, rufe den Task direkt in der `main()`-Funktion auf.

### Schritt 3: Ergebnis in eine Datei schreiben (optional, aber schön)

Erweitere die `execute()`-Methode in deinem Task (oder in main.py), damit die Daten gespeichert werden:

```python
import json
from pathlib import Path

# am Ende von execute() oder _do_work():
output_path = Path("data/quotes.json")
output_path.parent.mkdir(parents=True, exist_ok=True)

with open(output_path, "w", encoding="utf-8") as f:
    json.dump(result["quotes"], f, ensure_ascii=False, indent=2)

self.logger.success("Zitate gespeichert unter {}", output_path)
```

### Schritt 4: Bot starten und beobachten

```bash
uv run python main.py
```

**Was du jetzt sehen solltest:**

- Viele `INFO` Zeilen im Terminal („Starte Browser...“, „Seite erfolgreich geladen“, „Zitat 1 von 5: ...“)
- Am Ende ein `SUCCESS` mit „5 Zitate erfolgreich extrahiert“
- Eine neue Datei `data/quotes.json` mit schön formatierten Zitaten

**Öffne die Datei** und schau dir an, was drin steht. Das ist dein erstes echtes Bot-Ergebnis!

### Checkpoint – Hast du es geschafft?

- [ ] Der Bot startet ohne Fehler
- [ ] Du siehst im Log „5 Zitate erfolgreich extrahiert“
- [ ] Die Datei `data/quotes.json` existiert und enthält 5 Einträge
- [ ] Du hast verstanden, was `page.locator()` und `inner_text()` machen

**Herzlichen Glückwunsch!**  
Du hast gerade **deinen ersten echten Merle-Web-Bot** gebaut. Das ist genau das Muster, das in fast allen professionellen Web-Automatisierungen verwendet wird.

### Was du als Nächstes ausprobieren kannst (Steigerung)

- Statt 5 alle Zitate der Seite holen (es sind 10 pro Seite)
- Nur Zitate von einem bestimmten Autor filtern
- Die Daten zusätzlich als schöne Excel-Datei mit pandas ausgeben
- Den Bot so erweitern, dass er zur zweiten Seite geht (`?page=2`)

---

## 9b. Best Practices für E-Mail, PDF und Excel (Wie es die Profis machen)

Wenn du im Team an echten Enterprise-Bots arbeitest, wirst du fast immer mit E-Mails, PDFs und Excel-Tabellen zu tun haben. Der Bot `examples/invoice-processing/` zeigt dir als "Gold Standard", wie man diese drei typischen RPA-Muster hochprofessionell umsetzt.

Hier sind die drei wichtigsten Best Practices, die du direkt in deine eigenen Bots übernehmen solltest:

### 1. E-Mails: Der lokale Simulations-Modus

In der echten Welt liest dein Bot E-Mails von einem Server (z. B. Outlook/Exchange via IMAP). Wenn du deinen Bot aber lokal auf deinem Laptop entwickelst oder testest, hast du oft keine echten Login-Daten oder Internetverbindung.

- **Die Lösung:** Baue immer einen **Simulationsmodus** ein (gesteuert über `simulated_mode: bool = True` in deiner Config).
- **Wie es funktioniert:** Ist der Simulationsmodus aktiv, erzeugt der Bot im E-Mail-Task automatisch temporäre `.eml`-Dateien auf der Festplatte (mit Base64-kodierten PDF-Rechnungen darin) und liest diese ein, genau wie er es mit echten IMAP-Mails tun würde.
- **Vorteil:** Du und deine Kollegen können den Bot jederzeit sofort lokal starten und testen (`pytest`), ohne echte Zugangsdaten konfigurieren zu müssen.

### 2. PDFs: Robustes Layout-Parsing mit `pdfplumber`

Rechnungs-PDFs sehen fast immer unterschiedlich aus. Manchmal steht die Rechnungsnummer direkt neben dem Wort "Rechnungsnummer:", manchmal ist ein Leerzeichen dazwischen, und manchmal steht es in der nächsten Zeile.

- **Die Lösung:** Nutze `pdfplumber` zum Auslesen des Texts und baue **robuste Reguläre Ausdrücke (Regex)** mit sogenannten _Lookaheads_.
- **Beispiel:**

  ```python
  # Schlecht: Erkennt den Namen nicht, wenn ein Doppelpunkt oder Sonderzeichen folgt
  re.search(r"Supplier:\s*([A-Za-z0-9 ]+)", text)

  # Profi-Muster: Liest alles ab "Supplier:" bis zum Wort "Invoice ID" oder dem Zeilenende
  re.search(r"Supplier:\s*(.*?)(?=\s+Invoice ID|\n|$)", text)
  ```

- **Vorteil:** Dein Bot stürzt nicht sofort ab, wenn ein Lieferant sein Rechnungs-Layout minimal ändert.

### 3. Excel: Echte Formeln statt statischer Zahlen

Wenn dein Bot Excel-Berichte schreibt, berechne Summen oder Durchschnitte niemals direkt in Python, um sie dann als feste Zahlen in die Zellen zu schreiben.

- **Die Lösung:** Nutze `openpyxl` und schreibe **echte Excel-Formeln** in die Zellen (z. B. `=SUM(E2:E10)` für die Spaltensumme oder `=AVERAGE(Invoices!E2:E10)` für den Durchschnitt auf einem anderen Tabellenblatt).
- **Vorteil:** Wenn der Business-User die Excel-Datei öffnet und Zahlen anpasst, rechnen sich alle Summen und KPI-Sheets automatisch neu durch. Nutze zudem das offizielle Farbschema (`#1F4E79` für Merle) und richte Spaltenbreiten automatisch an der Textlänge aus. Highlighte wichtige Zeilen (z.B. Beträge > 10.000 €) mit farbigen Regeln (`CellIsRule` für bedingte Formatierung).

---

## 10. Python oder UiPath? Die einfache Entscheidung

Du wirst früher oder später gefragt: "Warum machen wir das nicht mit UiPath?"

**Die Merle-Regel ist ganz einfach:**

- **Webseiten, APIs, Excel, PDFs, E-Mails, moderne Systeme** → **Immer Python** (mit Playwright + pandas etc.)
- **Sehr alte Desktop-Programme** (alte SAP GUI, Citrix mit komischen Fenstern, spezielle Win32-Apps) → Hier kann UiPath manchmal besser sein.

**Faustregel für dich als Junior:**  
Wenn du unsicher bist, frag zuerst: "Können wir das mit Playwright + Python machen?"  
95 % der Fälle ist die Antwort "Ja".

Die genaue Entscheidungsmatrix findest du in `docs/concepts/entscheidungsmatrix.md`.

---

## 11. Dein Lernplan für die ersten 4 Wochen

### Woche 1 – Verstehen & Nachmachen

- [x] Devbox einrichten
- [x] Einen Bot mit `merle new-bot` erzeugen
- [x] Den Beispiel-Bot starten und Logs anschauen
- [x] Einen eigenen Task hinzufügen (auch wenn er erstmal nur "Hallo" sagt)

### Woche 2 – Lesen & Verstehen

- Lies den [Entwicklungsleitfaden](../concepts/entwicklungsleitfaden.md)
- Schau dir den Referenz-Bot `examples/invoice-processing/` an (sehr gutes Beispiel!)
- Verstehe, was `BaseBot` und `BaseTask` wirklich tun

### Woche 3 – Erste echte kleine Aufgabe

- Bekomme eine kleine echte Anforderung (z. B. "Lade diese eine Webseite und speichere den Titel")
- Baue sie mit einem neuen Task
- Schreibe einen Test dafür

### Woche 4 – Qualität & Review

- Lerne `ruff` und `mypy` (die prüfen deinen Code automatisch)
- Lass dir deinen ersten Bot von einem erfahrenen Kollegen reviewen
- Lies die Governance-Regeln (`docs/concepts/governance.md`)

---

## 12. Wo du immer Hilfe bekommst

### 1. Der RPA-Hybrid-Architekt (KI-Assistent)

Im Merle-Ordner einfach eingeben:

```bash
opencode
```

Dann steht dir sofort ein sehr guter KI-Assistent zur Verfügung, der **alle** Regeln von Merle kennt. Du kannst ihn fragen:

- "Erstelle mir einen neuen Task für PDF-Verarbeitung"
- "Warum funktioniert mein Retry nicht?"
- "Ist das hier template-konform?"

Er achtet darauf, dass du die Regeln einhältst.

### 2. Die Dokumentation

- `docs/getting-started/quickstart.md` – Schnellreferenz
- `docs/concepts/entwicklungsleitfaden.md` – Der große Entwicklungsleitfaden
- `examples/invoice-processing/` – Das beste reale Beispiel

### 3. Dein Team

Stelle Fragen! Bei Merle wird erwartet, dass Juniors Fragen stellen. Besser einmal zu viel gefragt als stundenlang hängen bleiben.

---

## 13. Die wichtigsten Befehle auf einen Blick

| Was ich will           | Befehl (innerhalb Devbox)                       |
| ---------------------- | ----------------------------------------------- |
| Neuen Bot anlegen      | `devbox run new-bot name --playwright --pandas` |
| Bot starten            | `uv run python main.py`                         |
| Tests ausführen        | `uv run pytest -v`                              |
| Code prüfen (Linting)  | `uv run ruff check .`                           |
| Code schön formatieren | `uv run ruff format .`                          |
| Typen prüfen           | `uv run mypy .`                                 |
| Bot im Docker testen   | `docker build ...` + `docker run ...`           |

---

## Abschlusswort

Du musst nicht alles sofort verstehen.

Merle ist so aufgebaut, dass du **schrittweise** besser wirst:

1. Bot anlegen (Template)
2. Einen Task verstehen und anpassen
3. Mehrere Tasks kombinieren
4. Eigene Anforderungen umsetzen
5. Später komplexe Orchestrierung und NATS (das kommt in Phase 3+)

**Du bist jetzt nicht allein.**  
Das Template + merle-core + der RPA-Hybrid-Architekt + dieses Team sorgen dafür, dass du von Anfang an gute Arbeit ablieferst.

---

**Nächster Schritt nach diesem Guide:**

Lies den [Schnellstart](quickstart.md) und dann den [Entwicklungsleitfaden](../concepts/entwicklungsleitfaden.md).

Viel Spaß beim Bauen deiner ersten richtig guten RPA-Bots mit Merle!

---

_Dieser Guide wurde mit Liebe zum Detail für Junior-Entwickler und Quereinsteiger geschrieben. Feedback gerne an das Merle-Team._
