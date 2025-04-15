import requests 
import os
from urllib.parse import urljoin
from exceptions import NetworkException
from config import SUICIDE_DETECTION_HOST, SUICIDE_DETECTION_PORT, SUICIDE_DETECTION_THRESHOLD, SUICIDE_DETECTION_LABEL

HOST = os.getenv(SUICIDE_DETECTION_HOST)
PORT = os.getenv(SUICIDE_DETECTION_PORT)
SUICIDE_LABEL = os.getenv(SUICIDE_DETECTION_LABEL)
SUICIDE_THRESHOLD = float(os.getenv(SUICIDE_DETECTION_THRESHOLD))

BASE_URL = f"http://{HOST}:{PORT}"

SUICIDE_DETECTION_URI = "suicide-risk"

def suicide_detect(text : str) -> bool:
    url = urljoin(BASE_URL, SUICIDE_DETECTION_URI)
    payload = {
        "text": text
    }
    try:
        response = requests.post(url , json = payload)
        response = response.json()
        if response["label"] == SUICIDE_LABEL and response["confidence"] >= SUICIDE_THRESHOLD:
            return True
        else:
            return False
    except Exception as e :
        raise NetworkException(f"Internal server error")
    

