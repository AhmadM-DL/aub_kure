# app.py
from flask import Flask, request, jsonify
from transformers import pipeline
from config import MODEL_CACHE
import os

app = Flask(__name__)

model = None 
model_path = os.path.join(MODEL_CACHE, "hub", "models--facebook--bart-large-mnli")

def get_model():
    global model
    success= True
    if model is None:
       if os.path.exists(model_path):
            print("Loading mood tracking model from cache...")
            model = pipeline(
                 "zero-shot-classification",
                  model="facebook/bart-large-mnli")
            print("mood tracking model loaded successfully!")
       else: 
           print("Model not found! Please download it first.")
           success= False
    return model, success


@app.route('/health', methods=['GET'])
def health():
    """Endpoint to check if the service is running."""
    return jsonify({"status": "Healthy"}), 200

@app.route('/sentiment', methods=['POST'])
def sentiment():
    """Endpoint to analyze sentiment of provided text."""
    data = request.json
    
    if not data or 'text' not in data:
        return jsonify({"error": "No text provided"}), 400
    
    text = data['text']
    
    # Define sentiment classes
    # nrc lexicon
    candidate_labels = ["Anger", "Disgust", "Sadness", "Surprise", "Fear", "Trust", "Joy", "Anticipation"]
    
    # Classify text
    model, success = get_model()
    if(success):
        results = model(text, candidate_labels, multi_label=True)
        response = {label: round(score, 4) for label, score in zip(results["labels"], results["scores"])}
        response_status = 200
    else:
       response ={"error": "Internal Server Error"}
       response_status= 500
    print(response)
    return jsonify(response), response_status

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)