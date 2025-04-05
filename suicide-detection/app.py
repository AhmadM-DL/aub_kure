import os
from flask import Flask, request, jsonify
from transformers import pipeline

app = Flask(__name__)

model = None 
cache_dir = "/root/.cache/huggingface"  
model_path = os.path.join(cache_dir, "hub", "models--vibhorag101--roberta-base-suicide-prediction-phr")

def get_model():
    global model
    if model is None:
       if os.path.exists(model_path):
            print("Loading suicide detection model from cache...")
            model = pipeline(
                 "text-classification",
                  model="vibhorag101/roberta-base-suicide-prediction-phr"
            )
            print("suicide detection model loaded successfully!")
       else: 
           print("Model not found! Please download it first.")
    return model




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
    model = get_model()
    if(model is not None):
       results = model(text)
       response = {"label": results[0]["label"], "confidence": round(results[0]["score"], 4)}
    else:
       response ={"error": "Model is not downloaded"}
    print(response)
    return jsonify(response)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
