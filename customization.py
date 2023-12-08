from fastapi import FastAPI, APIRouter, HTTPException, Depends
import requests
from pymongo import MongoClient
from fastapi.security import OAuth2PasswordBearer
import auth
from pydantic import BaseModel
from typing import List

app = FastAPI()
router = APIRouter(tags=["Customization"])

mongo_connection_string = "mongodb+srv://angela:C6b8KUv0UwbKDwr5@cluster0.tkkxnwj.mongodb.net/?retryWrites=true&w=majority"
client = MongoClient(mongo_connection_string)
db = client["tst"] 
collection = db["meal_customization"]

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

delightcook_api_url = "http://backenddelightcook.dtemg6gpcec2b0cy.southeastasia.azurecontainer.io"

username = "TST"
password = "gws"

class Ingredient(BaseModel):
    ingredient_id: int
    adjusted_quantity: float

class Item(BaseModel):
    custom_id: int
    Ingredients: List[Ingredient]
    order_id: int

def get_access_token():
    login_payload = {"username": username, "password": password}
    token_response = requests.post(f"{delightcook_api_url}/token", data=login_payload)
    
    if token_response.status_code == 200:
        return token_response.json().get("access_token")
    else:
        raise HTTPException(status_code=token_response.status_code, detail="Login failed")

def store_item(item_dict: dict):
    collection.insert_one(item_dict)

@router.post("/meal_customization")
async def add_meal_customization(item: Item, current_user: auth.User = Depends(auth.get_current_active_user)):
    item_dict = item.dict()

    url = "http://backenddelightcook.dtemg6gpcec2b0cy.southeastasia.azurecontainer.io/customization"
    headers = {"Authorization": f"Bearer {get_access_token()}"}
    response = requests.post(url, json=item_dict, headers=headers)

    if response.status_code == 200:
        store_item(item_dict)
        return response.json()
    else:
        raise HTTPException(status_code=response.status_code, detail="Failed to post data to delightcook's API")

@router.get("/meal_customization")
async def get_all_meal_customization(current_user: auth.User = Depends(auth.get_current_active_user)):
    all_meal_customization = list(collection.find({}, {'_id': 0}))

    if not all_meal_customization:
        raise HTTPException(status_code=404, detail="No meal_customization found in the database")

    return all_meal_customization