import tkinter as tk
import random

class OverlayUI:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Voice Assistant")
        self.root.geometry("600x300")
        self.root.configure(bg="#0f0f1a")

        # Labels
        self.status_label = tk.Label(
            self.root, text="Status: Idle",
            fg="white", bg="#0f0f1a", font=("Arial", 14, "bold")
        )
        self.status_label.pack(pady=5)

        self.command_label = tk.Label(
            self.root, text="Command: None",
            fg="cyan", bg="#0f0f1a", font=("Arial", 12)
        )
        self.command_label.pack(pady=5)

        self.response_label = tk.Label(
            self.root, text="Response: None",
            fg="lightgreen", bg="#0f0f1a", font=("Arial", 12),
            wraplength=550, justify="left"
        )
        self.response_label.pack(pady=5)

        # Canvas for animated waves
        self.canvas = tk.Canvas(self.root, bg="#0f0f1a", highlightthickness=0)
        self.canvas.pack(fill="both", expand=True)

        # Animation state
        self.listening = False
        self.speaking = False
        self.audio_level = 0
        self.center_x = 300
        self.center_y = 150

        # Start animation loop
        self.animate()

    # ---------------- State Updates ----------------
    def update_status(self, status):
        self.status_label.config(text=f"Status: {status}")
        self.root.update_idletasks()

    def update_command(self, command):
        self.command_label.config(text=f"Command: {command}")
        self.root.update_idletasks()

    def update_response(self, response):
        self.response_label.config(text=f"Response: {response}")
        self.root.update_idletasks()

    def set_listening(self, state=True):
        self.listening = state
        self.speaking = False
        self.update_status("Listening")

    def set_speaking(self, state=True):
        self.speaking = state
        self.listening = False
        self.update_status("Speaking")

    def set_idle(self):
        self.listening = False
        self.speaking = False
        self.update_status("Idle")

    # ---------------- Glow Drawing ----------------
    def draw_glow_circle(self, radius, color, intensity=1.0):
        """Draw concentric glow layers around a circle."""
        for i in range(4):  # 4 glow layers
            glow_radius = radius + i * 8
            alpha = max(0.1, 1 - (i * 0.25)) * intensity
            # Simulate glow by varying line width and brightness
            self.canvas.create_oval(
                self.center_x - glow_radius, self.center_y - glow_radius,
                self.center_x + glow_radius, self.center_y + glow_radius,
                outline=color, width=int(2 + alpha * 3)
            )

    # ---------------- Animation ----------------
    def animate(self):
        self.canvas.delete("all")

        if self.listening:
            color = "cyan"
            self.audio_level = random.randint(20, 80)
        elif self.speaking:
            color = "lime"
            self.audio_level = random.randint(30, 90)
        else:
            color = "gray"
            self.audio_level = 10

        base_radius = 30
        intensity = self.audio_level / 100.0
        for i in range(3):
            r = base_radius + i * 25 + int(self.audio_level / (i+1))
            self.draw_glow_circle(r, color, intensity)

        # Keep looping
        self.root.after(100, self.animate)

    # ---------------- Lifecycle ----------------
    def speaking(self, text):
        self.set_speaking()
        self.update_response(text)

    def show(self):
        self.root.deiconify()
        self.root.update()

    def hide(self):
        self.root.withdraw()

    def run(self):
        self.root.mainloop()
