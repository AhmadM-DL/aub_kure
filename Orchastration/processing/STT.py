import requests 


api_link = "http://localhost:5000"

def transcribe_audio(voice_note : str) -> str:
    
    headers = {"Content-Type": "application/json"}
    payload = {"audio_base64": voice_note}

    try:
        response = requests.post(f"{api_link}/transcribe", json=payload, headers=headers)
        print("Status Code:", response.status_code)
        status_code = response.status_code
        response.raise_for_status()
        return  status_code , response.json()["Text"]
    except requests.RequestException as e:
        raise RuntimeError(f"Whisper API call failed: {e}")
    
    
# if __name__ == "__main__":
#     # 🧪 Load test MP3 and convert to base64
#     import base64

#     with open("/home/hasanmog/AUB_Masters/projects/aub_kure/speech-to-text/resources/test_audio.mp3", "rb") as f:
#         audio_bytes = f.read()
#         audio_b64 = base64.b64encode(audio_bytes).decode('utf-8')

#     status , text= transcribe_audio(audio_b64)
#     print("Transcription:", text)
#     print("status" , status)