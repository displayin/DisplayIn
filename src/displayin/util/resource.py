import sys, os, platform
import importlib
import os

IS_WINDOWS = platform.system() == "Windows"
IS_LINUX = platform.system() == "Linux"
IS_MAC = platform.system() == "Darwin"
USE_OPENGL = IS_WINDOWS or IS_LINUX

# Needed for Wayland Support for OpenGL in Linux
#if IS_LINUX and 'WAYLAND_DISPLAY' in os.environ and 'PYOPENGL_PLATFORM' not in os.environ:
#    os.environ['PYOPENGL_PLATFORM'] = 'x11'

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
    
    @staticmethod
    def closeSpash():
        if '_PYIBoot_SPLASH' in os.environ and importlib.util.find_spec("pyi_splash"):
            import pyi_splash
            pyi_splash.update_text('UI Loaded ...')
            pyi_splash.close()

    @staticmethod
    def macAuthorizeCamera():
        if Resource.isMac():
            # WIP Does not work yet
            from AVFoundation import AVCaptureDevice
            video = AVCaptureDevice
