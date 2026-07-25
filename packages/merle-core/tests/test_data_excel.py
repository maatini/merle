"""
Unit tests for the Excel utilities (ExcelReader and ExcelWriter).
"""

from __future__ import annotations

from pathlib import Path

import pandas as pd
import pytest

from merle_core.data import ExcelReader, ExcelWriter
from merle_core.exceptions import ExcelError


def test_excel_write_and_read_success(tmp_path: Path):
    """Test writing a DataFrame to Excel and reading it back successfully."""
    excel_path = tmp_path / "test_report.xlsx"

    # Create dummy data
    data = {
        "Name": ["Alice", "Bob", "Charlie"],
        "Age": [25, 30, 35],
        "City": ["Berlin", "Munich", "Hamburg"],
    }
    df = pd.DataFrame(data)

    # Write DataFrame
    ExcelWriter.write_df_to_sheet(df, excel_path, sheet_name="Employees")
    assert excel_path.exists()

    # Read DataFrame back
    df_read = ExcelReader.read_sheet_to_df(excel_path, sheet_name="Employees")

    # Assert equality
    pd.testing.assert_frame_equal(df, df_read)


def test_excel_reader_raises_on_missing_file():
    """Test that ExcelReader raises ExcelError when the file does not exist."""
    missing_path = Path("this_file_does_not_exist_12345.xlsx")
    with pytest.raises(ExcelError) as exc_info:
        ExcelReader.read_sheet_to_df(missing_path)
    assert "Excel file not found" in str(exc_info.value)
