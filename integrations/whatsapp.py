import subprocess, time, pyautogui
from config.config import APP_ALIASES

def send(contact_name: str, message: str):
    if not contact_name or not message:
        return "Incomplete WhatsApp parameters."
    try:
        whatsapp_alias = APP_ALIASES.get("whatsapp")
        if not whatsapp_alias:
            return "WhatsApp alias not configured in config.py."
        subprocess.Popen(["explorer.exe", f"shell:AppsFolder\\{whatsapp_alias}"])
        time.sleep(5)
        pyautogui.hotkey("ctrl", "f")
        time.sleep(1)
        pyautogui.typewrite(contact_name, interval=0.05)
        time.sleep(2)
        pyautogui.press("enter")
        time.sleep(1)
        pyautogui.typewrite(message, interval=0.05)
        time.sleep(1)
        pyautogui.press("enter")
        return f"WhatsApp message sent to {contact_name}: {message}"
    except Exception as e:
        return f"Failed to send WhatsApp message: {str(e)}"
