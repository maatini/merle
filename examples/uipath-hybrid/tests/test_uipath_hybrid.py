"""
Unit tests for the UiPath hybrid example (no real Orchestrator).

- Simulate mode uses fixtures
- Live path uses mocked UiPathQueueHelper / client methods
"""

from __future__ import annotations

import sys
from pathlib import Path
from typing import Any
from unittest.mock import AsyncMock, MagicMock

import pytest

# Isolate this example's modules from other examples/* (shared names: config, main, tasks)
_EXAMPLE_ROOT = Path(__file__).resolve().parent.parent
for _key in list(sys.modules):
    if _key in ("config", "main", "tasks") or _key.startswith("tasks."):
        del sys.modules[_key]
sys.path = [p for p in sys.path if Path(p).resolve() != _EXAMPLE_ROOT]
sys.path.insert(0, str(_EXAMPLE_ROOT))

from config import UiPathHybridSettings  # noqa: E402
from main import UiPathHybridBot, build_orchestrator_client  # noqa: E402
from tasks import ProcessUiPathQueueTask  # noqa: E402
from tasks.process_queue import process_item_content  # noqa: E402


@pytest.fixture
def simulate_settings() -> UiPathHybridSettings:
    return UiPathHybridSettings(
        bot_name="uipath-hybrid-test",
        environment="dev",
        simulate=True,
        queue_name="InvoiceQueue",
        result_queue_name="InvoiceResultsQueue",
        enable_tracing=False,
    )


@pytest.fixture
def live_settings() -> UiPathHybridSettings:
    return UiPathHybridSettings(
        bot_name="uipath-hybrid-test",
        environment="dev",
        simulate=False,
        queue_name="InvoiceQueue",
        result_queue_name="InvoiceResultsQueue",
        uipath_client_id="test-client-id",
        uipath_client_secret="test-client-secret",
        uipath_tenant="Default",
        uipath_base_url="https://cloud.uipath.com",
        enable_tracing=False,
    )


def test_process_item_content_approval_threshold() -> None:
    approved = process_item_content({"invoice_id": "INV-1", "amount": 100.0, "vendor": "A"})
    rejected = process_item_content({"invoice_id": "INV-2", "amount": 5000.0, "vendor": "B"})
    assert approved["status"] == "processed"
    assert approved["approved"] is True
    assert rejected["approved"] is False


@pytest.mark.asyncio
async def test_process_queue_simulate_mode(simulate_settings: UiPathHybridSettings) -> None:
    task = ProcessUiPathQueueTask(simulate_settings)
    result = await task.run()

    assert result["status"] == "success"
    assert result["mode"] == "simulate"
    assert result["processed_items"] == 3
    assert len(result["results"]) == 3
    assert result["results"][0]["invoice_id"] == "INV-2026-001"
    assert result["results"][0]["source_queue_item_id"] == 1001


@pytest.mark.asyncio
async def test_process_queue_with_mock_helper(live_settings: UiPathHybridSettings) -> None:
    mock_items: list[dict[str, Any]] = [
        {
            "Id": 42,
            "SpecificContent": {
                "invoice_id": "INV-MOCK-1",
                "amount": 99.0,
                "vendor": "Mock Vendor",
            },
        }
    ]
    helper = MagicMock()
    helper.get_queue_items = AsyncMock(return_value=mock_items)
    helper.add_queue_item = AsyncMock(return_value={"Id": 99})

    task = ProcessUiPathQueueTask(live_settings, queue_helper=helper)
    result = await task.run()

    assert result["mode"] == "live"
    assert result["processed_items"] == 1
    assert result["results"][0]["invoice_id"] == "INV-MOCK-1"
    assert result["results"][0]["source_queue_item_id"] == 42
    helper.get_queue_items.assert_awaited_once_with("InvoiceQueue")
    helper.add_queue_item.assert_awaited_once()
    call_args = helper.add_queue_item.await_args
    assert call_args.args[0] == "InvoiceResultsQueue"
    assert call_args.args[1]["invoice_id"] == "INV-MOCK-1"


@pytest.mark.asyncio
async def test_process_queue_requires_helper_when_not_simulate(
    live_settings: UiPathHybridSettings,
) -> None:
    task = ProcessUiPathQueueTask(live_settings, queue_helper=None)
    with pytest.raises(ValueError, match="queue_helper is required"):
        await task.run()


@pytest.mark.asyncio
async def test_bot_pipeline_simulate(
    simulate_settings: UiPathHybridSettings,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    import config as config_mod
    import main as main_mod

    monkeypatch.setattr(config_mod, "settings", simulate_settings)
    monkeypatch.setattr(main_mod, "settings", simulate_settings)

    bot = UiPathHybridBot()
    result = await bot.run()

    assert result["mode"] == "simulate"
    assert result["processed_items"] == 3
    assert bot.status == "success"
    health = bot.health_check()
    assert health["status"] == "healthy"


@pytest.mark.asyncio
async def test_bot_pipeline_with_injected_helper(
    live_settings: UiPathHybridSettings,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    import config as config_mod
    import main as main_mod

    monkeypatch.setattr(config_mod, "settings", live_settings)
    monkeypatch.setattr(main_mod, "settings", live_settings)

    helper = MagicMock()
    helper.get_queue_items = AsyncMock(
        return_value=[
            {
                "Id": 7,
                "SpecificContent": {
                    "invoice_id": "INV-LIVE-7",
                    "amount": 10.0,
                    "vendor": "X",
                },
            }
        ]
    )
    helper.add_queue_item = AsyncMock(return_value={"Id": 8})

    bot = UiPathHybridBot(queue_helper=helper)
    result = await bot.run()

    assert result["mode"] == "live"
    assert result["processed_items"] == 1
    assert result["results"][0]["invoice_id"] == "INV-LIVE-7"
    helper.get_queue_items.assert_awaited_once()
    helper.add_queue_item.assert_awaited_once()


def test_build_orchestrator_client_requires_credentials(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    import main as main_mod
    from config import UiPathHybridSettings

    empty = UiPathHybridSettings(
        simulate=False,
        uipath_client_id="",
        uipath_client_secret="",
    )
    monkeypatch.setattr(main_mod, "settings", empty)
    with pytest.raises(ValueError, match="UIPATH_CLIENT_ID"):
        build_orchestrator_client()


def test_build_orchestrator_client_from_args() -> None:
    client = build_orchestrator_client(
        client_id="id",
        client_secret="secret",
        tenant="MyTenant",
        base_url="https://orch.example.com/",
    )
    assert client.client_id == "id"
    assert client.tenant == "MyTenant"
    assert client.base_url == "https://orch.example.com"
