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

            # Set InputStream
            self.audioInputStream = sd.InputStream(
                device=config.inputDeviceId, 
                samplerate=config.inputSampleRate, 
                blocksize=config.blockSize, 
                channels=config.inputChannels,
                latency=config.inputLatency,
                dtype=config.dtype)
            
            # Set OutputStream
            self.audioOutputStream = sd.OutputStream(
                device=config.outputDeviceId, 
                samplerate=config.outputSampleRate, 
                blocksize=config.blockSize, 
                channels=config.outputChannels,
                latency=config.outputLatency,
                dtype=config.dtype)
        except Exception as e:
            self.handleException(e)
            self.audioInputStream = None
            self.audioOutputStream = None

    def handleException(self, e: Exception):
        if self.exHandler:
            self.exHandler.handle(e)

    def start(self):
        try:
            # Start the audio stream
            self.running: bool = True
            if self.audioInputStream is not None and self.audioOutputStream is not None:
                self.audioInputStream.start()
                self.audioOutputStream.start()

                # Start the thread to read frames from the audio stream
                self.updatethread = Thread(target=self.read, args=())
                self.updatethread.start()
        except Exception as e:
            self.handleException(e)

    def read(self):
        try:
            while self.running:
                indata, overflowed = self.audioInputStream.read(self.config.blockSize)
                self.audioOutputStream.write(indata)

            # When we stop running, stop and close the stream
            self.audioInputStream.stop()
            self.audioInputStream.close()
            self.audioOutputStream.stop()
            self.audioOutputStream.close()

        except Exception as e:
            self.handleException(e)

    def stop(self):
        self.running = False