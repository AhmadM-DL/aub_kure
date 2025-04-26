# 🩺 Kure

[![Docker Compose CI/CD](https://github.com/AhmadM-DL/aub_kure/actions/workflows/docker%20build%20and%20compose.yml/badge.svg?branch=main)](https://github.com/AhmadM-DL/aub_kure/actions/workflows/docker%20build%20and%20compose.yml)

Kure is a mental health support platform designed to help individuals track and understand their emotional well-being through voice. By simply sending WhatsApp voice notes, users can record their thoughts, which are then transcribed, analyzed, and stored using AI. Kure detects emotional patterns, tracks mood shifts, and flags signs of suicidal ideation—empowering users and therapists with meaningful insights to support ongoing mental health care.

# 💡 Functionality

- Interfaced using whatsapp so you can communicate your thoughts easily!
- Transcribe your voice through state of the art AI models.
- State of the art suicide detection language model.
- State of the art emotion detection language model based on a sound emotion [lexicon](https://nrc-publications.canada.ca/eng/view/object/?id=0b6a5b58-a656-49d3-ab3e-252050a7a88c).
- Access your notes easily using a simple web interface.
- Dashboard to monitor your mood.

# ⚙️ Architecture

![](https://github.com/AhmadM-DL/aub_kure/blob/main/resources/Kure_Architecture.png)

# ⬇️ Deployment Docker

- Clone the repositroy (Use releases)
- 🔐 Create a secrets folder in the repo and including the following files/secrets:
  - backend_secret.txt (Django App Secret - Used For Hashing)
  - db_password.txt
  - db_user.txt
  - handshake_secret.txt (Whatsapp Handshake Secret)
  - whatsapp_secret.text (Whatsapp API Key)
  - **N.B. for convenience the secrets are stored in github**
- Compose
  - `docker-compose up -d --build`
- Build database
  - `docker exec aub_kure-backend-1 python manage.py migrate`
- Download Models
  - `docker exec aub_kure-mood-tracker-1 python download.py`
  - `docker exec aub_kure-speech-to-text-1 python download.py`
  - `docker exec aub_kure-suicide-detection-1 python download.py`
- Expose Whatsapp service through ngrok (Whatsapp requires HTTPS endpoint) in the background
  - `ngrok http --url=your-domain 5003 > /dev/null &`
- Open localhost:80 to access the web application

# Deployment K8s

- Clone the repositroy  (Use releases)
- 🔐 Create a secrets folder in kure-kustomize-deployment/overlays/production/ and including the following files:
  - backend_secret.txt (Django App Secret - Used For Hashing)
  - db_password.txt
  - db_user.txt
  - handshake_secret.txt (Whatsapp Handshake Secret)
  - whatsapp_secret.text (Whatsapp API Key)
  - **N.B. for convenience the secrets are stored in github**
- Build
  - `kubectl apply -k kure-kustomize-deployment/overlays/production`
- Make sure all images are pulled and pods are in `Running` state
  - `kubectl get pods`
- Build database
  - `kubectl exec deployment/backend -- python manage.py migrate`
- Download Models
  - `kubectl exec deployment/mood-tracker -- python download.py`
  - `kubectl exec deployment/speech-to-text -- python download.py`
  - `kubectl exec deployment/suicide-detection -- python download.py`
- Expose Whatsapp service through ngrok (Whatsapp requires HTTPS endpoint) in the background
  - `ngrok http --url=your-domain 30015 > /dev/null &`
- Open localhost:30014 to access the web application

# ▶️ Deployment Endpoints

- Web App: [http://3.133.156.16/](3.133.156.16)
- Dummy phone number: 96171177395
- Dummy password: password

# 🛝 Slides

- Canva Slides: [Link Here](https://www.canva.com/design/DAGlbkLfh5E/n5lD47Diiejwu7OzerHdUg/edit?utm_content=DAGlbkLfh5E&utm_campaign=designshare&utm_medium=link2&utm_source=sharebutton)
