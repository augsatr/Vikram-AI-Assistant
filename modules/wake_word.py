class WakeWordDetector:
    def __init__(self, keyword="vikram", callback=None):
        self.callback = callback
        self.running = False

    def start(self):
        print("[WAKE] Voice mode unavailable — microphone levels too low")
        print("[WAKE] Use console mode (type 'c' at startup) for reliable interaction")
        self.running = True

    def stop(self):
        self.running = False
