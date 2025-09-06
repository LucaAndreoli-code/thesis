from fastapi.testclient import TestClient
from src.main import app
from src.tests import user_token, mario_token, test_token

client = TestClient(app)

def test_get_balance_success():
    response = client.get(
        "/api/v1/wallet/balance",
        headers={"Authorization": f"Bearer {user_token}"}
    )
    assert response.status_code == 200
    data = response.json()
    assert "balance" in data
    assert "currency" in data
    assert isinstance(float(data["balance"]), float)
    assert data["currency"] == "EUR"

def test_get_balance_mario_success():
    response = client.get(
        "/api/v1/wallet/balance",
        headers={"Authorization": f"Bearer {mario_token}"}
    )
    assert response.status_code == 200
    data = response.json()
    assert "balance" in data
    assert "currency" in data

def test_get_balance_test_user_success():
    response = client.get(
        "/api/v1/wallet/balance",
        headers={"Authorization": f"Bearer {test_token}"}
    )
    assert response.status_code == 200
    data = response.json()
    assert "balance" in data
    assert "currency" in data

def test_get_balance_unauthorized():
    response = client.get("/api/v1/wallet/balance")
    assert response.status_code == 403
    assert response.json()["detail"] == "Not authenticated"

def test_deposit_wrong_card_number_length():
    response = client.post(
        "/api/v1/wallet/deposit",
        headers={"Authorization": f"Bearer {user_token}"},
        json={
            "amount": 100.00,
            "card_number": "11112222333344441111222233334444",  # 14 digits
            "card_holder": "Test User",
            "expiry_month": 12,
            "expiry_year": 2025,
            "cvv": "123"
        }
    )
    assert response.status_code == 422

def test_deposit_success():
    response = client.post(
        "/api/v1/wallet/deposit",
        headers={"Authorization": f"Bearer {user_token}"},
        json={
            "amount": 100.50,
            "card_number": "1111222233334444",
            "card_holder": "Test User",
            "expiry_month": 12,
            "expiry_year": 2025,
            "cvv": "123"
        }
    )
    assert response.status_code == 200
    data = response.json()
    assert "transaction_id" in data
    assert "reference_code" in data
    assert "status" in data
    assert "message" in data
    assert "new_balance" in data
    assert data["status"] == "completed"

def test_deposit_mario_success():
    response = client.post(
        "/api/v1/wallet/deposit",
        headers={"Authorization": f"Bearer {mario_token}"},
        json={
            "amount": 250.00,
            "card_number": "1111222233334444",
            "card_holder": "Mario Rossi",
            "expiry_month": 6,
            "expiry_year": 2026,
            "cvv": "456"
        }
    )
    assert response.status_code == 200
    data = response.json()
    assert "transaction_id" in data
    assert "new_balance" in data

def test_deposit_maximum_valid_amount():
    response = client.post(
        "/api/v1/wallet/deposit",
        headers={"Authorization": f"Bearer {test_token}"},
        json={
            "amount": 10000.00,
            "card_number": "1111222233334444",
            "card_holder": "Test User",
            "expiry_month": 12,
            "expiry_year": 2025,
            "cvv": "321"
        }
    )
    assert response.status_code == 200

def test_deposit_card_number_with_spaces():
    response = client.post(
        "/api/v1/wallet/deposit",
        headers={"Authorization": f"Bearer {user_token}"},
        json={
            "amount": 50.00,
            "card_number": "1111222233334444",
            "card_holder": "Test User",
            "expiry_month": 8,
            "expiry_year": 2026,
            "cvv": "654"
        }
    )
    assert response.status_code == 200

def test_deposit_invalid_amount_negative():
    response = client.post(
        "/api/v1/wallet/deposit",
        headers={"Authorization": f"Bearer {user_token}"},
        json={
            "amount": -50.00,
            "card_number": "1111222233334444",
            "card_holder": "Test User",
            "expiry_month": 12,
            "expiry_year": 2025,
            "cvv": "123"
        }
    )
    assert response.status_code == 422

def test_deposit_invalid_amount_zero():
    response = client.post(
        "/api/v1/wallet/deposit",
        headers={"Authorization": f"Bearer {user_token}"},
        json={
            "amount": 0.00,
            "card_number": "1111222233334444",
            "card_holder": "Test User",
            "expiry_month": 12,
            "expiry_year": 2025,
            "cvv": "123"
        }
    )
    assert response.status_code == 422

def test_deposit_invalid_amount_too_high():
    response = client.post(
        "/api/v1/wallet/deposit",
        headers={"Authorization": f"Bearer {user_token}"},
        json={
            "amount": 15000.00,
            "card_number": "1111222233334444",
            "card_holder": "Test User",
            "expiry_month": 12,
            "expiry_year": 2025,
            "cvv": "123"
        }
    )
    assert response.status_code == 422

def test_deposit_invalid_card_number_short():
    response = client.post(
        "/api/v1/wallet/deposit",
        headers={"Authorization": f"Bearer {user_token}"},
        json={
            "amount": 100.00,
            "card_number": "123456789012345",
            "card_holder": "Test User",
            "expiry_month": 12,
            "expiry_year": 2025,
            "cvv": "123"
        }
    )
    assert response.status_code == 422

def test_deposit_invalid_card_number_long():
    response = client.post(
        "/api/v1/wallet/deposit",
        headers={"Authorization": f"Bearer {user_token}"},
        json={
            "amount": 100.00,
            "card_number": "11112222333344447",
            "card_holder": "Test User",
            "expiry_month": 12,
            "expiry_year": 2025,
            "cvv": "123"
        }
    )
    assert response.status_code == 422

