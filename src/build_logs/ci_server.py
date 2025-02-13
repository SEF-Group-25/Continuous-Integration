import json, os, random
from datetime import datetime
from flask import Flask, request, jsonify

app = Flask(__name__)

HISTORY_FILE = "build_history.json"

@app.route('/', methods=['POST'])
def handle_request():
    """Webhook endpoint to trigger CI.

    Expects a JSON payload with a 'head_commit' key containing commit information.

    Returns:
        A JSON response containing a message, commit ID, and build status.
        If the payload is invalid, returns a plain text error message with HTTP status 400.
    """
    data = request.get_json()
    
    if not data or 'head_commit' not in data:
        return "Invalid payload", 400
    
    commit_id = data["head_commit"]["id"] 

    # Mock CI execution (random success/failure)
    status = "success" if random.random() > 0.2 else "failure"
    logs = f"Mock CI process for commit {commit_id}. Status: {status}."

    save_build(commit_id, status, logs)

    return jsonify({"message": "CI job processed", "commit_id": commit_id, "status": status})

@app.route('/history', methods=['GET'])
def get_build_history():
    """Return list of all past builds.

    Retrieves the entire build history from a JSON file.

    Returns:
        A JSON response containing a list of build records.
    """
    history = load_build_history()
    return jsonify(history)

@app.route('/history/<commit_id>', methods=['GET'])
def get_build_details(commit_id):
    """Retrieve detailed build information for a given commit.

    Args:
        commit_id (str): The commit identifier to look up in the build history.

    Returns:
        A JSON response with the build details if found, or an error message with HTTP status 404 if not found.
    """
    history = load_build_history()
    build = next((build for build in history if build["commit_id"] == commit_id), None)

    if build:
        return jsonify(build)
    return jsonify({"error": "Build not found"}), 404


def load_build_history():
    """Load build history from a JSON file, or return an empty list if the file does not exist or is invalid.

    Returns:
        list: A list of build records.
    """
    if os.path.exists(HISTORY_FILE):
        with open(HISTORY_FILE, "r") as f:
            try:
                return json.load(f)
            except json.JSONDecodeError:
                return []
    return []

def save_build(commit_id, status, logs):
    """Save a build result, ensuring only one build per commit.

    Updates the build history with the new build data and writes it to a JSON file.

    Args:
        commit_id (str): The commit identifier associated with the build.
        status (str): The build status (e.g., "success" or "failure").
        logs (str): Log details from the CI process.
    """
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