import pytest
from unittest.mock import MagicMock
from src.log import log_command_result, logs

def test_log_command_result_success():
    logs.clear()
    mock_result = MagicMock()
    mock_result.command = "pytest"
    mock_result.returncode = 0
    mock_result.stdout = "Success\nTest passed"
    mock_result.stderr = ""

    log_command_result("pytest", mock_result)

    assert len(logs) == 1
    log_entry = logs[0]
    assert log_entry["command"] == "pytest"
    assert log_entry["return_code"] == 0
    assert log_entry["stdout"] == ["Success", "Test passed"]
    assert log_entry["stderr"] == []

def test_log_command_result_failure():
    logs.clear()
    mock_result = MagicMock()
    mock_result.command = "pytest"
    mock_result.returncode = 1
    mock_result.stdout = ""
    mock_result.stderr = "Error\nTest failed"

    log_command_result("pytest", mock_result)

    assert len(logs) == 1
    log_entry = logs[0]
    assert log_entry["command"] == "pytest"
    assert log_entry["return_code"] == 1
    assert log_entry["stdout"] == []
    assert log_entry["stderr"] == ["Error", "Test failed"]
