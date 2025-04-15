import base64, threading
from flask import Flask, request, jsonify
from backend import login_with_phone, create_note, mark_suicide, register_mood
from speech_to_text import transcribe_audio
from mood_tracker import mood_detect
from suicide_detection import suicide_detect

app = Flask(__name__)


def process_note_pipeline(user_token, voice_note):
    try:
        # speech-to-text
        note_text = transcribe_audio(voice_note)

        # create note
        note_id = create_note(user_token=user_token, text=note_text)

        # suicide detection
        is_suicidal = suicide_detect(text=note_text)
        if is_suicidal:
            mark_suicide(user_token, note_id)

        # mood detection
        moods = mood_detect(note_text)
        for mood in moods:
            register_mood(user_token=user_token, note_id=note_id, mood=mood)
    except Exception as e:
        raise Exception("Internal Server Error")



@app.route("/note", methods=["POST"])
def process_note():
    data = request.get_json()

    if not data or "phone_number" not in data or "voice_note" not in data:
        print("error: Missing phone_number or voice_note")
        return jsonify({"error": "Internal Server Error"}), 400

    phone_number = data["phone_number"]
    voice_note = data["voice_note"]

    # authenticate
    authenticated, user_token = login_with_phone(phone_number)

    if authenticated:
        threading.Thread(target=process_note_pipeline, args=(user_token, voice_note)).start()
        return jsonify({"status": "ok"}), 200
    else:
        print("error: Authentication failed")
        return jsonify({"error": "Authentication failed"}), 401

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)

