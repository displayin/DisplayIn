import sys, os, platform

IS_WINDOWS = platform.system() == "Windows"
IS_LINUX = platform.system() == "Linux"
IS_MAC = platform.system() == "Darwin"
USE_OPENGL = IS_WINDOWS

class Resource:
    @staticmethod
    def getFilePath(fileName: str) -> str:

        path = fileName
        if getattr(sys, 'frozen', False) and hasattr(sys, '_MEIPASS'):
            path = os.path.join(sys._MEIPASS, fileName)

        return path

    @staticmethod
    def isWindows() -> bool:
        return IS_WINDOWS

    @staticmethod
    def isLinux() -> bool:
        return IS_LINUX

    @staticmethod
    def isMac() -> bool:
        return IS_MAC
    
    @staticmethod
    def useOpenGL() -> bool:
        return USE_OPENGL