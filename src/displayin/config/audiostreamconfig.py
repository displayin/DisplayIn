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
