"""
UiPath Orchestrator REST API client.
"""

from __future__ import annotations

from typing import Any

import httpx
from loguru import logger

from ..exceptions import UiPathError


class UiPathOrchestratorClient:
    """Client for the UiPath Orchestrator REST API."""

    def __init__(
        self,
        client_id: str,
        client_secret: str,
        tenant: str = "Default",
        base_url: str = "https://cloud.uipath.com",
    ) -> None:
        self.client_id = client_id
        self.client_secret = client_secret
        self.tenant = tenant
        self.base_url = base_url.rstrip("/")
        self.access_token: str | None = None
        self.logger = logger.bind(component="UiPathOrchestratorClient")

    async def authenticate(self) -> str:
        """
        Authenticate using OAuth 2.0 Client Credentials Grant.
        Saves the access token locally.
        """
        url = "https://account.uipath.com/oauth/token"
        if "cloud.uipath.com" not in self.base_url:
            # On-premises typically uses the same base URL for identity auth
            url = f"{self.base_url}/identity/connect/token"

        data = {
            "grant_type": "client_credentials",
            "client_id": self.client_id,
            "client_secret": self.client_secret,
        }

        try:
            async with httpx.AsyncClient() as client:
                response = await client.post(url, data=data, timeout=10.0)
                response.raise_for_status()
                token_data = response.json()
                self.access_token = token_data["access_token"]
                self.logger.info("Orchestrator authentication successful")
                return self.access_token
        except Exception as exc:
            raise UiPathError(f"OAuth authentication failed: {exc}") from exc

    async def get_headers(self) -> dict[str, str]:
        """Get common headers including Authorization header and Tenant Name."""
        if not self.access_token:
            await self.authenticate()
        return {
            "Authorization": f"Bearer {self.access_token}",
            "Content-Type": "application/json",
            "X-UIPATH-TenantName": self.tenant,
        }

    async def start_job(self, process_key: str, robot_id: int = 0) -> dict[str, Any]:
        """
        Start a job in the Orchestrator for the given process key.
        """
        url = f"{self.base_url}/odata/Jobs/UiPath.Server.Configuration.OData.StartJobs"
        payload = {
            "startInfo": {
                "ReleaseKey": process_key,
                "Strategy": "Specific" if robot_id else "All",
                "RobotIds": [robot_id] if robot_id else [],
                "NoOfRobots": 1,
            }
        }
        try:
            async with httpx.AsyncClient() as client:
                response = await client.post(url, json=payload, headers=await self.get_headers(), timeout=15.0)
                response.raise_for_status()
                result: dict[str, Any] = response.json()
                self.logger.info("Job successfully started: {}", result)
                return result
        except Exception as exc:
            raise UiPathError(f"Failed to start job for process {process_key}: {exc}") from exc

    async def get_job_status(self, job_id: int) -> str:
        """
        Query the current status of a specific job in the Orchestrator.
        """
        url = f"{self.base_url}/odata/Jobs({job_id})"
        try:
            async with httpx.AsyncClient() as client:
                response = await client.get(url, headers=await self.get_headers(), timeout=10.0)
                response.raise_for_status()
                job_data: dict[str, Any] = response.json()
                state = job_data.get("State", "Unknown")
                self.logger.info("Job {} status: {}", job_id, state)
                return str(state)
        except Exception as exc:
            raise UiPathError(f"Failed to get status for job {job_id}: {exc}") from exc
