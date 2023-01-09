
from config.videostreamconfig import VideoStreamConfig
from config.audiostreamconfig import AudioStreamConfig
from engine.videostream import VideoStream
from engine.audiostream import AudioStream
import sounddevice as sd
import cv2 as cv

import os
import gi
gi.require_version("Gtk", "3.0")
from gi.repository import Gtk

class UIHandler:
    def __init__(self, window) -> None:
        self.window = window

    def onSelectDisplay(self, obj):
        pass

    def onSelectAudioIn(self, obj):
        pass

    def onSelectAudioOut(self, obj):
        pass

    def onExit(self, obj):
        self.window.exit()
        pass

class MainWindow:
    def __init__(self) -> None:
        # Set Paths
        self.dirPath = os.path.dirname(os.path.realpath(__file__))
        self.gladePath = os.path.join(self.dirPath, "maingui.glade")

        # Initialize Gtk Builder
        self.builder = Gtk.Builder()
        self.builder.add_from_file(self.gladePath)
        self.builder.connect_signals(UIHandler(self))

        # Get Window
        self.window = self.builder.get_object("main")
        self.selectDisplay = self.builder.get_object("selectDisplay")
        self.selectAudioIn = self.builder.get_object("selectAudioIn")
        self.selectAudioOut = self.builder.get_object("selectAudioOut")

        # Initialize Devices Lists
        self.initVideo()
        self.initAudio()

    def initVideo(self):
        # Find all available video device ids
        self.videoDevices = []
        for i in range(50):
            cap = cv.VideoCapture(i)
            if cap.read()[0]:
                self.videoDevices.append(i)
                cap.release()
            else:
                break

        # Populate Drop Down
        for device in self.videoDevices:
            self.selectDisplay.append_text("Display " + device)
        pass

    def initAudio(self):
        # Get list of all sound devices
        self.audioDevices = sd.query_devices()
        pass

    def show(self):
        # Display Window
        self.window.show_all()
        Gtk.main()

    def exit(self):
        self.window.close()
        exit(0)