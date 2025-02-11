import os, sys, json, pytest
from datetime import datetime

project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
if project_root not in sys.path:
    sys.path.insert(0, project_root)

from src.build_logs.ci_server import app, load_build_history, save_build

@pytest.fixture
def client():
    app.config.update({
        "TESTING": True,
    })
    with app.test_client() as client:
        yield client

TEST_HISTORY_FILE = "test_build_history.json"

@pytest.fixture(autouse=True)
def mock_history_file(monkeypatch):
    """Monkeypatch history file to use a test file."""
    monkeypatch.setattr("src.build_logs.ci_server.HISTORY_FILE", TEST_HISTORY_FILE)
    
    with open(TEST_HISTORY_FILE, "w") as f:
        json.dump([], f)

    yield 

    # Cleanup
    if os.path.exists(TEST_HISTORY_FILE):
        os.remove(TEST_HISTORY_FILE)

# File exists
def test_load_build_history():
    test_data = [{"commit_id": "abc123", "status": "success", "logs": "Test log"}]
    with open(TEST_HISTORY_FILE, "w") as f:
        json.dump(test_data, f)
    
    history = load_build_history()
    assert history == test_data 

# File doesn't exist
def test_load_build_history_empty():
    if os.path.exists(TEST_HISTORY_FILE):
        os.remove(TEST_HISTORY_FILE)
    
    history = load_build_history()
    assert history == []  

# Test saving build
def test_save_build():
    commit_id = "test_commit"
    status = "success"
    logs = "Test logs"

    save_build(commit_id, status, logs)

    with open(TEST_HISTORY_FILE, "r") as f:
        history = json.load(f)

    assert len(history) == 1
    assert history[0]["commit_id"] == commit_id
    assert history[0]["status"] == status
    assert history[0]["logs"] == logs

# Test POST request to trigger CI
def test_handle_request(client):
    response = client.post("/", json={"head_commit": {"id": "commit123"}})

    assert response.status_code == 200
    data = response.get_json()
    assert "commit_id" in data
    assert "status" in data
    assert data["commit_id"] == "commit123"

# Test invalid payload in POST request
def test_handle_request_invalid(client):
    response = client.post("/", json={})
    assert response.status_code == 400

# Test GET /history when no builds exist
def test_get_build_history_empty(client):
    response = client.get("/history")
    assert response.status_code == 200
    assert response.get_json() == []

# Test GET /history when builds exist
def test_get_build_history(client):
    save_build("commit1", "success", "Log 1")
    save_build("commit2", "failure", "Log 2")

    response = client.get("/history")
    data = response.get_json()

    assert response.status_code == 200
    assert len(data) == 2
    assert data[0]["commit_id"] == "commit1"
    assert data[1]["commit_id"] == "commit2"

# Test GET /history/<commit_id> for an existing build
def test_get_build_details(client):
    commit_id = "commit123"
    save_build(commit_id, "success", "Test logs")

    response = client.get(f"/history/{commit_id}")
    data = response.get_json()

    assert response.status_code == 200
    assert data["commit_id"] == commit_id
    assert data["status"] == "success"

# Test GET /history/<commit_id> for a non-existing build
def test_get_build_details_not_found(client):
    response = client.get("/history/non_existent_commit")
    assert response.status_code == 404
    assert response.get_json() == {"error": "Build not found"}
