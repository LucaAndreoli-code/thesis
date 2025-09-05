from fastapi.testclient import TestClient

from migration_manager import setup_database
from .main import app

client = TestClient(app)
setup_database()

def test_read_main():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"msg": "Simple Pay API is running"}