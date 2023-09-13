import json, os

SETTINGS_FILE = "settings.json"

class Settings:
    def __init__(self, hideTaskbar: bool = False, displayDevice: str = None, audioIn: str = None, audioOut: str = None, volume: int = 50, resolution: str = "1920x1080", fps: int = 60, screenshotDir: str = 'screenshots', videoDir: str = 'recordings', logDir: str = 'logs'):
        
        self.logger = None
        self.settings = {}
        
        self.settings['hideTaskbar'] = hideTaskbar
        self.settings['displayDevice'] = displayDevice
        self.settings['audioIn'] = audioIn
        self.settings['audioOut'] = audioOut
        self.settings['volume'] = volume
        self.settings['resolution'] = resolution
        self.settings['fps'] = fps
        self.settings['screenshotDir'] = screenshotDir
        self.settings['videoDir'] = videoDir
        self.settings['logDir'] = logDir

    # Opens the settings file if it exists
    def open(self):

        if os.path.isfile(SETTINGS_FILE):
            settingsFile = open(SETTINGS_FILE, 'r')
            self.settings = json.loads(settingsFile.read())
            settingsFile.close()
            self.log("Settings file found")
        else:
            self.log("Settings file created from default")
            self.save()

    def save(self):
        settingsJson = json.dumps(self.settings)
        settingsFile = open(SETTINGS_FILE, 'w')
        settingsFile.write(settingsJson)
        settingsFile.close()
        
    def set(self, key, value):
        self.log('Setting "' + key + '" changed from "' + str(self.settings.get(key)) + '" to "' + str(value) + '"')
        self.settings[key] = value
        self.save()

    def get(self, key):
        value = self.settings.get(key)
        self.log('Setting "' + key + '" retrieved "' + str(value) + '"')
        return value
    
    def getOrDefault(self, key, default):
        value = self.get(key)
        if value == None:
            value = default
        return value
    
    def log(self, message):
        if not self.logger is None:
            self.logger.log(message)

    def logDump(self):
        settingsLog = ""
        for key in self.settings:
            settingsLog = settingsLog + key + ' -> ' + str(self.settings[key]) + '\n'
        self.log('Settings file Dump\n=Settings File=\n' + settingsLog + '=End Settings File=')
