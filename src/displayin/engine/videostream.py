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
from util.exceptionhandler import ExceptionHandler
from util.resource import Resource as res
from threading import Thread
import time
import cv2 as cv

class VideoStream(object):
    def __init__(self, config: VideoStreamConfig, exHandler: ExceptionHandler = None):
        self.exHandler = exHandler
        try:
            # Set config
            self.config: VideoStreamConfig = config

            # Set width and height
            self.width: int = config.width
            self.height: int = config.height
            
            # Create a VideoCapture object
            self.capture = cv.VideoCapture(config.deviceId, config.api)
            self.fourcc = cv.VideoWriter_fourcc('M', 'J', 'P', 'G')
            self.capture.set(cv.CAP_PROP_BUFFERSIZE, config.bufferSize)
            self.capture.set(cv.CAP_PROP_FOURCC, self.fourcc)
            if not res.isWindows():
                self.capture.set(cv.CAP_PROP_FRAME_WIDTH, config.width)
                self.capture.set(cv.CAP_PROP_FRAME_HEIGHT, config.height)

            # Create Video Writer
            self.writer = None
            self.recording = False
            self.recordingStartTime = None
            self.recordingFrameCount = 0

            # FPS = 1/X
            # X = desired FPS
            self.fps: float = 1/config.fps

            # Initialize Status
            self.status = False
            self.frame = []
            self.screenshotPath = None
            self.takeScreenshot = False
            self.watermark = None
        except Exception as e:
            self.handleException(e)

    def handleException(self, e: Exception):
        if self.exHandler:
            self.exHandler.handle(e)

    def start(self):
        try:
            if self.capture:
                # Start the thread to read frames from the video stream
                self.running: bool = True
                self.updatethread = Thread(target=self.read, args=())
                self.updatethread.start()
                self.writethread = Thread(target=self.write, args=())
                self.writethread.start()
        except Exception as e:
            self.handleException(e)

    def read(self):
        try:
            # Read the next frame from the stream in a different thread
            while self.running:
                if res.isLinux():
                    self.capture.set(cv.CAP_PROP_POS_FRAMES, 0)
                (self.status, self.frame) = self.capture.read()

                # Display frames in main program
                if self.capture.isOpened() and self.status and self.frame.any():
                    self.frame = self.setResolution(
                        self.frame, width=self.config.width, height=self.config.height)

                    if self.config.writeCallback:
                        # Call Write Callback
                        self.config.writeCallback(self.config.uiBuilder, self.frame, self.config.displayWidget)
                    else:
                        # Show using OpenCV
                        cv.imshow(self.config.name, self.frame)

                        # Press Q on keyboard to stop recording
                        key = cv.waitKey(1)
                        if key == ord('q'):
                            self.stop()

                # Limit Capture to FPS
                time.sleep(self.fps)

            # Release the capture
            self.capture.release()
            if not self.config.writeCallback:
                cv.destroyAllWindows()
                exit(0)
        except Exception as e:
            self.handleException(e)

    def write(self):
        try:
            # Read the next frame from the stream in a different thread
            while self.running:

                # Display frames in main program
                if self.capture.isOpened() and self.status and self.frame.any():
                    if self.takeScreenshot:
                        result = self.addWatermark(self.frame)
                        cv.imwrite(self.screenshotPath, result)
                        self.takeScreenshot = False

                    if self.recording:
                        self.writer.write(self.frame)
                        self.recordingFrameCount = self.recordingFrameCount + 1

                # Limit Capture to FPS
                time.sleep(self.fps / 2)
        except Exception as e:
            self.handleException(e)

    def stop(self):
        # Stop Recording
        if self.writer != None:
            self.writer.release()
            self.writer = None

        # Release the capture
        self.capture.release()
        self.running = False

    # Resizes a image and maintains aspect ratio
    def setResolution(self, image, width, height, inter=cv.INTER_AREA):

        dim = (width, height)

        # Return the resized image
        return cv.resize(image, dim, interpolation=inter)
    
    def screenshot(self, filename):
        self.screenshotPath = filename
        self.takeScreenshot = True
        pass
    
    def startRecording(self):
        res.deleteFileIfExists("temp.avi")
        self.writer = cv.VideoWriter(
            "temp.avi", self.fourcc, self.config.fps, (self.config.width, self.config.height))
        self.recording = True
        self.recordingStartTime = time.time()
        self.recordingFrameCount = 0

    def stopRecording(self):
        self.recording = False
        time.sleep(0.1)
        if self.writer != None:
            self.writer.release()
            self.writer = None

        elapsedTime = time.time() - self.recordingStartTime
        recordedFps = self.recordingFrameCount / elapsedTime
        return recordedFps
        
    def setWatermark(self, watermarkPath: str):
        self.watermark = cv.imread(watermarkPath)

    def addWatermark(self, frame):
        result = frame
        if not self.watermark is None:
            h, w, _ = self.watermark.shape

            # calculating from top, bottom, right and left
            topY = 30
            leftX = 30
            bottomY = topY + h
            rightX = leftX + w
            destination = frame[topY:bottomY, leftX:rightX]
            slice = cv.addWeighted(destination, 0.5, self.watermark, 0.5, 0)
            result[topY:bottomY, leftX:rightX] = slice
        return result

