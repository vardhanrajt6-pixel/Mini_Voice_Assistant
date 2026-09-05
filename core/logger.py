import logging
from colorama import Fore, Style, init

init(autoreset=True)

class ColorFormatter(logging.Formatter):
    def format(self, record):
        colors = {
            logging.INFO: Fore.GREEN,
            logging.WARNING: Fore.YELLOW,
            logging.ERROR: Fore.RED
        }
        color = colors.get(record.levelno, Fore.WHITE)
        return f"{color}{record.levelname} [{record.name}] {record.getMessage()}{Style.RESET_ALL}"

def get_logger(name="Jarvis"):
    logger = logging.getLogger(name)
    if not logger.handlers:
        handler = logging.StreamHandler()
        handler.setFormatter(ColorFormatter())
        logger.addHandler(handler)
        logger.setLevel(logging.INFO)
    return logger
