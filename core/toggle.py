from config import config

class ToggleControl:
    def __init__(self):
        self.active = config.ASSISTANT_ACTIVE

    def turn_on(self):
        self.active = True
        print("Jarvis Assistant is now ON")

    def turn_off(self):
        self.active = False
        print("Jarvis Assistant is now OFF")

    def is_active(self):
        return self.active
