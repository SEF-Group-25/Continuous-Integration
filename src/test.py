# test.py
# This is used to test the repo to be built,
# not to test the CI server itself

from src.utils import run_command
from config import TMP_DIR

def run_test():
    run_command("pytest", TMP_DIR)

# used for test
# should be deleted
if __name__ == "__main__":
    run_test()