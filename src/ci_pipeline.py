# ci_pipeline.py
# This workflow is triggered by webhook

import subprocess
from config import TMP_DIR
from src.prepare import prepare
from src.check_syntax import check_syntax

def run_ci_pipeline(repo_url, branch, commit_id, logger):

    build_success = True

    try:
        prepare(repo_url, logger)

        check_syntax(logger, TMP_DIR)

        # test()

    except subprocess.CalledProcessError:
        build_success = False
    except Exception as e:
        build_success = False
        logger.error(f"Build error: {e}")


    # notify()