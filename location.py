from fastapi import APIRouter, HTTPException
from pymongo import MongoClient
from pydantic import BaseModel
import auth

client = MongoClient("mongodb+srv://angela:C6b8KUv0UwbKDwr5@cluster0.tkkxnwj.mongodb.net/?retryWrites=true&w=majority")
db = client["tst"]
collection = db["location"]

class Item(BaseModel):
	location_id: int
	area_name: str
	description: str
	cardinal_direction: str
	floor: str

router = APIRouter(tags=["Location"])

def convert_objectid(object):
    object['_id'] = str(object['_id'])
    return object

@router.get('/location')
async def read_all_location():
    all_location = list(map(convert_objectid, collection.find()))
    return all_location

@router.get('/location/{item_id}')
async def read_location(item_id: int):
    location_item = collection.find_one({"location_id": item_id})
    if location_item:
        return convert_objectid(location_item)
    raise HTTPException(status_code=404, detail='Location not found')

@router.post('/location')
async def add_location(item: Item, current_user: auth.User = auth.Depends(auth.get_current_active_user)):
    item_dict = item.dict()
    existing_item = collection.find_one({"location_id": item_dict['location_id']})
    if existing_item:
        return f"Location ID {item_dict['location_id']} exists."
    
    collection.insert_one(item_dict)
    return convert_objectid(item_dict)

@router.put('/location')
async def update_location(item: Item, current_user: auth.User = auth.Depends(auth.get_current_active_user)):
    item_dict = item.dict()
    existing_item = collection.find_one({"location_id": item.location_id})
    if existing_item:
        collection.update_one({"location_id": item.location_id}, {"$set": item_dict})
        return "Updated"
    else:
        raise HTTPException(status_code=404, detail='Location ID not found')

@router.delete('/location/{item_id}')
async def delete_location(item_id: int, current_user: auth.User = auth.Depends(auth.get_current_active_user)):
    result = collection.delete_one({"location_id": item_id})
    if result.deleted_count == 1:
        return "Deleted"
    else:
        raise HTTPException(status_code=404, detail='Location ID not found')
