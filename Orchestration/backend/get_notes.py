import requests

api_link= "http://localhost:8000/api/notes/"

def get_notes(token: str) -> list:
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"
    }

    try:
        response = requests.get(api_link, headers=headers)
        response.raise_for_status()
        return response.json()
    except requests.RequestException as e:
        raise RuntimeError(f"Get user notes API call failed: {e}")
