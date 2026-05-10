"""
Tests für die Haupt-Workflow-Logik.
"""

import pytest
from unittest.mock import AsyncMock, patch
from tasks.example_task import ExampleTask


class TestExampleTask:
    """Unit-Tests für ExampleTask."""

    @pytest.mark.asyncio
    async def test_process_filters_active_items(self, settings):
        """_process() soll nur aktive Einträge zurückgeben."""
        task = ExampleTask(settings)
        data = [
            {"id": 1, "active": True},
            {"id": 2, "active": False},
            {"id": 3, "active": True},
        ]
        result = task._process(data)
        assert len(result) == 2
        assert all(item["active"] for item in result)

    @pytest.mark.asyncio
    async def test_fetch_data_success(self, settings):
        """_fetch_data() soll bei Erfolg Daten zurückgeben."""
        task = ExampleTask(settings)
        mock_response = AsyncMock()
        mock_response.json.return_value = [{"id": 1, "active": True}]

        with patch("httpx.AsyncClient.get", return_value=mock_response):
            result = await task._fetch_data()
            assert len(result) == 1
            assert result[0]["id"] == 1

    @pytest.mark.asyncio
    async def test_run_returns_status(self, settings):
        """run() soll Status-Dict mit items_processed zurückgeben."""
        task = ExampleTask(settings)
        mock_data = [
            {"id": 1, "active": True},
            {"id": 2, "active": False},
        ]

        with patch.object(task, "_fetch_data", return_value=mock_data):
            result = await task.run()
            assert result["status"] == "ok"
            assert result["items_processed"] == 1
