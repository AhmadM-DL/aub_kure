# download.py
from transformers import pipeline

print("Downloading the model 'facebook/bart-large-mnli'...")

# Initialize and cache the model
classifier = pipeline(
    "text-classification",
    model="vibhorag101/roberta-base-suicide-prediction-phr"
)
print("Model downloaded and cached successfully!")
