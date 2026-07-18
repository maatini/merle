"""
Mocked unit tests for merle_core.http_client.RpaHttpClient.
No real network — uses httpx.MockTransport.
"""

from __future__ import annotations

import httpx
import pytest

from merle_core.http_client import RpaHttpClient


def _patch_async_client(monkeypatch, transport: httpx.MockTransport) -> None:
    class _PatchedAsyncClient(httpx.AsyncClient):
        def __init__(self, *args, **kwargs):
            kwargs["transport"] = transport
            super().__init__(*args, **kwargs)

    monkeypatch.setattr("merle_core.http_client.httpx.AsyncClient", _PatchedAsyncClient)


@pytest.mark.asyncio
async def test_get_success_with_mock_transport(monkeypatch):
    def handler(request: httpx.Request) -> httpx.Response:
        assert request.method == "GET"
        assert request.url.path == "/items"
        assert request.headers.get("Authorization") == "Bearer secret-key"
        assert request.headers.get("User-Agent") == "RPA-Hybrid-Bot/1.0"
        return httpx.Response(200, json={"items": [1, 2, 3]})

    transport = httpx.MockTransport(handler)
    _patch_async_client(monkeypatch, transport)

    client = RpaHttpClient(base_url="https://api.example.com", api_key="secret-key")
    result = await client.get("/items")
    assert result == {"items": [1, 2, 3]}


@pytest.mark.asyncio
async def test_post_success_with_mock_transport(monkeypatch):
    def handler(request: httpx.Request) -> httpx.Response:
        assert request.method == "POST"
        assert request.url.path == "/create"
        body = request.read()
        assert b"hello" in body
        return httpx.Response(201, json={"id": 42, "ok": True})

    transport = httpx.MockTransport(handler)
    _patch_async_client(monkeypatch, transport)

    client = RpaHttpClient(base_url="https://api.example.com/")
    result = await client.post("/create", {"msg": "hello"})
    assert result["id"] == 42
    assert result["ok"] is True


@pytest.mark.asyncio
async def test_get_retries_on_http_status_error(monkeypatch):
    from tenacity import wait_none

    calls = {"n": 0}

    def handler(request: httpx.Request) -> httpx.Response:
        calls["n"] += 1
        if calls["n"] < 3:
            return httpx.Response(503, json={"error": "busy"})
        return httpx.Response(200, json={"status": "ok"})

    transport = httpx.MockTransport(handler)
    _patch_async_client(monkeypatch, transport)

    client = RpaHttpClient(base_url="https://api.example.com", timeout=2.0)
    client.get.retry.wait = wait_none()  # type: ignore[attr-defined]

    result = await client.get("/health")
    assert result == {"status": "ok"}
    assert calls["n"] == 3


@pytest.mark.asyncio
async def test_get_raises_after_retries_exhausted(monkeypatch):
    from tenacity import wait_none

    def handler(request: httpx.Request) -> httpx.Response:
        return httpx.Response(500, json={"error": "fail"})

    transport = httpx.MockTransport(handler)
    _patch_async_client(monkeypatch, transport)

    client = RpaHttpClient(base_url="https://api.example.com")
    client.get.retry.wait = wait_none()  # type: ignore[attr-defined]

    # tenacity default (no reraise) wraps final HTTPStatusError in RetryError
    from tenacity import RetryError

    with pytest.raises((httpx.HTTPStatusError, RetryError)):
        await client.get("/boom")


def test_headers_without_api_key():
    client = RpaHttpClient(base_url="https://api.example.com")
    headers = client._headers()
    assert "Authorization" not in headers
    assert headers["Accept"] == "application/json"


def test_headers_with_api_key():
    client = RpaHttpClient(base_url="https://api.example.com", api_key="tok")
    headers = client._headers()
    assert headers["Authorization"] == "Bearer tok"
