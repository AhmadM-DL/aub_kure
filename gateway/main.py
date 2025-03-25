from flask import Flask, request, jsonify
import requests

app = Flask(__name__)

ASR_URL = "http://speech-to-text:5000/transcribe"
MOOD_URL = "http://mood-tracker:5000/sentiment"
SUICIDE_URL = "http://suicide-detection:5000/classify"  # not defined yet


@app.route("/")
def home():
    return jsonify({"message": "KURE Gateway is running."})

@app.route("/pipeline", methods=["POST"])
def pipeline():
    data = request.get_json()
    if not data or "audio_base64" not in data:
        return jsonify({"error": "Missing 'audio_base64' in request body"}), 400

    audio_b64 = data["audio_base64"]

    try:
        # Step 1: Speech-to-Text
        
        asr_res = requests.post(ASR_URL, json={"audio_base64": audio_b64})
        asr_res.raise_for_status()

        transcript = asr_res.json().get("transcript", "")
        print("📢 ASR Transcript:", transcript)

        if not transcript:
            return jsonify({"error": "ASR returned empty transcript"}), 500

        # Step 2: Mood Analysis
        mood_res = requests.post(MOOD_URL, json={"text": transcript})
        mood_res.raise_for_status()
        mood = mood_res.json()

        # # Step 3: Suicide Risk Classification
        # suicide_res = requests.post(SUICIDE_URL, json={"text": transcript})
        # suicide_res.raise_for_status()
        # suicide = suicide_res.json().get("risk", "unknown")

        return jsonify({
            "transcript": transcript,
            "mood": mood,
            # "suicidal": suicide
        })

    except requests.exceptions.RequestException as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000)
