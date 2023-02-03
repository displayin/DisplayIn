import sys, os, platform

class Resource:
    @staticmethod
    def getFilePath(fileName: str) -> str:

        path = fileName
        if getattr(sys, 'frozen', False) and hasattr(sys, '_MEIPASS'):
            path = os.path.join(sys._MEIPASS, fileName)

        return path

    @staticmethod
    def isWindows() -> bool:
        return platform.system() == "Windows"

    @staticmethod
    def isLinux() -> bool:
        return platform.system() == "Linux"

    @staticmethod
    def isMac() -> bool:
        return platform.system() == "Darwin"