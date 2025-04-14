import requests 


api_link = "http://localhost:5002"

def suicide_detect(text : str) -> dict:
    
    headers = {"Content-Type": "application/json"}
    payload = {"text": text}

    try:
        response = requests.post(f"{api_link}/suicide-risk", json=payload, headers=headers)
        response.raise_for_status()
        return  response.json()["confidence"] , response.json()["label"]
    except requests.RequestException as e:
        raise RuntimeError(f"Suicide detector call failed: {e}")
    
    
# if __name__ == "__main__":

#     conf , label = suicide_detect(text = "I'm not okay today.")
#     print(conf , label)

