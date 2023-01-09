from config.videostreamconfig import VideoStreamConfig
from threading import Thread
import time
import cv2 as cv

class VideoStream(object):
    def __init__(self, config: VideoStreamConfig):
        # Set config
        self.config: VideoStreamConfig = config
        
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

    def start(self):
        # Start the thread to read frames from the video stream
        self.running: bool = True
        self.updatethread = Thread(target=self.read, args=())
        self.updatethread.start()

        self.writethread = Thread(target=self.write, args=())
        self.writethread.start()

    def read(self):
        # Read the next frame from the stream in a different thread
        while self.capture.isOpened():
            self.capture.set(cv.CAP_PROP_POS_FRAMES, 0)
            (self.status, self.frame) = self.capture.read()

        time.sleep(self.fps)

    def write(self):
        while self.running:
            try:
                # Display frames in main program
                if self.status and self.frame.any():
                    if self.config.writeCallback:
                        # Call Write Callback
                        self.config.writeCallback(self.config.uiBuilder, "display.jpg", self.frame)
                    else:
                        # Show
                        self.frame = self.setResolution(
                            self.frame, width=self.config.width, height=self.config.height)
                        cv.imshow(self.config.name, self.frame)

                        # Press Q on keyboard to stop recording
                        key = cv.waitKey(1)
                        if key == ord('q'):
                            self.stop()
            except Exception as e:
                pass

    def stop(self):
        self.running = False
        self.capture.release()
        if not self.config.writeCallback:
            cv.destroyAllWindows()
            exit(0)

    # Resizes a image and maintains aspect ratio
    def setResolution(self, image, width, height, inter=cv.INTER_AREA):

        dim = (width, height)

        # Return the resized image
        return cv.resize(image, dim, interpolation=inter)

