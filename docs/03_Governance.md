# Governance-Regeln

## Zweck

Dieses Dokument definiert die verbindlichen Governance-Regeln für das hybride RPA-Development-Kit.  
Jeder Bot, jedes Projekt und jede Architekturentscheidung muss diesen Regeln entsprechen.

## Regel 1: Python-First (Default-Regel)

**Regel**: Jede neue Automatisierung startet als Python-Projekt.  
**Ausnahme**: Nur mit dokumentierter Begründung gemäß Entscheidungsmatrix (`02_Wann_Python_vs_UiPath.md`).  
**Durchsetzung**: Der RPA-Hybrid-Architekt reviewt jede Technologieentscheidung.

## Regel 2: Template-Pflicht

**Regel**: Jeder neue Python-Bot wird aus `python_bots/template/` geklont und nicht von Null begonnen.  
**Umfang**: main.py, config.py, requirements.txt, logging, retry, testing, Docker.  
**Durchsetzung**: Code-Review-Checkliste prüft Template-Konformität.

## Regel 3: Keine hartcodierten Werte

**Regel**: Keine Credentials, URLs, API-Keys, Pfade oder Umgebungsabhängigkeiten im Code.  
**Lösung**: pydantic-settings mit `.env`-Datei, Umgebungsvariablen, Konfigurationsdateien.  
**Durchsetzung**: Automatische Scans (git-secrets, trufflehog) + manuelles Review.

## Regel 4: Logging und Monitoring

**Regel**: Jeder Bot muss strukturiertes Logging und grundlegendes Monitoring haben.  
**Standard**: loguru für Logging (JSON-Format in Produktion), Health-Check-Endpunkt.  
**Durchsetzung**: Code-Review-Prüfung auf Logger-Instanz und Health-Check.

## Regel 5: Fehlerbehandlung und Retry

**Regel**: Externe Aufrufe (HTTP, Dateisystem, Datenbank) müssen mit tenacity wiederholt werden.  
**Standard**: Exponentielles Backoff, max. 3–5 Versuche, unterscheidbare Fehlertypen.  
**Durchsetzung**: Code-Review prüft @retry-Dekoratoren.

## Regel 6: Tests

**Regel**: Jeder Bot muss grundlegende Tests haben.  
**Minimum**: Unit-Tests für Business-Logik und kritische Pfade.  
**Ziel**: >70 % Testabdeckung für Business-Logik.  
**Durchsetzung**: CI-Pipeline bricht bei fehlenden Tests ab.

## Regel 7: Linux-Container-Kompatibilität

**Regel**: Jeder Python-Bot muss in einem Linux-Container lauffähig sein.  
**Verboten**: Windows-only-Abhängigkeiten, absolute Windows-Pfade, COM-Objekte.  
**Durchsetzung**: CI-Pipeline baut Docker-Image und führt Smoke-Test aus.

## Regel 8: Dokumentation

**Regel**: Jeder Bot hat eine README.md mit Zweck, Konfiguration, Betriebsanleitung.  
**Minimum**: Projektzweck, Umgebungsvariablen, Start-Anleitung, Abhängigkeiten.  
**Durchsetzung**: Code-Review prüft README.md.

## Regel 9: Code-Review

**Regel**: Jede Änderung durchläuft ein Code-Review durch mindestens einen anderen Entwickler.  
**Fokus**: Template-Konformität, Security, Fehlerbehandlung, Tests.  
**Durchsetzung**: Branch-Protection in Git.

## Regel 10: Entscheidungsdokumentation

**Regel**: Jede Technologieentscheidung (insbesondere Python vs. UiPath) wird dokumentiert.  
**Format**: Siehe `02_Wann_Python_vs_UiPath.md`, Abschnitt „Entscheidungsdokumentation".  
**Durchsetzung**: Architecture Decision Records (ADR) im `docs/decisions/`-Verzeichnis.

## Governance-Prozess

```
Neues Projekt
     │
     ▼
┌─────────────────────┐
│ 1. Technologie-     │
│    Entscheidung      │
│    (Matrix anwenden) │
└────────┬────────────┘
         │
         ▼
┌─────────────────────┐
│ 2. Template klonen  │
│    (python_bots/)   │
└────────┬────────────┘
         │
         ▼
┌─────────────────────┐
│ 3. Entwickeln +     │
│    Tests schreiben  │
└────────┬────────────┘
         │
         ▼
┌─────────────────────┐
│ 4. Code-Review      │
│    (Governance-     │
│     Checkliste)     │
└────────┬────────────┘
         │
         ▼
┌─────────────────────┐
│ 5. CI/CD-Pipeline   │
│    (Tests, Docker)  │
└────────┬────────────┘
         │
         ▼
┌─────────────────────┐
│ 6. Deployment +     │
│    Monitoring       │
└─────────────────────┘
```

## Governance-Checkliste für Code-Reviews

- [ ] Technologieentscheidung dokumentiert (Python/UiPath)?
- [ ] Aus Template geklont?
- [ ] Keine hartcodierten Werte?
- [ ] Strukturiertes Logging (loguru)?
- [ ] Retry-Mechanismen (tenacity)?
- [ ] Tests vorhanden (>70 % Business-Logik)?
- [ ] Dockerfile vorhanden und baubar?
- [ ] README.md mit Dokumentation?
- [ ] Keine Windows-only-Abhängigkeiten?
- [ ] Einhaltung der Projektstruktur-Konventionen?

## Compliance und Auditing

- **Quartalsweises Audit**: Alle Bots auf Governance-Einhaltung prüfen
- **Automatische Scans**: git-secrets, pylint, mypy in CI
- **ADR-Review**: Alle Architecture Decision Records werden quartalsweise auf Aktualität geprüft

## Revision

| Version | Datum | Änderung | Autor |
|---------|-------|----------|-------|
| 1.0 | 2026-05-10 | Initiale Version | RPA-Hybrid-Architekt |
