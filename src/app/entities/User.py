from typing import Tuple
from errors.entity_errors import ParamNotValidated

class User:
    name: str
    agency: int
    account: str
    current_balance: float

    def __init__(self, name: str=None, agency: int=None, account: str=None, current_balance: float=None):
        validation_name = self.validate_name(name)
        if validation_name[0] is False:
            raise ParamNotValidated("name", validation_name[1])
        self.name = name
        
        validation_current_balance = self.validate_current_balance(current_balance)
        if validation_current_balance[0] is False:
            raise ParamNotValidated("current_balance", validation_current_balance[1])
        self.current_balance = current_balance

        validation_agency = self.validate_agency(agency)
        if validation_agency[0] is False:
            raise ParamNotValidated("agency", validation_agency[1])
        self.agency = agency
        
        validation_account = self.validate_account(account)
        if validation_account[0] is False:
            raise ParamNotValidated("account", validation_account[1])
        self.account = account
        
    @staticmethod
    def validate_name(name: str) -> Tuple[bool, str]:
        if name is None:
            return (False, "Name is required")
        if type(name) != str:
            return (False, "Name must be a string")
        if len(name) < 3:
            return (False, "Name must be at least 3 characters long")
        return (True, "")
        
    @staticmethod
    def validate_current_balance(current_balance: float) -> Tuple[bool, str]:
        if current_balance is None:
            return (False, "Current balance is required")
        if type(current_balance) != float:
            return (False, "Current balance must be a float")
        if current_balance < 0:
            return (False, "Current balance can't be negative")
        return (True, "")
    
    @staticmethod
    def validate_agency(agency: int) -> Tuple[bool, str]:
        if agency is None:
            return (False, "agency is required")
        if type(agency) != int:
            return (False, "agency must be a integer")
        if not agency >= 1000 & agency <= 9999:
            return (False, "agency must be a positive number")
        return (True, "")

    @staticmethod
    def validate_account(account: str) -> Tuple[bool, str]:
        if account is None:
            return (False, "account is required")
        if type(account) != str:
            return (False, "account must be a string")
        if account[-2] != "-":
            return (False, "account must be on the format XXXXX-X")
        if len(account) != 7:
            return (False, "account must be on the format XXXXX-X")
        if not account[:5].isdigit():
            return (False, "account must be on the format XXXXX-X")
        if not account[-1].isdigit():
            return (False, "account must be on the format XXXXX-X")
        return (True, "")
    
    def to_dict(self):
        return {
            "name": self.name,
            "agency": self.agency,
            "account": self.account,
            "current_balance": self.current_balance
        }
    