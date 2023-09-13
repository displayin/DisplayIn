import hashlib
import os
from util.resource import Resource as res

class Feature:

    def getFileHash(self, filename: str):
        md5Hash = hashlib.md5()

        calculatedHash = None
        with open(filename, "rb") as f:
            # Read and update hash in chunks of 4K
            for byteBlock in iter(lambda: f.read(4096), b""):
                md5Hash.update(byteBlock)
            calculatedHash = md5Hash.hexdigest()

        if calculatedHash is None:
            raise Exception("Could not calculated MD5 hash of " + filename)
        
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
