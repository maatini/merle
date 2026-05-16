"""
Beispiel: UiPath Orchestrator REST API Integration.

Dieses Skript zeigt, wie ein Python-Bot:
1. Sich am UiPath Orchestrator authentifiziert
2. Einen Job startet
3. Den Job-Status abfragt
4. Queue-Items erstellt und abruft

Voraussetzungen:
- UiPath Orchestrator Cloud oder On-Premises
- Client ID + Client Secret (OAuth 2.0)
- Tenant-Name
"""

import asyncio

import httpx
from loguru import logger


class OrchestratorClient:
    """Client für die UiPath Orchestrator REST API."""

    BASE_URL = "https://cloud.uipath.com"  # Cloud-URL — für On-Prem anpassen

    def __init__(self, client_id: str, client_secret: str, tenant: str = "Default"):
        self.client_id = client_id
        self.client_secret = client_secret
        self.tenant = tenant
        self.access_token: str | None = None

    async def authenticate(self) -> str:
        """Authentifiziere via OAuth 2.0 Client Credentials Grant."""
        url = "https://account.uipath.com/oauth/token"
        data = {
            "grant_type": "client_credentials",
            "client_id": self.client_id,
            "client_secret": self.client_secret,
        }
        async with httpx.AsyncClient() as client:
            response = await client.post(url, data=data)
            response.raise_for_status()
            token_data = response.json()
            self.access_token = token_data["access_token"]
            logger.info("Orchestrator-Authentifizierung erfolgreich")
            return self.access_token

    async def _headers(self) -> dict:
        if not self.access_token:
            await self.authenticate()
        return {
            "Authorization": f"Bearer {self.access_token}",
            "Content-Type": "application/json",
            "X-UIPATH-TenantName": self.tenant,
        }

    async def start_job(self, process_key: str, robot_id: int = 0) -> dict:
        """Starte einen Job im Orchestrator."""
        url = f"{self.BASE_URL}/odata/Jobs/UiPath.Server.Configuration.OData.StartJobs"
        payload = {
            "startInfo": {
                "ReleaseKey": process_key,
                "Strategy": "Specific" if robot_id else "All",
                "RobotIds": [robot_id] if robot_id else [],
                "NoOfRobots": 1,
            }
        }
        async with httpx.AsyncClient() as client:
            response = await client.post(url, json=payload, headers=await self._headers())
            response.raise_for_status()
            logger.info("Job gestartet: {}", response.json())
            return response.json()

    async def get_job_status(self, job_id: int) -> str:
        """Frage den Status eines Jobs ab."""
        url = f"{self.BASE_URL}/odata/Jobs({job_id})"
        async with httpx.AsyncClient() as client:
            response = await client.get(url, headers=await self._headers())
            response.raise_for_status()
            job = response.json()
            state = job.get("State", "Unknown")
            logger.info("Job {} Status: {}", job_id, state)
            return state

    async def add_queue_item(self, queue_name: str, content: dict) -> dict:
        """Füge ein Item zu einer Queue hinzu."""
        url = f"{self.BASE_URL}/odata/QueueItems"
        payload = {
            "ItemData": {
                "Name": queue_name,
                "Priority": "Normal",
                "SpecificContent": content,
            }
        }
        async with httpx.AsyncClient() as client:
            response = await client.post(url, json=payload, headers=await self._headers())
            response.raise_for_status()
            logger.info("Queue-Item hinzugefügt: {}", response.json())
            return response.json()


async def main():
    """Demo: Orchestrator-Integration."""
    # Diese Werte aus Umgebungsvariablen laden (niemals hartcodieren!)
    import os

    client_id = os.getenv("UIPATH_CLIENT_ID", "")
    client_secret = os.getenv("UIPATH_CLIENT_SECRET", "")
    tenant = os.getenv("UIPATH_TENANT", "Default")

    orchestrator = OrchestratorClient(client_id, client_secret, tenant)

    # 1. Authentifizieren
    await orchestrator.authenticate()

    # 2. Queue-Item erstellen (z.B. Rechnungsdaten)
    await orchestrator.add_queue_item(
        "InvoiceQueue",
        {
            "invoice_id": "INV-2026-001",
            "amount": 1500.00,
            "vendor": "ACME Corp",
        },
    )

    # 3. Job starten (z.B. Rechnungsverarbeitung)
    # result = await orchestrator.start_job("your-process-key-here")
    # job_id = result["value"][0]["Id"]
    # status = await orchestrator.get_job_status(job_id)


if __name__ == "__main__":
    asyncio.run(main())
