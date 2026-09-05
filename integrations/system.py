import os, subprocess
from config.config import APP_ALIASES

def open_app(app_name: str):
    if not app_name:
        return "No application name provided."
    app_name = app_name.lower()
    mapped = APP_ALIASES.get(app_name, app_name)
    try:
        if "!WhatsApp" in mapped or mapped.startswith("5319275A."):
            subprocess.Popen(["explorer.exe", f"shell:AppsFolder\\{mapped}"])
        elif mapped.endswith(".exe") or "\\" in mapped:
            subprocess.Popen([mapped], shell=True)
        else:
            os.system(f"start {mapped}")
        return f"Opened {app_name}."
    except Exception as e:
        return f"Failed to open {app_name}: {str(e)}"
