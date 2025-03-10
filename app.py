from flask import Flask, request, jsonify
import whisper
import os

app = Flask(__name__)


model = whisper.load_model("base")  # Other options: "small", "medium", "large"

@app.route('/transcribe', methods=['POST'])
def transcribe_audio():
    if 'file' not in request.files:
        return jsonify({'error': 'No file uploaded'}), 400
    
    file = request.files['file']
    filename = "temp_audio.mp3"
    file.save(filename)
    
    # Transcribe using Whisper
    result = model.transcribe(filename)
    os.remove(filename) 
    
    return jsonify({'transcription': result['text']})


# Health Check Endpoint
@app.route('/health', methods=['GET'])
def health_check():
    return jsonify({'status': 'healthy', 'message': 'Service is running'}), 200


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)

