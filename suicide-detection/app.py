from flask import Flask, request, jsonify
from transformers import pipeline

app = Flask(__name__)

# Load suicide risk classification model
classifier = pipeline(
    "text-classification",
    model="vibhorag101/roberta-base-suicide-prediction-phr",
    device=-1  # Use CPU by default; change to 0 for GPU
)

@app.route('/health', methods=['GET'])
def health():
    """Endpoint to check if the service is running."""
    return jsonify({"status": "healthy"}), 200

@app.route('/suicide-risk', methods=['POST'])
def suicide_risk():
    """Endpoint to detect suicide risk in text."""
    data = request.json

    if not data or 'text' not in data:
        return jsonify({"error": "No text provided"}), 400

    text = data['text']

    # Classify text
    results = classifier(text)
    response = {"label": results[0]["label"], "confidence": round(results[0]["score"], 4)}
    
    print(response)
    return jsonify(response)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
