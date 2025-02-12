import requests
import os


def read_tokens():
    with open("../token.txt", "r") as file:
        return [line.strip() for line in file.readlines()]



# GitHub Repo Info
REPO_OWNER = "SEF-Group-25"
REPO_NAME = "Continuous-Integration"

GITHUB_TOKEN = read_tokens()[0]  # os.getenv("GITHUB_TOKEN")  # Use export GITHUB_TOKEN=your_token in terminal

# Discord Webhook Info
DISCORD_WEBHOOK_URL = read_tokens()[1]


def set_commit_status(commit_sha, state="success", description="CI", context="ci-tool"):
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


def discord_notify(commit_sha, result):
    data = {
        "content": f"Commit: {commit_sha}\nStatus: {result}",
        "username": "CI Notifier",
    }

    response = requests.post(DISCORD_WEBHOOK_URL, json=data)

    if response.status_code == 204:
        print("Message sent successfully!")
    else:
        print(f"Failed to send message: {response.status_code}, {response.text}")


if __name__ == "__main__":
    #set_commit_status("ac707d7ae01c1dfb631380e68b5d730a5990f7fc")
    discord_notify("ac707d7ae01c1dfb631380e68b5d730a5990f7fc", "Success")
