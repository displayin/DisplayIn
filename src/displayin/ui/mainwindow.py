
from config.videostreamconfig import VideoStreamConfig
from config.audiostreamconfig import AudioStreamConfig
from engine.videostream import VideoStream
from engine.audiostream import AudioStream
import sounddevice as sd
import cv2 as cv

import os
import gi
gi.require_version("Gtk", "3.0")
from gi.repository import Gtk, GdkPixbuf

def writeDisplay(uiBuilder, fileName, frame):
    # Write Frame
    frame = cv.cvtColor(frame, cv.COLOR_BGR2RGB)
    h, w, d = frame.shape
    pixbuf = GdkPixbuf.Pixbuf.new_from_data(
        frame.tostring(), GdkPixbuf.Colorspace.RGB, False, 8, w, h, w*d)

    # Display File
    imageDisplay = uiBuilder.get_object("display")
    imageDisplay.set_from_pixbuf(pixbuf.copy())
    pass

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

        # initialize selected devices
        self.selectedDisplay = -1
        self.selectedAudioIn = -1
        self.selectedAudioOut = -1

        self.videoStream: VideoStream = None
        self.audioStream: AudioStream = None

        # Initialize Devices Lists
        self.initVideo()
        self.initAudio()

        # Start Video and Audio
        self.startVideo()
        self.startAudio()

    def initVideo(self):
        # Find all available video device ids
        self.videoDevices: list[VideoStreamConfig] = []
        for i in range(50):
            cap = cv.VideoCapture(i)
            if cap.read()[0]:
                config = VideoStreamConfig(
                    deviceId=i,
                    name=str("Display " + str(i)),
                    width=1280, # cap.get(cv.CAP_PROP_FRAME_WIDTH),
                    height=720, # cap.get(cv.CAP_PROP_FRAME_HEIGHT),
                    # fps=cap.get(cv.CAP_PROP_FPS),
                    uiBuilder=self.builder,
                    writeCallback=writeDisplay
                )
                self.videoDevices.append(config)
                cap.release()
            else:
                break

        # Populate Drop Down
        deviceListStore = Gtk.ListStore(int, str)
        currentDeviceId = -1
        device: VideoStreamConfig
        for device in self.videoDevices:
            deviceListStore.append([device.deviceId, device.name])
            currentDeviceId = device.deviceId

        if self.videoDevices:
            self.selectDisplay.set_model(deviceListStore)
            self.selectDisplay.set_id_column(0)
            self.selectDisplay.set_entry_text_column(1)
            self.selectDisplay.set_active(currentDeviceId)
            self.selectedDisplay = currentDeviceId
        pass

    def initAudio(self):
        # Get list of all sound devices
        self.audioDevices = sd.query_devices()

        inputDeviceListStore = Gtk.ListStore(int, int, str)
        outputDeviceListStore = Gtk.ListStore(int, int, str)

        i = 0
        j = 0
        currentInputDeviceId = -1
        currentOutputDeviceId = -1
        for device in self.audioDevices:
            if device["max_input_channels"] > 0:
                inputDeviceListStore.append([i, device["index"], device["name"]])
                # select first available input device
                if currentInputDeviceId == -1:
                    currentInputDeviceId = i
                    self.selectedAudioIn = device["index"]
                # Prioritize USB devices in input
                if "usb" in device["name"].lower():
                    currentInputDeviceId = i
                    self.selectedAudioIn = device["index"]
                i += 1

            if device["max_output_channels"] > 0:
                outputDeviceListStore.append([j, device["index"], device["name"]])
                # select first available output device
                if currentOutputDeviceId == -1:
                    currentOutputDeviceId = j
                    self.selectedAudioOut = device["index"]
                # If there is a default device, then set it
                if "default" in device["name"].lower():
                    currentOutputDeviceId = j
                    self.selectedAudioOut = device["index"]
                j += 1

        if len(inputDeviceListStore) > 0:
            self.selectAudioIn.set_model(inputDeviceListStore)
            self.selectAudioIn.set_id_column(0)
            self.selectAudioIn.set_entry_text_column(2)
            self.selectAudioIn.set_active(currentInputDeviceId)
            

        if len(outputDeviceListStore) > 0:
            self.selectAudioOut.set_model(outputDeviceListStore)
            self.selectAudioOut.set_id_column(0)
            self.selectAudioOut.set_entry_text_column(2)
            self.selectAudioOut.set_active(currentOutputDeviceId)

        pass

    def startVideo(self):
        if self.selectedDisplay != -1:
            videoConfig = self.videoDevices[self.selectedDisplay]
            if self.videoStream:
                self.videoStream.stop()

            self.videoStream = VideoStream(videoConfig)
            self.videoStream.start()
        pass

    def startAudio(self):
        if self.selectedAudioIn != -1 and self.selectedAudioOut != -1:
            audioIn = self.audioDevices[self.selectedAudioIn]
            audioOut = self.audioDevices[self.selectedAudioOut]
            
            if self.audioStream:
                self.audioStream.stop()

            audioConfig = AudioStreamConfig(audioIn["index"], audioOut["index"])
            self.audioStream = AudioStream(audioConfig)
            self.audioStream.start()
        pass

    def show(self):
        # Display Window
        self.window.show_all()
        Gtk.main()

    def exit(self):
        self.window.close()
        exit(0)