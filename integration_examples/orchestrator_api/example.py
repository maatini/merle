"""
Beispiel: UiPath Orchestrator REST API Integration (thin demo).

**SSOT:** Produktionscode lebt in ``merle_core.uipath``:
- ``UiPathOrchestratorClient`` — OAuth, start_job, get_job_status
- ``UiPathQueueHelper`` — add_queue_item, get_queue_items

Dieses Skript ist nur ein dünner Demo-Einstieg (env → client → queue item).
Für Bots: siehe ``examples/uipath-hybrid/`` (BaseBot + SIMULATE-Modus).

Voraussetzungen (Live):
- UiPath Orchestrator Cloud oder On-Premises
- Client ID + Client Secret (OAuth 2.0)
- Tenant-Name

Lokaler Smoke-Test ohne Credentials: SIMULATE=true (Default) loggt den Plan und exit 0.
"""

from __future__ import annotations

import asyncio
import os

from loguru import logger

from merle_core.uipath import UiPathOrchestratorClient, UiPathQueueHelper

# Re-export SSOT types for callers that historically imported from this module
__all__ = [
    "UiPathOrchestratorClient",
    "UiPathQueueHelper",
    "main",
]


async def main() -> None:
    """Demo: Orchestrator-Integration via merle_core.uipath."""
    simulate = os.getenv("SIMULATE", "true").lower() in ("1", "true", "yes")
    client_id = os.getenv("UIPATH_CLIENT_ID", "")
    client_secret = os.getenv("UIPATH_CLIENT_SECRET", "")
    tenant = os.getenv("UIPATH_TENANT", "Default")
    base_url = os.getenv("UIPATH_BASE_URL", "https://cloud.uipath.com")
    queue_name = os.getenv("UIPATH_QUEUE_NAME", "InvoiceQueue")

    if simulate or not client_id or not client_secret:
        logger.info(
            "SIMULATE/missing credentials — no Orchestrator HTTP. "
            "SSOT client: merle_core.uipath.UiPathOrchestratorClient / UiPathQueueHelper. "
            "Set SIMULATE=false + UIPATH_CLIENT_ID/SECRET for live demo."
        )
        logger.info(
            "Would authenticate, add_queue_item({!r}, invoice demo payload), optional start_job",
            queue_name,
        )
        return

    client = UiPathOrchestratorClient(
        client_id=client_id,
        client_secret=client_secret,
        tenant=tenant,
        base_url=base_url,
    )
    queue = UiPathQueueHelper(client)

    # 1. Authentifizieren
    await client.authenticate()

    # 2. Queue-Item erstellen (z.B. Rechnungsdaten)
    await queue.add_queue_item(
        queue_name,
        {
            "invoice_id": "INV-2026-001",
            "amount": 1500.00,
            "vendor": "ACME Corp",
        },
    )

    # 3. Job starten (optional — process key setzen)
    process_key = os.getenv("UIPATH_PROCESS_KEY")
    if process_key:
        result = await client.start_job(process_key)
        logger.info("Job started: {}", result)
        # job_id = result["value"][0]["Id"]
        # status = await client.get_job_status(job_id)


if __name__ == "__main__":
    asyncio.run(main())
