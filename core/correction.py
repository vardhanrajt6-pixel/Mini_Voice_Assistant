import re
from core.logger import get_logger

logger = get_logger("Correction")

CORRECTIONS = {
    r"\bwhat'?s up\b": "whatsapp",
    r"\bwater\b": "whatsapp",
    r"\bwhat sap\b": "whatsapp",
    r"\bwatsapp\b": "whatsapp",
    r"\bcaleneder\b": "calendar",
    r"\bcalender\b": "calendar",
    r"\bcommand\b": "cmd",
    r"\bterminal\b": "cmd",
    r"\bnote pad\b": "notepad",
    r"\bpaint\b": "mspaint",
    r"\bexplore\b": "explorer",
    r"\bedge browser\b": "msedge",
    r"\bchrome browser\b": "chrome",
    r"\bfire fox\b": "firefox",
    r"\bcalc\b": "calculator"
}

def correct_text(text: str) -> str:
    lowered = text.lower().strip()
    for wrong, right in CORRECTIONS.items():
        if re.search(wrong, lowered):
            logger.info(f"Corrected '{wrong}' → '{right}'")
            lowered = re.sub(wrong, right, lowered)
    return lowered
