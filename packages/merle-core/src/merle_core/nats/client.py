"""
Einfacher, robuster NATS Client für Merle (Phase 4 – A1 Variante).

Fokus liegt auf Einfachheit und guter Integration mit dem bestehenden
Retry- und Task-System.
"""

from __future__ import annotations

import asyncio
import json
from dataclasses import dataclass
from typing import TYPE_CHECKING, Any, Awaitable, Callable

from loguru import logger

from ..retry import default_http_retry, with_retry

if TYPE_CHECKING:
    from ..task import TaskResult, TaskSpec


@dataclass
class NatsMessage:
    """Repräsentiert eine empfangene NATS-Nachricht."""

    subject: str
    data: dict[str, Any]
    reply: str | None = None
    headers: dict[str, str] | None = None


class NatsClient:
    """
    Einfacher NATS Client mit guten Defaults für RPA-Use-Cases.

    Unterstützt:
    - Publish / Subscribe
    - Request / Reply (empfohlen für Tasks)
    - Automatische JSON (De-)Serialisierung
    - Integration mit merle_core.retry
    """

    def __init__(
        self,
        servers: str | list[str] = "nats://localhost:4222",
        name: str = "merle-bot",
        connect_timeout: float = 10.0,
        max_reconnects: int = 10,
        reconnect_time_wait: float = 2.0,
        retry_policy: Any = None,  # aus merle_core.retry
    ):
        self.servers = servers if isinstance(servers, list) else [servers]
        self.name = name
        self.connect_timeout = connect_timeout
        self.max_reconnects = max_reconnects
        self.reconnect_time_wait = reconnect_time_wait
        self.retry_policy = retry_policy or default_http_retry

        self._nc = None
        self._js = None  # JetStream context
        self._connected = False

    async def connect(self) -> None:
        """Stellt die Verbindung zu NATS her (mit Reconnect-Logik)."""
        try:
            import nats
        except ImportError as e:
            raise ImportError('NATS-Unterstützung erfordert das Extra: uv add "merle-core[nats]"') from e

        self._nc = await nats.connect(
            servers=self.servers,
            name=self.name,
            connect_timeout=self.connect_timeout,
            max_reconnect_attempts=self.max_reconnects,
            reconnect_time_wait=self.reconnect_time_wait,
            error_cb=self._error_callback,
            disconnected_cb=self._disconnected_callback,
            reconnected_cb=self._reconnected_callback,
        )

        self._js = self._nc.jetstream()
        self._connected = True

        logger.info("Verbunden mit NATS: {} (JetStream enabled)", self.servers)

    @property
    def jetstream(self) -> Any:
        """Gibt den JetStream Context zurück (für fortgeschrittene Nutzung)."""
        if not self._js:
            raise RuntimeError("JetStream ist nicht initialisiert (nicht verbunden?)")
        return self._js

    async def close(self) -> None:
        if self._nc:
            await self._nc.close()
            logger.info("NATS Verbindung geschlossen")

    async def __aenter__(self) -> "NatsClient":
        await self.connect()
        return self

    async def __aexit__(self, exc_type: Any, exc_val: Any, exc_tb: Any) -> None:
        await self.close()

    # ─────────────────────────────────────────────────────────────
    # Publish / Subscribe
    # ─────────────────────────────────────────────────────────────

    @with_retry(policy=default_http_retry)
    async def publish(self, subject: str, data: dict[str, Any], headers: dict | None = None) -> None:
        """Sendet eine Nachricht an ein Subject (mit Retry)."""
        if not self._nc or not self._connected:
            raise RuntimeError("NATS Client ist nicht verbunden")

        payload = json.dumps(data).encode()
        await self._nc.publish(subject, payload, headers=headers)
        logger.debug("Published to {}: {} keys", subject, len(data))

    async def subscribe(
        self,
        subject: str,
        handler: Callable[[NatsMessage], Awaitable[None]],
        queue: str | None = None,
    ):
        """
        Abonniert ein Subject.

        Args:
            subject: NATS Subject (kann Wildcards enthalten)
            handler: Async-Funktion, die eine NatsMessage erhält
            queue: Optionaler Queue-Group-Name für Load Balancing
        """
        if not self._nc:
            raise RuntimeError("NATS Client ist nicht verbunden")

        async def _wrapped(msg):
            try:
                data = json.loads(msg.data.decode())
                nats_msg = NatsMessage(
                    subject=msg.subject,
                    data=data,
                    reply=msg.reply,
                    headers=dict(msg.headers) if msg.headers else None,
                )
                await handler(nats_msg)
            except Exception as e:
                logger.exception("Fehler beim Verarbeiten der Nachricht auf {}: {}", subject, e)

        await self._nc.subscribe(subject, queue=queue, cb=_wrapped)
        logger.info("Subscribed to subject: {} (queue={})", subject, queue)

    # ─────────────────────────────────────────────────────────────
    # Request / Reply (empfohlen für Tasks)
    # ─────────────────────────────────────────────────────────────

    @with_retry(policy=default_http_retry)
    async def request(
        self,
        subject: str,
        data: dict[str, Any],
        timeout: float = 30.0,
    ) -> NatsMessage:
        """
        Sendet eine Request-Nachricht und wartet auf eine Antwort (mit Retry).

        Sehr nützlich für synchrone Task-Kommunikation.
        """
        if not self._nc or not self._connected:
            raise RuntimeError("NATS Client ist nicht verbunden")

        payload = json.dumps(data).encode()
        msg = await self._nc.request(subject, payload, timeout=timeout)

        response_data = json.loads(msg.data.decode())
        return NatsMessage(
            subject=msg.subject,
            data=response_data,
            reply=msg.reply,
            headers=dict(msg.headers) if msg.headers else None,
        )

    async def reply(self, subject: str, data: dict[str, Any]) -> None:
        """Sendet eine Antwort (wird meist innerhalb eines Request-Handlers genutzt)."""
        await self.publish(subject, data)

    # ─────────────────────────────────────────────────────────────
    # Task-spezifische Convenience-Methoden (Phase 4)
    # ─────────────────────────────────────────────────────────────

    async def publish_task(self, subject: str, task_spec: "TaskSpec") -> None:
        """Veröffentlicht eine TaskSpec auf einem Subject."""
        from ..task import TaskSpec

        if not isinstance(task_spec, TaskSpec):
            raise TypeError("Erwarte TaskSpec")
        await self.publish(subject, task_spec.to_dict())

    async def publish_to_stream(
        self,
        stream: str,
        subject: str,
        data: dict[str, Any],
    ) -> int | None:
        """
        Veröffentlicht eine Nachricht in einen JetStream Stream.
        Gibt die Stream Sequence Number zurück (falls verfügbar).
        """
        if not self._js:
            raise RuntimeError("JetStream nicht verfügbar")

        payload = json.dumps(data).encode()
        ack = await self._js.publish(subject, payload)
        logger.debug("Message an Stream '{}' gepusht (seq={})", stream, ack.seq)
        return ack.seq

    async def request_task(
        self,
        subject: str,
        task_spec: "TaskSpec",
        timeout: float = 60.0,
    ) -> "TaskResult":
        """Führt eine Task via Request/Reply aus und gibt TaskResult zurück."""
        if not isinstance(task_spec, TaskSpec):  # type: ignore[name-defined]
            raise TypeError("Erwarte TaskSpec")

        response = await self.request(subject, task_spec.to_dict(), timeout=timeout)
        return TaskResult.from_dict(response.data)  # type: ignore[attr-defined]

    # ─────────────────────────────────────────────────────────────
    # Callbacks
    # ─────────────────────────────────────────────────────────────

    async def _error_callback(self, e: Exception) -> None:
        logger.error("NATS Error: {}", e)

    async def _disconnected_callback(self) -> None:
        self._connected = False
        logger.warning("NATS Verbindung unterbrochen")

    async def _reconnected_callback(self) -> None:
        self._connected = True
        logger.info("NATS Verbindung wiederhergestellt")

    # ─────────────────────────────────────────────────────────────
    # JetStream Pull Consumer (wichtig für zuverlässige Task-Verarbeitung)
    # ─────────────────────────────────────────────────────────────

    async def create_pull_consumer(
        self,
        stream: str,
        durable: str,
        *,
        max_deliver: int = 5,
        ack_wait: int = 60,
        filter_subject: str | None = None,
        description: str | None = None,
    ) -> "PullConsumer":
        """
        Erstellt (oder holt) einen Pull-Consumer für einen JetStream Stream.

        Das ist die empfohlene Art, Tasks zuverlässig zu konsumieren.
        """
        if not self._js:
            raise RuntimeError("JetStream nicht verfügbar")

        config = {
            "durable_name": durable,
            "max_deliver": max_deliver,
            "ack_wait": ack_wait * 1_000_000_000,  # in Nanosekunden
            "description": description or f"Merle Consumer for stream {stream}",
        }

        if filter_subject:
            config["filter_subject"] = filter_subject

        try:
            consumer = await self._js.pull_subscribe(
                subject=filter_subject or f"{stream}.>",
                durable=durable,
                stream=stream,
                config=config,
            )
            logger.info("Pull Consumer erstellt: stream={}, durable={}", stream, durable)
            return PullConsumer(consumer, self)
        except Exception as e:
            logger.error("Fehler beim Erstellen des Consumers: {}", e)
            raise

    async def consume_tasks(
        self,
        stream: str,
        durable: str,
        *,
        max_deliver: int = 5,
        ack_wait: int = 60,
        batch: int = 5,
        timeout: float = 5.0,
    ) -> None:
        """
        High-Level Generator, der direkt TaskSpec-Objekte liefert.

        Sehr praktisch für Worker, die Tasks aus NATS konsumieren wollen.
        """
        consumer = await self.create_pull_consumer(
            stream=stream,
            durable=durable,
            max_deliver=max_deliver,
            ack_wait=ack_wait,
        )

        from ..task import TaskSpec

        async for nats_msg in consumer.messages(batch=batch, timeout=timeout):
            try:
                task_spec = TaskSpec.from_dict(nats_msg.data)
                yield task_spec, nats_msg
            except Exception as e:
                logger.exception("Konnte TaskSpec nicht deserialisieren: {}", e)
                await consumer.nak(nats_msg)


