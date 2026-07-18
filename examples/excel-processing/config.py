"""Configuration for the Excel Processing light example."""

from __future__ import annotations

from pathlib import Path
from typing import Literal

from pydantic import Field
from pydantic_settings import BaseSettings


class ExcelBotSettings(BaseSettings):
    bot_name: str = Field(default="excel-processing", validation_alias="BOT_NAME")
    environment: Literal["dev", "staging", "prod"] = Field(default="dev", validation_alias="ENVIRONMENT")
    input_file: Path = Field(
        default=Path("./data/rechnungen_q2.xlsx"),
        validation_alias="INPUT_FILE",
    )
    output_dir: Path = Field(
        default=Path("./data/output"),
        validation_alias="OUTPUT_DIR",
    )
    # When True, skip real openpyxl and return synthetic row counts
    simulated_mode: bool = Field(default=True, validation_alias="SIMULATED_MODE")

    model_config = {
        "env_file": ".env",
        "env_file_encoding": "utf-8",
        "extra": "ignore",
        "populate_by_name": True,
    }


settings = ExcelBotSettings()
