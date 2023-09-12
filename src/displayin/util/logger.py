from datetime import datetime
from util.resource import Resource as res
import os

class Logger:
    def __init__(self, logDir: str = "logs", logFile: str = None):
        self.logDir = logDir
        self.logFile = logFile

        if self.logFile == None:
            self.logFile = res.getLogFileName()
        
    
    def log(self, message: str) -> None:
        print(message)
        with open(os.path.join(self.logDir, self.logFile), 'w') as file:
            file.write(str(datetime.utcnow()) + ' - ' + message)
