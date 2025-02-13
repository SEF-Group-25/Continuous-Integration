# Continuous-Integration

The goal of this assignment is to master the core of continuous integration. To achieve this goal, the students are asked to implement a small continuous integration CI server. This CI server will only contain the core features of continuous integration.

# Local webhook setup

First create a Nrock account, get your authtoken and create a file named `auth.env` in `src` which only consists of `NGROK_AUTHTOKEN=[yourtoken]`. Make sure that this file is ignored and dosent get pushed.

Run `src/app.py`, copy the url that should look like `https://[url].ngrok-free.app`

Go to github webhooks in the settings and either add a new or modify an existing webhook. (preferebly that we have one per user so that multiple people can work at the same time)

set the url as `https://[url].ngrok-free.app/webhook`

set the content type as `application/json`

Webhook should now be working, you can check the "Recent Deliveries" tab to see if a ping was succesfully sent, or redeliver it if you updated an existing webhook. You can test pushing by running
```bash
% curl -X POST "https://[url].ngrok-free.app/webhook" -H "Content-Type: application/json" -H "X-GitHub-Event: push" -d "{\"ref\": \"refs/heads/assessment\", \"after\": \"commit_id_example\"}"
```

# Executing the automated tests (P2)

The tests of the group project are based on Pytest. To implement the execution of test, the program runs shell command `pytest` in the root directory of the repository, which will automatically search the test cases and execute. 

If any of the tests fails, there will be an exception. And the program will catch the exception and stop the build process. All of the commands executed by the program will be logged. To unit-test this feature, the testing program mocks the result of the shell command and check if there is an exception as expected.

# Environment Variables
Make sure to do export COMMIT_TOKEN="(GitHub token with repo:status and public_repo permissions)" and export DISCORD_WEBHOOK_URL="(Your Discord Webhook)".

# Environment Variables
Make sure to do export COMMIT_TOKEN="(GitHub token with repo:status and public_repo permissions)" and export DISCORD_WEBHOOK_URL="(Your Discord Webhook)".

# Build History Storage for CI Server (P7)

This feature implements **build history storage** for the CI server. It ensures that every processed build is logged, allowing users to track past builds, their statuses, and related metadata.

## Endpoints

| Method | Endpoint               | Description                                 |
| ------ | ---------------------- | ------------------------------------------- |
| `POST` | `/`                    | Triggers a new CI job and stores the result |
| `GET`  | `/history`             | Retrieves a list of all stored builds       |
| `GET`  | `/history/<commit_id>` | Retrieves details of a specific build       |

# Contributions
* Oscar Hellgren
  * P3 - Notification (set commit status and send messages to Discord)
  * Set up GitHub Actions with repository secrets.

* Anton Yderberg
  * P1 - Compilation
  * Set up GitHub webhook and Ngrok
    
* Zubair Yousafzai
  * P7 - Build history (build infomation persistance and display)
    
* Shangxuan Tang
  * P2 - Testing
  * Set up ci workflow with logger and error handler
