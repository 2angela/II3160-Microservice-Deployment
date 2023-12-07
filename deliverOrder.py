from fastapi import APIRouter, HTTPException
from pymongo import MongoClient
from pydantic import BaseModel
import auth

client = MongoClient("mongodb+srv://angela:C6b8KUv0UwbKDwr5@cluster0.tkkxnwj.mongodb.net/?retryWrites=true&w=majority")
db = client["tst"]
collection = db["deliverOrder"]

class Item(BaseModel):
	order_id: int
	custom_id: int
	location_id: int

router = APIRouter(tags=["Deliver Order"])

def convert_objectid(object):
    object['_id'] = str(object['_id'])
    return object

@router.get('/deliverOrder')
async def read_all_deliverOrder(current_user: auth.User = auth.Depends(auth.get_current_active_user)):
    all_deliverOrder = list(map(convert_objectid, collection.find()))
    return all_deliverOrder

@router.get('/deliverOrder/{item_id}')
async def read_deliverOrder(item_id: int, current_user: auth.User = auth.Depends(auth.get_current_active_user)):
    deliverOrder_item = collection.find_one({"deliverOrder_id": item_id})
    if deliverOrder_item:
        return convert_objectid(deliverOrder_item)
    raise HTTPException(status_code=404, detail='DeliverOrder not found')

@router.post('/deliverOrder')
async def add_deliverOrder(item: Item, current_user: auth.User = auth.Depends(auth.get_current_active_user)):
    all_ids = collection.distinct("deliverOrder_id")
    if all_ids:
        max_id = max(all_ids)
        next_id = max_id + 1
    else:
        next_id = 1
    
    item_dict = item.dict()
    item_dict['deliverOrder_id'] = next_id
    existing_item = collection.find_one({"deliverOrder_id": item_dict['deliverOrder_id']})
    if existing_item:
        return f"DeliverOrder ID {item_dict['deliverOrder_id']} exists."
    
    collection.insert_one(item_dict)
    return convert_objectid(item_dict)