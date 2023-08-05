import sys, os, platform
import importlib
import os
import gi
gi.require_version("Gtk", "3.0")
from gi.repository import Gtk, GdkPixbuf, GLib

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
    
    @staticmethod
    def deleteFileIfExists(file):
        if os.path.exists(file):
            os.remove(file)

    @staticmethod
    def saveFileDialog(message: str="Save video file as", fileFilterName="MP4 Video", fileFilter="*.mp4"):
        filePath = None
        dialog = Gtk.FileChooserDialog(message, None,
                                       Gtk.FileChooserAction.SAVE,
                                       (Gtk.STOCK_CANCEL, Gtk.ResponseType.CANCEL,
                                        Gtk.STOCK_SAVE, Gtk.ResponseType.OK))
        # Set File Filter
        filter = Gtk.FileFilter()
        filter.set_name(fileFilterName)
        filter.add_pattern(fileFilter)
        dialog.add_filter(filter)

        # Ask for Overwrite Confirmation
        dialog.set_do_overwrite_confirmation(True)

        response = dialog.run()
        if response == Gtk.ResponseType.OK:
            filePath = dialog.get_filename()

        dialog.destroy()

        return filePath
