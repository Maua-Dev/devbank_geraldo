import time
from fastapi import FastAPI, HTTPException
from fastapi.param_functions import Body
from mangum import Mangum
from .environments import Environments


app = FastAPI()

user_repo = Environments.get_user_repo()
transacation_repo = Environments.get_transaction_repo()

@app.get("/")
def get_user_data():    

    user = user_repo.get_user(user_id=1)

    if not user:
        raise HTTPException(status_code=404, detail="User Not found")

    return user.to_dict()  

@app.post("/deposit")
def deposit(request: dict = Body(...), user_repo=user_repo):
    user = user_repo.get_user(user_id=1)


    if not user:
        raise HTTPException(status_code=404, detail="User Not found")
    
    accepted_notes = [2, 5, 10, 20, 50, 100, 200]
    total_deposit = 0

    for note in accepted_notes:
        quantity = request.get(str(note), 0)

        if not isinstance(quantity, int) or quantity < 0:
            raise HTTPException(status_code=400, detail=f"Invalid quantity for note {note}")
        total_deposit += note * quantity

    if total_deposit >= 2 * user.current_balance:
        raise HTTPException(status_code=403, detail="Suspicious deposit amount")
    if total_deposit <= 0:
        raise HTTPException(status_code=400, detail="Invalid deposit amount")
    
    user.current_balance = user.current_balance + total_deposit
    current_balance = user.current_balance

    current_time = time.time() * 1000
    
    user_repo.update_user(
        name=user.name,
        agency=user.agency,
        account=user.account,
        current_balance=current_balance)

    transaction = transacation_repo.create_transaction(
        aux_type="deposit",
        value=float(total_deposit),
        current_balance=current_balance,
        timestamp=current_time
    )
    return {
        "current_balance": current_balance,
        "timestamp": current_time,
    }

@app.post("/withdrawal")
def withdrawal(request: dict = Body(...), user_repo=user_repo):
    user = user_repo.get_user(user_id=1)

    if not user:
        raise HTTPException(status_code=404, detail="User Not found")
    
    accepted_notes = [2, 5, 10, 20, 50, 100, 200]
    total_withdrawal = 0

    for note in accepted_notes:
        quantity = request.get(str(note), 0)

        if not isinstance(quantity, int) or quantity < 0:
            raise HTTPException(status_code=400, detail=f"Invalid quantity for note {note}")
        total_withdrawal += note * quantity

    if total_withdrawal > user.current_balance:
        raise HTTPException(status_code=403, detail="Saldo insuficiente para transação")
    if total_withdrawal < 0:
        raise HTTPException(status_code=403, detail="Saldo insuficiente para transação")
    
    user.current_balance = user.current_balance - total_withdrawal
    current_balance = user.current_balance

    user_repo.update_user(
        name=user.name,
        agency=user.agency,
        account=user.account,
        current_balance=current_balance
    )

    current_time = time.time() * 1000

    transaction = transacation_repo.create_transaction(
        aux_type="withdrawal",
        value=float(total_withdrawal),
        current_balance=user.current_balance,
        timestamp=current_time
    )
    return {
        "current_balance": current_balance,
        "timestamp": current_time,
    }

@app.get("/history")
def get_all_transactions():

    transactions = transacation_repo.get_all_transactions()

    if not transactions:
        raise HTTPException(status_code=404, detail="No transactions found")

    return {
        "all_transactions": [transaction.to_dict() for transaction in transactions]
    }

handler = Mangum(app, lifespan="off")