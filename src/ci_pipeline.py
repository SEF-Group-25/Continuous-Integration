# ci_pipeline.py
# This workflow is triggered by webhook

import subprocess
from src.prepare import prepare

def run_ci_pipeline(repo_url, branch, commit_id, logger):

    build_success = True

    try:
        prepare(repo_url, logger)

        # check_syntax()

        # test()

    except subprocess.CalledProcessError:
        build_success = False

    # notify()