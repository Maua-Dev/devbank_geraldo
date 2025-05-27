import pytest
from src.app.repo.user_repository_mock import UserRepositoryMock
from src.app.entities.User import User

class Test_UserRepositoryMock:
    def test_get_all_users(self):
        repo = UserRepositoryMock()
        user = repo.get_all_users()


        assert all([user_expect == user for user_expect, user in zip(repo.users.values(), repo.get_all_users())])

    def test_get_user(self):
        repo = UserRepositoryMock()
        user = repo.get_user(name="Geraldo")

        assert user.to_dict() == {
            "name": "Geraldo",
            "agency": 1000,
            "account": "10000-5",
            "current_balance": 1000.0
        }

    def test_get_user_not_found(self):
        repo = UserRepositoryMock()
        user = repo.get_user(name="test")

        assert user is None

    def test_create_user(self):
        repo = UserRepositoryMock()
        len_before = len(repo.users)
        user = User(name="test", agency=1000, account="10000-5", current_balance=1000.0)
        repo.create_user(user)
        len_after = len(repo.users)

        assert len_after == len_before + 1
        assert repo.users.get("test").name == user.name
        assert repo.users.get("test").agency == user.agency
        assert repo.users.get("test").account == user.account
        assert repo.users.get("test").current_balance == user.current_balance
        
    def test_delete_user_not_found(self):
        repo = UserRepositoryMock()
        user = repo.delete_user(name="test")

        assert user is None

    
    

    