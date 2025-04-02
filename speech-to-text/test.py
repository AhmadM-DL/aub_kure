"""
When using Base64 string as input , postman is adding new lines and spaces in the string , which is causing the code to pop an error. So this python code is for requests , 
it transforms audio file into base64 and this base 64 is the input for the api call.

"""

import requests
import base64


def encode_audio(audio_path):
    with open(audio_path, "rb") as audio_file:
        audio_content = audio_file.read()
        return base64.b64encode(audio_content).decode("utf-8")  

audio_base64 = encode_audio("./resources/test_audio.mp3")

url = "http://localhost:5000/transcribe"
data = {
    "audio_base64": audio_base64
}
headers = {"Content-Type": "application/json"}


response = requests.post(url, json=data, headers=headers)

print(response.json())




