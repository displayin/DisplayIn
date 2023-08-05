
from config.videostreamconfig import VideoStreamConfig
from config.audiostreamconfig import AudioStreamConfig
from config.settings import Settings
from engine.videostream import VideoStream
from engine.audiostream import AudioStream
from util.resource import Resource as res
import sounddevice as sd
import cv2 as cv
from util.exceptionhandler import ExceptionHandler
from util.logger import Logger
import numpy as np
import sys
import ffmpeg
import time

import os
import gi
gi.require_version("Gtk", "3.0")
from gi.repository import Gtk, GdkPixbuf, GLib

def writeDisplay(uiBuilder, frame, imageDisplay):
    # Write Frame
    frame = cv.cvtColor(frame, cv.COLOR_BGR2RGB)

    if res.useOpenGL():
        # Render frame using OpenGL
        GLib.idle_add(imageDisplay.render, frame)
    else:
        h, w, d = frame.shape
        pixbuf = GdkPixbuf.Pixbuf.new_from_data(
            frame.tostring(), GdkPixbuf.Colorspace.RGB, False, 8, w, h, w*d)

        # Render frame using Software Renderer
        imageDisplay = uiBuilder.get_object("display")
        GLib.idle_add(imageDisplay.set_from_pixbuf, pixbuf)
    pass

