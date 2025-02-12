# ci_pipeline.py
# This workflow is triggered by webhook

import subprocess
from src.prepare import prepare
from src.notify import set_commit_status, discord_notify


def run_ci_pipeline(repo_url, branch, commit_id, logger):
    build_success = True

    try:
        prepare(repo_url, branch, commit_id, logger)

        # check_syntax()

        # test()

    except subprocess.CalledProcessError as e:
        build_success = False

    if build_success == False:
        set_commit_status(commit_id, "failure")
        discord_notify(commit_id, "Failure")
    else:
        set_commit_status(commit_id, "success")
        discord_notify(commit_id, "Success")



# used for test
# should be deleted
if __name__ == "__main__":
    run_ci_pipeline("https://github.com/SEF-Group-25/Launch-Interceptor-Program.git", "main", "f995103", None)
