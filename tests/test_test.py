import pytest
import subprocess
from unittest.mock import patch
from src.test import run_test, TMP_DIR

def test_run_test_success():
    with patch("src.test.run_command") as mock_run_command:
        try:
            run_test()
        except Exception:
            pytest.fail("run_test() raised Exception unexpectedly!")

        mock_run_command.assert_called_once_with("pytest tests/", TMP_DIR)

def test_run_test_failure():
    with patch("src.test.run_command", side_effect=subprocess.CalledProcessError(1, "pytest tests/")) as mock_run_command:
        with pytest.raises(Exception, match="test: Test fails, check the logs"):
            run_test()

        mock_run_command.assert_called_once_with("pytest tests/", TMP_DIR)
