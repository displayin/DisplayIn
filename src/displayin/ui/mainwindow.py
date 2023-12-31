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
from util.feature import Feature
import numpy as np
import sys
from util.videoexporter import VideoExporter

import glob
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
        if self.exHandler:
            self.exHandler.logger = self.logger

    def setUiHandler(self, uiHandler):
        try:
            # Initialize Gtk Builder
            self.logger.log("[Program Started]")
            self.printSystemInfo()
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
            self.buttonReset = self.getGtkObject("buttonReset")
            self.buttonScreenshot = self.getGtkObject("buttonScreenshot")

            self.controls = [
                self.selectDisplay,
                self.selectAudioIn,
                self.selectAudioOut,
                self.selectDisplay1,
                self.selectAudioIn1,
                self.selectAudioOut1,
                self.selectResolution,
                self.selectFPS,
                self.buttonReset
            ]

            self.feature = Feature()
            self.feature.initializeFeatures()
            self.videExporter = VideoExporter(self)

            # Init Screenshot popover
            self.initScreenshotPopover()

            # Get Menubar
            self.menuBar = self.getGtkObject("menuBar")

            # Replace Viewport Display
            viewport = self.getGtkObject("viewport")

            if res.useOpenGL():
                from engine.openglrenderer import OpenGLRenderer
                displayWidget = self.getGtkObject("display")
                viewport.remove(displayWidget)
                self.glArea = OpenGLRenderer()
                self.glArea.logger = self.logger
                viewport.add(self.glArea)
                self.glArea.show()

            # initialize selected devices
            self.selectedDisplay: int = -1
            self.selectedAudioIn: int = -1
            self.selectedAudioOut: int = -1

            self.videoStream: VideoStream = None
            self.audioStream: AudioStream = None

            # initialize audio and video
            self.initialize()

        except Exception as e:
            self.handleException(e)

    def initialize(self, resetSettings = False):
        # initialize settings
        self.logger.log("initialize() started")
        self.settings = Settings()
        self.settings.logger = self.logger

        # save default settings
        if resetSettings:
            self.logger.log("Settings Reset")
            self.settings.save()

        self.settings.open()
        self.settings.logDump()

        # Display or hide action bar
        self.actionBar = self.getGtkObject("actionBar")
        self.selectHideTaskbar = self.getGtkObject("selectHideTaskbar")
        hideTaskbar = self.settings.get('hideTaskbar')
        self.selectHideTaskbar.set_state(hideTaskbar)
        self.actionBar.set_reveal_child(not hideTaskbar)

        # Initialize screenshots directory
        self.screenshotDir = self.settings.getOrDefault('screenshotDir', 'screenshots')
        res.makeDir(self.screenshotDir)

        # Initialize recordings directory
        self.videoDir = self.settings.getOrDefault('videoDir', 'recordings')
        res.makeDir(self.videoDir)

        # Initialize logs directory
        self.logDir = self.settings.getOrDefault('logDir', 'logs')
        res.makeDir(self.logDir)
        self.cleanLogFiles()

        # Set watermark
        self.overlayFileName = os.path.join('resource', 'images', "DisplayInLogoWatermark.png")
        self.integrityChecks()

        # Initialize Devices Lists
        self.initVideo()
        self.initAudio()
        self.logger.log("initialize() completed")

    def handleException(self, e: Exception):
        if self.exHandler:
            self.exHandler.handle(e)

    def logException(self, e: Exception):
        if self.exHandler:
            self.exHandler.logException(e)

    def integrityChecks(self):
        self.feature.integrityCheck(self.overlayFileName, '28230820f8d97b36a4375ddbed084fdb')
        self.removeWatermark = self.feature.featureEnabled('RemoveWatermark', '39f57763f883f33f1514ee186c97bf25')
        self.logger.log('Feature "RemoveWatermark" enabled is ' + str(self.removeWatermark))
        pass

    def cleanLogFiles(self):
        # Remove all but the last 10 log files
        searchDir = os.path.join(self.logDir, "*")
        files = list(filter(os.path.isfile, glob.glob(searchDir)))
        files.sort(key=lambda x: os.path.getmtime(x))
        if len(files) > 10:
            indexOfLatestFiles = len(files) - 10
            filesToDelete = files[:indexOfLatestFiles]
            for file in filesToDelete:
                res.deleteFileIfExists(file)
                self.logger.log("Deleted logfile " + file)
        pass

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
                if not self.removeWatermark:
                    self.videoStream.setWatermark(self.overlayFileName)
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
        self.setControlsEnabled(False)
        self.buttonRecord.set_image(res.getIconButton("media-playback-stop"))
        self.buttonRecord.set_tooltip_text("Stop recording")
        self.videoStream.startRecording()
        self.audioStream.startRecording()
        self.logger.log("Started Recording")
        pass

    def stopRecording(self):
        self.setControlsEnabled(True)
        self.buttonRecord.set_image(res.getIconButton("media-record"))
        self.buttonRecord.set_tooltip_text("Record")
        recordedFps = self.videoStream.stopRecording()
        self.audioStream.stopRecording()
        self.logger.log("Stopped Recording")
        self.videExporter.exportVideo(recordedFps)
        pass

    def screenshot(self):
        screenshotPath = os.path.join(self.screenshotDir, res.getScreenshotFileName())
        self.videoStream.screenshot(screenshotPath)

        # Show Screenshot Popover
        saveMessage = str("Saved screenshot to " + screenshotPath)
        self.screenshotLabel.set_text(saveMessage)
        self.logger.log(saveMessage)
        res.delayCall(0.5, self.openScreenshotPopup)
        if self.screenshotPopupTimer != None and self.screenshotPopupTimer.is_alive():
            self.screenshotPopupTimer.cancel()
        self.screenshotPopupTimer = res.delayCall(1, self.closeScreenshotPopup)

    def initScreenshotPopover(self):
        self.screenshotPopover = Gtk.Popover()
        self.screenshotLabel = Gtk.Label(label="")
        vbox = Gtk.Box(orientation=Gtk.Orientation.VERTICAL)
        vbox.pack_start(self.screenshotLabel, False, True, 10)
        vbox.show_all()
        self.screenshotPopover.add(vbox)
        self.screenshotPopover.set_position(Gtk.PositionType.TOP)
        self.buttonScreenshot.set_popover(self.screenshotPopover)
        self.screenshotPopupTimer = None

    def openScreenshotPopup(self):
        self.buttonScreenshot.set_active(True)

    def closeScreenshotPopup(self):
        self.buttonScreenshot.set_active(False)

    def setControlsEnabled(self, enabled):
        for widget in self.controls:
            widget.set_sensitive(enabled)

    def show(self):
        try:
            # Display Window
            self.window.show()
            Gtk.main()
        except Exception as e:
            self.handleException(e)

    def fullscreen(self):
        if self.isFullscreen:
            self.buttonFullscreen.set_image(res.getIconButton("view-fullscreen"))
            self.window.unfullscreen()
            self.menuBar.show()
        else:
            self.buttonFullscreen.set_image(res.getIconButton("view-restore"))
            self.window.fullscreen()
            self.menuBar.hide()

    def printSystemInfo(self):
        try:
            systemInfo = ""
            info = res.getSystemInfo()
            for key in info:
                systemInfo = systemInfo + key + \
                    ' -> ' + str(info[key]) + '\n'
            self.logger.log('System Info Dump\n=System Info=\n' +
                    systemInfo + '=End End System Info=')
        except Exception as e:
            self.logException(e)

    def getGtkObject(self, objectId: str):
        return self.builder.get_object(objectId)
    
    def exit(self):
        try:
            self.stopVideo()
            self.stopAudio()

            self.window.close()
            self.settings.logDump()
            self.logger.log("[Program Exited]")
            sys.exit(0)
        except Exception as e:
            self.handleException(e)
