from integrations import typing, system, browser, email, whatsapp
from core.logger import get_logger
from config.config import APP_ALIASES
import pyautogui, time, subprocess, psutil
from core.text_to_speech import TextToSpeech
from core.nlp_client import GeminiClient

logger = get_logger("Dispatcher")

class Dispatcher:
    def __init__(self):
        self.tts = TextToSpeech()
        self.gemini = GeminiClient()

    def route(self, intent_data):
        intent = intent_data.get("intent", "unknown")
        params = intent_data.get("parameters", {})
        raw_command = intent_data.get("raw_command", "")

        try:
            if intent == "open_app":
                app_name = params.get("app_name", "").lower()
                mapped = APP_ALIASES.get(app_name, app_name)
                system.open_app(mapped)
                return self.gemini.generate_text(f"I opened {app_name} for you.")

            elif intent == "search_web":
                return self.gemini.generate_text(browser.search(params.get("query")))

            elif intent == "send_email":
                return self.gemini.generate_text(email.send(params.get("to"), params.get("subject"), params.get("body")))

            elif intent == "send_whatsapp":
                return self.gemini.generate_text(whatsapp.send(params.get("to"), params.get("message")))

            elif intent in ["type_text", "write_text"]:
                return self.gemini.generate_text(typing.type_text(params.get("text", ""), params.get("app_name", "")))

            elif intent == "generate_text":
                prompt = params.get("prompt", "")
                if not prompt:
                    return "No prompt provided for text generation."
                generated = self.gemini.generate_text(prompt)
                subprocess.Popen(["notepad.exe"])
                time.sleep(1.5)
                pyautogui.typewrite(generated)
                return generated

            elif intent == "change_voice":
                return self.gemini.generate_text(self.tts.change_voice())

            elif intent == "system_info":
                cpu, ram = psutil.cpu_percent(), psutil.virtual_memory().percent
                battery = psutil.sensors_battery().percent if psutil.sensors_battery() else "N/A"
                return self.gemini.generate_text(f"System status: CPU {cpu}%, RAM {ram}%, Battery {battery}%.")

            elif intent == "stop_assistant":
                return "Stopping Voice Assistant..."

            elif intent == "error":
                return f"NLP failed: {params.get('message','Unknown error')}"

            # Conversational fallback
            logger.info(f"Routing conversational intent '{intent}' to Gemini.")
            prompt = raw_command or params.get("prompt", "") or f"User asked: {intent}"
            return self.gemini.generate_text(prompt)

        except Exception as e:
            logger.error(f"Error handling intent '{intent}': {str(e)}")
            return self.gemini.generate_text(f"An error occurred while handling '{intent}'.")
