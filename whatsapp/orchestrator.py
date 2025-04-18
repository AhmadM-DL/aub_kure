import requests
import os
from urllib.parse import urljoin
from exceptions import NetworkException
from config import ORCHESTRATOR_HOST, ORCHESTRATOR_PORT
import logging 

logger = logging.getLogger(__name__)

HOST = os.getenv(ORCHESTRATOR_HOST)
PORT = os.getenv(ORCHESTRATOR_PORT)
BASE_URL = f"http://{HOST}:{PORT}"

PROCESS_NOTE_URI = "note"

def process_note(phone_number:str, audio_base64:str) -> bool:
    url = urljoin(BASE_URL, PROCESS_NOTE_URI)
    payload = {
        "phone_number": phone_number,
        "audio_base64": audio_base64,
    }
    try:
        logger.info(f"Calling {url}")
        response = requests.post(url , json=payload)
        logger.info(f"Received response: {response}")
        if response.status_code == 200:
            return True
        else:
            return False
    except Exception as e :
        raise NetworkException(f"Internal server error", e)
    