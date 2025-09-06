from fastapi.testclient import TestClient
from src.main import app

client = TestClient(app)

try:
    user_login = client.post("api/v1/auth/login", json={"email": "user@example.com", "password": "password123"})
    mario_login = client.post("api/v1/auth/login", json={"email": "mario@example.com", "password": "password123"})
    test_login = client.post("api/v1/auth/login", json={"email": "test@example.com", "password": "password123"})

    user_token = user_login.json().get("access_token")
    mario_token = mario_login.json().get("access_token")
    test_token = test_login.json().get("access_token")
except Exception as e:
    print(f"Error during login: {e}")
    user_token = None
    mario_token = None
    test_token = None