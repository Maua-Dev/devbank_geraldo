from abc import ABC, abstractmethod
from typing import List, Optional
from ..entities.User import User
from ..entities.transaction import Transaction


class IUserRepository(ABC):
    
    
    @abstractmethod
    def get_all_users(self) -> List[User]:
        '''
        Returns all the users in the database 
        '''
        pass
    
    @abstractmethod
    def get_user(self, name: str) -> Optional[User]:
        '''
        Returns the users with the given id.
        If the users does not exist, returns None
        '''
        pass
    
    @abstractmethod
    def create_user(self, name: str, agency: int, account: str, current_balance: float) -> Transaction:
        '''
        Creates a new user in the database
        '''
        pass
    
    @abstractmethod
    def delete_user(self, name: str) -> User:
        '''
        Deletes the user with the given id.
        If the user does not exist, returns None
        '''
        
    @abstractmethod
    def update_user(self, name: str, agency: int, account: str, current_balance: float) -> Transaction:
        '''
        Updates the user with the given id.
        If the user does not exist, returns None
        '''
        pass
    
    