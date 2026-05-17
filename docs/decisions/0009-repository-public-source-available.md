# ADR-0009: Repository Visibility — Public / Source-Available

**Status:** Accepted  
**Date:** 2026-05-17  
**Deciders:** Martin Richardt (persönlich)  
**Supersedes:** ADR-0008 (Repository Visibility and Internal Governance)

## Kontext

Die in ADR-0008 getroffene Entscheidung, das Repository `maatini/merle` dauerhaft **privat** zu halten und "nie public zu machen", wird hiermit bewusst revidiert.

Das gesamte Projekt (inklusive Historie, ADRs, merle-core, Template, rpa-opencode-hybrid, Beispiele und interner Dokumentation) wird auf GitHub öffentlich sichtbar gemacht.

## Entscheidung

**Das Repository `maatini/merle` wird von PRIVATE auf PUBLIC umgestellt (Visibility = Public).**

Es handelt sich um ein **Source-Available** Modell: Der Quellcode ist frei einsehbar und klonbar, die Rechte bleiben vollständig bei Martin Richardt (persönlich) durch die bestehende Proprietary License.

### Warum diese Kehrtwende?

- Erhöhte Sichtbarkeit des Merle-Frameworks (Recruiting, Community-Feedback, strategische Transparenz)
- Vereinfachung der Zusammenarbeit mit externen Partnern und Contractors (kein separater Invite + PAT nötig)
- Bewusste Akzeptanz, dass die komplette Git-Historie dauerhaft öffentlich wird
- Die tatsächliche *Nutzung* des Codes bleibt weiterhin stark eingeschränkt (NDA + Lizenzpflicht)

Die in ADR-0008 beschriebene Alternative ("bei Open-Sourcing ein komplett neues, bereinigtes Repo anlegen") wird hier **nicht** gewählt. Stattdessen wird das bestehende Repository geöffnet.

## Konsequenzen

**Positiv:**
- Niedrigere Einstiegshürde für berechtigte externe Entwickler
- Bessere Auffindbarkeit und Reputation des Projekts
- GitHub Pages funktioniert ohne GitHub Enterprise Cloud
- Kein "geheimes" Repo mehr, das misstrauen erwecken könnte

**Negativ / Risiken (bewusst in Kauf genommen):**
- Die komplette Historie inkl. aller ADRs, interner Diskussionen, Code-Beispiele und Architektur-Details ist unwiderruflich öffentlich
- Mögliche Forks können entstehen (Nutzung unterliegt trotzdem der LICENSE)
- Die starken internen Warnungen ("STRICTLY CONFIDENTIAL") müssen entfernt werden
- Bei späterem erneuten Wechsel auf privat würde die öffentliche Phase trotzdem in Archiven (Wayback, GitHub forks, etc.) bestehen bleiben

## Umsetzung (Mai 2026)

1. ADR-0008 als **Superseded** markieren + Verweis auf diese ADR
2. README.md / README.en.md Banner und alle Sichtbarkeits-Warnungen anpassen
3. `gh repo edit maatini/merle --visibility public` ausführen
4. Index der ADRs aktualisieren
5. Private-Repo-Kommentare in mkdocs.yml und Workflows bereinigen
6. Optional: GitHub Topics und Description anpassen

## Bleibende Schutzmechanismen

- Die **LICENSE** bleibt "PROPRIETARY LICENSE — INTERNAL USE ONLY" (unverändert)
- Nur Mitarbeiter und Contractor mit gültigem NDA dürfen den Code produktiv einsetzen
- Jede kommerzielle Nutzung oder Weitergabe ohne Zustimmung von Martin Richardt erfordert eine separate Lizenzvereinbarung
- Interne Governance (Code Reviews, ADRs, Template-Pflicht, etc.) gilt weiterhin für alle internen und beauftragten Entwickler
- Security-Vorfälle werden weiterhin bevorzugt privat gemeldet (SECURITY.md)

## Verweise

- [ADR-0008 (Superseded)](0008-repository-visibility-and-internal-governance.md)
- [LICENSE](./LICENSE)
- [README.md (Banner aktualisiert)](/README.md)
- [SECURITY.md](./SECURITY.md) — verantwortungsvolle Offenlegung
