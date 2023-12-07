from fastapi import APIRouter, HTTPException
from pymongo import MongoClient
from pydantic import BaseModel
import auth
from passlib.context import CryptContext

client = MongoClient("mongodb+srv://angela:C6b8KUv0UwbKDwr5@cluster0.tkkxnwj.mongodb.net/?retryWrites=true&w=majority")
db = client["tst"]
collection = db["user"]

class Item(BaseModel):
	user_id: int
	username: str
	password: str
	user_type: str
	disabled: bool

class UserInDB(Item):
    hashed_password: str

router = APIRouter()

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def get_password_hash(password):
    return pwd_context.hash(password)

def convert_objectid(object):
    object['_id'] = str(object['_id'])
    return object

@router.get('/user')
async def read_all_user(current_user: auth.User = auth.Depends(auth.get_current_active_user)):
	return list(map(convert_objectid, collection.find()))

@router.get('/user/{item_id}')
async def read_user(item_id: int, current_user: auth.User = auth.Depends(auth.get_current_active_user)):
	user_item = collection.find_one({"user_id": item_id})
	if user_item:
		return convert_objectid(user_item)
	raise HTTPException(status_code=404, detail='InteractionLog not found')

@router.post('/user')
async def add_user(item: Item, current_user: auth.User = auth.Depends(auth.get_current_active_user)):
	item_dict = item.dict()
	existing_item = collection.find_one({"user_id": item_dict['user_id']})
	if existing_item:
		return f"User ID {item_dict['user_id']} exists."
    
	hashed_password = get_password_hash(item_dict['password'])
	item_dict['hashed_password'] = hashed_password
	del item_dict['password']
	collection.insert_one(item_dict)
	return convert_objectid(item_dict)

@router.put('/user')
async def update_user(item_id: int, item: Item, current_user: auth.User = auth.Depends(auth.get_current_active_user)):
	item_dict = item.dict()
	existing_item = collection.find_one({"user_id": item_id})
	if existing_item:
		hashed_password = get_password_hash(item_dict['password'])
		item_dict['hashed_password'] = hashed_password
		del item_dict['password']
		collection.update_one({"user_id": item_id}, {"$set": item_dict})
		return "Updated"
	else:
		raise HTTPException(status_code=404, detail='User ID not found')

@router.delete('/user/{item_id}')
async def delete_user(item_id: int, current_user: auth.User = auth.Depends(auth.get_current_active_user)):
	result = collection.delete_one({"user_id": item_id})
	if result.deleted_count == 1:
		return "Deleted"
	else:
		raise HTTPException(status_code=404, detail='User ID not found')