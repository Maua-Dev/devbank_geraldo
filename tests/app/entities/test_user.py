import pytest
from src.app.entities.User import User
from src.app.errors.entity_errors import ParamNotValidated

class Test_user:
    def test_user(self):
        user = User("Geraldo", 2005, "10000-9", 1000.0)
        assert user.name == "Geraldo"
        assert user.agency == 2005
        assert user.account == "10000-9"
        assert user.current_balance == 1000.0

    def test_user_name_none(self):
        with pytest.raises(ParamNotValidated):
            User(agency=2005, account="10000-9", current_balance=1000.0)

    def test_user_name_type(self):
        with pytest.raises(ParamNotValidated):
            User(name= 10, agency=2005, account="10000-9", current_balance=1000.0)

    def test_user_agency_none(self):
        with pytest.raises(ParamNotValidated):
            User(name= "Geraldo", account="10000-9", current_balance=1000.0)

    def test_user_account_none(self):
        with pytest.raises(ParamNotValidated):
            User(name= "Geraldo", agency=2005, current_balance=1000.0)

    def test_user_current_balance_none(self):
        with pytest.raises(ParamNotValidated):
            User(name= "Geraldo", agency=2005, account="10000-9")

    def test_user_agency_invalid_format(self):
        with pytest.raises(ParamNotValidated):
            User(name= "Geraldo", agency="Geraldo", account="10000-9", current_balance=1000.0)

    def test_user_account_invalid_format(self):
        with pytest.raises(ParamNotValidated):
            User(name= "Geraldo", agency=2005, account="1000b-9", current_balance=1000.0)

    def test_user_current_balance_invalid_value(self):
        with pytest.raises(ParamNotValidated):
            User(name= "Geraldo", agency=2005, account="10000-9", current_balance=-10.0)

