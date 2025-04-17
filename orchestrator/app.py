import base64, threading
from flask import Flask, request, jsonify
from backend import login_with_phone, create_note, mark_suicide, register_mood , register_user , get_notes , login_with_password
from speech_to_text import transcribe_audio
from mood_tracker import mood_detect
from suicide_detection import suicide_detect
from logging_config import setup_logging

setup_logging()

app = Flask(__name__)

def process_note_pipeline(user_token, voice_note):
    try:
        # speech-to-text
        app.logger.info("Transcribing audio ...")
        note_text = transcribe_audio(voice_note)
        app.logger.info(f"Transcribed audio: {note_text}")

        # create note
        app.logger.info("Creating Note ...")
        note_id = create_note(user_token=user_token, text=note_text)

        # suicide detection
        app.logger.info("Checking suicidality ...")
        is_suicidal = suicide_detect(text=note_text)
        app.logger.info(f"Suicidality: {is_suicidal}")
        if is_suicidal:
            app.logger.info("Registering suicidality ...")
            mark_suicide(user_token, note_id)

        # mood detection
        app.logger.info("Checking mood ...")
        moods = mood_detect(note_text)
        app.logger.info(f"Moods: {moods}")
        for mood in moods:
            app.logger.info(f"Registering mood: {mood}")
            register_mood(user_token=user_token, note_id=note_id, mood=mood)
    except Exception as e:
        raise Exception("Internal Server Error")


@app.route("/note", methods=["POST"])
def process_note():
    data = request.get_json()

    if not data or "phone_number" not in data or "voice_note" not in data:
        print("error: Missing phone_number or voice note")
        return jsonify({"error": "Missing phone number or audio"}), 400 # message to be checked

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
    
        
@app.route("/register" , methods = ["POST"])
def user_register():
    data = request.get_json()
    if not data or "email" not in data or "phone_number" not in data or "password" not in data:
        print("error: Missing email , phone number or password")
        return jsonify({"error" : "missing email , phone number or password "}) , 400  #message to be checked
    
    phone_number = data["phone_number"]
    email = data["email"]
    password = data["password"]
    app.logger.info("Registering User")
    response = register_user(email , phone_number , password)
    print(response)
    return jsonify({"status": "ok"}), 200  # put the message as user registered successfully ? 

@app.route("/login" , methods = ["POST"])
def password_login():
    data = request.get_json()
    if not data or "phone_number" not in data or "password" not in data :
        print("error: Missing phone number or password")
        return jsonify({"error" : "Missing phone number or password"}) , 400 # message to be checked
    
    phone_number = data["phone_number"]
    password = data["password"]
    app.logger.info("Authentication Check")
    authenticated , access_token = login_with_password(phone_number , password)
    
    if authenticated:
        return jsonify({"access_token": access_token}), 200
 
    else:
        print("error: Authentication failed")
        return jsonify({"error": "Authentication failed"}), 401
    
    
@app.route("/notes", methods=["GET"])
def get_user_notes():
    app.logger.info("Authorization Check")
    auth_header = request.headers.get("Authorization")
    if not auth_header or not auth_header.startswith("Bearer"):
        return jsonify({"error": "Authorization header missing or invalid"}), 401
    app.logger.info("Authorization Success")
    user_token = auth_header.split(" ")[1]

    try:
        app.logger.info("Fetching Notes")
        notes = get_notes(user_token)
        return jsonify({"notes": notes}), 200
    except Exception as e:
        print(f"Error fetching notes: {e}")
        return jsonify({"error": "Internal Server Error"}), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)

