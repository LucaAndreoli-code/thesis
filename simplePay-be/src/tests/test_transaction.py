from fastapi.testclient import TestClient
from src.database.database import get_db
from src.main import app

client = TestClient(app)

def test_transaction_send_success_1():
    login_response = client.post("api/v1/auth/login", json={"email": "user@example.com", "password": "password123"})
    assert login_response.status_code == 200
    auth_token = login_response.json()["access_token"]
    headers = {"Authorization": f"Bearer {auth_token}"}

    response = client.post(
        "api/v1/payments/send",
        headers=headers,
        json={
            "to_user_email": "mario@example.com",
            "amount": 100.50,
            "description": "test"
        }
    )
    assert response.status_code == 200
    assert "Payment completed successfully" in response.json()["message"]

def test_transaction_send_success_2():
    login_response = client.post("api/v1/auth/login", json={"email": "mario@example.com", "password": "password123"})
    assert login_response.status_code == 200
    auth_token = login_response.json()["access_token"]
    headers = {"Authorization": f"Bearer {auth_token}"}

    response = client.post(
        "api/v1/payments/send",
        headers=headers,
        json={
            "to_user_email": "user@example.com",
            "amount": 100.50,
            "description": "test"
        }
    )
    assert response.status_code == 200
    assert "Payment completed successfully" in response.json()["message"]

def test_transaction_send_minimum_amount_1():
    login_response = client.post("api/v1/auth/login", json={"email": "test@example.com", "password": "password123"})
    auth_token = login_response.json()["access_token"]
    headers = {"Authorization": f"Bearer {auth_token}"}

    response = client.post(
        "api/v1/payments/send",
        headers=headers,
        json={
            "to_user_email": "user@example.com",
            "amount": 0.01,
            "description": "test"
        }
    )
    assert response.status_code == 200

def test_transaction_send_minimum_amount_2():
    login_response = client.post("api/v1/auth/login", json={"email": "user@example.com", "password": "password123"})
    auth_token = login_response.json()["access_token"]
    headers = {"Authorization": f"Bearer {auth_token}"}

    response = client.post(
        "api/v1/payments/send",
        headers=headers,
        json={
            "to_user_email": "test@example.com",
            "amount": 0.01,
            "description": "test"
        }
    )
    assert response.status_code == 200

def test_transaction_send_without_description_1():
    login_response = client.post("api/v1/auth/login", json={"email": "test@example.com", "password": "password123"})
    auth_token = login_response.json()["access_token"]
    headers = {"Authorization": f"Bearer {auth_token}"}

    response = client.post(
        "api/v1/payments/send",
        headers=headers,
        json={
            "to_user_email": "mario@example.com",
            "amount": 50.00
        }
    )
    assert response.status_code == 200

def test_transaction_send_without_description_2():
    login_response = client.post("api/v1/auth/login", json={"email": "mario@example.com", "password": "password123"})
    auth_token = login_response.json()["access_token"]
    headers = {"Authorization": f"Bearer {auth_token}"}

    response = client.post(
        "api/v1/payments/send",
        headers=headers,
        json={
            "to_user_email": "test@example.com",
            "amount": 50.00
        }
    )
    assert response.status_code == 200


def test_transaction_send_large_amount():
    login_response = client.post("api/v1/auth/login", json={"email": "test@example.com", "password": "password123"})
    auth_token = login_response.json()["access_token"]
    headers = {"Authorization": f"Bearer {auth_token}"}

    response = client.post(
        "api/v1/payments/send",
        headers=headers,
        json={
            "to_user_email": "user@example.com",
            "amount": 9999.99,
            "description": "test"
        }
    )
    assert response.status_code == 400
    assert "insufficient balance" in response.json()["detail"].lower()


def test_transaction_send_to_invalid_user():
    login_response = client.post("api/v1/auth/login", json={"email": "user@example.com", "password": "password123"})
    auth_token = login_response.json()["access_token"]
    headers = {"Authorization": f"Bearer {auth_token}"}

    response = client.post(
        "api/v1/payments/send",
        headers=headers,
        json={
            "to_user_email": "testnotexists@example.com",
            "amount": 50.00
        }
    )
    assert response.status_code == 404
    assert "destination wallet not found" in response.json()["detail"].lower()


def test_transaction_send_negative_amount():
    login_response = client.post("api/v1/auth/login", json={"email": "user@example.com", "password": "password123"})
    auth_token = login_response.json()["access_token"]
    headers = {"Authorization": f"Bearer {auth_token}"}

    response = client.post(
        "api/v1/payments/send",
        headers=headers,
        json={
            "to_user_email": "mario@example.com",
            "amount": -10.00
        }
    )
    assert response.status_code == 422


def test_transaction_send_zero_amount():
    login_response = client.post("api/v1/auth/login", json={"email": "user@example.com", "password": "password123"})
    auth_token = login_response.json()["access_token"]
    headers = {"Authorization": f"Bearer {auth_token}"}

    response = client.post(
        "api/v1/payments/send",
        headers=headers,
        json={
            "to_user_email": "mario@example.com",
            "amount": 0.00
        }
    )
    assert response.status_code == 422


def test_transaction_send_to_self():
    login_response = client.post("api/v1/auth/login", json={"email": "user@example.com", "password": "password123"})
    auth_token = login_response.json()["access_token"]
    headers = {"Authorization": f"Bearer {auth_token}"}

    response = client.post(
        "api/v1/payments/send",
        headers=headers,
        json={
            "to_user_email": "user@example.com",
            "amount": 100.00
        }
    )
    assert response.status_code == 400
    assert "cannot transfer to the same wallet" in response.json()["detail"].lower()


def test_transaction_send_missing_fields():
    login_response = client.post("api/v1/auth/login", json={"email": "user@example.com", "password": "password123"})
    auth_token = login_response.json()["access_token"]
    headers = {"Authorization": f"Bearer {auth_token}"}

    response = client.post(
        "api/v1/payments/send",
        headers=headers,
        json={
            "amount": 100.00
        }
    )
    assert response.status_code == 422