# Plan: Dokumentations-Verbesserung & Visualisierung (Phase 3+)

**Status:** Draft  
**Zieltermin:** Q3 2026 (parallel zu Phase 4 NATS)  
**Verantwortlich:** Merle RPA-Hybrid-Architekt + Tech Writing Support

---

## 1. Vision: „Docs, die man verstehen will“

Merle-Dokumentation soll **nicht nur korrekt**, sondern **überzeugend und sofort verständlich** sein. 

**Zielbild 2026:**
- Neue Entwickler verstehen innerhalb von **15 Minuten**, warum Python-First gilt und wie ein guter Merle-Bot aussieht.
- Die Entscheidungsmatrix und die 10 Governance-Regeln sind **visuell so stark**, dass man sie ausdrucken und an die Wand hängen möchte.
- Architektur-Diagramme (C4 + NATS-Vision) sind der Standard für alle internen und externen Reviews.
- OpenCode + der RPA-Hybrid-Architekt wird durch klare Visuals als echter Produktivitäts-Booster verstanden.

**Leitprinzipien für Visuals:**
- Weniger Text, mehr Bild
- Ein Diagramm ersetzt oft 3–4 Absätze
- Mermaid für versionierte, wartbare Diagramme (Architecture, Flows)
- Hochwertige generierte Bilder für „Hero Visuals“ und Onboarding (professionelles Design, Icons, Farben)
- Konsistente visuelle Sprache (Farben, Icons, Stil) über alle Dokumente

---

## 2. Aktuelle Schwachstellen (Gap Analysis)

| Bereich                    | Problem                                      | Auswirkung                          | Priorität |
|---------------------------|----------------------------------------------|-------------------------------------|---------|
| **Navigation & Struktur** | MkDocs-Nav zeigt viele nicht-existierende Seiten (`concepts/strategie.md`, ganze `merle-core/` Sektion, `development/`) | Verwirrung, hohe Einstiegshürde   | P0 |
| **Entscheidungsmatrix**   | Nur ASCII-Art Flowchart                      | Wirkt veraltet, schwer lesbar       | P0 |
| **Governance (10 Regeln)**| Reine Text-Liste, keine visuelle Übersicht   | Regeln werden nicht verinnerlicht   | P0 |
| **Bot Lifecycle**         | Kein durchgängiges visuelles Modell          | Unklar, wie ein Bot von Idee bis AKS kommt | P1 |
| **NATS Vision**           | Nur Tabelle in architecture.md               | Komplexe Phase-4-Architektur schwer vorstellbar | P1 |
| **OpenCode Integration**  | Nur Text in README + AGENTS.md               | Viele verstehen nicht, wie `.opencode/` + Fork zusammenwirken | P1 |
| **merle-core Komponenten**| Kein Komponenten-Diagramm                    | Schwierig zu erklären, was drin ist | P2 |
| **Hybrid Patterns**       | Nur Code-Beispiele                           | Integrationsmuster nicht intuitiv   | P2 |
| **Bilder & Assets**       | Praktisch keine Bilder im `docs/`            | Niedrige visuelle Attraktivität     | P0 |

---

## 3. Priorisierter Umsetzungsplan

### Phase 1 – Foundation (2–3 Wochen)

**Ziel:** Struktur stabilisieren + erste starke Visuals liefern.

1. **MkDocs Navigation reparieren**
   - Entweder flache Struktur beibehalten (01–06) oder echte Ordnerstruktur unter `concepts/`, `merle-core/`, `development/` anlegen.
   - Empfehlung: **Hybride Struktur** — Nummerierte Kern-Docs bleiben, zusätzlich thematische Ordner mit besseren Namen.

2. **Hero Visuals erstellen** (dieser Plan)
   - Entscheidungsfluss Python vs. UiPath (professionelles Flowchart)
   - Die 10 Governance-Regeln als visuelle Karte / Icon-Grid
   - Merle Bot Lifecycle (End-to-End)

3. **Mermaid-Standards einführen**
   - Alle C4-Diagramme auf einheitlichen Stil bringen (bestehende in `concepts/architecture.md` als Vorlage).
   - Mermaid-Theme definieren (Farben passend zu Indigo-Theme).

### Phase 2 – Vertiefung & NATS (parallel zu Phase 4)

- Detailliertes NATS-Orchestrierungs-Visual (Publisher → Streams → Workers → Dead Letter + Cobra Monitoring)
- OpenCode RPA-Hybrid-Setup Diagramm (`.opencode/` vs. `rpa-opencode-hybrid/`)
- merle-core Komponenten-Diagramm (BaseTask, Retry, Observability, NATS, Playwright Wrapper, Secrets)

### Phase 3 – Interaktive & Erweiterte Formate

- PDF-Export der wichtigsten Visuals (für Workshops, Reviews, Onboarding-Pakete)
- Interaktive Mermaid-Diagramme mit Klick-Navigation (wo sinnvoll)
- Kurze Erklärvideos (2–3 min) zu den Top-3 Visuals (optional, hoher Impact)

---

## 4. Konkrete Diagramm- & Bildvorschläge (mit Priorität)

### P0 – Sofort umsetzen (nächste 4 Wochen)

