from config.audiostreamconfig import AudioStreamConfig
from util.exceptionhandler import ExceptionHandler
from threading import Thread
import sounddevice as sd

class AudioStream(object):
    def __init__(self, config: AudioStreamConfig, exHandler: ExceptionHandler = None):
        self.exHandler = exHandler
        try:
            # Set config
            self.config: AudioStreamConfig = config
            self.audiostream = sd.Stream(device=(config.inputDeviceId, config.outputDeviceId), samplerate=config.sampleRate, blocksize=config.blockSize, channels=config.channels)
        except Exception as e:
            self.handleException(e)

    def handleException(self, e: Exception):
        if self.exHandler:
            self.exHandler.handle(e)

    def start(self):
        try:
            # Start the audio stream
            self.running: bool = True
            if self.audiostream is not None:
                self.audiostream.start()

                # Start the thread to read frames from the audio stream
                self.updatethread = Thread(target=self.read, args=())
                self.updatethread.start()
        except Exception as e:
            self.handleException(e)

    def read(self):
        try:
            while self.running:
                indata, overflowed = self.audiostream.read(self.config.blockSize)
                self.audiostream.write(indata)

            # When we stop running, stop and close the stream
            self.audiostream.stop()
            self.audiostream.close()

        except Exception as e:
            self.handleException(e)

    def stop(self):
        self.running = False