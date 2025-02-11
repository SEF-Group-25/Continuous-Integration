# ci_pipeline.py
# This workflow is triggered by webhook

import subprocess
from config import TMP_DIR
from src.prepare import prepare
from src.check_syntax import check_syntax
from src.test import run_test

def run_ci_pipeline(repo_url, branch, commit_id, logger):

    build_success = True

    try:
        prepare(repo_url, branch, commit_id, logger)

        check_syntax(logger, TMP_DIR)

        run_test()

    except subprocess.CalledProcessError as e:
        build_success = False
    except Exception as e:
        build_success = False
        logger.error(f"Build error: {e}")


    # notify()

# used for test
# should be deleted
if __name__ == "__main__":
    run_ci_pipeline("https://github.com/SEF-Group-25/Launch-Interceptor-Program.git", "main", "f995103", None)