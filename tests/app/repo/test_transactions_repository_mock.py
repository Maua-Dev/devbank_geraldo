import pytest
from src.app.repo.transaction_repository_mock import TransactionRepositoryMock

class Test_TransactionRepositoryMock:
    def test_get_all_transactions(self):
        repo = TransactionRepositoryMock()
        
        assert all([transaction_expect == transaction for transaction_expect, transaction in zip(repo.transactions, repo.get_all_transactions())]) 
        
    def test_get_transaction(self):
        repo = TransactionRepositoryMock()
        transaction = repo.get_transaction(type="withdrawal")
        
        expected_transaction = next((t for t in repo.transactions if t.type == "withdrawal"), None)
        assert transaction == expected_transaction

    
    def test_get_transaction_not_found(self):
        repo = TransactionRepositoryMock()
        transaction = repo.get_transaction(type="test")
        
        assert transaction is None
        
    def test_create_transaction(self):
        repo = TransactionRepositoryMock()
        len_before = len(repo.transactions)
        transaction = repo.create_transaction(aux_type="deposit", value=160.0, current_balance=1500.0, timestamp=45.0)
        len_after = len(repo.transactions)

        assert transaction.type == "deposit"
        assert transaction.value == 160.0
        assert transaction.current_balance == 1500.0
        assert transaction.timestamp == 45.0
        assert len_after == len_before + 1

        
    def test_delete_transaction(self):
        repo = TransactionRepositoryMock()
        transaction_expected_to_be_deleted = repo.transactions[1]

        len_before = len(repo.transactions)

        transaction = repo.delete_transaction(timestamp=transaction_expected_to_be_deleted.timestamp)
        len_after = len(repo.transactions)

        assert transaction == transaction_expected_to_be_deleted
        assert len_after == len_before - 1

        
    def test_delete_transaction_not_found(self):
        repo = TransactionRepositoryMock()
        transaction = repo.delete_transaction(timestamp=10.0)
        
        assert transaction is None