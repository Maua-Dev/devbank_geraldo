from typing import Dict, Optional, List

from src.app.entities.user import User
from src.app.repo.user_repository_interface import IUserRepository
from ..enums.item_type_enum import ItemTypeEnum
from ..entities.transaction import Transaction
from ..entities.item import Item

class UserRepositoryMock(IUserRepository):
    users: Dict[int, Transaction]
    
    def __init__(self):
        self.users = {
            1: User(name="Geraldo", agency= 1000, account= "10000-5", current_balance= 1000.0),
            2: User(name="Leo", agency= 1500, account= "12000-5", current_balance= 1200.0),
            3: User(name="Rodas", agency= 1600, account= "13000-5", current_balance= 1800.0),
            4: User(name="Soller", agency= 1900, account= "15000-5", current_balance= 5000.0),
        }
        
    def get_all_users(self) -> List[User]:
        return self.users.values()
    
    def get_user(self, name):
        return self.users.get(name, None)
    
    def create_user(self, user: User):
        name = user.name
        agency = user.agency
        account = user.account
        current_balance = user.current_balance
        user = User(name=name, agency=agency, account=account, current_balance=current_balance)
        self.users[name] = user
    
    def delete_user(self, name: str) -> User:
        user = self.users.pop(name, None)
        return user
        
        
    def update_user(self, name="Soller", agency= 1900, account= "15000-5", current_balance= 5000.0) -> User:
        user = self.users.get(name, None)
        if user is None:
            return None
        
        if name is not None:
            user.name = name
        if agency is not None:
            user.agency = agency
        if account is not None:
            user.account = account
        if current_balance is not None:
            user.current_balance = current_balance
        self.users[name] = user
        
        return user
