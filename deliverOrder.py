from fastapi import APIRouter, HTTPException
from pymongo import MongoClient
from pydantic import BaseModel
import auth

client = MongoClient("mongodb+srv://angela:C6b8KUv0UwbKDwr5@cluster0.tkkxnwj.mongodb.net/?retryWrites=true&w=majority")
db = client["tst"]
collection = db["deliverOrder"]

class Item(BaseModel):
	deliverOrder_id: int
	order_id: int
	custom_id: int
	location_id: int

router = APIRouter()

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
    item_dict = item.dict()
    existing_item = collection.find_one({"deliverOrder_id": item_dict['deliverOrder_id']})
    if existing_item:
        return f"DeliverOrder ID {item_dict['deliverOrder_id']} exists."
    
    collection.insert_one(item_dict)
    return convert_objectid(item_dict)

@router.put('/deliverOrder/{item_id}')
async def update_deliverOrder(item_id: int, item: Item, current_user: auth.User = auth.Depends(auth.get_current_active_user)):
    item_dict = item.dict()
    existing_item = collection.find_one({"deliverOrder_id": item_id})
    if existing_item:
        collection.update_one({"deliverOrder_id": item_id}, {"$set": item_dict})
        return "Updated"
    else:
        raise HTTPException(status_code=404, detail='InteractionLog ID not found')

@router.delete('/deliverOrder/{item_id}')
async def delete_deliverOrder(item_id: int, current_user: auth.User = auth.Depends(auth.get_current_active_user)):
    result = collection.delete_one({"deliverOrder_id": item_id})
    if result.deleted_count == 1:
        return "Deleted"
    else:
        raise HTTPException(status_code=404, detail='DeliverOrder ID not found')