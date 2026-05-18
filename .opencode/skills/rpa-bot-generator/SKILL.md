# RPA Bot Generator (Phase 3+)

## Purpose

Generiert einen neuen Python-Bot **strikt nach dem aktuellen Merle-Standard**
(Copier-Template + merle-core + Governance).

## When to Use

- Nach der Prozessanalyse (via `rpa-process-analyzer`)
- Immer wenn ein neuer Bot erstellt werden soll

## Empfohlener Prozess (Phase 1+)

### 1. Voraussetzungen prüfen

- Technologieentscheidung ist dokumentiert?
- Bot-Name folgt der Konvention (`<domain>_<action>`)?
- Zielverzeichnis `python_bots/<bot_name>/` existiert noch nicht?

### 2. Bot mit Copier erzeugen (empfohlen)

```bash
# Beste Variante
merle new-bot <bot_name> --playwright --pandas

# Alternative
copier copy templates/bot python_bots/<bot_name>
```

### 3. Nach der Generierung anpassen (Phase 2+)

#### 3.1 config.py erweitern

- `bot_name` korrekt setzen
- Projektspezifische Felder hinzufügen
- `AzureKeyVaultSettings` nutzen, wenn Secrets aus Key Vault kommen sollen

#### 3.2 Tasks modern umsetzen

- **Immer** von `BaseTask` erben
- `execute()` implementieren
- Logging über `self.logger`
- Retry über `@with_retry` aus `merle_core.retry`

#### 3.3 main.py anpassen (Phase 2+)

- `configure_observability(service_name=...)` am Anfang aufrufen
- Tasks orchestrieren

#### 3.4 Tests, README und .env.example pflegen

### 4. Qualitäts-Checkliste (Phase 3+)

- [ ] Bot wurde mit `merle new-bot` oder Copier erstellt
- [ ] `merle-core` wird verwendet
- [ ] `BaseTask` wird für fachliche Logik verwendet
- [ ] `configure_observability()` ist vorhanden
- [ ] Alle 10 Governance-Regeln erfüllt (inkl. Rule 10)

## Hard Constraints (Phase 3+)

- **Immer** Copier / `merle new-bot` verwenden
- **Immer** `BaseTask` nutzen
- **Immer** Observability aktivieren
- **Immer** `merle-core` als Dependency deklarieren

## References

- `templates/bot/` — Offizielles Copier-Template
- `docs/concepts/entwicklungsleitfaden.md`
- `docs/concepts/governance.md` (inkl. Rule 10)
- `merle_core/task.py` — TaskSpec & TaskResult
- `merle_core/nats/` — NATS-Integration (ab Phase 4)
