import requests

api_link = "http://localhost:5001"

def mood_detect(text: str) -> dict:
    headers = {"Content-Type": "application/json"}
    payload = {"text": text}

    try:
        response = requests.post(f"{api_link}/sentiment", json=payload, headers=headers)
        response.raise_for_status()
        return response.json()
    except requests.RequestException as e:
        raise RuntimeError(f"Sentiment analysis API call failed: {e}")
    
# if __name__ == "__main__":
#     test_text = "I feel scared and alone right now."
#     result = mood_detect(test_text)
#     print("Sentiment Scores:", result)

