# ADR-0002: Verbindliche Template-Architektur für neue Python-Bots

## Status
Akzeptiert

## Kontext
Wenn mehrere RPA-Entwickler und -Teams ohne feste Vorgaben Skripte schreiben, entsteht schnell eine unübersichtliche Code-Basis ("Grüne Wiese"-Problem). Jeder Entwickler implementiert eigenes Logging, unterschiedliche Fehlerbehandlungsstrategien und Konfigurationsformate. Dies erschwert das Code-Review, das Testing und den stabilen Betrieb der Bots im Cluster enorm.

## Entscheidung
Es wird eine strikte Template-Architektur eingeführt. Jeder neue Python-Bot **muss** als direkte Kopie des Verzeichnisses `python_bots/template/` beginnen.
Dieses Template gibt folgende Standards verbindlich vor:
- **Logging:** Verwendung von `loguru` für strukturiertes, farbiges Logging.
- **Error Handling & Retry:** Verwendung von `tenacity` für Retry-Mechanismen mit Backoff.
- **Konfiguration:** Verwendung von `pydantic-settings` zur typsicheren Konfiguration via Environment-Variablen.
- **Struktur:** Vordefinierte Struktur für Tests (`pytest`), Einstiegspunkte (`main.py`) und Abhängigkeiten (`requirements.txt`).

Ein Neustart oder die Entwicklung eines Bots von Grund auf ohne dieses Template ist nicht zulässig und wird bei Code-Reviews (auch durch KI-Agenten wie den `governance-validator`) abgewiesen.

## Konsequenzen
- **Positiv:** Drastische Reduzierung von Boilerplate-Code. Einheitliche Struktur über alle Bots hinweg. Erhöhte Ausfallsicherheit, da essenzielle Cloud-Native-Patterns (Retry, strukturiertes Logging) bereits standardisiert integriert sind.
- **Negativ/Risiken:** Geringere Flexibilität für Entwickler bei der Wahl grundlegender Frameworks. Updates am Basis-Template müssen koordiniert an bestehende Bots ausgerollt oder kommuniziert werden.
