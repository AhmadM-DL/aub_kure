import requests 
import os

api_link = os.getenv("suicide_url" , "http://suicide-detection:5000/suicide-risk")

def suicide_detect(text : str) -> dict:
    
    headers = {"Content-Type": "application/json"}
    payload = {"text": text}

    try:
        response = requests.post(f"{api_link}", json=payload, headers=headers)
        response.raise_for_status()
        return  response.json()["confidence"] , response.json()["label"]
    except requests.RequestException as e:
        raise RuntimeError(f"Suicide detector call failed: {e}")
    
    

