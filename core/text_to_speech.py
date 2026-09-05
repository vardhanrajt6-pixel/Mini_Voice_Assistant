import pyttsx3

class TextToSpeech:
    def __init__(self):
        self.rate = 175
        self.volume = 1.0
        self.current_voice_index = 0

    def speak(self, text, language="en", overlay=None):
        engine = pyttsx3.init()
        engine.setProperty("rate", self.rate)
        engine.setProperty("volume", self.volume)

        voices = engine.getProperty("voices")
        if voices:
            engine.setProperty("voice", voices[self.current_voice_index].id)

        safe_text = str(text).strip() or "I didn’t catch that, please try again."
        print(f"Assistant says ({language}): {safe_text}")

        if overlay:
            overlay.set_speaking()

        engine.say(safe_text)
        engine.runAndWait()

        if overlay:
            overlay.set_idle()

    def change_voice(self):
        voices = pyttsx3.init().getProperty("voices")
        if not voices:
            return "No voices available."
        self.current_voice_index = (self.current_voice_index + 1) % len(voices)
        return f"Voice changed to {voices[self.current_voice_index].name}."

    def set_emotion(self, emotion):
        emotion = emotion.lower()
        if emotion == "excited":
            self.rate, self.volume = 200, 1.0
            return "Emotion set to Excited (faster, louder)."
        elif emotion == "calm":
            self.rate, self.volume = 150, 0.8
            return "Emotion set to Calm (slower, softer)."
        elif emotion == "serious":
            self.rate, self.volume = 175, 1.0
            return "Emotion set to Serious (steady tone)."
        return f"Unknown emotion: {emotion}. Available: excited, calm, serious."
