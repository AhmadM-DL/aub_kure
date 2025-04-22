# 🩺 Kure

Kure is a mental health support platform designed to help individuals track and understand their emotional well-being through voice. By simply sending WhatsApp voice notes, users can record their thoughts, which are then transcribed, analyzed, and stored using AI. Kure detects emotional patterns, tracks mood shifts, and flags signs of suicidal ideation—empowering users and therapists with meaningful insights to support ongoing mental health care.

## ⬇️ Deployment
* Clone the repositroy
* 🔐 Create a secrets folder in the repo and including the following files/secrets:
    * backend_secret.txt (Django App Secret - Used For Hashing)
    * db_password.txt
    * db_user.txt 
    * handshake_secret.txt (Whatsapp Handshake Secret)
    * whatsapp_secret.text (Whatsapp API Key)
    * **N.B. for convenience the secrets are stored in github**
* Build database
    * `docker exec aub_kure-backend-1 python maange.py makemigrations`
    * `docker exec aub_kure-backend-1 python maange.py migrate`
    * `docker restart aub_kure-backend-1`
* Download Models
    * `docker exec aub_kure-mood-tracker-1 python download.py`
    * `docker exec aub_kure-speech-to-text-1 python download_model.py`
    * `docker exec aub_kure-suicide-detection-1 python download.py`
* Expose Whatsapp service through ngrok in the background
    * `ngrok http --url=your-domain 5003 > /dev/null &`

## ▶️ Deployment Endpoints
* Web App: [http://18.224.45.207/](http://18.224.45.207/)
* Dummy phone number: 96171177395
* Dummy password: password 
