import json, os

SETTINGS_FILE = "settings.json"

class Settings:
    def __init__(self, hideTaskbar: bool = False, displayDevice: str = None, audioIn: str = None, audioOut: str = None, volume: int = 50, resolution: str = "1920x1080", fps: int = 60):
        self.settings = {}
        
        self.settings['hideTaskbar'] = hideTaskbar
        self.settings['displayDevice'] = displayDevice
        self.settings['audioIn'] = audioIn
        self.settings['audioOut'] = audioOut
        self.settings['volume'] = volume
        self.settings['resolution'] = resolution
        self.settings['fps'] = fps

    # Opens the settings file if it exists
    def open(self):

        if os.path.isfile(SETTINGS_FILE):
            settingsFile = open(SETTINGS_FILE, 'r')
            self.settings = json.loads(settingsFile.read())
            settingsFile.close()
        else:
            self.save()

    def save(self):
        settingsJson = json.dumps(self.settings)
        settingsFile = open(SETTINGS_FILE, 'w')
        settingsFile.write(settingsJson)
        settingsFile.close()
        
    def set(self, key, value):
        self.settings[key] = value
        self.save()

    def get(self, key):
        return self.settings[key]
