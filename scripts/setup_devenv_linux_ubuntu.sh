#!/bin/bash
##
## Copyright (c) 2023 Tekst LLC.
##
## This file is part of DisplayIn 
## (see https://github.com/displayin).
##
## This program is free software: you can redistribute it and/or modify
## it under the terms of the GNU General Public License as published by
## the Free Software Foundation, either version 3 of the License, or
## (at your option) any later version.
##
## This program is distributed in the hope that it will be useful,
## but WITHOUT ANY WARRANTY; without even the implied warranty of
## MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
## GNU General Public License for more details.
##
## You should have received a copy of the GNU General Public License
## along with this program. If not, see <http://www.gnu.org/licenses/>.##
sudo apt install python3-gi python3-gi-cairo gir1.2-gtk-3.0 python-is-python3 python3-pip python3-opencv python3-tk

# Install Debugpy
sudo pip install debugpy

# Install PyInstaller
sudo pip install pyinstaller

# Install sounddevice
sudo pip install sounddevice

# Install PyOpenGL
sudo pip install pyopengl

# Install FFmpeg
sudo pip install ffmpeg-python

# Install licenseheaders
sudo pip install licenseheaders