import subprocess
import psutil
import pyautogui
import webbrowser
import requests
import json
import platform
from pathlib import Path

class ActionEngine:
    def __init__(self):
        self.os_name = platform.system()

    def execute(self, command: str) -> str:
        command = command.lower().strip()

        if "open" in command and ("chrome" in command or "browser" in command):
            return self.open_browser()
        elif "open" in command and "youtube" in command:
            return self.open_youtube()
        elif "open" in command and ("notepad" in command or "editor" in command):
            return self.open_notepad()
        elif "open" in command and "spotify" in command:
            return self.open_spotify()
        elif "volume up" in command or "increase volume" in command:
            return self.volume_up()
        elif "volume down" in command or "decrease volume" in command:
            return self.volume_down()
        elif "volume mute" in command or "mute" in command:
            return self.volume_mute()
        elif "screenshot" in command:
            return self.take_screenshot()
        elif "search" in command or "google" in command:
            query = command.replace("search", "").replace("google", "").replace("for", "").strip()
            return self.google_search(query)
        elif "weather" in command:
            return self.get_weather()
        elif "time" in command or "date" in command:
            from datetime import datetime
            return f"The current time is {datetime.now().strftime('%I:%M %p')} on {datetime.now().strftime('%B %d, %Y')}."
        elif "shutdown" in command or "turn off" in command:
            return self.shutdown_pc()
        elif "restart" in command or "reboot" in command:
            return self.restart_pc()
        elif "lock" in command or "lock pc" in command:
            return self.lock_pc()
        elif "battery" in command:
            return self.get_battery()
        elif "cpu" in command or "usage" in command:
            return self.get_system_usage()
        elif "type" in command:
            text = command.replace("type", "").strip()
            return self.type_text(text)
        elif "minimize" in command or "minimise" in command:
            pyautogui.hotkey("win", "d")
            return "Minimized all windows."
        elif "close" in command:
            pyautogui.hotkey("alt", "f4")
            return "Closed current window."
        else:
            return None

    def open_browser(self):
        chrome_paths = [
            r"C:\Program Files\Google\Chrome\Application\chrome.exe",
            r"C:\Program Files (x86)\Google\Chrome\Application\chrome.exe",
            r"C:\Users\HP\AppData\Local\Google\Chrome\Application\chrome.exe",
        ]
        for path in chrome_paths:
            if Path(path).exists():
                subprocess.Popen([path])
                return "Opening Chrome."
        return "Chrome not found. Opening default browser."

    def open_youtube(self):
        webbrowser.open("https://youtube.com")
        return "Opening YouTube."

    def open_notepad(self):
        subprocess.Popen(["notepad.exe"])
        return "Opening Notepad."

    def open_spotify(self):
        spotify_paths = [
            r"C:\Users\HP\AppData\Roaming\Spotify\Spotify.exe",
            r"C:\Program Files\Spotify\Spotify.exe",
        ]
        for path in spotify_paths:
            if Path(path).exists():
                subprocess.Popen([path])
                return "Opening Spotify."
        webbrowser.open("https://open.spotify.com")
        return "Opening Spotify web player."

    def volume_up(self):
        pyautogui.press("volumeup", presses=5)
        return "Volume increased."

    def volume_down(self):
        pyautogui.press("volumedown", presses=5)
        return "Volume decreased."

    def volume_mute(self):
        pyautogui.press("volumemute")
        return "Volume toggled mute."

    def take_screenshot(self):
        screenshots_dir = Path.home() / "Pictures" / "Screenshots"
        screenshots_dir.mkdir(parents=True, exist_ok=True)
        path = screenshots_dir / f"screenshot_{int(__import__('time').time())}.png"
        pyautogui.screenshot(str(path))
        return f"Screenshot saved to {path}."

    def google_search(self, query):
        if not query:
            webbrowser.open("https://google.com")
            return "Opening Google."
        webbrowser.open(f"https://google.com/search?q={query.replace(' ', '+')}")
        return f"Searching Google for {query}."

    def get_weather(self):
        try:
            resp = requests.get("https://wttr.in/?format=%C+%t", timeout=5)
            return f"Weather: {resp.text.strip()}"
        except:
            return "Could not fetch weather."

    def shutdown_pc(self):
        subprocess.run(["shutdown", "/s", "/t", "10"])
        return "Shutting down in 10 seconds. Say 'cancel shutdown' to abort."

    def restart_pc(self):
        subprocess.run(["shutdown", "/r", "/t", "10"])
        return "Restarting in 10 seconds. Say 'cancel shutdown' to abort."

    def lock_pc(self):
        subprocess.run(["rundll32.exe", "user32.dll,LockWorkStation"])
        return "Locking PC."

    def get_battery(self):
        battery = psutil.sensors_battery()
        if battery:
            plug = "plugged in" if battery.power_plugged else "on battery"
            return f"Battery at {battery.percent}%, {plug}."
        return "No battery detected."

    def get_system_usage(self):
        cpu = psutil.cpu_percent(interval=1)
        mem = psutil.virtual_memory().percent
        return f"CPU at {cpu}%, Memory at {mem}%."

    def type_text(self, text):
        pyautogui.write(text, interval=0.05)
        pyautogui.press("enter")
        return f"Typed: {text}"
