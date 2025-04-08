import os
import uuid
import base64
from flask import Flask, request, jsonify
import whisper
from pydub import AudioSegment
from .config import TEMP_AUDIO_DIR, MODEL_CACHE_DIR

app = Flask(__name__)

os.makedirs(TEMP_AUDIO_DIR, exist_ok=True)
model_path = os.path.join(MODEL_CACHE_DIR, "base.pt")
model = None 

def get_model():
    global model
    if model is None:
       if os.path.exists(model_path):
            print("Loading Whisper model from cache...")
            model = whisper.load_model("base")
            print("Whisper model loaded successfully!")
       else: 
           print("Model not found! Please download it first.")
           return None
    return model


@app.route('/health', methods=['GET'])
def health_check():
    return jsonify({'status': 'OK', 'message': 'Whisper API is running'}), 200

@app.route('/transcribe', methods=['POST'])
def transcribe_audio():
    if not request.is_json:
        return jsonify({'error': 'Unsupported Media Type. Use application/json'}), 415

    data = request.get_json()

    if 'audio_base64' not in data:
        return jsonify({'error': 'No base64 audio provided'}), 400

    try:
        audio_data = base64.b64decode(data['audio_base64'])
        unique_id = str(uuid.uuid4())
        temp_mp3 = os.path.join(TEMP_AUDIO_DIR, f"{unique_id}.mp3")
        temp_wav = os.path.join(TEMP_AUDIO_DIR, f"{unique_id}.wav")

        with open(temp_mp3, "wb") as audio_file:
            audio_file.write(audio_data)

        audio = AudioSegment.from_file(temp_mp3).set_frame_rate(16000).set_channels(1)
        audio.export(temp_wav, format="wav")

        if not os.path.exists(temp_wav) or os.path.getsize(temp_wav) == 0:
            return jsonify({'error': 'FFmpeg conversion failed. WAV file is empty or missing'}), 500

        model = get_model()
        if model is None:
            return jsonify({'error': 'Whisper model not found. Please ensure it is downloaded to the cache.'}), 500

        result = model.transcribe(temp_wav)

        os.remove(temp_mp3)
        os.remove(temp_wav)

        return jsonify({'transcription': result['text']})

    except (base64.binascii.Error, ValueError, TypeError):
        return jsonify({'error': 'Invalid Base64 encoding'}), 400
    except Exception as e:
        return jsonify({'error': f'Internal server error: {str(e)}'}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)





