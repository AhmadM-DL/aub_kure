import whisper

if __name__ == "__main__":
    try:
        print("Downloading Whisper model...")
        model = whisper.load_model("base.en", download_root="/root/.cache/whisper")
        print("Whisper model cached successfully at /root/.cache/whisper")
    except Exception as e:
        print(f"Failed to download model: {e}")




