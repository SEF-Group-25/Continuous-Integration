import requests
import os

# GitHub Repo Info
REPO_OWNER = "SEF-Group-25"
REPO_NAME = "Continuous-Integration"

GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")  # Use export GITHUB_TOKEN=your_token in terminal

def set_commit_status(commit_sha, state="success", description="CI Test", context="ci-tool"):
    url = f"https://api.github.com/repos/{REPO_OWNER}/{REPO_NAME}/statuses/{commit_sha}"

    headers = {
        "Authorization": f"token {GITHUB_TOKEN}",
        "Accept": "application/vnd.github+json",
    }

    data = {
        "state": state,  # Can be "success", "failure", "pending", or "error"
        "target_url": f"https://github.com/{REPO_OWNER}/{REPO_NAME}/actions",
        "description": description,
        "context": context,
    }

    response = requests.post(url, json=data, headers=headers)

    if response.status_code == 201:
        print(f"Commit {commit_sha} marked as {state}.")
    else:
        print(f"Failed to set status: {response.text}")


if __name__ == "__main__":
    set_commit_status("")
