from starlette.testclient import TestClient
from server import app


def test_app():
    client = TestClient(app)
    with client.websocket_connect("/ws") as websocket:
        data = websocket.receive_text()
        assert data == "Hello world"
