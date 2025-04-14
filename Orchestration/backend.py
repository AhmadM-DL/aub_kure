import requests
import os

api_link = os.getenv("backend_url", "http://backend:8000/api")


def login_with_phone(phone_number : dict) -> dict:
    try:
        response = requests.post(f"{api_link}/auth/login-phone/" , json = phone_number)
        response.raise_for_status()
        return response.json()
    
    except requests.RequestException as e :
        raise RuntimeError(f"Auth API call failed {e}")
    
    
def create_note(token: str , text: str) -> int:
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"
    }
    payload = {"text": text}

    try:
        response = requests.post(f"{api_link}/note/", json=payload, headers=headers)
        response.raise_for_status()
        return response.json()["id"]
    except requests.RequestException as e:
        raise RuntimeError(f"Create note API call failed: {e}")
    
# To Be deleted
def get_notes(token: str) -> list:
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"
    }

    try:
        response = requests.get(f"{api_link}/notes/", headers=headers)
        response.raise_for_status()
        return response.json()
    except requests.RequestException as e:
        raise RuntimeError(f"Get user notes API call failed: {e}")
    

def mark_suicide(token: str , note_id: str) -> int:
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"
    }
    payload = {"id": note_id}

    try:
        response = requests.post(f"{api_link}/note/mark_suicidal/", json=payload, headers=headers)
        response.raise_for_status()
        return response.status_code
    except requests.RequestException as e:
        raise RuntimeError(f"Mark suicide API call failed: {e}")
    
def register_mood(token: str, note_id: int, mood_data: str) -> int:
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"
    }

    payload = {"note_id": note_id , 
               "mood" : mood_data}
    
    try:
        response = requests.post(f"{api_link}/mood/", json=payload, headers=headers)
        response.raise_for_status()
        return response.status_code
    except requests.RequestException as e:
        raise RuntimeError(f"Register mood API call failed: {e}")