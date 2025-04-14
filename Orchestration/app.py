import base64
from flask import Flask, request, jsonify
from backend import login_with_phone, create_note, mark_suicide, register_mood
from STT import transcribe_audio
from mood import mood_detect
from suicide import suicide_detect

app = Flask(__name__)
threshold = 0.75

@app.route("/process-note", methods=["POST"])
def process_note():
    data = request.get_json()

    if not data or "phone_number" not in data or "voice_note" not in data:
        print("error: Missing phone_number or voice_note")
        return jsonify({"error": "Internal Server Error"}), 400

    phone = {"phone_number": data["phone_number"]}
    voice_note = data["voice_note"]

    try:
        # login
        tokens = login_with_phone(phone)
        access_token = tokens["access"]

        # STT
        _, text = transcribe_audio(voice_note)

        # create note
        note_id = create_note(token=access_token, text=text)

        # suicide detection
        confidence, label = suicide_detect(text=text)
        if label == "suicidal" and confidence > threshold:
            mark_suicide(access_token, note_id)

        # mood detection
        moods = mood_detect(text)
        for mood, score in moods.items():
            if score > threshold:
                register_mood(token=access_token, note_id=note_id, mood_data={mood: score})
                
        return jsonify({"status": "ok"}), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)

