# download.py
from transformers import pipeline

print("Downloading the model 'facebook/bart-large-mnli'...")

# Initialize and cache the model
classifier = pipeline(
    "zero-shot-classification",
    model="facebook/bart-large-mnli"
)

print("Model downloaded and cached successfully!")
