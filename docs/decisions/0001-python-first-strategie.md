# ADR-0001: Python-First Strategie für RPA

## Status
Akzeptiert

## Kontext
Die Entwicklung von RPA-Bots (Robotic Process Automation) wurde in der Vergangenheit häufig exklusiv mit Legacy-Tools und rein visuellen Workflows (z. B. UiPath) umgesetzt. Diese Herangehensweise hat sich für viele Anwendungsfälle als schwer wartbar, nur eingeschränkt versionierbar (fehlende `git diff`-Fähigkeit) und schwer in moderne CI/CD-Pipelines integrierbar erwiesen. Zudem sind visuelle Workflows schwerer mit klassischen Unit-Tests abzusichern und erzwingen häufig eine Vendor-Lock-in Infrastruktur (z. B. Windows-only Ausführung).

## Entscheidung
Für das **Merle-Framework** gilt ab sofort die "Python-First"-Strategie. 
Das bedeutet:
- **80–90 % aller Automatisierungen** werden in modernem, Python-basiertem Code geschrieben.
- Zu den Standard-Bibliotheken gehören `rpaframework`, `Playwright` (für Web-Automatisierung) sowie Tools wie `pandas` und `Prefect`.
- **UiPath wird nur noch als begründungspflichtige Ausnahme eingesetzt**, beispielsweise wenn eine hochkomplexe Legacy-Desktop-UI (alte SAP GUI, Citrix) oder sehr starke Document Understanding-Anforderungen vorliegen, die sich mit Python nicht wirtschaftlich abbilden lassen. Jede Nutzung von UiPath erfordert einen expliziten Verweis auf die Entscheidungsmatrix.

## Konsequenzen
- **Positiv:** Bots können containerisiert (Linux/Docker) in der Cloud (Azure AKS Cluster) betrieben werden. Echte Test-getriebene Entwicklung (TDD) und saubere Code-Reviews werden möglich. Lizenzkosten sinken.
- **Negativ/Risiken:** Erfordert von Citizen Developers und klassischen RPA-Entwicklern ein Umdenken und den Aufbau von Python-Kompetenzen. Der Onboarding-Prozess für Entwickler muss entsprechend angepasst werden.
