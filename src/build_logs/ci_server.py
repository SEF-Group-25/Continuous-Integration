import json, os, random
from datetime import datetime
from flask import Flask, request, jsonify

app = Flask(__name__)

HISTORY_FILE = "build_history.json"

@app.route('/', methods=['POST'])
def handle_request():
    """Webhook endpoint to trigger CI."""
    data = request.get_json()
    
    if not data or 'head_commit' not in data:
        return "Invalid payload", 400
    
    commit_id = data["head_commit"]["id"] 

    # Mock CI execution (random success/failure)
    status = "success" if random.random() > 0.2 else "failure"
    logs = f"Mock CI process for commit {commit_id}. Status: {status}."

    save_build(commit_id, status, logs)

    return jsonify({"message": "CI job processed", "commit_id": commit_id, "status": status})

def load_build_history():
    """Load build history from JSON file, or return an empty list if it doesn't exist."""
    if os.path.exists(HISTORY_FILE):
        with open(HISTORY_FILE, "r") as f:
            try:
                return json.load(f)
            except json.JSONDecodeError:
                return []
    return []

def save_build(commit_id, status, logs):
    """Save a build result, ensuring only one build per commit (overwrite old build)."""
    history = load_build_history()

    history = [b for b in history if b["commit_id"] != commit_id]

    build_data = {
        "commit_id": commit_id,
        "status": status,
        "timestamp": datetime.now().isoformat(),
        "logs": logs
    }

    history.append(build_data) 

    with open(HISTORY_FILE, "w") as f:
        json.dump(history, f, indent=4)

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8080)