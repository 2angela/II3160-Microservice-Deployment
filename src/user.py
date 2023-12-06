from fastapi import APIRouter, HTTPException
import json
from pydantic import BaseModel
import auth
from passlib.context import CryptContext

class Item(BaseModel):
	user_id: int
	username: str
	password: str
	user_type: str
	disabled: bool

class UserInDB(Item):
    hashed_password: str

json_filename="data/user.json"

with open(json_filename,"r") as read_file:
	data = json.load(read_file)

router = APIRouter()

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def get_password_hash(password):
    return pwd_context.hash(password)

@router.get('/user')
async def read_all_user(current_user: auth.User = auth.Depends(auth.get_current_active_user)):
	return data['user']


@router.get('/user/{item_id}')
async def read_user(item_id: int, current_user: auth.User = auth.Depends(auth.get_current_active_user)):
	for user_item in data['user']:
		print(user_item)
		if user_item['user_id'] == item_id:
			return user_item
	raise HTTPException(
		status_code=404, detail=f'user not found'
	)

@router.post('/user')
async def add_user(item: Item, current_user: auth.User = auth.Depends(auth.get_current_active_user)):
	item_dict = item.dict()
	item_found = False
	for user_item in data['user']:
		if user_item['user_id'] == item_dict['user_id']:
			item_found = True
			return "User ID "+str(item_dict['user_id'])+" exists."
	
	if not item_found:
		hashed_password = get_password_hash(item_dict['password'])
		item_dict['hashed_password'] = hashed_password
		del item_dict['password']
		data['user'].append(item_dict)
		with open(json_filename,"w") as write_file:
			json.dump(data, write_file)

		return item_dict
	raise HTTPException(
		status_code=404, detail=f'item not found'
	)

@router.put('/user')
async def update_user(item: Item, current_user: auth.User = auth.Depends(auth.get_current_active_user)):
	item_dict = item.dict()
	item_found = False
	for user_idx, user_item in enumerate(data['user']):
		if user_item['user_id'] == item_dict['user_id']:
			item_found = True
			data['user'][user_idx]=item_dict
			
			with open(json_filename,"w") as write_file:
				json.dump(data, write_file)
			return "updated"
	
	if not item_found:
		return "User ID not found."
	raise HTTPException(
		status_code=404, detail=f'item not found'
	)

@router.delete('/user/{item_id}')
async def delete_user(item_id: int, current_user: auth.User = auth.Depends(auth.get_current_active_user)):

	item_found = False
	for user_idx, user_item in enumerate(data['user']):
		if user_item['user_id'] == item_id:
			item_found = True
			data['user'].pop(user_idx)
			
			with open(json_filename,"w") as write_file:
				json.dump(data, write_file)
			return "updated"
	
	if not item_found:
		return "User ID not found."
	raise HTTPException(
		status_code=404, detail=f'item not found'
	)