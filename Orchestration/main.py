import base64
from backend import login_with_phone , create_note , mark_suicide , register_mood , get_notes
from processing import transcribe_audio , suicide_detect , mood_detect

threshold = 0.75
# Get the login phone number from google service with the voice (TO BE REMOVE ; JUST FOR TESTING)
phone = {"phone_number": "961000000"}  
with open("/home/hasanmog/AUB_Masters/projects/aub_kure/speech-to-text/resources/test_audio.mp3", "rb") as f:
    audio_bytes = f.read()
    voice_note = base64.b64encode(audio_bytes).decode('utf-8')

#login with phone 
login_tokens = login_with_phone(phone)
access_token = login_tokens['access']

# voice to text
stt_status , text = transcribe_audio(voice_note) # status to be sent to whatsapp later
# Faced error when rerunning after first attempt , got error 500 (TO BE CHECKED)
# print("text" , text)

# create note
note_id = create_note(token = access_token , text = text)
# print("note_id" , note_id)

# Store if suicidal note
confidence , label = suicide_detect(text = text)

if label == "suicidal" and confidence > threshold :
    _ = mark_suicide(access_token , note_id) 
    
# mood tracker and register based on threshold
moods = mood_detect(text)
# print("moods" , moods)
for mood , score in moods.items() :
    if score > threshold:
        #store
        # print("mood after threshold" , mood)
        _ = register_mood(token = access_token , note_id = note_id ,  mood_data = mood )

# get notes (just for testing)
notes = get_notes(token = access_token)





