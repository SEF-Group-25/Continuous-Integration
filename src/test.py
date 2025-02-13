# test.py
# This is used to test the repo to be built,
# not to test the CI server itself

import subprocess
from src.utils import run_command
from config import TMP_DIR

def run_test():
    """
    Run pytest to execute test cases under /tests
    The result of pytest will be stored in the log
    """

    try:
        run_command("pytest tests/", TMP_DIR)

    except subprocess.CalledProcessError:
        raise Exception("test: Test fails, check the logs")

# used for test
# should be deleted
if __name__ == "__main__":
    run_test()