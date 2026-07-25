#!/usr/bin/env python3
"""
Merle UiPath Hybrid Bot — Python + Orchestrator Queue example.

Demonstrates:
- merle_core.uipath.UiPathOrchestratorClient (OAuth + jobs)
- merle_core.uipath.UiPathQueueHelper (queue get / add)
- BaseBot + BaseTask lifecycle
- SIMULATE=true default for local/CI (no real credentials)

Production path (SIMULATE=false):
  export UIPATH_CLIENT_ID=...
  export UIPATH_CLIENT_SECRET=...
  export UIPATH_TENANT=Default
  export UIPATH_BASE_URL=https://cloud.uipath.com
  export SIMULATE=false
  uv run python main.py
"""

from __future__ import annotations

import asyncio
from typing import Any

from loguru import logger

from merle_core import BaseBot, configure_observability
from merle_core.uipath import UiPathOrchestratorClient, UiPathQueueHelper

from config import settings
from tasks import ProcessUiPathQueueTask


def build_orchestrator_client(
    *,
    client_id: str | None = None,
    client_secret: str | None = None,
    tenant: str | None = None,
    base_url: str | None = None,
) -> UiPathOrchestratorClient:
    """Construct a real UiPathOrchestratorClient from settings / overrides."""
    cid = client_id if client_id is not None else settings.uipath_client_id
    secret = client_secret if client_secret is not None else settings.uipath_client_secret
    if not cid or not secret:
        raise ValueError("UIPATH_CLIENT_ID and UIPATH_CLIENT_SECRET are required when SIMULATE=false")
    return UiPathOrchestratorClient(
        client_id=cid,
        client_secret=secret,
        tenant=tenant if tenant is not None else settings.uipath_tenant,
        base_url=base_url if base_url is not None else settings.uipath_base_url,
    )


class UiPathHybridBot(BaseBot):
    """
    Orchestrates queue processing via merle_core UiPath helpers.

    Inject ``queue_helper`` (and optionally ``client``) for tests / mocks.
    When ``settings.simulate`` is True and no helper is injected, the task
    uses in-memory fixtures and never opens HTTP connections.
    """

    def __init__(
        self,
        *,
        queue_helper: UiPathQueueHelper | None = None,
        client: UiPathOrchestratorClient | None = None,
    ) -> None:
        super().__init__(settings, name="uipath-hybrid")
        self._queue_helper = queue_helper
        self._client = client

    async def execute(self) -> dict[str, Any]:
        self.logger.info(
            "Starting UiPath hybrid pipeline (env={}, simulate={})",
            settings.environment,
            settings.simulate,
        )

        queue_helper = self._queue_helper
        client = self._client

        if queue_helper is None and not settings.simulate:
            client = client or build_orchestrator_client()
            await client.authenticate()
            queue_helper = UiPathQueueHelper(client)
            self.logger.info(
                "Authenticated against Orchestrator (tenant={}, base_url={})",
                settings.uipath_tenant,
                settings.uipath_base_url,
            )

        task = ProcessUiPathQueueTask(settings, queue_helper=queue_helper)
        queue_result = await task.run()

        job_result: dict[str, Any] | None = None
        if not settings.simulate and settings.process_key and (client is not None or self._client is not None):
            job_client = client or self._client
            assert job_client is not None
            self.logger.info("Starting UiPath job for process_key={}", settings.process_key)
            job_result = await job_client.start_job(settings.process_key)

        summary: dict[str, Any] = {
            "mode": queue_result.get("mode"),
            "processed_items": queue_result.get("processed_items", 0),
            "results": queue_result.get("results", []),
            "job": job_result,
        }
        return summary

    def _on_success(self, result: dict[str, Any]) -> None:
        self.logger.success(
            "UiPath hybrid completed: mode={}, processed={}",
            result.get("mode"),
            result.get("processed_items"),
        )

    def _on_failure(self, exception: Exception) -> None:
        self.logger.error("UiPath hybrid failed: {}", exception)


async def main() -> None:
    if settings.enable_tracing and configure_observability is not None:
        try:
            configure_observability(
                service_name="merle-uipath-hybrid-bot",
                service_version="0.1.0",
                otlp_endpoint=settings.otlp_endpoint,
                enable_tracing=True,
                enable_metrics=False,
                resource_attributes={"deployment.environment": settings.environment},
            )
        except Exception as e:
            logger.warning("Observability partially disabled: {}", e)

    bot = UiPathHybridBot()
    result = await bot.run()
    logger.info("Final result: {}", result)
    logger.info("Health: {}", bot.health_check())


if __name__ == "__main__":
    asyncio.run(main())
