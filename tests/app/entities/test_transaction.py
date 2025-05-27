import pytest
from src.app.entities.transaction import Transaction
from src.app.errors.entity_errors import ParamNotValidated

class Test_transaction:
    def test_transaction(self):

        transaction = Transaction("deposit", 1000.0, 1000.0, 1672531199.0)
        assert transaction.type == "deposit"
        assert transaction.value == 1000.0
        assert transaction.current_balance == 1000.0
        assert transaction.timestamp == 1672531199.0
        
    def test_transaction_type_none(self):
        with pytest.raises(ParamNotValidated):
            Transaction(value=1000.0, current_balance=1000.0, timestamp=1672531199.0)
    
    def test_transaction_type_invalid(self):
        with pytest.raises(ParamNotValidated):
            Transaction(type="invalid_type", value=1000.0, current_balance=1000.0, timestamp=1672531199.0)

    def test_transaction_value_none(self):
        with pytest.raises(ParamNotValidated):
            Transaction(type="deposit", current_balance=1000.0, timestamp=1672531199.0)
    
    def test_transaction_value_invalid_format(self):
        with pytest.raises(ParamNotValidated):
            Transaction(type="deposit", value="invalid_value", current_balance=1000.0, timestamp=1672531199.0)

    def test_transaction_value_invalid_value(self):
        with pytest.raises(ParamNotValidated):
            Transaction(type="deposit", value=-1000.0, current_balance=1000.0, timestamp=1672531199.0)
        
    def test_transaction_current_balance_none(self):
        with pytest.raises(ParamNotValidated):
            Transaction(type="deposit", value=1000.0, timestamp=1672531199.0)
    
    def test_transaction_current_balance_invalid_format(self):
        with pytest.raises(ParamNotValidated):
            Transaction(type="deposit", value=1000.0, current_balance="invalid_balance", timestamp=1672531199.0)
        
    def test_transaction_current_balance_invalid_value(self):
        with pytest.raises(ParamNotValidated):
            Transaction(type="deposit", value=1000.0, current_balance=-1000.0, timestamp=1672531199.0)
    
    def test_transaction_timestamp_none(self):
        with pytest.raises(ParamNotValidated):
            Transaction(type="deposit", value=1000.0, current_balance=1000.0)
    
    def test_transaction_timestamp_invalid_format(self):
        with pytest.raises(ParamNotValidated):
            Transaction(type="deposit", value=1000.0, current_balance=1000.0, timestamp="invalid_timestamp")

    def test_transaction_timestamp_invalid_value(self):
        with pytest.raises(ParamNotValidated):
            Transaction(type="deposit", value=1000.0, current_balance=1000.0, timestamp=-1672531199.0)

    