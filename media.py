from fastapi import APIRouter, HTTPException
from pymongo import MongoClient
from pydantic import BaseModel
import auth

client = MongoClient("mongodb+srv://angela:C6b8KUv0UwbKDwr5@cluster0.tkkxnwj.mongodb.net/?retryWrites=true&w=majority")
db = client["tst"]
collection = db["media"]

class Item(BaseModel):
    media_id: int
    title: str
    location_id: int
    image_url: str
    description: str
    tags: str

router = APIRouter()

def convert_objectid(object):
    object['_id'] = str(object['_id'])
    return object

@router.get('/media')
async def read_all_media():
    all_media = list(map(convert_objectid, collection.find()))
    return all_media

@router.get('/media/{item_id}')
async def read_media(item_id: int):
    media_item = collection.find_one({"media_id": item_id})
    if media_item:
        return convert_objectid(media_item)
    raise HTTPException(status_code=404, detail='Media not found')

@router.post('/media')
async def add_media(item: Item, current_user: auth.User = auth.Depends(auth.get_current_active_user)):
    item_dict = item.dict()
    existing_item = collection.find_one({"media_id": item_dict['media_id']})
    if existing_item:
        return f"Media ID {item_dict['media_id']} exists."
    
    collection.insert_one(item_dict)
    return convert_objectid(item_dict)

@router.put('/media/{item_id}')
async def update_media(item_id: int, item: Item, current_user: auth.User = auth.Depends(auth.get_current_active_user)):
    item_dict = item.dict()
    existing_item = collection.find_one({"media_id": item_id})
    if existing_item:
        collection.update_one({"media_id": item_id}, {"$set": item_dict})
        return "Updated"
    else:
        raise HTTPException(status_code=404, detail='Media ID not found')

@router.delete('/media/{item_id}')
async def delete_media(item_id: int, current_user: auth.User = auth.Depends(auth.get_current_active_user)):
    result = collection.delete_one({"media_id": item_id})
    if result.deleted_count == 1:
        return "Deleted"
    else:
        raise HTTPException(status_code=404, detail='Media ID not found')
