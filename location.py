from fastapi import APIRouter, HTTPException
import json
from pydantic import BaseModel
import OAuth


class Item(BaseModel):
	location_id: int
	area_name: str
	description: str
	cardinal_direction: str
	floor: str

json_filename="location.json"

with open(json_filename,"r") as read_file:
	data = json.load(read_file)

router = APIRouter()

@router.get('/location')
async def read_all_location(current_user: OAuth.User = OAuth.Depends(OAuth.get_current_active_user)):
	return data['location']


@router.get('/location/{item_id}')
async def read_location(item_id: int, current_user: OAuth.User = OAuth.Depends(OAuth.get_current_active_user)):
	for location_item in data['location']:
		print(location_item)
		if location_item['location_id'] == item_id:
			return location_item
	raise HTTPException(
		status_code=404, detail=f'location not found'
	)

@router.post('/location')
async def add_location(item: Item, current_user: OAuth.User = OAuth.Depends(OAuth.get_current_active_user)):
	item_dict = item.dict()
	item_found = False
	for location_item in data['location']:
		if location_item['location_id'] == item_dict['location_id']:
			item_found = True
			return "Location ID "+str(item_dict['location_id'])+" exists."
	
	if not item_found:
		data['location'].append(item_dict)
		with open(json_filename,"w") as write_file:
			json.dump(data, write_file)

		return item_dict
	raise HTTPException(
		status_code=404, detail=f'item not found'
	)

@router.put('/location')
async def update_location(item: Item, current_user: OAuth.User = OAuth.Depends(OAuth.get_current_active_user)):
	item_dict = item.dict()
	item_found = False
	for location_idx, location_item in enumerate(data['location']):
		if location_item['location_id'] == item_dict['location_id']:
			item_found = True
			data['location'][location_idx]=item_dict
			
			with open(json_filename,"w") as write_file:
				json.dump(data, write_file)
			return "updated"
	
	if not item_found:
		return "Location ID not found."
	raise HTTPException(
		status_code=404, detail=f'item not found'
	)

@router.delete('/location/{item_id}')
async def delete_location(item_id: int, current_user: OAuth.User = OAuth.Depends(OAuth.get_current_active_user)):

	item_found = False
	for location_idx, location_item in enumerate(data['location']):
		if location_item['location_id'] == item_id:
			item_found = True
			data['location'].pop(location_idx)
			
			with open(json_filename,"w") as write_file:
				json.dump(data, write_file)
			return "updated"
	
	if not item_found:
		return "Location ID not found."
	raise HTTPException(
		status_code=404, detail=f'item not found'
	)
