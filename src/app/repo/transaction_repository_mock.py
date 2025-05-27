from typing import Dict, Optional, List
from ..repo.transaction_repository_interface import ITransactionsRepository
from ..entities.transaction import Transaction

class TransactionRepositoryMock(ITransactionsRepository):
    transactions: Dict[int, Transaction]
    
    def __init__(self):
        self.transactions = {
            1: Transaction(type="deposit", value=20.0, current_balance=1000.0, timestamp=20.0),
            2: Transaction(type="deposit", value=40.0, current_balance=850.0, timestamp=35.0),
            3: Transaction(type="withdrawal", value=120.0, current_balance=550.0, timestamp=45.0),
            4: Transaction(type="withdrawal", value=160.0, current_balance=1500.0, timestamp=45.0)
        }
        
    def get_all_transactions(self) -> List[Transaction]:
        return self.transactions.values()
    
    def get_transaction(self, type: str) -> Optional[Transaction]:
        return self.transactions.get(type, None)
    
    def create_transaction(self, aux_type, value, current_balance, timestamp):
        new_transaction = Transaction(type=aux_type, value=value, current_balance=current_balance, timestamp=timestamp)
        self.transactions[aux_type] = new_transaction
        return new_transaction
    
    def delete_transaction(self, timestamp: float) -> Transaction:
        transaction = self.transactions.pop(timestamp, None)
        return transaction

