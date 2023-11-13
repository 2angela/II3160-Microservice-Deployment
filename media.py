from fastapi import APIRouter, HTTPException
import json
from pydantic import BaseModel
import OAuth

class Item(BaseModel):
	media_id: int
	media_type: str
	title: str
	description: str
	file_path: str
	location_id: int
	keywords: str

json_filename="media.json"

with open(json_filename,"r") as read_file:
	data = json.load(read_file)

router = APIRouter()

@router.get('/media')
async def read_all_media(current_user: OAuth.User = OAuth.Depends(OAuth.get_current_active_user)):
	return data['media']


@router.get('/media/{item_id}')
async def read_media(item_id: int, current_user: OAuth.User = OAuth.Depends(OAuth.get_current_active_user)):
	for media_item in data['media']:
		print(media_item)
		if media_item['media_id'] == item_id:
			return media_item
	raise HTTPException(
		status_code=404, detail=f'media not found'
	)

@router.post('/media')
async def add_media(item: Item, current_user: OAuth.User = OAuth.Depends(OAuth.get_current_active_user)):
	item_dict = item.dict()
	item_found = False
	for media_item in data['media']:
		if media_item['media_id'] == item_dict['media_id']:
			item_found = True
			return "Media ID "+str(item_dict['media_id'])+" exists."
	
	if not item_found:
		data['media'].append(item_dict)
		with open(json_filename,"w") as write_file:
			json.dump(data, write_file)

		return item_dict
	raise HTTPException(
		status_code=404, detail=f'item not found'
	)

@router.put('/media')
async def update_media(item: Item, current_user: OAuth.User = OAuth.Depends(OAuth.get_current_active_user)):
	item_dict = item.dict()
	item_found = False
	for media_idx, media_item in enumerate(data['media']):
		if media_item['media_id'] == item_dict['media_id']:
			item_found = True
			data['media'][media_idx]=item_dict
			
			with open(json_filename,"w") as write_file:
				json.dump(data, write_file)
			return "updated"
	
	if not item_found:
		return "Media ID not found."
	raise HTTPException(
		status_code=404, detail=f'item not found'
	)

@router.delete('/media/{item_id}')
async def delete_media(item_id: int, current_user: OAuth.User = OAuth.Depends(OAuth.get_current_active_user)):

	item_found = False
	for media_idx, media_item in enumerate(data['media']):
		if media_item['media_id'] == item_id:
			item_found = True
			data['media'].pop(media_idx)
			
			with open(json_filename,"w") as write_file:
				json.dump(data, write_file)
			return "updated"
	
	if not item_found:
		return "Media ID not found."
	raise HTTPException(
		status_code=404, detail=f'item not found'
	)