class MainWindow:
    def __init__(self, exHandler: ExceptionHandler=None) -> None:
        self.exHandler = exHandler
        self.isFullscreen: bool = False
        self.logger = Logger()
        self.glArea = None
        self.videoDevices = None
        self.recording = False

    def setUiHandler(self, uiHandler):
        try:
            # Initialize Gtk Builder
            self.builder = Gtk.Builder()
            self.builder.add_from_file(res.getFilePath("resource/ui/maingui.glade"))
            self.builder.connect_signals(uiHandler)

            # Get Window
            self.window = self.getGtkObject("main")
            self.selectDisplay = self.getGtkObject("selectDisplay")
            self.selectAudioIn = self.getGtkObject("selectAudioIn")
            self.selectAudioOut = self.getGtkObject("selectAudioOut")

            # Get Settings Objects
            self.selectDisplay1 = self.getGtkObject("selectDisplay1")
            self.selectAudioIn1 = self.getGtkObject("selectAudioIn1")
            self.selectAudioOut1 = self.getGtkObject("selectAudioOut1")
            self.selectResolution = self.getGtkObject("selectResolution")
            self.selectFPS = self.getGtkObject("selectFPS")
            self.selectVolume = self.getGtkObject("selectVolume")
            self.selectVolume1 = self.getGtkObject("selectVolume1")
            self.buttonRecord = self.getGtkObject("buttonRecord")
            self.buttonFullscreen = self.getGtkObject("buttonFullscreen")

            # Get Menubar
            self.menuBar = self.getGtkObject("menuBar")

            # Replace Viewport Display
            viewport = self.getGtkObject("viewport")

            if res.useOpenGL():
                from engine.openglrenderer import OpenGLRenderer
                displayWidget = self.getGtkObject("display")
                viewport.remove(displayWidget)
                self.glArea = OpenGLRenderer()
                viewport.add(self.glArea)
                self.glArea.show()

            # initialize selected devices
            self.selectedDisplay: int = -1
            self.selectedAudioIn: int = -1
            self.selectedAudioOut: int = -1

            self.videoStream: VideoStream = None
            self.audioStream: AudioStream = None

            # initialize audio and vidoe
            self.initialize()

        except Exception as e:
            self.handleException(e)

    def initialize(self, resetSettings = False):
        # initialize settings
        self.settings = Settings()

        # save default settings
        if resetSettings:
            self.settings.save()

        self.settings.open()

        # Display or hide action bar
        self.actionBar = self.getGtkObject("actionBar")
        self.selectHideTaskbar = self.getGtkObject("selectHideTaskbar")
        hideTaskbar = self.settings.get('hideTaskbar')
        self.selectHideTaskbar.set_state(hideTaskbar)
        self.actionBar.set_reveal_child(not hideTaskbar)

        # Initialize Devices Lists
        self.initVideo()
        self.initAudio()

    def handleException(self, e: Exception):
        if self.exHandler:
            self.exHandler.handle(e)

    def initVideoSettings(self):
        self.setComboValue(self.selectResolution, self.settings.get('resolution'), 0)
        self.setComboValue(self.selectFPS, self.settings.get('fps'), 1)
        pass

    def setComboValue(self, combo, value, index):
        model = combo.get_model()

        i = 0
        for selection in model:
            if selection[index] == value:
                combo.set_active(-1)
                combo.set_active(i)
                break
            i += 1
        pass

    def initVideo(self):
        try:
            self.logger.log("Initializing Video...")

            # Init Video Settings
            self.initVideoSettings()

            # Select Video API
            videoApi = cv.CAP_ANY

            if res.isLinux():
                videoApi = cv.CAP_V4L2
            elif res.isWindows():
                videoApi = cv.CAP_GSTREAMER

            # Find all available video device ids
            videoDevices: list[VideoStreamConfig] = []

            if self.videoDevices == None:
                self.videoDevices = videoDevices

            deviceListStore = Gtk.ListStore(int, str)
            currentDeviceId = -1

            for i in range(50):
                deviceId = i
                if res.isWindows():
                    # deviceId = 'mfvideosrc device-index=' + str(i) + ' ! mfh264enc max-qp=20 low-latency=true ! openh264dec ! videoconvert ! appsink'
                    deviceId = 'mfvideosrc device-index=' + str(i) + ' ! videoconvert ! videoscale ! appsink'

                cap = cv.VideoCapture(deviceId, videoApi)
                if cap.read()[0]:
                    cap.release()
                    config = VideoStreamConfig(
                        deviceId=deviceId,
                        # TODO Localize String
                        name=str("Display " + str(i)),
                        uiBuilder=self.builder,
                        writeCallback=writeDisplay,
                        api=videoApi,
                        displayWidget=self.glArea
                    )
                    videoDevices.append(config)
                    self.logger.log(config.name)

                    # Populate Drop Down
                    device: VideoStreamConfig = config
                    deviceListStore.append([i, device.name])
                    currentDeviceId = i
                    self.logger.log(str("Current Selected Device: " + str(currentDeviceId)))
                else:
                    break

            if len(videoDevices) > 0:
                self.videoDevices = videoDevices

            # load from settings
            self.defaultDisplayDevice = currentDeviceId
            itemCount = len(deviceListStore)
            settingDisplayDevice = self.settings.get('displayDevice')
            if settingDisplayDevice != None and settingDisplayDevice < itemCount:
                currentDeviceId = settingDisplayDevice

            if self.videoDevices:
                self.initSelectDisplay(self.selectDisplay, deviceListStore, currentDeviceId)
                self.initSelectDisplay(self.selectDisplay1, deviceListStore, currentDeviceId)

            self.logger.log("Video Initialized!")
        except Exception as e:
            self.handleException(e)

    def initSelectDisplay(self, selectDisplay, deviceListStore, currentDeviceId):
        selectDisplay.set_model(deviceListStore)
        selectDisplay.set_id_column(0)
        selectDisplay.set_entry_text_column(1)
        selectDisplay.set_active(-1)
        selectDisplay.set_active(currentDeviceId)
    
    def setDisplay(self, deviceId):
        
        self.setActive(self.selectDisplay, deviceId)
        self.setActive(self.selectDisplay1, deviceId)

        if self.selectedDisplay != deviceId:
            self.selectedDisplay = deviceId
            self.startVideo()
            self.logger.log("Video Started!")

    def setActive(self, selection, id):
        active = selection.get_active()

        if (id != active):
            selection.set_active(id)

    def initAudio(self):
        try:
            self.logger.log("Initializing Audio...")

            # Get list of host audio apis
            self.selectAudioHostApi()

            # Get list of all sound devices
            self.getAudioDevices()

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
                    # Prioritize USB devices in input
                    if "usb" in device["name"].lower() and "voip" not in device["name"].lower():
                        currentInputDeviceId = i
                    i += 1

                if device["max_output_channels"] > 0:
                    outputDeviceListStore.append([j, device["index"], device["name"]])
                    # select first available output device
                    if currentOutputDeviceId == -1:
                        currentOutputDeviceId = j
                    # If there is a default device, then set it
                    if "default" in device["name"].lower():
                        currentOutputDeviceId = j
                    j += 1

            # Load Audio Devices from Settings
            self.defaultAudioIn = currentInputDeviceId
            itemCount = len(inputDeviceListStore)
            settingAudioIn = self.settings.get('audioIn')
            if settingAudioIn != None and settingAudioIn < itemCount:
                currentInputDeviceId = settingAudioIn

            self.defaultAudioOut = currentOutputDeviceId
            itemCount = len(outputDeviceListStore)
            settingAudioOut = self.settings.get('audioOut')
            if settingAudioOut != None and settingAudioOut < itemCount:
                currentOutputDeviceId = settingAudioOut

            if len(inputDeviceListStore) > 0:
                self.initSelectAudio(self.selectAudioIn, inputDeviceListStore, currentInputDeviceId)
                self.initSelectAudio(self.selectAudioIn1, inputDeviceListStore, currentInputDeviceId)

                
            if len(outputDeviceListStore) > 0:
                self.initSelectAudio(self.selectAudioOut, outputDeviceListStore, currentOutputDeviceId)
                self.initSelectAudio(self.selectAudioOut1, outputDeviceListStore, currentOutputDeviceId)

            # Load Volume from settings
            self.selectVolume.set_value(self.settings.get('volume'))
            self.selectVolume1.set_value(self.settings.get('volume'))

            self.logger.log("Audio Initialized!")
        except Exception as e:
            self.handleException(e)
    
    def initSelectAudio(self, selectAudio, deviceListStore, currentDeviceId):
        selectAudio.set_model(deviceListStore)
        selectAudio.set_id_column(0)
        selectAudio.set_entry_text_column(2)
        selectAudio.set_active(-1)
        selectAudio.set_active(currentDeviceId)

    def setAudioIn(self, deviceId, selected):
        self.setActive(self.selectAudioIn, selected)
        self.setActive(self.selectAudioIn1, selected)

        if self.selectAudioIn != deviceId:
            self.selectedAudioIn = deviceId
            self.startAudio()
            self.logger.log("Audio Started!")


    def setAudioOut(self, deviceId, selected):
        self.setActive(self.selectAudioOut, selected)
        self.setActive(self.selectAudioOut1, selected)

        if self.selectedAudioOut != deviceId:
            self.selectedAudioOut = deviceId
            self.startAudio()
            self.logger.log("Audio Started!")

    def selectAudioHostApi(self):
        # Get list of host audio apis
        self.hostApiIndex = 0
        self.audioHostApis = sd.query_hostapis()
        i = 0
        for api in self.audioHostApis:
            # TODO Make Configurable for all OSes
            if res.isWindows() and api["name"] == "MME":
                self.hostApiIndex = i
                break
            i+=1
        pass

    def getAudioDevices(self):
        self.audioDevices = sd.query_devices()
        if res.isWindows():
            self.audioDevices = list(filter(lambda audioDevice: audioDevice["hostapi"] == self.hostApiIndex, self.audioDevices))

        pass

    def startVideo(self):
        try:
            if self.selectedDisplay != -1 and len(self.videoDevices) > 0:
                videoConfig = self.videoDevices[self.selectedDisplay]
                if self.videoStream:
                    self.videoStream.stop()

                # Set Resolution
                resolution = self.settings.get('resolution').split('x')
                videoConfig.width = int(resolution[0].strip())
                videoConfig.height = int(resolution[1].strip())

                # Set FPS
                videoConfig.fps = self.settings.get('fps')

                self.videoStream = VideoStream(videoConfig, self.exHandler)
                self.videoStream.start()
        except Exception as e:
            self.handleException(e)

    def startAudio(self):
        try:
            if self.selectedAudioIn != -1 and self.selectedAudioOut != -1:
                audioIn = next(filter(lambda device: device["index"] == self.selectedAudioIn, self.audioDevices))
                audioOut = next(filter(lambda device: device["index"] == self.selectedAudioOut, self.audioDevices))
                
                if self.audioStream:
                    self.audioStream.stop()

                audioConfig = AudioStreamConfig(
                    inputDeviceId=audioIn["index"],
                    outputDeviceId=audioOut["index"],
                    inputSampleRate=audioIn["default_samplerate"], 
                    outputSampleRate=audioOut["default_samplerate"], 
                    inputChannels=audioIn["max_input_channels"],
                    outputChannels=audioIn["max_input_channels"], 
                    inputLatency=audioIn["default_low_input_latency"], 
                    outputLatency=audioOut["default_low_input_latency"],
                    dtype=np.int32,
                    blockSize=8192)
                self.audioStream = AudioStream(audioConfig, self.exHandler)
                self.audioStream.start()
        except Exception as e:
            self.handleException(e)

    def stopVideo(self):
        if self.videoStream:
            self.videoStream.stop()

    def stopAudio(self):
        if self.audioStream:
            self.audioStream.stop()

    def startRecording(self):
        icon = Gtk.Image.new_from_icon_name("gtk-media-stop", size=Gtk.IconSize.BUTTON)
        self.buttonRecord.set_image(icon)
        self.videoStream.startRecording()
        self.audioStream.startRecording()
        pass

    def stopRecording(self):
        icon = Gtk.Image.new_from_icon_name("gtk-media-record", size=Gtk.IconSize.BUTTON)
        self.buttonRecord.set_image(icon)
        self.videoStream.stopRecording()
        self.audioStream.stopRecording()
        videoFile = ffmpeg.input("temp.avi")
        audioFile = ffmpeg.input("temp.wav")
        ffmpeg.output(videoFile, audioFile, "out.mp4").run(overwrite_output=True)
        res.deleteFileIfExists("temp.avi")
        res.deleteFileIfExists("temp.wav")
        pass

    def show(self):
        try:
            # Display Window
            self.window.show()
            Gtk.main()
        except Exception as e:
            self.handleException(e)

    def fullscreen(self):
        if self.isFullscreen:
            icon = Gtk.Image.new_from_icon_name("gtk-fullscreen", size=Gtk.IconSize.BUTTON)
            self.buttonFullscreen.set_image(icon)
            self.window.unfullscreen()
            self.menuBar.show()
        else:
            icon = Gtk.Image.new_from_icon_name("gtk-leave-fullscreen", size=Gtk.IconSize.BUTTON)
            self.buttonFullscreen.set_image(icon)
            self.window.fullscreen()
            self.menuBar.hide()

    def getGtkObject(self, objectId: str):
        return self.builder.get_object(objectId)
    
    def exit(self):
        try:
            self.stopVideo()
            self.stopAudio()

            self.window.close()
            sys.exit(0)
        except Exception as e:
            self.handleException(e)
