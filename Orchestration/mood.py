import requests
import os

api_link = os.getenv("mood_url" , "http://mood-tracker:5000/sentiment")

def mood_detect(text: str) -> dict:
    headers = {"Content-Type": "application/json"}
    payload = {"text": text}

    try:
        response = requests.post(f"{api_link}", json=payload, headers=headers)
        response.raise_for_status()
        return response.json()
    except requests.RequestException as e:
        raise RuntimeError(f"Sentiment analysis API call failed: {e}")


