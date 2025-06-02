from typing import Dict, List
from ..entities.User import User
from ..repo.user_repository_interface import IUserRepository
from ..entities.transaction import Transaction

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
    
    def get_user(self, user_id: int) -> User:
        return self.users.get(user_id)
        
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
        
        
    def update_user(self, user_id: int, name:str, agency: int, account: str, current_balance: float) -> User:
        user = self.users.get(user_id)
        if user:
            user.name=name,
            user.agency=agency,
            user.account=account,
            user.current_balance=current_balance
            return user
        return None


    def to_dict(self):
        return {
            "name": self.name,
            "agency": self.agency,
            "account": self.account,
            "current_balance": self.current_balance
        }