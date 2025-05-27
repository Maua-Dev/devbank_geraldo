import time
from fastapi import FastAPI, HTTPException
from .environments import Environments


app = FastAPI()

user_repo = Environments.get_user_repo()
transacation_repo = Environments.get_transaction_repo()

@app.get("/")
def get_user_data(name: str):    

    user_repo = Environments.get_user_repo()
    user = user_repo.get_user(name=name)

    if not user:
        raise HTTPException(status_code=404, detail="User Not found")

    return user.to_dict()  

@app.post("/deposit")
def deposit(request: dict):
    user = user_repo.get_user(name=request.get("name"))

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
    
    current_balance = user.current_balance + total_deposit

    current_time = time.time() * 1000

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
def withdrawal(request: dict):
    user = user_repo.get_user(name=request.get("name"))

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
    
    current_balance = user.current_balance - total_withdrawal

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

# @app.get("/items/get_all_items")
# def get_all_items():
#     items = repo.get_all_items()
#     return {
#         "items": [item.to_dict() for item in items]
#     }
    

# @app.get("/items/{item_id}")
# def get_item(item_id: int):
#     validation_item_id = Item.validate_item_id(item_id=item_id)
#     if not validation_item_id[0]:
#         raise HTTPException(status_code=400, detail=validation_item_id[1])
    
#     item = repo.get_item(item_id)
    
#     if item is None:
#         raise HTTPException(status_code=404, detail="Item Not found")
    
#     return {
#         "item_id": item_id,
#         "item": item.to_dict()    
#     }

# @app.post("/items/create_item", status_code=201)
# def create_item(request: dict):
#     item_id = request.get("item_id")
    
#     validation_item_id = Item.validate_item_id(item_id=item_id)
#     if not validation_item_id[0]:
#         raise HTTPException(status_code=400, detail=validation_item_id[1])
    
#     item = repo.get_item(item_id)
#     if item is not None:
#         raise HTTPException(status_code=409, detail="Item already exists")
    
#     name = request.get("name")
#     price = request.get("price")
#     item_type = request.get("item_type")
#     if item_type is None:
#         raise HTTPException(status_code=400, detail="Item type is required")
#     if type(item_type) != str:
#         raise HTTPException(status_code=400, detail="Item type must be a string")
#     if item_type not in [possible_type.value for possible_type in ItemTypeEnum]:
#         raise HTTPException(status_code=400, detail="Item type is not a valid one")
    
#     admin_permission = request.get("admin_permission")
    
#     try:
#         item = Item(name=name, price=price, item_type=ItemTypeEnum[item_type], admin_permission=admin_permission)
#     except ParamNotValidated as err:
#         raise HTTPException(status_code=400, detail=err.message)
    
#     item_response = repo.create_item(item, item_id)
#     return {
#         "item_id": item_id,
#         "item": item_response.to_dict()    
#     }
    
# @app.delete("/items/delete_item")
# def delete_item(request: dict):
#     item_id = request.get("item_id")
    
#     validation_item_id = Item.validate_item_id(item_id=item_id)
#     if not validation_item_id[0]:
#         raise HTTPException(status_code=400, detail=validation_item_id[1])
    
#     item = repo.get_item(item_id)
    
#     if item is None:
#         raise HTTPException(status_code=404, detail="Item Not found")
    
#     if item.admin_permission == True:
#         raise HTTPException(status_code=403, detail="Item Not found")
    
#     item_deleted = repo.delete_item(item_id)
    
#     return {
#         "item_id": item_id,
#         "item": item_deleted.to_dict()    
#     }
    
# @app.put("/items/update_item")
# def update_item(request: dict):
#     item_id = request.get("item_id")
    
#     validation_item_id = Item.validate_item_id(item_id=item_id)
#     if not validation_item_id[0]:
#         raise HTTPException(status_code=400, detail=validation_item_id[1])
    
#     item = repo.get_item(item_id)
    
#     if item is None:
#         raise HTTPException(status_code=404, detail="Item Not found")
    
#     if item.admin_permission == True:
#         raise HTTPException(status_code=403, detail="Item Not found")
    
#     name = request.get("name")
#     price = request.get("price")
#     admin_permission = request.get("admin_permission")
    
#     item_type_value = request.get("item_type")
#     if item_type_value != None:
#         if type(item_type_value) != str:
#             raise HTTPException(status_code=400, detail="Item type must be a string")
#         if item_type_value not in [possible_type.value for possible_type in ItemTypeEnum]:
#             raise HTTPException(status_code=400, detail="Item type is not a valid one")
#         item_type = ItemTypeEnum[item_type_value]
#     else:
#         item_type = None
        
#     item_updated = repo.update_item(item_id, name, price, item_type, admin_permission)
    
#     return {
#         "item_id": item_id,
#         "item": item_updated.to_dict()    
#     }
    


# handler = Mangum(app, lifespan="off")
