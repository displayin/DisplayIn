class AudioStreamConfig:
  def __init__(self, inputDeviceId: int, outputDeviceId: int, sampleRate: int = 48000.0, blockSize: int =4096, channels: int =2):
    self.inputDeviceId: int = inputDeviceId
    self.outputDeviceId: int = outputDeviceId
    self.sampleRate = sampleRate
    self.blockSize = blockSize
    self.channels = channels
