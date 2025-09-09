from fastapi.testclient import TestClient
from src.database.database import get_db
from src.main import app
from src.service.user import UserService

client = TestClient(app)

def test_login():
    response = client.post("api/v1/auth/login", json={"email": "user@example.com", "password": "password123"})
    assert response.status_code == 200
    assert "access_token" in response.json()
    assert response.json()["token_type"] == "bearer"

def test_login_invalid_credentials():
    response = client.post("api/v1/auth/login", json={"email": "emailerror@example.com", "password": "wrongpassword"})
    assert response.status_code == 404
    assert response.json() == {"detail": "User not found"}

def test_login_wrong_credentials():
    response = client.post("api/v1/auth/login", json={"email": "user@example.com", "password": "wrongpassword"})
    assert response.status_code == 401
    assert response.json() == {"detail": "Invalid email or password"}

def test_login_wrong_email_format():
    response = client.post("api/v1/auth/login", json={"email": "userexample.com", "password": "password123"})
    assert response.status_code == 422

def test_register():
    db = next(get_db())
    response = client.post("api/v1/auth/register", json={
        "username": "newuser",
        "email": "register@example.com",
        "password": "newpassword123",
        "first_name": "New",
        "last_name": "User"
    })
    assert response.status_code == 200
    data = response.json()
    assert data["email"] == "register@example.com"
    assert data["username"] == "newuser"
    UserService(db).delete_by_email("register@example.com")

def test_register_existing_email():
    response = client.post("api/v1/auth/register", json={
        "username": "existinguser",
        "email": "user@example.com",
        "password": "password123",
        "first_name": "Existing",
        "last_name": "User"
    })
    assert response.status_code == 400
    assert response.json() == {"detail": "User with this username or email already exists"}

def test_register_invalid_email_format():
    response = client.post("api/v1/auth/register", json={
        "username": "invalidemailuser",
        "email": "invalidemail.com",
        "password": "password123",
        "first_name": "Invalid",
        "last_name": "Email"
    })
    assert response.status_code == 422

def test_register_invalid_password():
    response = client.post("api/v1/auth/register", json={
        "username": "invalidpassworduser",
        "email": "invalid@passworduser.com",
        "password": "p",
        "first_name": "Invalid",
        "last_name": "password"
    })
    assert response.status_code == 400
    assert response.json() == {"detail": "Password must be at least 8 characters long"}



