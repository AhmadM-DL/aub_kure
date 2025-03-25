"""
When using Base64 string as input , postman is adding new lines and spaces in the string , which is causing the code to pop an error. So this python code is for requests , 
it transforms audio file into base64 and this base 64 is the input for the api call.

"""

import base64
import requests

def encode_audio(audio_path):
    with open(audio_path, "rb") as audio_file:
        audio_content = audio_file.read()
        return base64.b64encode(audio_content).decode("utf-8")

# Path to your test MP3
audio_base64 = encode_audio("./resources/test_audio.mp3")

# Send to GATEWAY
url = "http://localhost:8001/pipeline"
data = {
    "audio_base64": audio_base64
}
headers = {"Content-Type": "application/json"}

response = requests.post(url, json=data, headers=headers)

print("Status Code:", response.status_code)
print("Response:", response.json())





