import requests

api_link = "http://localhost:8000/api" # will be changed later for kubernetes

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
    
    
# if __name__ == "__main__":

#     access_token = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNzQ0NzA0MjYwLCJpYXQiOjE3NDQ2MTc4NjAsImp0aSI6IjM2NDI5NzYwMTE4MTRjNjQ4ZjEwZDU5NTliMjEzNGFkIiwidXNlcl9pZCI6MX0.YGd33AwOeVfk0MXXwpw27e1XYH_MgWaHGOYPcGi75BU"
#     id = 5 
#     response = mark_suicide(access_token, id)
#     print(response)