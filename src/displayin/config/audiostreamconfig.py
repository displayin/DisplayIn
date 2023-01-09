class AudioStreamConfig:
  def __init__(self, inputDeviceId, outputDeviceId, sampleRate: int = 48000.0, blockSize: int =4096, channels: int =2):
    self.inputDeviceId = inputDeviceId
    self.outputDeviceId = outputDeviceId
    self.sampleRate = sampleRate
    self.blockSize = blockSize
    self.channels = channels
