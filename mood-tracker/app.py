# app.py
from flask import Flask, request, jsonify
from transformers import pipeline

app = Flask(__name__)

# Initialize the zero-shot classification pipeline only once
classifier = pipeline(
    "zero-shot-classification",
    model="facebook/bart-large-mnli")

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
    results = classifier(text, candidate_labels,multi_label=True)
    response = {label: round(score, 4) for label, score in zip(results["labels"], results["scores"])}
    print(response)
    return jsonify(response)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)