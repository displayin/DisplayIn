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
import sys
import os
import platform
import socket
import re
import uuid
import psutil
import importlib
import os
import time
from threading import Timer
import gi
gi.require_version("Gtk", "3.0")
from gi.repository import Gtk, GdkPixbuf, GLib

IS_WINDOWS = platform.system() == "Windows"
IS_LINUX = platform.system() == "Linux"
IS_MAC = platform.system() == "Darwin"
USE_OPENGL = IS_WINDOWS or IS_LINUX
LOG_FILENAME = str("log_" + str(int(time.time())) + ".txt")

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
    def saveFileDialog(defaultFileName = "recording.mp4", currentFolder = ".", message: str = "Save video file as", fileFilterName="MP4 Video", fileFilter="*.mp4"):
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
        dialog.set_current_name(defaultFileName)
        dialog.set_current_folder(currentFolder)

        # Ask for Overwrite Confirmation
        dialog.set_do_overwrite_confirmation(True)

        response = dialog.run()
        if response == Gtk.ResponseType.OK:
            filePath = dialog.get_filename()

        dialog.destroy()

        return filePath
    
    @staticmethod
    def getIconButton(name: str):
        return Gtk.Image.new_from_icon_name(name, size=Gtk.IconSize.BUTTON)
    
    @staticmethod
    def getFileTimestamp():
        return int(time.time())

    @staticmethod
    def getScreenshotFileName():
        return str("screenshot_" + str(Resource.getFileTimestamp()) + ".png")
    
    @staticmethod
    def getRecordingFileName():
        return str("recording_" + str(Resource.getFileTimestamp()) + ".mp4")
    
    @staticmethod
    def getLogFileName():
        return LOG_FILENAME
    
    @staticmethod
    def delayCall(delayInSeconds: float, function):
        timer = Timer(delayInSeconds, function)
        timer.start()
        return timer
    
    @staticmethod
    def makeDir(directory: str):
        os.makedirs(directory, exist_ok=True)
            

    @staticmethod
    def getSystemInfo():
        info = {}
        info['platform'] = platform.system()
        info['platform-release'] = platform.release()
        info['platform-version'] = platform.version()
        info['architecture'] = platform.machine()
        info['hostname'] = socket.gethostname()
        info['ip-address'] = socket.gethostbyname(socket.gethostname())
        info['mac-address'] = ':'.join(re.findall('..',
                                        '%012x' % uuid.getnode()))
        info['processor'] = platform.processor()
        info['ram'] = str(
            round(psutil.virtual_memory().total / (1024.0 ** 3)))+"GB"
        return info
