from fastapi.testclient import TestClient
from ragapp.main import app
client = TestClient(app)

def test_hit_and_miss():
    hit = client.post("/ask", json={"question": 'Why does the platform refuse latest tags in production?'}).json()
    assert hit["answered"] is True
    assert hit["citation"] == 'policy.pdf'
    miss = client.post("/ask", json={"question": "orbital cafeteria soup"}).json()
    assert miss["answered"] is False

def test_empty():
    assert client.post("/ask", json={"question": " "}).status_code == 422

