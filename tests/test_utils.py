import pytest
import subprocess
from unittest.mock import patch, MagicMock
from src.utils import run_command

def test_run_command_success():
    mock_result = MagicMock()
    mock_result.returncode = 0
    mock_result.stdout = "Execution successful"
    mock_result.stderr = ""

    with patch("src.utils.subprocess.run", return_value=mock_result) as mock_run, \
         patch("src.utils.log_command_result") as mock_log:

        run_command("echo hello", "/tmp")

        mock_run.assert_called_once_with("echo hello", cwd="/tmp", shell=True, capture_output=True, text=True)
        mock_log.assert_called_once_with("echo hello", mock_result)

def test_run_command_failure():
    mock_result = MagicMock()
    mock_result.returncode = 1
    mock_result.stdout = ""
    mock_result.stderr = "Error occurred"

    with patch("src.utils.subprocess.run", return_value=mock_result) as mock_run, \
         patch("src.utils.log_command_result") as mock_log:

        with pytest.raises(subprocess.CalledProcessError) as exc_info:
            run_command("invalid_command", "/tmp")

        mock_run.assert_called_once_with("invalid_command", cwd="/tmp", shell=True, capture_output=True, text=True)
        mock_log.assert_called_once_with("invalid_command", mock_result)

        assert exc_info.value.returncode == 1
        assert exc_info.value.cmd == "invalid_command"
