# ci_pipeline.py
# This workflow is triggered by webhook

from config import TMP_DIR
from src.prepare import prepare
from src.check_syntax import check_syntax
from src.test import run_test

def run_ci_pipeline(repo_url, branch, commit_id):

    build_success = True
    status = "success"

    try:
        prepare(repo_url, branch, commit_id)

        check_syntax(TMP_DIR)

        run_test()

    except Exception as e:
        build_success = False
        error_type, _, message = str(e).partition(": ")

    if not build_success:
        status = f"fail_{error_type}"

    # notify()

# used for test
# should be deleted
if __name__ == "__main__":
    run_ci_pipeline("https://github.com/SEF-Group-25/Launch-Interceptor-Program.git", "main", "f995103")