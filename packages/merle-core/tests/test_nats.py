"""
Tests für das merle_core.nats Modul (Phase 4).

Da ein laufender NATS-Server für echte Integrationstests nötig ist,
fokussieren sich diese Tests vor allem auf:
- Serialisierung / Deserialisierung
- Korrekte Verwendung von TaskSpec / TaskResult
- Verhalten bei fehlender Verbindung
- Mock-Tests für Client-Methoden (Fake nc/js, no real NATS)
"""

import json
from unittest.mock import AsyncMock, MagicMock, patch

import pytest

from merle_core import TaskResult, TaskSpec, TaskStatus
from merle_core.nats import NatsClient, NatsMessage, PullConsumer


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


def _connected_client() -> NatsClient:
    """NatsClient with fake nc/js already attached (no real network)."""
    client = NatsClient(servers="nats://fake:4222", name="test-bot")
    client._nc = AsyncMock()
    client._js = AsyncMock()
    client._connected = True
    return client


class TestNatsClientBehavior:
    """Mock-basierte Tests für den NatsClient."""

    @pytest.mark.asyncio
    async def test_publish_without_connection_raises(self):
        from merle_core.exceptions import RetryExhaustedError

        client = NatsClient()
        # publish is @with_retry — non-connection RuntimeError becomes RetryExhaustedError
        with pytest.raises((RuntimeError, RetryExhaustedError), match=r"nicht verbunden|Retry exhausted"):
            await client.publish("test.subject", {"hello": "world"})

    @pytest.mark.asyncio
    async def test_request_without_connection_raises(self):
        from merle_core.exceptions import RetryExhaustedError

        client = NatsClient()
        with pytest.raises((RuntimeError, RetryExhaustedError), match=r"nicht verbunden|Retry exhausted"):
            await client.request("test.subject", {"hello": "world"})

    @pytest.mark.asyncio
    async def test_publish_task_validates_type(self):
        client = NatsClient()
        # Wir mocken die Verbindung, damit nur der Typ-Check greift
        client._nc = MagicMock()
        client._connected = True

        with pytest.raises(TypeError, match="Erwarte TaskSpec"):
            await client.publish_task("tasks.test", {"not": "a taskspec"})

    @pytest.mark.asyncio
    async def test_connect_raises_import_error_when_nats_missing(self):
        client = NatsClient()
        # None in sys.modules makes `import nats` raise ImportError/ModuleNotFoundError
        with patch.dict("sys.modules", {"nats": None}):
            with pytest.raises(ImportError, match="merle-core\\[nats\\]"):
                await client.connect()

    @pytest.mark.asyncio
    async def test_connect_sets_jetstream(self):
        client = NatsClient(servers=["nats://localhost:4222"])
        fake_js = MagicMock()
        # jetstream() is sync on real nats client — use MagicMock, not AsyncMock
        fake_nc = MagicMock()
        fake_nc.jetstream.return_value = fake_js

        fake_nats_mod = MagicMock()
        fake_nats_mod.connect = AsyncMock(return_value=fake_nc)

        with patch.dict("sys.modules", {"nats": fake_nats_mod}):
            await client.connect()

        assert client._connected is True
        assert client._js is fake_js
        fake_nats_mod.connect.assert_awaited()

    @pytest.mark.asyncio
    async def test_publish_json_payload(self):
        client = _connected_client()
        await client.publish("tasks.demo", {"hello": "world"}, headers={"x": "1"})

        client._nc.publish.assert_awaited_once()
        args, kwargs = client._nc.publish.await_args
        assert args[0] == "tasks.demo"
        assert json.loads(args[1].decode()) == {"hello": "world"}
        assert kwargs.get("headers") == {"x": "1"}

    @pytest.mark.asyncio
    async def test_subscribe_invokes_handler_with_nats_message(self):
        client = _connected_client()
        received: list[NatsMessage] = []

        async def handler(msg: NatsMessage) -> None:
            received.append(msg)

        # Capture the cb passed to nc.subscribe
        async def fake_subscribe(subject, queue=None, cb=None):
            raw = MagicMock()
            raw.data = json.dumps({"k": "v"}).encode()
            raw.subject = subject
            raw.reply = "inbox.1"
            raw.headers = {"h": "1"}
            await cb(raw)

        client._nc.subscribe = AsyncMock(side_effect=fake_subscribe)
        await client.subscribe("tasks.>", handler, queue="workers")

        assert len(received) == 1
        assert received[0].data == {"k": "v"}
        assert received[0].subject == "tasks.>"
        assert received[0].reply == "inbox.1"

    @pytest.mark.asyncio
    async def test_subscribe_without_connection_raises(self):
        client = NatsClient()

        async def handler(_msg):
            pass

        with pytest.raises(RuntimeError, match="nicht verbunden"):
            await client.subscribe("x", handler)

    @pytest.mark.asyncio
    async def test_request_returns_nats_message(self):
        client = _connected_client()
        raw = MagicMock()
        raw.data = json.dumps({"answer": 42}).encode()
        raw.subject = "tasks.reply"
        raw.reply = None
        raw.headers = None
        client._nc.request = AsyncMock(return_value=raw)

        msg = await client.request("tasks.ask", {"q": 1}, timeout=1.0)
        assert msg.data["answer"] == 42
        assert msg.subject == "tasks.reply"

    @pytest.mark.asyncio
    async def test_publish_task_and_request_task(self):
        client = _connected_client()
        spec = TaskSpec(task_id="t1", task_type="demo", payload={"a": 1})

        await client.publish_task("tasks.in", spec)
        published = json.loads(client._nc.publish.await_args[0][1].decode())
        assert published["task_id"] == "t1"

        result = TaskResult.success(task_id="t1", result={"ok": True}, processor="w1")
        raw = MagicMock()
        raw.data = json.dumps(result.to_dict()).encode()
        raw.subject = "tasks.out"
        raw.reply = None
        raw.headers = None
        client._nc.request = AsyncMock(return_value=raw)

        tr = await client.request_task("tasks.out", spec, timeout=2.0)
        assert tr.status == TaskStatus.SUCCESS
        assert tr.result["ok"] is True

    @pytest.mark.asyncio
    async def test_publish_to_stream(self):
        client = _connected_client()
        ack = MagicMock()
        ack.seq = 7
        client._js.publish = AsyncMock(return_value=ack)

        seq = await client.publish_to_stream("TASKS", "tasks.new", {"x": 1})
        assert seq == 7

    @pytest.mark.asyncio
    async def test_publish_to_stream_without_js_raises(self):
        client = NatsClient()
        with pytest.raises(RuntimeError, match="JetStream"):
            await client.publish_to_stream("S", "s.x", {})

    @pytest.mark.asyncio
    async def test_jetstream_property_requires_connection(self):
        client = NatsClient()
        with pytest.raises(RuntimeError, match="JetStream"):
            _ = client.jetstream

    @pytest.mark.asyncio
    async def test_close_and_callbacks(self):
        client = _connected_client()
        await client.close()
        client._nc.close.assert_awaited_once()

        await client._error_callback(RuntimeError("boom"))
        await client._disconnected_callback()
        assert client._connected is False
        await client._reconnected_callback()
        assert client._connected is True

    @pytest.mark.asyncio
    async def test_create_pull_consumer(self):
        client = _connected_client()
        fake_consumer = MagicMock()
        client._js.pull_subscribe = AsyncMock(return_value=fake_consumer)

        pc = await client.create_pull_consumer(
            stream="TASKS",
            durable="worker-1",
            filter_subject="tasks.>",
        )
        assert isinstance(pc, PullConsumer)
        client._js.pull_subscribe.assert_awaited_once()

    @pytest.mark.asyncio
    async def test_context_manager(self):
        client = NatsClient()
        client.connect = AsyncMock()
        client.close = AsyncMock()

        async with client:
            client.connect.assert_awaited_once()
        client.close.assert_awaited_once()


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

    @pytest.mark.asyncio
    async def test_pull_consumer_fetch_timeout_returns_empty(self):
        mock_js_consumer = MagicMock()
        mock_js_consumer.fetch = AsyncMock(side_effect=TimeoutError())

        consumer = PullConsumer(mock_js_consumer, MagicMock())
        # asyncio.TimeoutError is alias of TimeoutError in 3.11+

        mock_js_consumer.fetch = AsyncMock(side_effect=TimeoutError())
        messages = await consumer.fetch(batch=1, timeout=0.1)
        assert messages == []

    @pytest.mark.asyncio
    async def test_ack_nak_term(self):
        mock_js_consumer = MagicMock()
        consumer = PullConsumer(mock_js_consumer, MagicMock())
        msg = NatsMessage(subject="s", data={"a": 1})
        raw = AsyncMock()
        msg._raw_msg = raw  # type: ignore[attr-defined]

        await consumer.ack(msg)
        raw.ack.assert_awaited_once()

        await consumer.nak(msg, delay=2)
        raw.nak.assert_awaited_once_with(delay=2)

        await consumer.term(msg)
        raw.term.assert_awaited_once()

    @pytest.mark.asyncio
    async def test_fetch_naks_unparseable_messages(self):
        mock_js_consumer = MagicMock()
        bad = MagicMock()
        bad.data = b"not-json"
        bad.subject = "tasks.bad"
        bad.reply = None
        bad.nak = AsyncMock()
        mock_js_consumer.fetch = AsyncMock(return_value=[bad])

        consumer = PullConsumer(mock_js_consumer, MagicMock())
        messages = await consumer.fetch(batch=1)
        assert messages == []
        bad.nak.assert_awaited_once()


# Hinweis für echte Integrationstests:
# Man kann später einen Fixture bauen, der NATS in Docker startet
# oder Tests mit pytest.mark.skipif überspringt, wenn kein NATS verfügbar ist.
