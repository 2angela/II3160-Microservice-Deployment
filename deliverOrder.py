from fastapi import APIRouter, HTTPException
import json
from pydantic import BaseModel
import auth

class Item(BaseModel):
	deliverOrder_id: int
	order_id: int
	location_id: int
	custom_id: int

json_filename="data/deliverOrder.json"

with open(json_filename,"r") as read_file:
	data = json.load(read_file)

router = APIRouter()

@router.get('/deliverOrder')
async def read_all_deliverOrder(current_user: auth.User = auth.Depends(auth.get_current_active_user)):
	return data['deliverOrder']


@router.get('/deliverOrder/{item_id}')
async def read_deliverOrder(item_id: int, current_user: auth.User = auth.Depends(auth.get_current_active_user)):
	for deliverOrder_item in data['deliverOrder']:
		print(deliverOrder_item)
		if deliverOrder_item['deliverOrder_id'] == item_id:
			return deliverOrder_item
	raise HTTPException(
		status_code=404, detail=f'deliverOrder not found'
	)

@router.post('/deliverOrder')
async def add_deliverOrder(item: Item, current_user: auth.User = auth.Depends(auth.get_current_active_user)):
	item_dict = item.dict()
	item_found = False
	for deliverOrder_item in data['deliverOrder']:
		if deliverOrder_item['deliverOrder_id'] == item_dict['deliverOrder_id']:
			item_found = True
			return "deliverOrder ID "+str(item_dict['deliverOrder_id'])+" exists."
	
	if not item_found:
		data['deliverOrder'].append(item_dict)
		with open(json_filename,"w") as write_file:
			json.dump(data, write_file)

		return item_dict
	raise HTTPException(
		status_code=404, detail=f'item not found'
	)