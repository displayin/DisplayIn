class AudioStreamConfig:
  def __init__(self, inputDeviceId, outputDeviceId, sampleRate: int=48000.0, blockSize: int=8192, channels=2, latency=None, dtype=None):
    self.inputDeviceId = inputDeviceId
    self.outputDeviceId = outputDeviceId
    self.sampleRate = sampleRate
    self.blockSize = blockSize
    self.channels = channels
    self.latency = latency
    self.dtype = dtype
