from flask import Flask, request, jsonify
from orchestrator import process_note
from utils import read_secret
from config import HANDSHAKE_SECRET_FILE
from meta import download_media, get_media_url, send_message
import base64
import random
import threading
from logging_config import setup_logging

setup_logging()

app = Flask(__name__)

WELL_RECIEVED_MESSAGES = [
    "Thanks! We received your voice message.",
    "Got it—thanks for sending your voice note!",
    "Voice message received loud and clear 🎤",
    "Thanks, your audio message has been recorded.",
    "Appreciate your voice message!",
    "Noted!",
    "Well received!",
    "Keep healthy!",
    "I hope it is a good note!",
]

NOT_REGISTERED_MESSAGE="Thank you for your intrest in Kure app! You are not registered yet. Register now on kure.com."

def process_whatsapp_message(data:dict):
    try:
        for entry in data.get('entry', []):
            for change in entry.get('changes', []):
                value = change.get('value', {})
                metadata = value.get('metadata', {})
                phone_number_id = metadata.get('phone_number_id')
                messages = value.get('messages', [])
                app.logger.info(f"Recieved messages {messages}")
                for message in messages:
                    msg_type = message.get('type')
                    if msg_type == 'audio':
                        app.logger.info("Recieved audio ...")
                        phone_number = message['from']
                        app.logger.info(f"From {phone_number}")
                        audio_id = message['audio']['id']

                        app.logger.info("Getting audio url ...")
                        media_url = get_media_url(audio_id)
                        app.logger.info(f"Url {media_url}")
                        if not media_url:
                            continue
                        app.logger.info("Downloading audio ...")
                        audio_binary = download_media(media_url)
                        audio_b64 = base64.b64encode(audio_binary).decode('utf-8')
                        app.logger.info("Processing note ...")
                        success = process_note(phone_number, audio_b64)
                        if success:
                            reply = random.choice(WELL_RECIEVED_MESSAGES)
                            send_message(phone_number_id, phone_number, reply)
                        else:
                            reply = NOT_REGISTERED_MESSAGE
                            send_message(phone_number_id, phone_number, reply)
    except Exception as e:
        app.logger.error(f"Error {e}")

@app.route('/health', methods=['GET'])
def health_check():
    return jsonify({"status": "ok"}), 200

@app.route('/webhook', methods=['GET'])
def webhook_handshake():
    mode = request.args.get("hub.mode")
    token = request.args.get("hub.verify_token")
    challenge = request.args.get("hub.challenge")
    VERIFY_TOKEN = read_secret(HANDSHAKE_SECRET_FILE) 
    if mode == "subscribe" and token == VERIFY_TOKEN:
        return challenge, 200
    else:
        return "Forbidden", 403

@app.route('/webhook', methods=['POST'])
def webhook_receive():
    data = request.get_json()
    threading.Thread(target=process_whatsapp_message, args=(data,)).start()
    return jsonify({"status": "processed"}), 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)

