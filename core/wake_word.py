import numpy as np
import sounddevice as sd
import difflib
from config import config
from core.model_manager import whisper_model

class WakeWordDetector:
    def __init__(self, samplerate=16000):
        self.samplerate = samplerate
        self.last_language = "en"

    def _is_wake_word(self, text):
        if not text:
            return False
        candidates = [w.lower() for w in config.WAKE_WORDS]
        return bool(difflib.get_close_matches(text.lower(), candidates, cutoff=0.7))

    def listen_once(self, duration=3):
        """Listen until a wake word is detected, then return True once."""
        print(f"Listening for wake words: {config.WAKE_WORDS}...")

        audio = sd.rec(int(duration * self.samplerate),
                       samplerate=self.samplerate,
                       channels=1,
                       dtype='float32')
        sd.wait()

        segments, _ = whisper_model.transcribe(np.squeeze(audio), vad_filter=True)
        text = " ".join([segment.text for segment in segments]).lower().strip()

        print("Heard:", text)
        if self._is_wake_word(text):
            print(f"Wake word detected: {text}")
            self.last_language = "en"
            return True
        return False
