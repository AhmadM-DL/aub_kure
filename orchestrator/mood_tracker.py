import requests
import os
from urllib.parse import urljoin
from exceptions import NetworkException
from config import MOOD_TRACKER_HOST, MOOD_TRACKER_PORT, MOOD_TRACKER_THRESHOLD
import logging 

logger = logging.getLogger(__name__)

HOST = os.getenv(MOOD_TRACKER_HOST)
PORT = os.getenv(MOOD_TRACKER_PORT)
MOOD_THRESHOLD = float(os.getenv(MOOD_TRACKER_THRESHOLD))

BASE_URL = f"http://{HOST}:{PORT}"

MOOD_TRACK_URI = "sentiment"

def mood_detect(text: str) -> list:
    url = urljoin(BASE_URL, MOOD_TRACK_URI)
    payload = {
        "text": text
    }

    try:
        response = requests.post(url , json = payload)
        response = response.json()
        logger.info(f"Mood detection response: {response}")
        moods = []
        for mood, score in response.items():
            if score >= MOOD_THRESHOLD:
                moods.append(mood)
        return moods                
    except Exception as e :
        raise NetworkException(f"Internal server error", e)
    

