import tkinter as tk
import numpy as np
import sounddevice as sd
import random

class AnimatedOverlay:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Jarvis Overlay")

        # ✅ Small fixed window at top-right corner (400x300)
        screen_width = self.root.winfo_screenwidth()
        self.root.geometry(f"400x300+{screen_width-410}+10")
        self.root.configure(bg="#0f0f1a")
        self.root.attributes("-topmost", True)
        self.root.overrideredirect(True)
        self.root.attributes("-alpha", 0.0)

        # ESC key closes overlay with fade
        self.root.bind("<Escape>", lambda e: self.fade_out())

        # ✅ Enable dragging
        self.root.bind("<ButtonPress-1>", self.start_move)
        self.root.bind("<ButtonRelease-1>", self.stop_move)
        self.root.bind("<B1-Motion>", self.do_move)

        # Canvas for waveform circles
        self.canvas = tk.Canvas(self.root, bg="#0f0f1a", highlightthickness=0)
        self.canvas.pack(fill="both", expand=True)

        # States
        self.listening = False
        self.speaking = False

        # ✅ Status, Command, Response labels aligned top-right
        self.status_text = tk.Label(self.root, text="Status: Idle",
                                    fg="cyan", bg="#0f0f1a",
                                    font=("Arial", 12, "bold"))
        self.status_text.place(relx=1.0, x=-10, y=10, anchor="ne")

        self.command_text = tk.Label(self.root, text="Command: None",
                                     fg="lightgreen", bg="#0f0f1a",
                                     font=("Arial", 10))
        self.command_text.place(relx=1.0, x=-10, y=35, anchor="ne")

        self.response_text = tk.Label(self.root, text="Response: None",
                                      fg="orange", bg="#0f0f1a",
                                      font=("Arial", 10), wraplength=380, justify="right")
        self.response_text.place(relx=1.0, x=-10, y=60, anchor="ne")

        # ✅ Close button (X) with hover highlight
        self.close_button = tk.Label(self.root, text="✕",
                                     fg="white", bg="#333333",
                                     font=("Arial", 12, "bold"))
        self.close_button.place(relx=1.0, x=-5, y=5, anchor="ne")
        self.close_button.bind("<Enter>", lambda e: self.close_button.config(bg="red", fg="white"))
        self.close_button.bind("<Leave>", lambda e: self.close_button.config(bg="#333333", fg="white"))
        self.close_button.bind("<Button-1>", lambda e: self.fade_out())

        # Variables for dragging
        self._drag_data = {"x": 0, "y": 0}

        # Waveform parameters
        self.audio_level = 0
        self.center_x = 200
        self.center_y = 150

        # Start audio stream
        self.stream = sd.InputStream(callback=self.audio_callback)
        self.stream.start()

    # ---------------- Dragging methods ----------------
    def start_move(self, event):
        self._drag_data["x"] = event.x
        self._drag_data["y"] = event.y

    def stop_move(self, event):
        self._drag_data["x"] = 0
        self._drag_data["y"] = 0

    def do_move(self, event):
        x = self.root.winfo_x() + (event.x - self._drag_data["x"])
        y = self.root.winfo_y() + (event.y - self._drag_data["y"])
        self.root.geometry(f"+{x}+{y}")

    # ---------------- Audio + Animation ----------------
    def audio_callback(self, indata, frames, time, status):
        """Capture audio amplitude for visualization."""
        if self.listening:
            volume_norm = np.linalg.norm(indata) * 10
            self.audio_level = min(volume_norm, 100)

    def simulate_tts_waveform(self):
        """Simulate waveform pulses when TTS is speaking."""
        if self.speaking:
            self.audio_level = random.randint(20, 80)

    def draw_glow_circle(self, radius, color="#00ffff", intensity=1):
        """Draw concentric glow around a circle."""
        for i in range(3):  # 3 glow layers
            glow_radius = radius + i * 6
            alpha = max(0.1, 1 - (i * 0.3)) * intensity
            self.canvas.create_oval(
                self.center_x - glow_radius, self.center_y - glow_radius,
                self.center_x + glow_radius, self.center_y + glow_radius,
                outline=color, width=2
            )

    def animate(self):
        self.canvas.delete("all")

        # Pick color based on state
        if self.listening:
            color = "cyan"
        elif self.speaking:
            color = "lime"
            self.simulate_tts_waveform()
        else:
            color = "gray"

        # Draw concentric glow circles based on audio_level
        base_radius = 30
        intensity = self.audio_level / 100.0
        for i in range(3):
            r = base_radius + i * 25 + int(self.audio_level / (i+1))
            self.draw_glow_circle(r, color=color, intensity=intensity)

        self.root.after(50, self.animate)

    # ---------------- State methods ----------------
    def set_listening(self, state=True):
        self.listening = state
        self.speaking = False
        self.status_text.config(text="Status: Listening")

    def set_speaking(self, state=True):
        self.speaking = state
        self.listening = False
        self.status_text.config(text="Status: Speaking")

    def set_idle(self):
        self.listening = False
        self.speaking = False
        self.status_text.config(text="Status: Idle")

    def update_command(self, command):
        self.command_text.config(text=f"Command: {command}")

    def update_response(self, response):
        self.response_text.config(text=f"Response: {response}")

    # ---------------- Lifecycle methods ----------------
    def run(self):
        self.animate()
        self.fade_in()
        self.root.mainloop()

    def fade_in(self):
        for i in range(0, 101, 5):
            self.root.attributes("-alpha", i/100)
            self.root.update()
            self.root.after(30)

    def fade_out(self):
        for i in range(100, -1, -5):
            self.root.attributes("-alpha", i/100)
            self.root.update()
            self.root.after(30)
        self.close()

    def close(self):
        self.stream.stop()
        self.stream.close()
        self.root.destroy()
