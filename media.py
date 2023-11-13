from fastapi import FastAPI, HTTPException
import json
from pydantic import BaseModel

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

app = FastAPI()

@app.get('/')
async def read_all_media():
	return data['media']

@app.get('/{item_id}')
async def read_media(item_id: int):
	for media_item in data['media']:
		print(media_item)
		if media_item['media_id'] == item_id:
			return media_item
	raise HTTPException(
		status_code=404, detail=f'media not found'
	)

@app.post('/')
async def add_media(item: Item):
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

@app.put('/')
async def update_media(item: Item):
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

@app.delete('/{item_id}')
async def delete_media(item_id: int):

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
