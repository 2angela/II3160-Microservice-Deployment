from fastapi import FastAPI, APIRouter, HTTPException, Depends
import requests
from pymongo import MongoClient
from fastapi.security import OAuth2PasswordBearer
import auth
from pydantic import BaseModel

app = FastAPI()
router = APIRouter()

mongo_connection_string = "mongodb+srv://angela:C6b8KUv0UwbKDwr5@cluster0.tkkxnwj.mongodb.net/?retryWrites=true&w=majority"
client = MongoClient(mongo_connection_string)
db = client["tst"] 
collection = db["order"]

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

delightcook_api_url = "http://localhost:8888"

username = "angela"
password = "admin200"

class Item(BaseModel):
    order_id: int
    customer_id: int
    menu_id: int

def get_access_token():
    login_payload = {"username": username, "password": password}
    token_response = requests.post(f"{delightcook_api_url}/token", data=login_payload)
    
    if token_response.status_code == 200:
        return token_response.json().get("access_token")
    else:
        raise HTTPException(status_code=token_response.status_code, detail="Login failed")

def store_item(item_dict: dict):
    collection.insert_one(item_dict)

@router.post("/order")
async def add_order(item: Item, current_user: auth.User = Depends(auth.get_current_active_user)):
    # Convert the Pydantic model to a dictionary
    item_dict = item.dict()

    url = "http://localhost:8888/order"
    headers = {"Authorization": f"Bearer {get_access_token()}"}
    response = requests.post(url, json=item_dict, headers=headers)

    if response.status_code == 200:
        store_item(item_dict)
        return response.json()
    else:
        raise HTTPException(status_code=response.status_code, detail="Failed to post data to delightcook's API")

@router.get("/order")
async def get_all_order(current_user: auth.User = Depends(auth.get_current_active_user)):
    all_order = list(collection.find({}, {'_id': 0}))

    if not all_order:
        raise HTTPException(status_code=404, detail="No order found in the database")

    return {"order": all_order}