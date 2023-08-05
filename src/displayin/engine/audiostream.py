from config.audiostreamconfig import AudioStreamConfig
from util.exceptionhandler import ExceptionHandler
from threading import Thread
import sounddevice as sd
import wave

class AudioStream(object):
    def __init__(self, config: AudioStreamConfig, exHandler: ExceptionHandler = None):
        self.exHandler = exHandler
        self.volume: int = 2
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
            
            self.audioFrames = []
            self.recording = False
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
                self.audioOutputStream.write(indata * self.volume)

                if self.recording:
                    self.audioFrames.append(indata)

            # When we stop running, stop and close the stream
            self.audioInputStream.stop()
            self.audioInputStream.close()
            self.audioOutputStream.stop()
            self.audioOutputStream.close()

        except Exception as e:
            self.handleException(e)

    def stop(self):
        self.running = False

    def setVolume(self, volume: float):
        if volume < 0:
            self.volume = 0
        elif volume > 100:
            self.volume = 3

        self.volume = int(round((volume / 100) * 3))

    def startRecording(self):
        self.recording = True

    def stopRecording(self):
        self.recording = False
        waveFile = wave.open("temp.wav", 'wb')
        waveFile.setnchannels(self.config.outputChannels)
        waveFile.setsampwidth(2)
        waveFile.setframerate(self.config.outputSampleRate)
        waveFile.writeframes(b''.join(self.audioFrames))
        waveFile.close()
