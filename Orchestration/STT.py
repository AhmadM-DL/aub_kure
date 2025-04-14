import requests 
import os

api_link = os.getenv("whisper_url" , "http://speech-to-text:5000/transcribe")

def transcribe_audio(voice_note : str) -> str:
    
    headers = {"Content-Type": "application/json"}
    payload = {"audio_base64": voice_note}

    try:
        response = requests.post(f"{api_link}", json=payload, headers=headers)
        print("Status Code:", response.status_code)
        status_code = response.status_code
        response.raise_for_status()
        return  status_code , response.json()["Text"]
    except requests.RequestException as e:
        raise RuntimeError(f"Whisper API call failed: {e}")
    
    