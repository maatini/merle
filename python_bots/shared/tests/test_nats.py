"""
Tests für das merle_core.nats Modul (Phase 4).

Da ein laufender NATS-Server für echte Integrationstests nötig ist,
fokussieren sich diese Tests vor allem auf:
- Serialisierung / Deserialisierung
- Korrekte Verwendung von TaskSpec / TaskResult
- Verhalten bei fehlender Verbindung
- Mock-Tests für Client-Methoden
"""

from unittest.mock import AsyncMock, MagicMock, patch

import pytest

from merle_core import TaskSpec, TaskResult, TaskStatus
from merle_core.nats import NatsClient, NatsMessage


class TestNatsMessage:
    def test_nats_message_creation(self):
        msg = NatsMessage(subject="tasks.test", data={"foo": "bar"})
        assert msg.subject == "tasks.test"
        assert msg.data == {"foo": "bar"}
        assert msg.reply is None


class TestTaskSerialization:
    """Tests, ob TaskSpec und TaskResult sauber über NATS transportiert werden können."""

    def test_task_spec_roundtrip(self):
        spec = TaskSpec(
            task_id="abc-123",
            task_type="web_scrape",
            payload={"url": "https://example.com"},
            metadata={"priority": "high"},
            retry_policy="browser_retry",
        )

        data = spec.to_dict()
        restored = TaskSpec.from_dict(data)

        assert restored.task_id == spec.task_id
        assert restored.task_type == "web_scrape"
        assert restored.payload["url"] == "https://example.com"

    def test_task_result_roundtrip(self):
        result = TaskResult.success(
            task_id="abc-123",
            result={"items": 42},
            processor="worker-01",
        )

        data = result.to_dict()
        restored = TaskResult.from_dict(data)

        assert restored.status == TaskStatus.SUCCESS
        assert restored.result["items"] == 42


class TestNatsClientBehavior:
    """Mock-basierte Tests für den NatsClient."""

    @pytest.mark.asyncio
    async def test_publish_without_connection_raises(self):
        client = NatsClient()
        with pytest.raises(RuntimeError, match="nicht verbunden"):
            await client.publish("test.subject", {"hello": "world"})

    @pytest.mark.asyncio
    async def test_request_without_connection_raises(self):
        client = NatsClient()
        with pytest.raises(RuntimeError, match="nicht verbunden"):
            await client.request("test.subject", {"hello": "world"})

    @pytest.mark.asyncio
    async def test_publish_task_validates_type(self):
        client = NatsClient()
        # Wir mocken die Verbindung, damit nur der Typ-Check greift
        client._nc = MagicMock()
        client._connected = True

        with pytest.raises(TypeError, match="Erwarte TaskSpec"):
            await client.publish_task("tasks.test", {"not": "a taskspec"})


class TestPullConsumer:
    """Tests für den PullConsumer (meist gemockt)."""

    @pytest.mark.asyncio
    async def test_pull_consumer_fetch_returns_messages(self):
        # Mock eines JetStream Pull Consumers
        mock_js_consumer = MagicMock()
        mock_msg = MagicMock()
        mock_msg.data = b'{"task_id": "123", "task_type": "test"}'
        mock_msg.subject = "tasks.test"
        mock_msg.reply = None

        mock_js_consumer.fetch = AsyncMock(return_value=[mock_msg])

        consumer = PullConsumer(mock_js_consumer, MagicMock())
        messages = await consumer.fetch(batch=1)

        assert len(messages) == 1
        assert messages[0].data["task_id"] == "123"


# Hinweis für echte Integrationstests:
# Man kann später einen Fixture bauen, der NATS in Docker startet
# oder Tests mit pytest.mark.skipif überspringt, wenn kein NATS verfügbar ist.
