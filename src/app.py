import os
from flask import Flask, request, jsonify
from ci_pipeline import run_ci_pipeline
from pyngrok import ngrok
from dotenv import load_dotenv

dotenv_path = os.path.join(os.path.dirname(__file__), "auth.env")
load_dotenv(dotenv_path)

# load NGROK_AUTHTOKEN 
ngrok_authtoken = os.getenv("NGROK_AUTHTOKEN")

if not ngrok_authtoken:
    raise ValueError("NGROK_AUTHTOKEN environment variable not set.")

ngrok.set_auth_token(ngrok_authtoken)

app = Flask(__name__)

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
        if ref:
            branch = ref.split("/")[-1]
        else:
            branch = None
        commit_id = payload.get("after", None)

        if not branch or not commit_id:
            return jsonify({"error": "Missing branch or commit_id in payload"}), 400

        app.logger.info(f"Received push event for branch: {branch}, commit: {commit_id}")
        run_ci_pipeline(branch, commit_id)
        return jsonify({"message": "CI pipeline triggered"}), 200

    # For other event types
    return jsonify({"message": f"Unhandled event type: {event_type}"}), 200

@app.route("/history", methods=["GET"])
def history():
    pass

@app.route("/history/<commit_id>", methods=["GET"])
def history_details(commit_id):
    pass

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)