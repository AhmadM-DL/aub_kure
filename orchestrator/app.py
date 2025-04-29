import threading, time, os
from flask import Flask, request, jsonify, Response, make_response
from backend import login_with_phone, create_note, mark_suicide
from backend import register_mood, register, get_notes, login_with_password
from speech_to_text import transcribe_audio
from mood_tracker import mood_detect
from suicide_detection import suicide_detect
from logging_config import setup_logging
from metrics import  speech_to_text_latency_ms, suicide_detection_latency_ms, mood_tracker_latency_ms
from prometheus_client import generate_latest, CONTENT_TYPE_LATEST
from config import COOKIE_HTTPS

setup_logging()

app = Flask(__name__)
cookie_https = os.getenv(COOKIE_HTTPS).lower()=="true"

def process_note_pipeline(user_token, voice_note):
    try:
        # speech-to-text
        app.logger.info("Transcribing audio ...")
        # with speech_to_text_time.time():
        start = time.time()
        note_text = transcribe_audio(voice_note)
        end = time.time()
        latency_ms = (end - start) * 1000
        speech_to_text_latency_ms.set(latency_ms)
        app.logger.info(f"Transcribed audio: {note_text}")

        # create note
        app.logger.info("Creating Note ...")
        note_id = create_note(user_token=user_token, text=note_text)

        # suicide detection
        app.logger.info("Checking suicidality ...")
        
        start = time.time()
        is_suicidal = suicide_detect(text=note_text)
        end = time.time()
        latency_ms = (end - start) * 1000
        suicide_detection_latency_ms.set(latency_ms)
        app.logger.info(f"Suicidality: {is_suicidal}")
        if is_suicidal:
            app.logger.info("Registering suicidality ...")
            mark_suicide(user_token, note_id)

        # mood detection
        app.logger.info("Checking mood ...")
        mood_tracker_latency_ms
        start = time.time()
        moods = mood_detect(note_text)
        end = time.time()
        latency_ms=(end - start) * 1000
        mood_tracker_latency_ms.set(latency_ms)
        app.logger.info(f"Moods: {moods}")
        for mood in moods:
            app.logger.info(f"Registering mood: {mood}")
            register_mood(user_token=user_token, note_id=note_id, mood=mood)
    except Exception as e:
        raise Exception("Internal Server Error")

@app.route("/note", methods=["POST"])
def process_note():
    data = request.get_json()

    if not data:
        print("error: Missing data")
        return jsonify({"error": "Missing data"}), 400

    if "phone_number" not in data:
        print("error: Missing phone number")
        return jsonify({"error": "Missing phone number"}), 400

    if "audio_base64" not in data:
        print("error: Missing audio_base64")
        return jsonify({"error": "Missing audio"}), 400

    phone_number = data["phone_number"]
    voice_note = data["audio_base64"]

    authenticated, user_token = login_with_phone(phone_number)

    if authenticated:
        threading.Thread(target=process_note_pipeline, args=(user_token, voice_note)).start()
        return jsonify({"status": "ok"}), 200
    else:
        print("error: Authentication failed")
        return jsonify({"error": "Authentication failed"}), 401
    
        
@app.route("/register" , methods = ["POST"])
def register_user():
    data = request.get_json()

    if not data:
        print("error: Missing data")
        return jsonify({"error": "Missing data"}), 400

    if "email" not in data:
        print("error: Missing email")
        return jsonify({"error": "Missing email"}), 400

    if "phone_number" not in data:
        print("error: Missing phone number")
        return jsonify({"error": "Missing phone number"}), 400

    if "password" not in data:
        print("error: Missing password")
        return jsonify({"error": "Missing password"}), 400

    phone_number = data["phone_number"]
    email = data["email"]
    password = data["password"]
    app.logger.info("Registering User ...")
    success = register(email, phone_number, password)
    if success:
        return jsonify({"status": "ok"}), 200
    else:
        return jsonify({"status": "Registration failed"}), 400

@app.route("/login" , methods = ["POST"])
def login():
    data = request.get_json()

    if not data:
        print("error: Missing data")
        return jsonify({"error": "Missing data"}), 400

    if "phone_number" not in data:
        print("error: Missing phone number")
        return jsonify({"error": "Missing phone number"}), 400

    if "password" not in data:
        print("error: Missing password")
        return jsonify({"error": "Missing password"}), 400

    phone_number = data["phone_number"]
    password = data["password"]
    app.logger.info("Authentication Check ...")
    authenticated , access_token = login_with_password(phone_number , password)

    if authenticated:
        response = make_response(jsonify({"message": "Login successful"}), 200)
        response.set_cookie(
            "access_token",
            access_token,
            httponly=True,
            secure=cookie_https,
            samesite='Lax',
            max_age=7200
        )
        return response
    else:
        return jsonify({"error": "Authentication failed"}), 401
    
@app.route("/notes", methods=["GET"])
def get_user_notes():

    access_token = request.cookies.get("access_token")

    if not access_token:
        return jsonify({"error": "Missing access token"}), 401

    try:
        app.logger.info("Fetching Notes ...")
        notes = get_notes(access_token)
        return jsonify({"notes": notes}), 200
    except Exception as e:
        print(f"Error fetching notes: {e}")
        return jsonify({"error": "Internal Server Error"}), 500
    
@app.route('/metrics')
def metrics():
    return Response(generate_latest(), mimetype=CONTENT_TYPE_LATEST)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)

