# BaseBot & BaseTask

`BaseBot` und `BaseTask` bilden das Fundament jedes Merle-Bots.

## Philosophie

- **BaseTask**: Jede fachliche Logik lebt in einer Klasse, die von `BaseTask` erbt.
- **BaseBot**: Koordiniert mehrere Tasks, konfiguriert Observability und übernimmt das Lebenszyklus-Management.

## BaseTask (empfohlen ab Phase 3+)

```python
from merle_core import BaseTask, TaskResult
from merle_core.retry import with_retry


class InvoiceProcessingTask(BaseTask):
    async def execute(self, invoice_id: str) -> TaskResult:
        self.logger.info("Verarbeite Rechnung {}", invoice_id)

        data = await self.fetch_invoice(invoice_id)
        result = await self.process_invoice(data)

        return TaskResult.success(data=result)

    @with_retry
    async def fetch_invoice(self, invoice_id: str): ...
```

### Wichtige Methoden

- `execute()` – muss implementiert werden
- `self.logger` – bereits konfigurierte loguru-Instanz
- `self.config` – Zugriff auf die Bot-Konfiguration

## BaseBot

```python
from merle_core import BaseBot, configure_observability


class MyBot(BaseBot):
    async def run(self):
        configure_observability(service_name="invoice-bot")

        task = InvoiceProcessingTask()
        result = await task.run(invoice_id="INV-12345")
```

---

**Nächste Schritte**: Siehe [Entwicklungsleitfaden](../concepts/entwicklungsleitfaden.md) für den empfohlenen Aufbau eines neuen Bots.
