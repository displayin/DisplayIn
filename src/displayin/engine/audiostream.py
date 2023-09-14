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
from config.audiostreamconfig import AudioStreamConfig
from util.exceptionhandler import ExceptionHandler
from util.resource import Resource as res
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
        res.deleteFileIfExists("temp.wav")
        self.audioFrames = []
        self.recording = True

    def stopRecording(self):
        self.recording = False
        waveFile = wave.open("temp.wav", 'wb')
        waveFile.setnchannels(self.config.outputChannels)
        waveFile.setsampwidth(self.getSampleWidth())
        waveFile.setframerate(self.config.outputSampleRate)
        waveFile.writeframes(b''.join(self.audioFrames))
        waveFile.close()

    def getSampleWidth(self):
        return int(self.config.blockSize / 2048)
