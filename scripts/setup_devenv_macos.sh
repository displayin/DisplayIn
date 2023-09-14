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


# Install Git
brew install git

# Install VS Code
brew install --cask visual-studio-code

# Install Python
brew install python@3.11

# Install GTK3
brew install gtk+3

# Install PyGObject
brew install pygobject3

# Install OpenCV
brew install opencv

# Install PyInstaller
brew install pyinstaller

# Set Default Python
ln -s -f /usr/local/bin/python3.11 /usr/local/bin/python

# Upgrade PIP
python3 -m pip install --upgrade pip

# Install OpenCV Python
python3 -m pip install opencv-python

# Install Debugpy
python3 -m pip install debugpy

# Install sounddevice
python3 -m pip install sounddevice

# Install Pillow
python3 -m pip install pillow

# Install PyObj AVFoundation
python3 -m pip install pyobjc-framework-AVFoundation

# Install PyOpenGL
python3 -m pip install PyOpenGL