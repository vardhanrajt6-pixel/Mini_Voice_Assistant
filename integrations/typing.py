import time, pyautogui
from integrations import system
from config.config import APP_ALIASES

def type_text(text: str, app_name: str = None):
    if not text:
        return "No text provided."
    try:
        if app_name:
            mapped = APP_ALIASES.get(app_name.lower(), app_name)
            system.open_app(mapped)
            time.sleep(2)
        pyautogui.typewrite(text, interval=0.05)
        return f"Typed '{text}' in {app_name or 'current window'}."
    except Exception as e:
        return f"Failed to type text: {str(e)}"
