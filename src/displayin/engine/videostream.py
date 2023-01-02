from config.videostreamconfig import VideoStreamConfig
from threading import Thread
import time
import cv2 as cv


class VideoStream(object):
    def __init__(self, config: VideoStreamConfig):
        
        self.config: VideoStreamConfig = config
        
        # Create a VideoCapture object
        self.capture = cv.VideoCapture(config.deviceId, config.api)
        self.capture.set(cv.CAP_PROP_BUFFERSIZE, config.bufferSize)
        self.capture.set(cv.CAP_PROP_FOURCC, cv.VideoWriter_fourcc('M', 'J', 'P', 'G'))
        self.capture.set(cv.CAP_PROP_FRAME_WIDTH, config.width)
        self.capture.set(cv.CAP_PROP_FRAME_HEIGHT, config.height)

        # FPS = 1/X
        # X = desired FPS
        fps: float = 1/config.fps
        self.fpsMs: int = int(fps * 1000)

    def start(self):
        # Start the thread to read frames from the video stream
        self.thread = Thread(target=self.update, args=())
        self.thread.daemon = True
        self.thread.start()

    def read(self):
        # Read the next frame from the stream in a different thread
        while self.capture.isOpened():
            self.capture.set(cv.CAP_PROP_POS_FRAMES, 0)
            (self.status, self.frame) = self.capture.read()

    def write(self):
        # Display frames in main program
        if self.status:
            self.frame = self.setResolution(self.frame, height=1280, width=720)
            cv.imshow('DisplayIn Video Stream', self.frame)

        # Press Q on keyboard to stop recording
        key = cv.waitKey(1)
        if key == ord('q'):
            self.capture.release()
            cv.destroyAllWindows()
            exit(1)

    # Resizes a image and maintains aspect ratio
    def setResolution(self, image, width, height, inter=cv.INTER_AREA):

        dim = (height, width)

        # Return the resized image
        return cv.resize(image, dim, interpolation=inter)

