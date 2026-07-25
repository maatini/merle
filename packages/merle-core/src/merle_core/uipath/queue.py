"""
UiPath Queue Helper for queue management.
"""

from __future__ import annotations

from typing import Any

import httpx
from loguru import logger

from ..exceptions import QueueItemError
from .orchestrator import UiPathOrchestratorClient


class UiPathQueueHelper:
    """Helper to interact with UiPath Orchestrator Queues."""

    def __init__(self, client: UiPathOrchestratorClient) -> None:
        self.client = client
        self.logger = logger.bind(component="UiPathQueueHelper")

    async def add_queue_item(
        self,
        queue_name: str,
        content: dict[str, Any],
        priority: str = "Normal",
    ) -> dict[str, Any]:
        """
        Add an item to a UiPath Orchestrator Queue.
        """
        url = f"{self.client.base_url}/odata/QueueItems"
        payload = {
            "ItemData": {
                "Name": queue_name,
                "Priority": priority,
                "SpecificContent": content,
            }
        }
        try:
            async with httpx.AsyncClient() as client:
                response = await client.post(
                    url,
                    json=payload,
                    headers=await self.client.get_headers(),
                    timeout=10.0,
                )
                response.raise_for_status()
                result: dict[str, Any] = response.json()
                self.logger.info("Successfully added item to queue '{}'", queue_name)
                return result
        except Exception as exc:
            raise QueueItemError(f"Failed to add item to queue {queue_name}: {exc}") from exc

    async def get_queue_items(
        self,
        queue_name: str,
        filter_query: str | None = None,
    ) -> list[dict[str, Any]]:
        """
        Retrieve items from a UiPath Orchestrator Queue, optionally filtered.
        """
        url = f"{self.client.base_url}/odata/QueueItems"
        params = {"$filter": f"QueueDefinitionName eq '{queue_name}'"}
        if filter_query:
            params["$filter"] += f" and {filter_query}"

        try:
            async with httpx.AsyncClient() as client:
                response = await client.get(
                    url,
                    headers=await self.client.get_headers(),
                    params=params,
                    timeout=10.0,
                )
                response.raise_for_status()
                data: dict[str, Any] = response.json()
                value: list[dict[str, Any]] = data.get("value", [])
                return value
        except Exception as exc:
            raise QueueItemError(f"Failed to retrieve items from queue {queue_name}: {exc}") from exc