class PullConsumer:
    """
    Wrapper um einen JetStream Pull Consumer mit praktischen Methoden.
    """

    def __init__(self, js_consumer: Any, client: NatsClient) -> None:
        self._consumer = js_consumer
        self._client = client

    async def fetch(self, batch: int = 1, timeout: float = 5.0) -> list[NatsMessage]:
        """Holt eine bestimmte Anzahl an Nachrichten (Pull)."""
        try:
            msgs = await self._consumer.fetch(batch=batch, timeout=timeout)
            result = []
            for msg in msgs:
                try:
                    data = json.loads(msg.data.decode())
                    result.append(
                        NatsMessage(
                            subject=msg.subject,
                            data=data,
                            reply=msg.reply,
                        )
                    )
                    # Wir merken uns die Original-Nachricht für Ack
                    result[-1]._raw_msg = msg  # type: ignore
                except Exception as e:
                    logger.exception("Fehler beim Parsen einer NATS-Nachricht: {}", e)
                    await msg.nak()
            return result
        except asyncio.TimeoutError:
            return []

    async def ack(self, message: NatsMessage) -> None:
        """Bestätigt eine Nachricht erfolgreich."""
        if hasattr(message, "_raw_msg"):
            await message._raw_msg.ack()  # type: ignore

    async def nak(self, message: NatsMessage, delay: int | None = None) -> None:
        """Weist eine Nachricht zurück (mit optionaler Verzögerung)."""
        if hasattr(message, "_raw_msg"):
            await message._raw_msg.nak(delay=delay)

    async def term(self, message: NatsMessage) -> None:
        """Beendet eine Nachricht endgültig (Dead Letter)."""
        if hasattr(message, "_raw_msg"):
            await message._raw_msg.term()

    async def messages(self, batch: int = 10, timeout: float = 5.0) -> Any:
        """
        Asynchroner Generator, der Nachrichten liefert.
        Der Consumer muss die Nachricht selbst acken/naken.
        """
        while True:
            msgs = await self.fetch(batch=batch, timeout=timeout)
            for msg in msgs:
                yield msg
            if not msgs:
                await asyncio.sleep(0.2)
