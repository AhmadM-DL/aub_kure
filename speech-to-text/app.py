import os
import uuid
import base64
from flask import Flask, request, jsonify
import whisper
from logging_config import setup_logging
from pydub import AudioSegment
from config import TEMP_AUDIO_DIR, MODEL_CACHE_DIR

setup_logging()
app = Flask(__name__)

os.makedirs(TEMP_AUDIO_DIR, exist_ok=True)
model_path = os.path.join(MODEL_CACHE_DIR, "base.pt")
model = None 

def get_model():
    global model
    success= True
    if model is None:
       if os.path.exists(model_path):
            app.logger.info("Loading Whisper model from cache...")
            model = whisper.load_model("base.en")
            app.logger.info("Whisper model loaded successfully!")
       else: 
           app.logger.info("Model not found! Please download it first.")
           success = False
    return model, success


@app.route('/health', methods=['GET'])
def health_check():
    app.logger.info("'status': 'OK', 'message': 'Whisper API is running")
    return jsonify({"Message":"The service is running properly"}), 200

@app.route('/transcribe', methods=['POST'])
def transcribe_audio():
    
    model, success = get_model()
    if not success:
        app.logger.info("Skipping transcription due to missing model")
        return jsonify({"error": "Internal Server Error"}), 500
    
    if not request.is_json:
        app.logger.info("'error': 'Unsupported Media Type. Use application/json'")
        return jsonify({"error": "Internal Server Error"}), 415

    data = request.get_json()

    if 'audio_base64' not in data:
        app.logger.info("error : No base64 audio provided")
        return jsonify({"error": "Internal Server Error"}), 400

    try:
        audio_data = base64.b64decode(data['audio_base64'])
        unique_id = str(uuid.uuid4())
        temp_mp3 = os.path.join(TEMP_AUDIO_DIR, f"{unique_id}.mp3")
        temp_wav = os.path.join(TEMP_AUDIO_DIR, f"{unique_id}.wav")

        with open(temp_mp3, "wb") as audio_file:
            audio_file.write(audio_data)

        audio = AudioSegment.from_file(temp_mp3).set_frame_rate(16000).set_channels(1)
        with open(temp_wav, "wb") as f:
            audio.export(f, format="wav")


        if not os.path.exists(temp_wav) or os.path.getsize(temp_wav) == 0:
            app.logger.info("'error': 'FFmpeg conversion failed. WAV file is empty or missing'")
            return jsonify({"error": "Internal Server Error"}), 500

        result = model.transcribe(temp_wav)

        os.remove(temp_mp3)
        os.remove(temp_wav)

        return jsonify({'Text': result['text']})

    except (base64.binascii.Error, ValueError, TypeError):
        app.logger.info("'error': 'Invalid Base64 encoding")
        return jsonify({"error": "Internal Server Error"}), 400
    except Exception as e:
        app.logger.info(f"error: 'Internal server error: {str(e)}' ")
        return jsonify({"error": "Internal Server Error"}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)





