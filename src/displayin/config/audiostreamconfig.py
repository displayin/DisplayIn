class AudioStreamConfig:
  def __init__(self, inputDeviceId, outputDeviceId, inputSampleRate: int=48000.0, outputSampleRate: int=48000.0, blockSize: int=8192, inputChannels=2, outputChannels=2, inputLatency=None, outputLatency=None, dtype=None):
    self.inputDeviceId = inputDeviceId
    self.outputDeviceId = outputDeviceId
    self.inputSampleRate = inputSampleRate
    self.outputSampleRate = outputSampleRate
    self.blockSize = blockSize
    self.inputChannels = inputChannels
    self.outputChannels = outputChannels
    self.inputLatency = inputLatency
    self.outputLatency = outputLatency
    self.dtype = dtype
