from config.audiostreamconfig import AudioStreamConfig
from threading import Thread
import sounddevice as sd

class AudioStream(object):
    def __init__(self, config: AudioStreamConfig):
        # Set config
        self.config: AudioStreamConfig = config
        self.audiostream = sd.Stream(device=(config.inputDeviceId, config.outputDeviceId), samplerate=config.sampleRate, blocksize=config.blockSize, channels=config.channels)

    def start(self):
        # Start the audio stream
        self.running: bool = True
        self.audiostream.start()

        # Start the thread to read frames from the audio stream
        self.updatethread = Thread(target=self.read, args=())
        self.updatethread.start()

    def read(self):
        while self.running:
            try:
                indata, overflowed = self.audiostream.read(self.config.blockSize)
                self.audiostream.write(indata)
            except AttributeError:
                pass

    def stop(self):
        self.running = False

