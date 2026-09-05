import sys
import threading
from config import config
from core.wake_word import WakeWordDetector
from core.toggle import ToggleControl
from core.speech_to_text import SpeechToText
from core.text_to_speech import TextToSpeech
from core.nlp_client import GeminiClient
from core.dispatcher import Dispatcher
from core.logger import get_logger
from core.correction import correct_text
from ui.animated_overlay import AnimatedOverlay

logger = get_logger("Jarvis")

def detect_language(text: str) -> str:
    """Detect language based on Unicode ranges (Telugu vs English)."""
    if any("\u0C00" <= ch <= "\u0C7F" for ch in text):
        return "te"
    return "en"

def assistant_loop(ui: AnimatedOverlay):
    """Main assistant loop: wake word detection, command handling, response generation."""
    toggle = ToggleControl()
    tts = TextToSpeech()
    stt = SpeechToText()
    gemini = GeminiClient()
    dispatcher = Dispatcher()
    detector = WakeWordDetector()

    while toggle.is_active():
        ui.set_idle()
        logger.info("Listening for wake word...")

        if not detector.listen_once():
            continue

        lang = detector.last_language
        logger.info(f"Wake word detected ({lang.upper()}). Ready for commands.")
        tts.speak("Hello Sir, I am ready for your command.", language=lang, overlay=ui)
        ui.set_listening()

        while toggle.is_active():
            command = stt.listen()
            if not command:
                continue

            corrected_command = correct_text(command)
            logger.info(f"Command heard: {command} → corrected: {corrected_command}")
            ui.update_command(corrected_command)

            lowered = corrected_command.lower().strip()
            if any(word in lowered for word in ["stop", "stop listening", "exit", "quit", "jarvis stop"]):
                logger.warning("Voice Assistant stopped by voice command.")
                tts.speak("Stopping Voice Assistant.", language=lang, overlay=ui)
                ui.set_idle()
                ui.fade_out()
                toggle.turn_off()
                return

            lang = detect_language(corrected_command)
            response = gemini.get_intent(corrected_command, language=lang)
            logger.info(f"Gemini Response ({lang}): {response}")

            action_result = dispatcher.route(response)
            logger.info(f"Action Result: {action_result}")

            ui.update_response(action_result)
            tts.speak(action_result, language=lang, overlay=ui)

            if response.get("intent") == "stop_assistant":
                logger.warning("Voice Assistant stopped by Gemini intent.")
                tts.speak("Stopping Voice Assistant.", language=lang, overlay=ui)
                ui.set_idle()
                ui.fade_out()
                toggle.turn_off()
                return

    # If assistant is inactive
    ui.set_idle()
    ui.fade_out()
    logger.info("Voice Assistant is OFF")

def main():
    try:
        if not config.ASSISTANT_ACTIVE:
            logger.info("Voice Assistant is OFF (config toggle). Enable in config.py to start.")
            sys.exit(0)

        logger.info("Starting Voice Assistant...")
        ui = AnimatedOverlay()

        assistant_thread = threading.Thread(target=assistant_loop, args=(ui,), daemon=True)
        assistant_thread.start()

        ui.run()

    except KeyboardInterrupt:
        logger.error("Voice Assistant stopped manually (Ctrl+C).")
        if 'ui' in locals():
            ui.fade_out()
        sys.exit(0)

    finally:
        logger.info("Voice Assistant exited cleanly.")

if __name__ == "__main__":
    main()
