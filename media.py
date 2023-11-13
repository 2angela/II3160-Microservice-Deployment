from fastapi import FastAPI, HTTPException
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

app = FastAPI(debug=True)

@app.post("/token", response_model=OAuth.Token)
async def login_for_access_token(form_data: OAuth.OAuth2PasswordRequestForm = OAuth.Depends()):
    user = OAuth.authenticate_user(OAuth.db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(status_code=OAuth.status.HTTP_401_UNAUTHORIZED, detail="Incorrect username or password", headers={"WWW-Authenticate": "Bearer"})
    access_token_expires = OAuth.timedelta(minutes=OAuth.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = OAuth.create_access_token(data={"sub": user.username}, expires_delta=access_token_expires)
    return {"access_token": access_token, "token_type": "bearer"}

@app.get("/users/me/", response_model=OAuth.User)
async def read_users_me(current_user: OAuth.User = OAuth.Depends(OAuth.get_current_active_user)):
    return current_user

@app.get("/users/me/items", response_model=OAuth.User)
async def read_own_items(current_user: OAuth.User = OAuth.Depends(OAuth.get_current_active_user)):
    return [{"item_id": 1, "owner": current_user}]

@app.get('/users/me/media', response_model=OAuth.User)
async def read_all_media(current_user: OAuth.User = OAuth.Depends(OAuth.get_current_active_user)):
	return data['media']

@app.get('/media/{item_id}')
async def read_media(item_id: int):
	for media_item in data['media']:
		print(media_item)
		if media_item['media_id'] == item_id:
			return media_item
	raise HTTPException(
		status_code=404, detail=f'media not found'
	)

@app.post('/media')
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

@app.put('/media')
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

@app.delete('/media/{item_id}')
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
