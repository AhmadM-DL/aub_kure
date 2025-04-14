import requests

api_link = "http://localhost:8000/api/auth" # will be changed later for kubernetes

def login_with_phone(phone_number : dict) -> dict:
    try:
        response = requests.post(f"{api_link}/login-phone/" , json = phone_number)
        response.raise_for_status()
        return response.json()
    
    except requests.RequestException as e :
        raise RuntimeError(f"Auth API call failed {e}")
    
    
# if __name__ == "__main__":
    # test_payload = {"phone_number": "961000000"}  
    # result = login_with_phone(test_payload)
    # print(result)

    



