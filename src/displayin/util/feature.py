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
import hashlib
import os
from util.resource import Resource as res

class Feature:

    def getFileHash(self, filename: str):
        md5Hash = hashlib.md5()

        calculatedHash = None
        
        if os.path.exists(filename):
            with open(filename, "rb") as f:
                # Read and update hash in chunks of 4K
                for byteBlock in iter(lambda: f.read(4096), b""):
                    md5Hash.update(byteBlock)
                calculatedHash = md5Hash.hexdigest()

        if calculatedHash is None:
            raise Exception("Could not calculate MD5 hash of " + filename)
        
        return calculatedHash

    def integrityCheck(self, filename: str, md5Hash: str):
        fileMd5Hash = self.getFileHash(filename)
        if fileMd5Hash != md5Hash:
            raise Exception("File integrity compromised! Program will not work as expected!\n" + filename)
        
    def featureEnabled(self, featureName: str, md5Hash: str):
        enabled = False
        featureFilePath = os.path.join('features', featureName, 'data')
        if os.path.exists(featureFilePath):
            fileMd5Hash = self.getFileHash(featureFilePath)
            enabled = fileMd5Hash == md5Hash

        return enabled
    
    def initializeFeatures(self):
        res.makeDir('features')
