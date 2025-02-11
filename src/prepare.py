import os
import shutil
from src.utils import run_command
from config import TMP_DIR

# This function prepares environment for build
def prepare(repo_url, branch, commit_id, logger):

    if os.path.exists(TMP_DIR):
        shutil.rmtree(TMP_DIR)
    os.makedirs(TMP_DIR, exist_ok=False)

    clone_repo(repo_url, branch, commit_id)

    install_dependencies()


def clone_repo(repo_url, branch, commit_id):
    run_command(f"git clone -b {branch} --single-branch {repo_url} .", TMP_DIR)
    run_command(f"git checkout {commit_id}", TMP_DIR)

def install_dependencies():
    run_command("pip install -r requirements.txt", TMP_DIR)

# used for test
if __name__ == "__main__":
    prepare("https://github.com/SEF-Group-25/Launch-Interceptor-Program.git", "main", "9c08d7e", None)
