import pytest
import time
from fastapi.exceptions import HTTPException
from src.app.main import deposit, get_all_transactions, get_user_data, withdrawal
from src.app.repo.transaction_repository_mock import TransactionRepositoryMock
from src.app.repo.user_repository_mock import UserRepositoryMock

class Test_Main:

    def test_get_user_data(self):
        repo = UserRepositoryMock()
        user = get_user_data(name="Geraldo")

        assert user == {
            "name": "Geraldo",
            "agency": 1000,
            "account": "10000-5",
            "current_balance": 1000.0
        }



    def test_get_user_not_found(self):
        repo = UserRepositoryMock()
        with pytest.raises(HTTPException) as err:
            get_user_data(name="naoexiste")

        assert err.value.status_code == 404
        assert err.value.detail == "User Not found"

    def test_deposit(self):
        repo = UserRepositoryMock()
        body = {
            "name": "Geraldo",
            "2": 1,
            "5": 1,
            "10": 1,
            "20": 1,
            "50": 1,
            "100": 1,
            "200": 1
        }
        response = deposit(request=body)

        assert response["current_balance"] == 1000.0 + (2 + 5 + 10 + 20 + 50 + 100 + 200)
        assert response["timestamp"] > 0

    def test_deposit_invalid_quantity(self):
        repo = UserRepositoryMock()
        body = {
            "name": "Geraldo",
            "2": "errado",
            "5": 1,
            "10": 1,
            "20": 1,
            "50": 1,
            "100": 1,
            "200": 1
        }
        with pytest.raises(HTTPException) as err:
            deposit(request=body)

        assert err.value.status_code == 400
        assert err.value.detail == "Invalid quantity for note 2"

    def test_deposit_suspicious_amount(self):
        repo = UserRepositoryMock()
        body = {
            "name": "Geraldo",
            "2": 1000,
            "5": 1000,
            "10": 1000,
            "20": 1000,
            "50": 1000,
            "100": 1000,
            "200": 1000
        }
        with pytest.raises(HTTPException) as err:
            deposit(request=body)

        assert err.value.status_code == 403
        assert err.value.detail == "Suspicious deposit amount"

    def test_deposit_invalid_amount(self):
        repo = UserRepositoryMock()
        body = {
            "name": "Geraldo",
            "2": 0,
            "5": 0,
            "10": 0,
            "20": 0,
            "50": 0,
            "100": 0,
            "200": 0
        }
        with pytest.raises(HTTPException) as err:
            deposit(request=body)

        assert err.value.status_code == 400
        assert err.value.detail == "Invalid deposit amount"

    def test_withdrawal(self):
        repo = UserRepositoryMock()
        body = {
            "name": "Geraldo",
            "2": 1,
            "5": 1,
            "10": 1,
            "20": 1,
            "50": 1,
            "100": 1,
            "200": 1
        }
        response = withdrawal(request=body)

        assert response["current_balance"] == 1000.0 - (2 + 5 + 10 + 20 + 50 + 100 + 200)
        assert response["timestamp"] > 0

    def test_withdrawal_invalid_quantity(self):
        repo = UserRepositoryMock()
        body = {
            "name": "Geraldo",
            "2": "errado",
            "5": 1,
            "10": 1,
            "20": 1,
            "50": 1,
            "100": 1,
            "200": 1
        }
        with pytest.raises(HTTPException) as err:
            withdrawal(request=body)

        assert err.value.status_code == 400
        assert err.value.detail == "Invalid quantity for note 2"
    
    def test_withdrawal_insufficient_balance(self):
        repo = UserRepositoryMock()
        body = {
            "name": "Geraldo",
            "2": 1000,
            "5": 1000,
            "10": 1000,
            "20": 1000,
            "50": 1000,
            "100": 1000,
            "200": 1000
        }
        with pytest.raises(HTTPException) as err:
            withdrawal(request=body)

        assert err.value.status_code == 403
        assert err.value.detail == "Saldo insuficiente para transação"

    def test_get_all_transactions(self):
        repo = TransactionRepositoryMock()

        response = repo.get_all_transactions()

        expected_transactions = [
            {"type": "deposit", "value": 20.0, "current_balance": 1000.0, "timestamp": 20.0},
            {"type": "deposit", "value": 40.0, "current_balance": 850.0, "timestamp": 35.0},
            {"type": "withdrawal", "value": 120.0, "current_balance": 550.0, "timestamp": 45.0},
            {"type": "withdrawal", "value": 160.0, "current_balance": 1500.0, "timestamp": 45.0},
        ]
        response_dicts = [t.__dict__ for t in response]

        assert response_dicts == expected_transactions

        