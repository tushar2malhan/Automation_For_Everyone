""" FAST API CRUD WITH ENCRYPTION DECRYPTION """
from fastapi import FastAPI
from enum import Enum
from werkzeug.security import generate_password_hash, check_password_hash
from cryptography.fernet import Fernet
from passlib.context import CryptContext
key = Fernet.generate_key()
 
# Instance the Fernet class with the key
 
fernet = Fernet(key)

app = FastAPI()
inventory = {
    1:{ 
        "name":"tushar",
        "nation":"india" 
        } 
    ,
    2:{ 
        "name":"jm",
        "nation":"Uk" 
        } 
    }
# Dynamically takes the value from the url > eg: /{name}  > hello tushar

# flask vs fastapi == no data validation in flask but with enum in fastapi
class Available_names(str,Enum):
    tushar1 = 'tushar'
    rajat1 = 'rajat'
    shubham1 = 'shubham'

@app.get("/{name}")
async def hello(name : str):
    print({"message": f"Hello {name}"})
    return {"message": f"Hello {name}"}

@app.get("/id/{id}")
def get_id (id:int):
    # import pdb; pdb.set_trace()
    return inventory.get(id,{"message":"id not found"})
# uvicorn dir.filename:app --reload    > to run it dynamically
# uvicorn app.main:app --reload    > to run it dynamically


## make a post request and add it to inventory
values = {}
@app.post("/add/")
def add_to_inventory(item:dict):
    name = item.get('name')
    print(name,end='\n\n')
    message = name
    encMessage = fernet.encrypt(message.encode())
    print('\n\n',encMessage)
    decMessage = fernet.decrypt(encMessage).decode()
    print('\n\n',decMessage)
    inventory[len(inventory)+1] = item
    values[item.get('name')] = encMessage
    print('\n\n',values)
    # print('\n\n',item)
    return inventory

## Put request into inventory
@app.put("/update/{id}")
def update_inventory(id:int,item:dict):
    inventory[id] = item
    print(inventory)
    return inventory

# Delete request
@app.delete("/delete/{id}")
def delete_inventory(id:int):
    inventory.pop(id)
    print(inventory)
    return inventory