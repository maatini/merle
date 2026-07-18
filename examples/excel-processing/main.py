#!/usr/bin/env python3
"""
Excel Processing — light Merle example.

BaseTask + pydantic-settings; simulated by default so CI needs no Excel files.
"""

from __future__ import annotations

import asyncio
from typing import Any

from config import settings
from loguru import logger

from merle_core import BaseTask


class ProcessExcelTask(BaseTask):
    """Process an Excel workbook (simulated or real)."""

    def __init__(self, settings: Any, *, rows: list[dict[str, Any]] | None = None) -> None:
        super().__init__(settings, name="ProcessExcel")
        self._rows = rows

    async def execute(self) -> dict[str, Any]:
        if self._rows is not None:
            processed = len(self._rows)
            self.logger.info("Processed {} injected rows", processed)
            return {
                "status": "success",
                "rows_processed": processed,
                "file": str(self.settings.input_file),
                "mode": "injected",
            }

        if self.settings.simulated_mode:
            processed_rows = 1247
            self.logger.info("Simulated Excel processing ({} rows)", processed_rows)
            return {
                "status": "success",
                "rows_processed": processed_rows,
                "file": str(self.settings.input_file),
                "mode": "simulated",
            }

        # Real path would use merle_core.data.excel / pandas here
        self.logger.info("Loading {}", self.settings.input_file)
        raise NotImplementedError("Real Excel path: set SIMULATED_MODE=true or inject rows")


async def main() -> None:
    settings.output_dir.mkdir(parents=True, exist_ok=True)
    task = ProcessExcelTask(settings)
    result = await task.run()
    logger.info("Excel processing complete: {}", result)


if __name__ == "__main__":
    asyncio.run(main())
