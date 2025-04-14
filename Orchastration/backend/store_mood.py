import requests

api_link = "http://localhost:8000/api"

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

if __name__ == "__main__":
    test_token = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNzQ0NzA0MjYwLCJpYXQiOjE3NDQ2MTc4NjAsImp0aSI6IjM2NDI5NzYwMTE4MTRjNjQ4ZjEwZDU5NTliMjEzNGFkIiwidXNlcl9pZCI6MX0.YGd33AwOeVfk0MXXwpw27e1XYH_MgWaHGOYPcGi75BU"
    test_note_id = 5
    mood = "anger"
    
    status_code = register_mood(test_token, test_note_id, mood)
    print("Mood registered with status:", status_code)
