"""
Unit tests for merle_core.logging_config.
"""

from __future__ import annotations

from pathlib import Path
from unittest.mock import patch

from loguru import logger

from merle_core.logging_config import setup_logging


def test_setup_logging_removes_default_handlers_and_adds_stderr():
    """setup_logging should remove existing handlers and attach stderr sink."""
    # Ensure at least one handler exists before setup
    logger.add(lambda _: None)

    with patch.object(logger, "remove") as mock_remove, patch.object(logger, "add") as mock_add:
        setup_logging(level="DEBUG", json_format=False)

        mock_remove.assert_called_once_with()
        assert mock_add.call_count == 1
        args, kwargs = mock_add.call_args
        assert kwargs.get("level") == "DEBUG"
        # First positional is the sink (sys.stderr)
        import sys

        assert args[0] is sys.stderr


def test_setup_logging_json_format_adds_file_sink(tmp_path: Path, monkeypatch):
    """json_format=True should register an additional serialized file sink."""
    # Point CWD so any real path side-effects stay under tmp if sinks execute
    monkeypatch.chdir(tmp_path)

    with patch.object(logger, "remove") as mock_remove, patch.object(logger, "add") as mock_add:
        setup_logging(level="INFO", json_format=True)

        mock_remove.assert_called_once_with()
        assert mock_add.call_count == 2

        # Second sink: JSON file with serialize=True
        _, kwargs = mock_add.call_args_list[1]
        assert kwargs.get("serialize") is True
        assert kwargs.get("level") == "INFO"
        assert "rotation" in kwargs
        assert "retention" in kwargs


def test_setup_logging_actually_logs_without_error(tmp_path: Path, monkeypatch, capsys):
    """End-to-end: setup_logging should allow a simple log call."""
    monkeypatch.chdir(tmp_path)
    setup_logging(level="INFO", json_format=False)
    logger.info("logging_config smoke test")
    # Restore a sane default for subsequent tests
    logger.remove()
    logger.add(lambda _: None)
