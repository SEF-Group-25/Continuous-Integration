import pytest
import subprocess
import os
from unittest.mock import patch, MagicMock
from src.prepare import prepare, TMP_DIR

def test_prepare_success():
    prepare("https://github.com/SEF-Group-25/Launch-Interceptor-Program.git", "main", "9c08d7e")

    assert len(os.listdir(TMP_DIR)) > 0

def test_clone_failure():
    with pytest.raises(Exception, match="prepare: Fail at command 'git clone -b main --single-branch https://example.com/repo.git .'"):
        prepare("https://example.com/repo.git", "main", "123456")

def test_install_failure():
    with pytest.raises(Exception, match="prepare: Fail at command 'pip install -r requirements.txt'"):
        prepare("https://github.com/SEF-Group-25/Launch-Interceptor-Program.git", "main", "f995103")