def test_deposit_invalid_card_number_non_numeric():
    response = client.post(
        "/api/v1/wallet/deposit",
        headers={"Authorization": f"Bearer {user_token}"},
        json={
            "amount": 100.00,
            "card_number": "abcd5678901234ef",
            "card_holder": "Test User",
            "expiry_month": 12,
            "expiry_year": 2025,
            "cvv": "123"
        }
    )
    assert response.status_code == 422

def test_deposit_unauthorized():
    response = client.post(
        "/api/v1/wallet/deposit",
        json={
            "amount": 100.00,
            "card_number": "1111222233334444",
            "card_holder": "Test User",
            "expiry_month": 12,
            "expiry_year": 2025,
            "cvv": "123"
        }
    )
    assert response.status_code == 403
    assert response.json()["detail"] == "Not authenticated" 

def test_deposit_missing_required_fields():
    response = client.post(
        "/api/v1/wallet/deposit",
        headers={"Authorization": f"Bearer {user_token}"},
        json={
            "amount": 100.00,
            "card_number": "1111222233334444",
        }
    )
    assert response.status_code == 422

# POST /api/v1/wallet/withdraw Tests
def test_withdraw_success():
    response = client.post(
        "/api/v1/wallet/withdraw",
        headers={"Authorization": f"Bearer {user_token}"},
        json={
            "amount": 50.00,
            "bank_account": "IT641217273217213979271321",
            "back_account_name": "Test User"
        }
    )
    assert response.status_code == 200
    data = response.json()
    assert "transaction_id" in data
    assert "reference_code" in data
    assert "status" in data
    assert "message" in data
    assert "new_balance" in data
    assert data["status"] == "completed"

def test_withdraw_mario_success():
    response = client.post(
        "/api/v1/wallet/withdraw",
        headers={"Authorization": f"Bearer {mario_token}"},
        json={
            "amount": 25.00,
            "bank_account": "IT641217273217213979271321",
            "back_account_name": "Mario Rossi"
        }
    )
    assert response.status_code == 200
    data = response.json()
    assert "transaction_id" in data
    assert "new_balance" in data

def test_withdraw_minimum_amount():
    response = client.post(
        "/api/v1/wallet/withdraw",
        headers={"Authorization": f"Bearer {test_token}"},
        json={
            "amount": 0.01,
            "bank_account": "IT641217273217213979271321",
            "back_account_name": "Test User"
        }
    )
    assert response.status_code == 200

def test_withdraw_maximum_valid_amount():
    response = client.post(
        "/api/v1/wallet/withdraw",
        headers={"Authorization": f"Bearer {test_token}"},
        json={
            "amount": 99999.00,
            "bank_account": "IT641217273217213979271321",
            "back_account_name": "Test User"
        }
    )
    assert response.status_code == 422
    assert 'Amount must be between 0 and 50000' in str(response.json()["detail"])

def test_withdraw_invalid_amount_negative():
    response = client.post(
        "/api/v1/wallet/withdraw",
        headers={"Authorization": f"Bearer {user_token}"},
        json={
            "amount": -25.00,
            "bank_account": "IT641217273217213979271321",
            "back_account_name": "Test User"
        }
    )
    assert response.status_code == 422

def test_withdraw_invalid_amount_zero():
    response = client.post(
        "/api/v1/wallet/withdraw",
        headers={"Authorization": f"Bearer {user_token}"},
        json={
            "amount": 0.00,
            "bank_account": "IT641217273217213979271321",
            "back_account_name": "Test User"
        }
    )
    assert response.status_code == 422

def test_withdraw_invalid_amount_too_high():
    response = client.post(
        "/api/v1/wallet/withdraw",
        headers={"Authorization": f"Bearer {user_token}"},
        json={
            "amount": 75000.00,
            "bank_account": "IT641217273217213979271321",
            "back_account_name": "Test User"
        }
    )
    assert response.status_code == 422

def test_withdraw_insufficient_funds():
    response = client.post(
        "/api/v1/wallet/withdraw",
        headers={"Authorization": f"Bearer {user_token}"},
        json={
            "amount": 50000.00,
            "bank_account": "IT641217273217213979271321",
            "back_account_name": "Test User"
        }
    )
    assert response.status_code == 400
    assert "insufficient balance" in response.json()["detail"].lower()

def test_withdraw_unauthorized():
    response = client.post(
        "/api/v1/wallet/withdraw",
        json={
            "amount": 50.00,
            "bank_account": "IT641217273217213979271321",
            "back_account_name": "Test User"
        }
    )
    assert response.status_code == 403
    assert response.json()["detail"] == "Not authenticated"

def test_withdraw_missing_required_fields():
    response = client.post(
        "/api/v1/wallet/withdraw",
        headers={"Authorization": f"Bearer {user_token}"},
        json={
            "amount": 50.00
        }
    )
    assert response.status_code == 422

def test_withdraw_missing_bank_account():
    response = client.post(
        "/api/v1/wallet/withdraw",
        headers={"Authorization": f"Bearer {user_token}"},
        json={
            "amount": 50.00,
            "back_account_name": "Test User"
        }
    )
    assert response.status_code == 422

def test_withdraw_missing_account_name():
    response = client.post(
        "/api/v1/wallet/withdraw",
        headers={"Authorization": f"Bearer {user_token}"},
        json={
            "amount": 50.00,
            "bank_account": "IT641217273217213979271321"
        }
    )
    assert response.status_code == 422