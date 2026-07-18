"""Light unit tests for excel-processing example (no real xlsx required)."""

from __future__ import annotations

from pathlib import Path
import sys

import pytest

_EXAMPLE_ROOT = Path(__file__).resolve().parent.parent
for _key in list(sys.modules):
    if _key in ("config", "main", "tasks") or _key.startswith("tasks."):
        del sys.modules[_key]
sys.path = [p for p in sys.path if Path(p).resolve() != _EXAMPLE_ROOT]
sys.path.insert(0, str(_EXAMPLE_ROOT))

from config import ExcelBotSettings  # noqa: E402
from main import ProcessExcelTask  # noqa: E402


@pytest.fixture
def mock_settings(tmp_path: Path) -> ExcelBotSettings:
    return ExcelBotSettings(
        bot_name="excel-test",
        input_file=tmp_path / "in.xlsx",
        output_dir=tmp_path / "out",
        simulated_mode=True,
    )


@pytest.mark.asyncio
async def test_simulated_processing(mock_settings: ExcelBotSettings) -> None:
    task = ProcessExcelTask(mock_settings)
    result = await task.run()
    assert result["status"] == "success"
    assert result["rows_processed"] == 1247
    assert result["mode"] == "simulated"


@pytest.mark.asyncio
async def test_injected_rows(mock_settings: ExcelBotSettings) -> None:
    rows = [{"id": 1}, {"id": 2}, {"id": 3}]
    task = ProcessExcelTask(mock_settings, rows=rows)
    result = await task.run()
    assert result["rows_processed"] == 3
    assert result["mode"] == "injected"
