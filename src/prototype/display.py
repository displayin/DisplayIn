# Real-Time Camera
# https://stackoverflow.com/questions/55828451/video-streaming-from-ip-camera-in-python-using-opencv-cv2-videocapture
# https://stackoverflow.com/questions/58293187/opencv-real-time-streaming-video-capture-is-slow-how-to-drop-frames-or-get-sync
# https://stackoverflow.com/questions/65683036/delay-lag-in-opencv-videocapture
# https://stackoverflow.com/questions/37799847/python-playing-a-video-with-audio-with-opencv
from threading import Thread
import time, cv2, wave, threading
import sounddevice as sd

class VideoStreamCapture(object):
    def __init__(self, src=0):
        # Create a VideoCapture object
        self.capture = cv2.VideoCapture(src, cv2.CAP_V4L2)
        self.capture.set(cv2.CAP_PROP_BUFFERSIZE, 2)
        self.capture.set(cv2.CAP_PROP_FOURCC, cv2.VideoWriter_fourcc('M', 'J', 'P', 'G'))
        width = 1920
        height = 1080
        self.capture.set(cv2.CAP_PROP_FRAME_WIDTH, width)
        self.capture.set(cv2.CAP_PROP_FRAME_HEIGHT, height)

        # FPS = 1/X
        # X = desired FPS
        self.FPS = 1/60
        self.FPS_MS = int(self.FPS * 1000)

        # Fullscreen
        cv2.namedWindow("Display", cv2.WINDOW_AUTOSIZE)
        cv2.setWindowProperty("Display", cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_FULLSCREEN)

        # Start the thread to read frames from the video stream
        self.thread = Thread(target=self.update, args=())
        self.thread.daemon = True
        self.thread.start()

    def update(self):
        # Read the next frame from the stream in a different thread
        while True:
            if self.capture.isOpened():
                self.capture.set(cv2.CAP_PROP_POS_FRAMES, 0)
                (self.status, self.frame) = self.capture.read()
            # time.sleep(self.FPS)

    def show_frame(self):
        # Display frames in main program
        if self.status:
            self.frame = self.set_resolution(self.frame, height=1280, width=720)
            cv2.imshow('DisplayIn Video Stream', self.frame)

        # Press Q on keyboard to stop recording
        key = cv2.waitKey(1)
        if key == ord('q'):
            self.capture.release()
            cv2.destroyAllWindows()
            exit(1)

    # Resizes a image and maintains aspect ratio
    def set_resolution(self, image, height, width, inter=cv2.INTER_AREA):

        dim = (height, width)

        # Return the resized image
        return cv2.resize(image, dim, interpolation=inter)

if __name__ == '__main__':
    stream_link = 0
    video_stream_widget = VideoStreamCapture(stream_link)
    # sd.default.device = 10
    # sd.default.samplerate = 44100
    # sd.default.channels = 2

    devices = sd.query_devices()
    
    audiostream = sd.Stream(device=(10, 15), samplerate=48000.0, blocksize=4096, channels=2)
    audiostream.start()
    while True:
        try:
            video_stream_widget.show_frame()
            indata, overflowed = audiostream.read(4096)
            audiostream.write(indata)
        except AttributeError:
            pass
    