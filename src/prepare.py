import os
import subprocess
import shutil
from src.utils import run_command
from config import TMP_DIR

def prepare(repo_url, branch, commit_id):
    """
    Prepares the repo and dependencies specified by:
    - repo_url
    - branch
    - commit_id
    """

    if os.path.exists(TMP_DIR):
        shutil.rmtree(TMP_DIR)
    os.makedirs(TMP_DIR, exist_ok=False)

    try:
        clone_repo(repo_url, branch, commit_id)

        install_dependencies()
    
    except subprocess.CalledProcessError as e:
        raise Exception(f"prepare: Fail at command \'{e.cmd}\'")


def clone_repo(repo_url, branch, commit_id):
    run_command(f"git clone -b {branch} --single-branch {repo_url} .", TMP_DIR)
    run_command(f"git checkout {commit_id}", TMP_DIR)

def install_dependencies():
    run_command("pip install -r requirements.txt", TMP_DIR)

# used for test
if __name__ == "__main__":
    prepare("https://github.com/SEF-Group-25/Launch-Interceptor-Program.git", "main", "9c08d7e", None)
    from src.log import logs
    import json
    with open("logs.json", "w") as f:
        json.dump(logs, f, indent=4)
