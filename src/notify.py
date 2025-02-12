import requests
import os


def read_tokens():
    try:
        with open("../token.txt", "r") as file:
            return [line.strip() for line in file.readlines()]
    except:
        with open("token.txt", "r") as file:
            return [line.strip() for line in file.readlines()]

try:
    COMMIT_TOKEN = read_tokens()[0]

    # Discord Webhook Info
    DISCORD_WEBHOOK_URL = read_tokens()[1]

except:
    COMMIT_TOKEN = os.getenv("COMMIT_TOKEN") # For github
    DISCORD_WEBHOOK_URL = os.getenv("DISCORD_WEBHOOK_URL")



def set_commit_status(commit_sha, state="success", description="CI", REPO_OWNER="SEF-Group-25", REPO_NAME="Continuous-Integration", TOKEN=COMMIT_TOKEN):
    url = f"https://api.github.com/repos/{REPO_OWNER}/{REPO_NAME}/statuses/{commit_sha}"

    headers = {
        "Authorization": f"token {TOKEN}",
        "Accept": "application/vnd.github+json",
    }

    data = {
        "state": state,  # Can be "success", "failure", "pending", or "error"
        "target_url": f"https://github.com/{REPO_OWNER}/{REPO_NAME}/actions",
        "description": description,
        "context": "ci-tool",
    }

    response = requests.post(url, json=data, headers=headers)

    if response.status_code == 201:
        print(f"Commit {commit_sha} marked as {state}.")
    else:
        print(f"Failed to set status: {response.text}")

    return response.status_code


def discord_notify(commit_sha, result, webhook=DISCORD_WEBHOOK_URL):
    data = {
        "content": f"Commit: {commit_sha}\nStatus: {result}",
        "username": "CI Notifier",
    }

    try:
        response = requests.post(webhook, json=data)
        if response.status_code == 204:
            print("Message sent successfully!")
        else:
            print(f"Failed to send message: {response.status_code}, {response.text}")
    except:
        print("Failed to send message")


if __name__ == "__main__":
    # set_commit_status("ac707d7ae01c1dfb631380e68b5d730a5990f7fc")
    discord_notify("ac707d7ae01c1dfb631380e68b5d730a5990f7fc", "Success", "DWadw")
