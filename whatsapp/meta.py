from urllib.parse import urljoin
from utils import read_secret
from config import WHATSAPP_API_FILE
from exceptions import NetworkException
import requests
import logging

logger = logging.getLogger(__name__)

META_API_VERSION = "v19.0"
META_GRAPH_URI= f'https://graph.facebook.com/{META_API_VERSION}/'

WHATSAPP_TOKEN = read_secret(WHATSAPP_API_FILE)

def get_media_url(media_id):
    url = urljoin(META_GRAPH_URI, media_id)
    headers = {
        'Authorization': f'Bearer {WHATSAPP_TOKEN}'
    }
    try: 
        logger.info(f"Calling {url}")
        response = requests.get(url, headers=headers)
        logger.info(f"Response {response}")
        if response.status_code == 200:
            return response.json().get('url')
        else:
            return None
    except Exception as e:
        raise NetworkException("Internal Server Error", e)


def download_media(media_url):
    headers = {
        'Authorization': f'Bearer {WHATSAPP_TOKEN}'
    }
    try:
        response = requests.get(media_url, headers=headers)
        return response.content
    except Exception as e:
        raise NetworkException("Internal Server Error", e)

def send_message(from_number_id, to_number, message):
    url = urljoin(META_GRAPH_URI, "/".join([from_number_id, "messages"]))
    headers = {"Authorization": f"Bearer {WHATSAPP_TOKEN}"}
    payload = {
        'messaging_product': 'whatsapp',
        'to': to_number,
        'text': {'body': message},
    }
    try:
        logger.info(f"Calling {url}")
        response = requests.post(url, headers = headers, json=payload)
        logger.info(f"Received Response: {response}")
        logger.info(f"Received Response: {response.json()}")
        return response
    except Exception as e:
        raise NetworkException("Network Exception", e)