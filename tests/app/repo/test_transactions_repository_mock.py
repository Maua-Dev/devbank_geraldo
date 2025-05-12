import pytest
from src.app.entities.transaction import Transaction
from src.app.enums.item_type_enum import ItemTypeEnum
from src.app.repo.transaction_repository_mock import TransactionRepositoryMock

class Test_TransactionRepositoryMock:
    def test_get_all_transactions(self):
        repo = TransactionRepositoryMock()
        
        assert all([transaction_expect == transaction for transaction_expect, transaction in zip(repo.transactions.values(), repo.get_all_transactions())]) 
        
    def test_get_transaction(self):
        repo = TransactionRepositoryMock()
        transaction = repo.get_transaction(type="withdrawal")
        
        assert transaction == repo.transactions.get("withdrawal")
    
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
        transaction_expected_to_be_deleted = repo.transactions.get(1)
        len_before = len(repo.transactions)
        
        transaction = repo.delete_transaction(timestamp=1.0)
        len_after = len(repo.transactions)
        
        assert len_after == len_before - 1
        assert transaction == transaction_expected_to_be_deleted
        
    def test_delete_transaction_not_found(self):
        repo = TransactionRepositoryMock()
        transaction = repo.delete_transaction(timestamp=10.0)
        
        assert transaction is None