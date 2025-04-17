import requests
import os
from urllib.parse import urljoin
from exceptions import NetworkException
from config import BACKEND_HOST, BACKEND_PORT
import logging 

logger = logging.getLogger(__name__)

HOST = os.getenv(BACKEND_HOST)
PORT = os.getenv(BACKEND_PORT)
BASE_URL = f"http://{HOST}:{PORT}"

REGISTER_URI = "api/register/"
LOGIN_PASS_URI = "api/auth/login-password/"
AUTH_URI = "api/auth/login-phone/"
CREATE_NOTE_URI = "api/note/"
GET_NOTES_URI = "api/notes/"
MARK_SUICIDE_URI = "api/note/mark_suicidal/"
REGISTER_MOOD_URI = "api/mood/"


def register_user(email : str , phone_number : str , password : str):
    url = urljoin(BASE_URL, REGISTER_URI)
    payload = {
        "email": email,
        "phone_number": phone_number,
        "password": password,
    }
    try:
        response = requests.post(url , json = payload)
        response = response.json()
        return response['message']
    except Exception as e :
        raise NetworkException(f"Internal server error", e)
    
def login_with_password(phone_number : str , password : str ):
    url = urljoin(BASE_URL , LOGIN_PASS_URI)
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

def login_with_phone(phone_number : str) -> str:
    url = urljoin(BASE_URL, AUTH_URI)
    payload={
        "phone_number": phone_number,
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
    
    
def create_note(user_token: str , text: str) -> int:
    url = urljoin(BASE_URL, CREATE_NOTE_URI)
    payload={
        "text": text,
    }
    headers = {
        "Authorization": f"Bearer {user_token}",
    }
    try:
        response = requests.post(url , json = payload, headers=headers)
        response = response.json()
        return response["id"]
    except Exception as e :
        raise NetworkException(f"Internal server error", e)
    
def get_notes(user_token: str) -> list:
    url = urljoin(BASE_URL, GET_NOTES_URI)
    headers = {
        "Authorization": f"Bearer {user_token}",
    }
    try:
        response = requests.get(url, headers=headers)
        response = response.json()
        return response.json()
    except Exception as e :
        raise NetworkException(f"Internal server error", e)
     

def mark_suicide(user_token: str , note_id: str) -> bool:
    url = urljoin(BASE_URL, MARK_SUICIDE_URI)
    payload={
        "id": note_id,
    }
    headers = {
        "Authorization": f"Bearer {user_token}",
    }
    try:
        response = requests.post(url , json = payload, headers=headers)
        logger.info(f"Mark suicide response: {response}")
        if response.status_code==200:
            return True
        else:
            return False
    except Exception as e :
        raise NetworkException(f"Internal server error", e)
    
def register_mood(user_token: str, note_id: int, mood: str) -> None:
    url = urljoin(BASE_URL, REGISTER_MOOD_URI)
    payload={
        "note_id": note_id,
        "mood": mood,
    }
    headers = {
        "Authorization": f"Bearer {user_token}",
    }
    try:
        response = requests.post(url , json = payload, headers=headers)
        logger.info(f"Mark suicide response: {response}")
        if response.status_code==200:
            return True
        else:
            return False
    except Exception as e :
        raise NetworkException(f"Internal server error", e)