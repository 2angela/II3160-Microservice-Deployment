from fastapi import APIRouter, HTTPException
import json
from pydantic import BaseModel
import auth

class Item(BaseModel):
	interactionLog_id: int
	user_id: int
	staff_id: int
	interaction_type: str
	message: str
	interaction_time: str

json_filename="data/interactionLog.json"

with open(json_filename,"r") as read_file:
	data = json.load(read_file)

router = APIRouter()

@router.get('/interactionLog')
async def read_all_interactionLog(current_user: auth.User = auth.Depends(auth.get_current_active_user)):
	return data['interactionLog']


@router.get('/interactionLog/{item_id}')
async def read_interactionLog(item_id: int, current_user: auth.User = auth.Depends(auth.get_current_active_user)):
	for interactionLog_item in data['interactionLog']:
		print(interactionLog_item)
		if interactionLog_item['interactionLog_id'] == item_id:
			return interactionLog_item
	raise HTTPException(
		status_code=404, detail=f'interactionLog not found'
	)

@router.post('/interactionLog')
async def add_interactionLog(item: Item, current_user: auth.User = auth.Depends(auth.get_current_active_user)):
	item_dict = item.dict()
	item_found = False
	for interactionLog_item in data['interactionLog']:
		if interactionLog_item['interactionLog_id'] == item_dict['interactionLog_id']:
			item_found = True
			return "interactionLog ID "+str(item_dict['interactionLog_id'])+" exists."
	
	if not item_found:
		data['interactionLog'].append(item_dict)
		with open(json_filename,"w") as write_file:
			json.dump(data, write_file)

		return item_dict
	raise HTTPException(
		status_code=404, detail=f'item not found'
	)

@router.put('/interactionLog')
async def update_interactionLog(item: Item, current_user: auth.User = auth.Depends(auth.get_current_active_user)):
	item_dict = item.dict()
	item_found = False
	for interactionLog_idx, interactionLog_item in enumerate(data['interactionLog']):
		if interactionLog_item['interactionLog_id'] == item_dict['interactionLog_id']:
			item_found = True
			data['interactionLog'][interactionLog_idx]=item_dict
			
			with open(json_filename,"w") as write_file:
				json.dump(data, write_file)
			return "updated"
	
	if not item_found:
		return "interactionLog ID not found."
	raise HTTPException(
		status_code=404, detail=f'item not found'
	)

@router.delete('/interactionLog/{item_id}')
async def delete_interactionLog(item_id: int, current_user: auth.User = auth.Depends(auth.get_current_active_user)):

	item_found = False
	for interactionLog_idx, interactionLog_item in enumerate(data['interactionLog']):
		if interactionLog_item['interactionLog_id'] == item_id:
			item_found = True
			data['interactionLog'].pop(interactionLog_idx)
			
			with open(json_filename,"w") as write_file:
				json.dump(data, write_file)
			return "updated"
	
	if not item_found:
		return "interactionLog ID not found."
	raise HTTPException(
		status_code=404, detail=f'item not found'
	)
