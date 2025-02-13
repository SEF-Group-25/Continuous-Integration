import os
from flask import Flask, request, jsonify
from src.ci_pipeline import run_ci_pipeline
from src.build_logs.ci_server import save_build, load_build_history
from pyngrok import ngrok
from dotenv import load_dotenv
from src.log import get_logs

dotenv_path = os.path.join(os.path.dirname(__file__), "auth.env")
load_dotenv(dotenv_path)

# load NGROK_AUTHTOKEN 
ngrok_authtoken = os.getenv("NGROK_AUTHTOKEN")

if not ngrok_authtoken:
    raise ValueError("NGROK_AUTHTOKEN environment variable not set.")

ngrok.set_auth_token(ngrok_authtoken)

app = Flask(__name__)

public_url = ngrok.connect(5000).public_url
print(f"\n Ngrok Tunnel URL: {public_url}\n")

@app.route("/webhook", methods=["POST"])
def webhook():
    event_type = request.headers.get("X-GitHub-Event", "unknown")
    payload = request.get_json()

    app.logger.info(f"Received event: {event_type}")

    # Special handling for pings
    if event_type == "ping":
        return jsonify({"message": "Ping received"}), 200

    # Push events
    if event_type == "push":
        # GitHub push payload should include "ref" and "after"
        ref = payload.get("ref", "")
        if ref.startswith("refs/heads/"):
            branch = ref.replace("refs/heads/", "")
        else:
            branch = ref

        commit_id = payload.get("after", None)
        repo_url = payload.get("repository", {}).get("html_url", "") + ".git"

        if not branch or not commit_id or not repo_url:
            return jsonify({"error": "Missing repository URL, branch, or commit_id in payload"}), 400
        
        app.logger.info(f"Received push event for repo: {repo_url}, branch: {branch}, commit: {commit_id}")
        
        build_success = run_ci_pipeline(repo_url, branch, commit_id)

        status = "success" if build_success else "failure"

        save_build(commit_id, status, get_logs())

        return jsonify({"message": "CI pipeline triggered", "status": status}), 200
    
    # For other event types
    return jsonify({"message": f"Unhandled event type: {event_type}"}), 200

@app.route("/history", methods=["GET"])
def history():
    """Retrieve a list of all past builds."""
    return jsonify(load_build_history()), 200

@app.route("/history/<commit_id>", methods=["GET"])
def history_details(commit_id):
    """Retrieve details of a specific build."""
    history = load_build_history()
    build = next((b for b in history if b["commit_id"] == commit_id), None)

    if build:
        return jsonify(build), 200
    return jsonify({"error": "Build not found"}), 404

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)