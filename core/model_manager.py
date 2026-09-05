# model_manager.py
# No longer needed for faster-whisper, but kept for compatibility

from faster_whisper import WhisperModel

# Choose model size: tiny, base, small, medium, large-v2
# Use device="cuda" if you have GPU, else "cpu"
whisper_model = WhisperModel("base", device="cuda", compute_type="float16")
