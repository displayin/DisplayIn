import json

class Settings:
    def __init__(self, hideTaskbar: bool = False, displayDevice: str = None, audioIn: str = None, audioOut: str = None, volume: int = 100, resolution: str = "1920x1080", fps: int = 60):
        self.hideTaskbar = hideTaskbar
        self.displayDevice = displayDevice
        self.audioIn = audioIn
        self.audioOut = audioOut
        self.volume = volume
        self.resolution = resolution
        self.fps = fps


