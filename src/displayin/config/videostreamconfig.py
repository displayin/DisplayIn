import cv2 as cv

class VideoStreamConfig:
  def __init__(self, deviceId: int, name: str = None, fps: int = 60, width: int = 1920, height: int = 1080, bufferSize: int = 2, api = cv.CAP_V4L2):
    self.deviceId: int = deviceId
    self.name = name
    self.fps: int = fps
    self.width: int = width
    self.height: int = height
    self.bufferSize: int = bufferSize
    self.api = api
