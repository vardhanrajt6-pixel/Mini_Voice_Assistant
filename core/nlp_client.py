import requests, json, time, re
from config import config
from core.logger import get_logger

logger = get_logger("GeminiClient")

class GeminiClient:
    def __init__(self):
        self.api_key = config.GEMINI_API_KEY
        self.endpoint = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-flash-latest:generateContent?key={self.api_key}"

    def get_intent(self, text, language="en", retries=3):
        headers = {"Content-Type": "application/json"}
        prompt = f"""
        You are an intent extractor for a Windows voice assistant.
        Input command: "{text}"
        Language: {language}
        Respond ONLY with a valid JSON object.
        Keys: intent (string), parameters (object)
        """
        data = {"contents": [{"parts": [{"text": prompt}]}]}

        for attempt in range(retries):
            try:
                response = requests.post(self.endpoint, headers=headers, json=data)
                if response.status_code == 200:
                    raw_text = response.json()["candidates"][0]["content"]["parts"][0]["text"]
                    cleaned = re.sub(r"```json|```", "", raw_text).strip()
                    try:
                        parsed = json.loads(cleaned)
                        parsed["raw_command"] = text
                        return parsed
                    except json.JSONDecodeError:
                        logger.warning(f"Gemini returned non-JSON: {raw_text}")
                        return self._manual_fallback(text, raw_text)
                elif response.status_code == 429:
                    wait = 2 ** attempt
                    logger.warning(f"Rate limit hit. Retrying in {wait}s...")
                    time.sleep(wait)
                else:
                    logger.error(f"Gemini API error {response.status_code}: {response.text}")
                    break
            except Exception as e:
                logger.error(f"Gemini API request failed: {str(e)}")
                break

        return self._manual_fallback(text, "Gemini API request failed after retries")

    def generate_text(self, text, language="en"):
        headers = {"Content-Type": "application/json"}
        data = {"contents": [{"parts": [{"text": text}]}]}
        try:
            response = requests.post(self.endpoint, headers=headers, json=data)
            if response.status_code == 200:
                return response.json()["candidates"][0]["content"]["parts"][0]["text"].strip()
            logger.error(f"Gemini text API error {response.status_code}: {response.text}")
            return "I'm having trouble responding right now."
        except Exception as e:
            logger.error(f"Gemini text generation failed: {str(e)}")
            return "I couldn’t generate a response."

    def _manual_fallback(self, text, raw_text):
        lowered = text.lower()
        mapping = {
            "stop": "stop_assistant",
            "exit": "stop_assistant",
            "quit": "stop_assistant",
            "jarvis stop": "stop_assistant",
            "change voice": "change_voice",
            "weather": "get_weather",
            "news": "get_news",
            "quote": "quote",
            "joke": "fun",
            "fun": "fun",
            "system": "system_info"
        }
        for key, intent in mapping.items():
            if key in lowered:
                return {"intent": intent, "parameters": {}, "raw_command": text}
        return {"intent": "unknown", "parameters": {"raw": raw_text}, "raw_command": text}
