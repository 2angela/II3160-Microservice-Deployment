from fastapi import FastAPI, HTTPException
import json
from pydantic import BaseModel


class Item(BaseModel):
	location_id: int
	area_name: str
	description: str
	cardinal_direction: str
	floor: str

json_filename="location.json"

with open(json_filename,"r") as read_file:
	data = json.load(read_file)

app = FastAPI()

@app.get('/location')
async def read_all_location():
	return data['location']


@app.get('/location/{item_id}')
async def read_location(item_id: int):
	for location_item in data['location']:
		print(location_item)
		if location_item['location_id'] == item_id:
			return location_item
	raise HTTPException(
		status_code=404, detail=f'location not found'
	)

@app.post('/location')
async def add_location(item: Item):
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

@app.put('/location')
async def update_location(item: Item):
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

@app.delete('/location/{item_id}')
async def delete_location(item_id: int):

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