| # | Visual | Typ | Wo platziert? | Warum wichtig? | Aufwand |
|---|--------|-----|---------------|----------------|--------|
| 1 | **Python vs. UiPath Entscheidungsfluss** | Schönes farbiges Flowchart (mit Icons) | `docs/02_Wann_Python_vs_UiPath.md` + `index.md` | Ersetzt schwaches ASCII, wird am häufigsten gebraucht | Mittel |
| 2 | **Die 10 Governance-Regeln – Visuelle Übersicht** | Icon-Grid / Poster-Style (10 Karten) | `docs/03_Governance.md` + als eigenes One-Pager | Regeln werden endlich verinnerlicht und diskutiert | Hoch |
| 3 | **Merle Bot Lifecycle** (Idee → Template → Entwicklung → CI/CD → AKS + Monitoring) | Horizontales Timeline-Diagramm | `docs/05_Entwicklungsleitfaden.md` + Getting Started | Macht den gesamten Prozess greifbar | Mittel |
| 4 | **C4 Architecture – NATS-Variante** | Erweitertes Mermaid C4 (Level 1–3) | `docs/concepts/architecture.md` | Macht Phase-4-Vision konkret | Mittel |

### P1 – Phase 4 begleitend

| # | Visual | Typ | Wo? | Zweck |
|---|--------|-----|-----|-------|
| 5 | **NATS Orchestrierung – Moderne Architektur** | Layered Architecture (Publishers, JetStream, Workers, DLQ, Cobra, Grafana) | Neues Kapitel in `concepts/` oder `merle-core/nats.md` | Verständnis für die größte zukünftige Architekturveränderung |
| 6 | **OpenCode RPA-Hybrid Integration** | Komponenten-Diagramm (`.opencode/` → Agent/Skills/Tool → rpa-hybrid Persona) | README.md + neuer Abschnitt „KI-gestützte Entwicklung“ | Erklärt den neuen Produktivitätsvorteil klar |
| 7 | **merle-core Bausteine** | Modular Architecture Diagram | `docs/merle-core/` (wenn aufgebaut) | Zeigt, was man mit `uv add merle-core[...]` wirklich bekommt |

### P2 – Nice-to-have

- Vergleich: Legacy Template (`python_bots/template/`) vs. modernes Copier-Template (`templates/bot/`)
- Hybrid-Integrations-Patterns (4 Varianten als visuelle Kacheln)
- Secrets-Management Flow (Azure Key Vault → pydantic-settings → Bot)

---

## 5. Technische Umsetzung

### 5.1 Mermaid (Versioniert & wartbar)

- Bereits aktiviert (`mermaid2` Plugin + superfences)
- Vorteil: Lebt im Git, wird mit dem Code versioniert, leicht änderbar
- Empfehlung: Alle Architecture-Diagramme, Flows und C4-Modelle als Mermaid halten.

### 5.2 Generierte Bilder („Schick & Einprägsam“)

- Für Hero-Visuals, Onboarding und Druck/PDF
- Tool: xAI Imagine (via `image_gen`) oder Midjourney / Flux / Leonardo
- Stil-Empfehlung:
  - Clean, modern, techy
  - Indigo + Cyan Akzente (passend zum MkDocs Theme)
  - Leichte 3D-/Isometrie-Elemente oder starke Flat-Icons
  - Hohe Lesbarkeit auch in kleineren Größen
- Speicherort: `docs/assets/images/` (neu anlegen)
- Namenskonvention: `governance-rules-overview.png`, `bot-lifecycle.png` etc.

### 5.3 Assets-Struktur (neu)

```
docs/
├── assets/
│   ├── images/
│   │   ├── decisions/
│   │   ├── architecture/
│   │   └── onboarding/
│   └── diagrams/          # exportierte Mermaid SVGs (optional)
└── ...
```

---

## 6. Erfolgsmetriken

- Zeit bis „erster lauffähiger Bot“ für neue Entwickler sinkt um ≥ 30 %
- In Reviews wird aktiv auf die Visuals verwiesen („Schau dir das Lifecycle-Diagramm an“)
- Die Governance-Visual wird ausgedruckt und hängt in mindestens 3 Büros
- Anzahl der ADRs mit begleitendem Diagramm steigt von aktuell ~1 auf ≥ 5

---

## 7. Nächste Schritte (empfohlen)

1. **Diesen Plan reviewen** und priorisieren (P0-Visuals festlegen)
2. **Erste 3 Visuals generieren** (Python-vs-UiPath Flow + Governance Overview + Bot Lifecycle)
3. MkDocs-Navigation in einem separaten kleinen Task fixen
4. Die Visuals in die jeweiligen Docs einbauen + kurze erläuternde Texte drumherum schreiben
5. Feedback-Runde mit dem Team („Welches Visual hat dir am meisten geholfen?“)

---

**Merke:** Gute Dokumentation mit starken Visuals ist einer der größten Hebel für die Skalierung des Merle-Frameworks. Sie senkt die Einstiegshürde, erhöht die Governance-Adhärenz und macht die Architekturentscheidungen (besonders NATS in Phase 4) für alle Beteiligten nachvollziehbar.

---

*Erstellt von Grok 4.3 im Rahmen der RPA-Hybrid-Architektur-Unterstützung – Mai 2026*