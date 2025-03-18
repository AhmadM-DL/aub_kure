import whisper

print("📥 Downloading Whisper model...")

# Explicitly set cache directory (to match volume)
model = whisper.load_model("base", download_root="/root/.cache/whisper")

print("✅ Whisper model cached successfully at /root/.cache/whisper")
