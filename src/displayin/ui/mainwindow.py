
from config.videostreamconfig import VideoStreamConfig
from config.audiostreamconfig import AudioStreamConfig
from engine.videostream import VideoStream
from engine.audiostream import AudioStream
from util.resource import Resource as res
import sounddevice as sd
import cv2 as cv
from util.exceptionhandler import ExceptionHandler
from util.logger import Logger
import numpy as np
import sys

from engine.openglrenderer import OpenGLRenderer

import os
import gi
gi.require_version("Gtk", "3.0")
from gi.repository import Gtk, GdkPixbuf, GLib

USE_OPENGL = res.isWindows()

def writeDisplay(uiBuilder, frame, imageDisplay):
    # Write Frame
    frame = cv.cvtColor(frame, cv.COLOR_BGR2RGB)

    if USE_OPENGL:
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

            # Replace Viewport Display
            viewport = self.getGtkObject("viewport")

            if USE_OPENGL:
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

            # Initialize Devices Lists
            self.initVideo()
            self.initAudio()
        except Exception as e:
            self.handleException(e)

    def handleException(self, e: Exception):
        if self.exHandler:
            self.exHandler.handle(e)

    def initVideo(self):
        try:
            self.logger.log("Initializing Video...")

            # Select Video API
            videoApi = cv.CAP_ANY

            if res.isLinux():
                videoApi = cv.CAP_V4L2
            elif res.isWindows():
                videoApi = cv.CAP_GSTREAMER

            # Find all available video device ids
            self.videoDevices: list[VideoStreamConfig] = []

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
                    self.videoDevices.append(config)
                    self.logger.log(config.name)

                    # Populate Drop Down
                    device: VideoStreamConfig = config
                    deviceListStore.append([i, device.name])
                    currentDeviceId = i
                    self.logger.log(str("Current Selected Device: " + str(currentDeviceId)))
                else:
                    break

            if self.videoDevices:
                self.selectDisplay.set_model(deviceListStore)
                self.selectDisplay.set_id_column(0)
                self.selectDisplay.set_entry_text_column(1)
                self.selectDisplay.set_active(currentDeviceId)
            self.logger.log("Video Initialized!")
        except Exception as e:
            self.handleException(e)

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
            self.logger.log("Audio Initialized!")
        except Exception as e:
            self.handleException(e)

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
            if self.selectedDisplay != -1:
                videoConfig = self.videoDevices[self.selectedDisplay]
                if self.videoStream:
                    self.videoStream.stop()

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

    def show(self):
        try:
            # Display Window
            self.window.show()
            Gtk.main()
        except Exception as e:
            self.handleException(e)

    def fullscreen(self):
        if self.isFullscreen:
            self.window.unfullscreen()
        else:
            self.window.fullscreen()

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
