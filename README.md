# Continuous-Integration

The goal of this assignment is to master the core of continuous integration. To achieve this goal, the students are asked to implement a small continuous integration CI server. This CI server will only contain the core features of continuous integration.

# Local webhook setup

First create a Nrock account, get your authtoken and create a file named auth.env in src which only consists of
"NGROK_AUTHTOKEN=[yourtoken]"
make sure that this file is ignored and dosent get pushed.

run src/app.py
copy the url that should look like https://[url].ngrok-free.app
go to github webhooks in the settings and either add a new or modify an existing webhook (preferebly that we have one per user so that multiple people can work at the same time)
set the url as https://[url].ngrok-free.app/webhook.
set the content type as application/json

Webhook should now be working, you can check the "Recent Deliveries" tab to see if a ping was succesfully sent, or redeliver it if you updated an existing webhook. You can test pushing by running
"
curl -X POST "https://[url].ngrok-free.app/webhook" -H "Content-Type: application/json" -H "X-GitHub-Event: push" -d "{\"ref\": \"refs/heads/assessment\", \"after\": \"commit_id_example\"}"
"

# Build History Storage for CI Server (P7)

## Overview

This feature implements **build history storage** for the CI server. It ensures that every processed build is logged, allowing users to track past builds, their statuses, and related metadata.

## Endpoints

| Method | Endpoint               | Description                                 |
| ------ | ---------------------- | ------------------------------------------- |
| `POST` | `/`                    | Triggers a new CI job and stores the result |
| `GET`  | `/history`             | Retrieves a list of all stored builds       |
| `GET`  | `/history/<commit_id>` | Retrieves details of a specific build       |
