from starlette.testclient import TestClient
from server import app


def test_app():
    client = TestClient(app)
    with client.websocket_connect("/ws") as websocket:
        data = websocket.receive_text()
        assert data == "Hello world"


def test_upload_endpoint():
    client = TestClient(app)
    
    # Create a node
    response = client.post("/upload")
    assert response.status_code == 200
    data = response.json()
    assert "node_id" in data
    node_id = data["node_id"]
    assert node_id == 999
    
    # Delete the node
    delete_response = client.delete(f"/upload/{node_id}")
    assert delete_response.status_code == 204
