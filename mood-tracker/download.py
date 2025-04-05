from transformers import pipeline

if __name__ == "__main__":
    try:
        print("Downloading mood tracking model...")
        # Initialize and cache the model
        classifier = pipeline(
            "zero-shot-classification",
            model="facebook/bart-large-mnli"
        )

        print("mood tracking model downloaded successfully ")
    except Exception as e:
        print(f"Failed to download model: {e}")