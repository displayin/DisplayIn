#
# Copyright (c) 2023 Tekst LLC.
#
# This file is part of DisplayIn 
# (see https://github.com/displayin).
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program. If not, see <http://www.gnu.org/licenses/>.#
from datetime import datetime
from util.resource import Resource as res
import os

class Logger:
    def __init__(self, logDir: str = "logs", logFile: str = None):
        self.logDir = logDir
        self.logFile = logFile

        if self.logFile == None:
            self.logFile = res.getLogFileName()

        if not os.path.exists(self.logDir):
            res.makeDir(self.logDir)
        
    
    def log(self, message: str) -> None:
        print(message)
        with open(os.path.join(self.logDir, self.logFile), 'a') as file:
            file.write(str(datetime.utcnow()) + ' - ' + message + '\n')
