from transformers import pipeline

if __name__ == "__main__":
    try:
        print("Downloading suicide detection model...")
        # Initialize and cache the model
        classifier = pipeline(
            "text-classification",
            model="vibhorag101/roberta-base-suicide-prediction-phr"
        )

        print("suicide detection model downloaded successfully ")
    except Exception as e:
        print(f"Failed to download model: {e}")
