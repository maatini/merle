"""
Unit tests for the UiPath integration utilities (Orchestrator client and Queue helpers).
"""

from __future__ import annotations

from unittest.mock import AsyncMock, MagicMock, patch
import pytest

from merle_core.uipath import UiPathOrchestratorClient, UiPathQueueHelper
from merle_core.exceptions import UiPathError, QueueItemError


@pytest.mark.asyncio
async def test_uipath_orchestrator_client_authenticate_success():
    """Test successful Orchestrator authentication."""
    client = UiPathOrchestratorClient(client_id="id", client_secret="secret")

    mock_response = MagicMock()
    mock_response.status_code = 200
    mock_response.json.return_value = {"access_token": "token123"}
    mock_response.raise_for_status = MagicMock()

    with patch("httpx.AsyncClient.post", new_callable=AsyncMock, return_value=mock_response) as mock_post:
        token = await client.authenticate()
        assert token == "token123"
        assert client.access_token == "token123"
        mock_post.assert_called_once()


@pytest.mark.asyncio
async def test_uipath_orchestrator_client_start_job_success():
    """Test starting a job successfully in UiPath."""
    client = UiPathOrchestratorClient(client_id="id", client_secret="secret")
    client.access_token = "token123"

    mock_response = MagicMock()
    mock_response.status_code = 200
    mock_response.json.return_value = {"job": "started"}
    mock_response.raise_for_status = MagicMock()

    with patch("httpx.AsyncClient.post", new_callable=AsyncMock, return_value=mock_response) as mock_post:
        res = await client.start_job("process_key")
        assert res == {"job": "started"}
        mock_post.assert_called_once()


@pytest.mark.asyncio
async def test_uipath_orchestrator_client_raises_on_http_error():
    """Test that start_job raises UiPathError on http failure."""
    client = UiPathOrchestratorClient(client_id="id", client_secret="secret")
    client.access_token = "token123"

    with patch("httpx.AsyncClient.post", new_callable=AsyncMock, side_effect=Exception("Timeout")):
        with pytest.raises(UiPathError) as exc_info:
            await client.start_job("process_key")
        assert "Failed to start job" in str(exc_info.value)


@pytest.mark.asyncio
async def test_uipath_queue_helper_add_item_success():
    """Test adding queue items successfully."""
    client = UiPathOrchestratorClient(client_id="id", client_secret="secret")
    client.access_token = "token123"

    helper = UiPathQueueHelper(client)

    mock_response = MagicMock()
    mock_response.status_code = 201
    mock_response.json.return_value = {"item": "added"}
    mock_response.raise_for_status = MagicMock()

    with patch("httpx.AsyncClient.post", new_callable=AsyncMock, return_value=mock_response) as mock_post:
        res = await helper.add_queue_item("QueueName", {"key": "val"})
        assert res == {"item": "added"}
        mock_post.assert_called_once()


@pytest.mark.asyncio
async def test_uipath_queue_helper_raises_on_error():
    """Test that add_queue_item raises QueueItemError on HTTP error."""
    client = UiPathOrchestratorClient(client_id="id", client_secret="secret")
    client.access_token = "token123"

    helper = UiPathQueueHelper(client)

    with patch("httpx.AsyncClient.post", new_callable=AsyncMock, side_effect=Exception("Failed connection")):
        with pytest.raises(QueueItemError) as exc_info:
            await helper.add_queue_item("QueueName", {"key": "val"})
        assert "Failed to add item to queue" in str(exc_info.value)


@pytest.mark.asyncio
async def test_uipath_queue_helper_get_queue_items_success():
    """Test retrieving queue items successfully."""
    client = UiPathOrchestratorClient(client_id="id", client_secret="secret")
    client.access_token = "token123"

    helper = UiPathQueueHelper(client)

    mock_response = MagicMock()
    mock_response.status_code = 200
    mock_response.json.return_value = {
        "value": [
            {"Id": 1, "Status": "New", "SpecificContent": {"a": 1}},
            {"Id": 2, "Status": "InProgress", "SpecificContent": {"b": 2}},
        ]
    }
    mock_response.raise_for_status = MagicMock()

    with patch("httpx.AsyncClient.get", new_callable=AsyncMock, return_value=mock_response) as mock_get:
        items = await helper.get_queue_items("QueueName")
        assert len(items) == 2
        assert items[0]["Id"] == 1
        mock_get.assert_called_once()
        call_kwargs = mock_get.call_args
        assert call_kwargs.kwargs.get("params") or call_kwargs[1].get("params")


@pytest.mark.asyncio
async def test_uipath_queue_helper_get_queue_items_with_filter():
    """Test get_queue_items appends an extra OData filter clause."""
    client = UiPathOrchestratorClient(client_id="id", client_secret="secret")
    client.access_token = "token123"

    helper = UiPathQueueHelper(client)

    mock_response = MagicMock()
    mock_response.status_code = 200
    mock_response.json.return_value = {"value": []}
    mock_response.raise_for_status = MagicMock()

    with patch("httpx.AsyncClient.get", new_callable=AsyncMock, return_value=mock_response) as mock_get:
        items = await helper.get_queue_items("QueueName", filter_query="Status eq 'New'")
        assert items == []
        params = mock_get.call_args.kwargs.get("params") or mock_get.call_args[1].get("params")
        assert "QueueDefinitionName eq 'QueueName'" in params["$filter"]
        assert "Status eq 'New'" in params["$filter"]


@pytest.mark.asyncio
async def test_uipath_queue_helper_get_queue_items_raises_on_error():
    """Test that get_queue_items raises QueueItemError on HTTP error."""
    client = UiPathOrchestratorClient(client_id="id", client_secret="secret")
    client.access_token = "token123"

    helper = UiPathQueueHelper(client)

    with patch("httpx.AsyncClient.get", new_callable=AsyncMock, side_effect=Exception("network down")):
        with pytest.raises(QueueItemError) as exc_info:
            await helper.get_queue_items("QueueName")
        assert "Failed to retrieve items from queue" in str(exc_info.value)


@pytest.mark.asyncio
async def test_uipath_queue_helper_add_item_with_priority():
    """Test add_queue_item passes priority in the payload."""
    client = UiPathOrchestratorClient(client_id="id", client_secret="secret")
    client.access_token = "token123"

    helper = UiPathQueueHelper(client)

    mock_response = MagicMock()
    mock_response.status_code = 201
    mock_response.json.return_value = {"Id": 42}
    mock_response.raise_for_status = MagicMock()

    with patch("httpx.AsyncClient.post", new_callable=AsyncMock, return_value=mock_response) as mock_post:
        res = await helper.add_queue_item("Q", {"x": 1}, priority="High")
        assert res == {"Id": 42}
        payload = mock_post.call_args.kwargs.get("json") or mock_post.call_args[1].get("json")
        assert payload["ItemData"]["Priority"] == "High"
        assert payload["ItemData"]["Name"] == "Q"
        assert payload["ItemData"]["SpecificContent"] == {"x": 1}
