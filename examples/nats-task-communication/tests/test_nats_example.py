"""
Unit tests for NATS task communication example.

No live NATS server required — TaskSpec/TaskResult roundtrips and mocked client.
"""

from __future__ import annotations

import json
from pathlib import Path
import sys
from unittest.mock import AsyncMock, MagicMock

import pytest

_EXAMPLE_ROOT = Path(__file__).resolve().parent.parent
for _key in list(sys.modules):
    if _key in ("config", "main", "tasks") or _key.startswith("tasks."):
        del sys.modules[_key]
sys.path = [p for p in sys.path if Path(p).resolve() != _EXAMPLE_ROOT]
sys.path.insert(0, str(_EXAMPLE_ROOT))

from merle_core import TaskResult, TaskSpec, TaskStatus  # noqa: E402
from merle_core.nats import NatsClient, NatsMessage  # noqa: E402
from tasks import build_scrape_spec, build_success_result, handle_scrape_spec  # noqa: E402


class TestTaskSpecRoundtrip:
    def test_build_scrape_spec_roundtrip(self) -> None:
        spec = build_scrape_spec(
            "https://example.com",
            selectors=[".title"],
            task_id="fixed-id",
        )
        data = spec.to_dict()
        restored = TaskSpec.from_dict(data)

        assert restored.task_id == "fixed-id"
        assert restored.task_type == "web_scrape"
        assert restored.payload["url"] == "https://example.com"
        assert restored.payload["selectors"] == [".title"]
        # JSON-safe for NATS transport
        assert json.loads(json.dumps(data))["task_id"] == "fixed-id"

    def test_task_result_roundtrip(self) -> None:
        result = build_success_result("abc-123", records=7)
        data = result.to_dict()
        restored = TaskResult.from_dict(data)

        assert restored.status == TaskStatus.SUCCESS
        assert restored.result is not None
        assert restored.result["records"] == 7
        assert restored.metadata.get("processor") == "data-processor-bot"


class TestProcessorPure:
    def test_handle_scrape_spec(self) -> None:
        spec = build_scrape_spec("https://shop.example", selectors=["a", "b"])
        result = handle_scrape_spec(spec)

        assert result.task_id == spec.task_id
        assert result.status == TaskStatus.SUCCESS
        assert result.result is not None
        assert result.result["processed"] is True
        assert result.result["records"] == 12  # 2 selectors * 6
        assert result.result["url"] == "https://shop.example"


def _connected_client() -> NatsClient:
    client = NatsClient(servers="nats://fake:4222", name="test")
    client._nc = AsyncMock()
    client._js = AsyncMock()
    client._connected = True
    return client


class TestNatsClientMocked:
    @pytest.mark.asyncio
    async def test_publish_scrape_spec(self) -> None:
        client = _connected_client()
        spec = build_scrape_spec("https://example.com", task_id="t-1")

        await client.publish("tasks.web_scrape", spec.to_dict())

        client._nc.publish.assert_awaited()  # type: ignore[union-attr]
        call_args = client._nc.publish.await_args  # type: ignore[union-attr]
        subject = call_args.args[0]
        payload = json.loads(call_args.args[1].decode())
        assert subject == "tasks.web_scrape"
        assert payload["task_id"] == "t-1"

    @pytest.mark.asyncio
    async def test_subscribe_handler_receives_nats_message(self) -> None:
        client = _connected_client()
        received: list[NatsMessage] = []

        async def handler(msg: NatsMessage) -> None:
            received.append(msg)

        # Capture the wrapped callback passed to nc.subscribe
        async def fake_subscribe(subject: str, queue: str | None = None, cb=None):  # type: ignore[no-untyped-def]
            raw = MagicMock()
            raw.data = json.dumps({"task_id": "x", "task_type": "web_scrape", "payload": {}}).encode()
            raw.subject = subject
            raw.reply = None
            raw.headers = None
            assert cb is not None
            await cb(raw)

        client._nc.subscribe = fake_subscribe  # type: ignore[method-assign]

        await client.subscribe("tasks.web_scrape", handler)

        assert len(received) == 1
        assert received[0].data["task_id"] == "x"

    @pytest.mark.asyncio
    async def test_end_to_end_handler_logic(self) -> None:
        """Processor logic over a deserialised NATS payload (no broker)."""
        spec = build_scrape_spec("https://example.com", task_id="e2e-1")
        wire = spec.to_dict()
        msg = NatsMessage(subject="tasks.web_scrape", data=wire, reply="inbox.1")

        restored = TaskSpec.from_dict(msg.data)
        result = handle_scrape_spec(restored)

        assert result.task_id == "e2e-1"
        assert result.to_dict()["status"] == "success"
