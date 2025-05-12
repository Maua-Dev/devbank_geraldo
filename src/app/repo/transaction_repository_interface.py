from abc import ABC, abstractmethod
from typing import List, Optional, Tuple

from ..enums.item_type_enum import ItemTypeEnum
from ..entities.transaction import Transaction
from ..entities.item import Item


class ITransactionsRepository(ABC):
    
    
    @abstractmethod
    def get_all_transactions(self) -> List[Transaction]:
        '''
        Returns all the transactions in the database 
        '''
        pass
    
    @abstractmethod
    def get_transaction(self, type: str) -> Optional[Transaction]:
        '''
        Returns the transaction with the given id.
        If the transaction does not exist, returns None
        '''
        pass
    
    @abstractmethod
    def create_transaction(self, type: str, value: float, current_balance: float, timestamp: float) -> Transaction:
        '''
        Creates a new transaction in the database
        '''
        pass
    
    @abstractmethod
    def delete_transaction(self, timestamp: float) -> Transaction:
        '''
        Deletes the transaction with the given id.
        If the transaction does not exist, returns None
        '''
    
    