from faster_whisper import WhisperModel
import sounddevice as sd
import numpy as np

class SpeechToText:
    def __init__(self, model_size="base", device="cuda", compute_type="float16"):
        # ✅ Configurable model size and device
        self.model = WhisperModel(model_size, device=device, compute_type=compute_type)

    def listen(self, duration=5, samplerate=16000):
        """Capture voice input and convert to text using faster-whisper"""
        print("Listening for command...")

        audio = sd.rec(int(duration * samplerate),
                       samplerate=samplerate,
                       channels=1,
                       dtype='float32')
        sd.wait()

        segments, _ = self.model.transcribe(np.squeeze(audio), vad_filter=True)
        text = " ".join([segment.text for segment in segments]).strip()

        if text:
            print(f"You said: {text}")
            return text.lower()
        print("Sorry, I could not understand.")
        return ""
