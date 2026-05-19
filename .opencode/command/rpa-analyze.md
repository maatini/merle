---
description: Prozessbeschreibung analysieren und Technologie-Empfehlung (Python vs. UiPath) erstellen
model: opencode/gpt-5.4
subtask: false
---

Analysiere eine Prozessbeschreibung und erstelle eine fundierte, datenbasierte Python-vs-UiPath-Empfehlung mit ausführlicher Begründung gemäss dem **rpa-process-analyzer** Skill.

## Vorgehen

1. Frage den Benutzer nach der Beschreibung des Prozesses (Systeme, Schnittstellen, Daten, Frequenz, Komplexität), falls nicht bereits angegeben.
2. Führe die Analyse durch und verwende dabei die Kriterien und die Entscheidungsmatrix aus `docs/concepts/entscheidungsmatrix.md`.
3. Gib das Ergebnis strukturiert aus (Score, Empfehlung, Begründung, Risiko & Mitigation, Nächste Schritte).
