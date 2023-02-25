import cv2 as cv

class VideoStreamConfig:
  def __init__(self, deviceId, name: str=None, width: int=1920, height: int=1080, fps: int=60, bufferSize: int = 2, api=cv.CAP_V4L2, writeCallback=None, uiBuilder=None, displayWidget=None):
    self.deviceId = deviceId
    self.name = name
    self.fps: int = fps
    self.width: int = width
    self.height: int = height
    self.bufferSize: int = bufferSize
    self.api = api
    self.writeCallback = writeCallback
    self.uiBuilder = uiBuilder
    self.displayWidget = displayWidget
