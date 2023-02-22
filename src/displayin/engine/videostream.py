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

            self.capture.set(cv.CAP_PROP_BUFFERSIZE, config.bufferSize)
            self.capture.set(cv.CAP_PROP_FOURCC, cv.VideoWriter_fourcc('M', 'J', 'P', 'G'))
            self.capture.set(cv.CAP_PROP_FRAME_WIDTH, config.width)
            self.capture.set(cv.CAP_PROP_FRAME_HEIGHT, config.height)

            # FPS = 1/X
            # X = desired FPS
            self.fps: float = 1/config.fps

            # Initialize Status
            self.status = False
            self.frame = []
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
        except Exception as e:
            self.handleException(e)

    def read(self):
        try:
            # Read the next frame from the stream in a different thread
            while self.running and self.capture.isOpened():
                if res.isLinux():
                    self.capture.set(cv.CAP_PROP_POS_FRAMES, 0)
                (self.status, self.frame) = self.capture.read()

                # Display frames in main program
                if self.status and self.frame.any():
                    self.frame = self.setResolution(
                        self.frame, width=self.config.width, height=self.config.height)
                    if self.config.writeCallback:
                        # Call Write Callback
                        self.config.writeCallback(self.config.uiBuilder, self.frame)
                    else:
                        # Show using OpenCV
                        cv.imshow(self.config.name, self.frame)

                        # Press Q on keyboard to stop recording
                        key = cv.waitKey(1)
                        if key == ord('q'):
                            self.stop()

            # Release the capture
            self.capture.release()
            if not self.config.writeCallback:
                cv.destroyAllWindows()
                exit(0)
        except Exception as e:
            self.handleException(e)

    def stop(self):
        self.running = False

    # Resizes a image and maintains aspect ratio
    def setResolution(self, image, width, height, inter=cv.INTER_AREA):

        dim = (width, height)

        # Return the resized image
        return cv.resize(image, dim, interpolation=inter)

