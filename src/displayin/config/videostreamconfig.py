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
