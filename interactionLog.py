from fastapi import APIRouter, HTTPException
from pymongo import MongoClient
from pydantic import BaseModel
import auth
from datetime import datetime

client = MongoClient("mongodb+srv://angela:C6b8KUv0UwbKDwr5@cluster0.tkkxnwj.mongodb.net/?retryWrites=true&w=majority")
db = client["tst"]
collection = db["interactionLog"]

class Item(BaseModel):
	user_id: int
	staff_id: int
	interaction_type: str
	message: str

router = APIRouter(tags=["Interaction Log"])

def convert_objectid(object):
    object['_id'] = str(object['_id'])
    return object

@router.get('/interactionLog')
async def read_all_interactionLog(current_user: auth.User = auth.Depends(auth.get_current_active_user)):
    all_interactionLog = list(map(convert_objectid, collection.find()))
    return all_interactionLog

@router.get('/interactionLog/{item_id}')
async def read_interactionLog(item_id: int, current_user: auth.User = auth.Depends(auth.get_current_active_user)):
    interactionLog_item = collection.find_one({"interactionLog_id": item_id})
    if interactionLog_item:
        return convert_objectid(interactionLog_item)
    raise HTTPException(status_code=404, detail='InteractionLog not found')

@router.post('/interactionLog')
async def add_interactionLog(item: Item, current_user: auth.User = auth.Depends(auth.get_current_active_user)):
    all_ids = collection.distinct("interactionLog_id")
    if all_ids:
        max_id = max(all_ids)
        next_id = max_id + 1
    else:
        next_id = 1
    
    item_dict = item.dict()
    item_dict['interactionLog_id'] = next_id
    interaction_time = datetime.now()
    item_dict['interaction_time'] = interaction_time
    existing_item = collection.find_one({"interactionLog_id": item_dict['interactionLog_id']})
    if existing_item:
        return f"InteractionLog ID {item_dict['interactionLog_id']} exists."
    
    collection.insert_one(item_dict)
    return convert_objectid(item_dict)

@router.put('/interactionLog/{item_id}')
async def update_interactionLog(item_id: int, item: Item, current_user: auth.User = auth.Depends(auth.get_current_active_user)):
    item_dict = item.dict()
    existing_item = collection.find_one({"interactionLog_id": item_id})
    if existing_item:
        collection.update_one({"interactionLog_id": item_id}, {"$set": item_dict})
        return "Updated"
    else:
        raise HTTPException(status_code=404, detail='InteractionLog ID not found')

@router.delete('/interactionLog/{item_id}')
async def delete_interactionLog(item_id: int, current_user: auth.User = auth.Depends(auth.get_current_active_user)):
    result = collection.delete_one({"interactionLog_id": item_id})
    if result.deleted_count == 1:
        return "Deleted"
    else:
        raise HTTPException(status_code=404, detail='InteractionLog ID not found')
