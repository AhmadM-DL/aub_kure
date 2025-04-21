from config import ORCHESTRATOR_HOST, ORCHESTRATOR_PORT
import os, requests
from urllib.parse import urljoin
from exceptions import NetworkException


ORCHESTRATOR_HOST = os.getenv("ORCHESTRATOR_HOST")
ORCHESTRATOR_PORT = os.getenv("ORCHESTRATOR_PORT")

BASE_URL = f"http://{ORCHESTRATOR_HOST}:{ORCHESTRATOR_PORT}"

AUTH_URL = "login"
REGISTER_URL = "register"
GET_NOTES_URL = "notes"

def login(phone_number:str, password:str):
    url = urljoin(BASE_URL, AUTH_URL)
    payload = {
        "phone_number": phone_number,
        "password": password,
    }
    try:
        response = requests.post(url , json = payload)
        if response.status_code==200:
            response = response.json()
            return True, response["access"]
        else:
            return False, None
    except Exception as e :
        raise NetworkException(f"Internal server error", e)
    
def register(email: str, phone_number:str, password:str) -> bool:
    url = urljoin(BASE_URL, REGISTER_URL)
    payload = {
        "email": email,
        "phone_number": phone_number,
        "password": password,
    }
    try:
        response = requests.post(url , json = payload)
        if response.status_code == 200:
            return True
        else:
            return False
    except Exception as e :
        raise NetworkException(f"Internal server error", e)
   
def get_notes(user_token:str) -> list:
    url = urljoin(BASE_URL, GET_NOTES_URL)
    headers = {
        "Authorization": f"Bearer {user_token}",
    }
    try:
        response = requests.get(url, headers=headers)
        return response.json()
    except Exception as e :
        raise NetworkException(f"Internal server error", e)
     
