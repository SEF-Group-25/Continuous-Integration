import pytest
from unittest.mock import patch, MagicMock
from src.utils import run_command
from config import TMP_DIR
from src.test import run_test

# positive case
@patch("src.test.run_command")
def test_run_test_success(mock_run_command):
    mock_run_command.return_value = MagicMock(returncode=0)
    
    try:
        run_test()
    except Exception as e:
        pytest.fail(f"Test failed unexpectedly: {e}")

# negative case
@patch("src.test.run_command")
def test_run_test_failure(mock_run_command):
    mock_run_command.return_value = MagicMock(returncode=1)
    
    with pytest.raises(Exception) as excinfo:
        run_test()
    
    assert str(excinfo.value) == "test: Test fails, check the logs"