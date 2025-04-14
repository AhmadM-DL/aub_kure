import requests

api_link = "http://localhost:8000/api" # will be changed later for kubernetes

def create_note(token: str , text: str) -> int:
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"
    }
    payload = {"text": text}

    try:
        response = requests.post(f"{api_link}/note/", json=payload, headers=headers)
        # print("Status Code:", response.status_code)
        # print("Response Text:", response.text)
        response.raise_for_status()
        return response.json()["id"]
    except requests.RequestException as e:
        raise RuntimeError(f"Create note API call failed: {e}")
    
    
# if __name__ == "__main__":

    # access_token = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNzQ0NzA0MjYwLCJpYXQiOjE3NDQ2MTc4NjAsImp0aSI6IjM2NDI5NzYwMTE4MTRjNjQ4ZjEwZDU5NTliMjEzNGFkIiwidXNlcl9pZCI6MX0.YGd33AwOeVfk0MXXwpw27e1XYH_MgWaHGOYPcGi75BU"
    # test_text = "Hello? This is a test audio file to check the Whisper API transcription."
    # note_id = create_note(access_token, test_text)
    # print("Created note with ID:", note_id)
