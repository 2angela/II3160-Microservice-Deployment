from fastapi import FastAPI, APIRouter, HTTPException, Depends
import requests
from fastapi.security import OAuth2PasswordBearer
import auth

app = FastAPI()
router = APIRouter(tags=["Menu, Ingredients, Composition"])

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

delightcook_api_url = "http://localhost:8888"

username = "angela"
password = "admin200"

def get_access_token():
    login_payload = {"username": username, "password": password}
    token_response = requests.post(f"{delightcook_api_url}/token", data=login_payload)
    
    if token_response.status_code == 200:
        return token_response.json().get("access_token")
    else:
        raise HTTPException(status_code=token_response.status_code, detail="Login failed")

def get_all_menu():
    try:
        url = f"{delightcook_api_url}/location"
        
        headers = {'Authorization': f'Bearer {get_access_token()}'}
        response = requests.get(url, headers=headers)
        api_data = response.json()

        if isinstance(api_data, list):
            filtered_locations = [
                location for location in api_data
                if 'relax' in location['description'].lower() or 'rest' in location['description'].lower()
            ]

            return {'location': filtered_locations}
        else:
            raise ValueError("Unexpected API response format")

    except Exception as e:
        print(f"Error in get_and_filter_location: {str(e)}")
        raise HTTPException(status_code=500, detail="Internal Server Error")

@router.get("/menu")
async def get_all_menu(current_user: auth.User = Depends(auth.get_current_active_user)):
    try:
        url = f"{delightcook_api_url}/menu_items"
        
        headers = {'Authorization': f'Bearer {get_access_token()}'}
        response = requests.get(url, headers=headers)
        api_data = response.json()

        if isinstance(api_data, list):
            return api_data
        else:
            raise ValueError("Unexpected API response format")

    except Exception as e:
        print(f"Error in get_all_menu: {str(e)}")
        raise HTTPException(status_code=500, detail="Internal Server Error")

@router.get("/ingredients")
async def get_all_ingredients(current_user: auth.User = Depends(auth.get_current_active_user)):
    try:
        url = f"{delightcook_api_url}/ingredients"
        
        headers = {'Authorization': f'Bearer {get_access_token()}'}
        response = requests.get(url, headers=headers)
        api_data = response.json()

        if isinstance(api_data, list):
            return api_data
        else:
            raise ValueError("Unexpected API response format")

    except Exception as e:
        print(f"Error in get_all_ingredients: {str(e)}")
        raise HTTPException(status_code=500, detail="Internal Server Error")
    
@router.get("/composition")
async def get_all_composition(current_user: auth.User = Depends(auth.get_current_active_user)):
    try:
        url = f"{delightcook_api_url}/composition"
        
        headers = {'Authorization': f'Bearer {get_access_token()}'}
        response = requests.get(url, headers=headers)
        api_data = response.json()

        if isinstance(api_data, list):
            return api_data
        else:
            raise ValueError("Unexpected API response format")

    except Exception as e:
        print(f"Error in get_all_composition: {str(e)}")
        raise HTTPException(status_code=500, detail="Internal Server Error")