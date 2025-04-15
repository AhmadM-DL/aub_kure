import requests
import os
from urllib.parse import urljoin
from exceptions import NetworkException
from config import SPEECH_TO_TEXT_HOST, SPEECH_TO_TEXT_PORT

HOST = os.getenv(SPEECH_TO_TEXT_HOST)
PORT = os.getenv(SPEECH_TO_TEXT_PORT)
BASE_URL = f"http://{HOST}:{PORT}"

TRANSCRIBE_URI = "transcribe"

def transcribe_audio(audio_base64 : str) -> str:
    url = urljoin(BASE_URL, TRANSCRIBE_URI)
    payload = {
        "audio_base64": audio_base64
    }

    try:
        response = requests.post(url , json = payload)
        response = response.json()
        return response["text"]
    except Exception as e :
        raise NetworkException(f"Internal server error")
    
    