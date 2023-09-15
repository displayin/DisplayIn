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

# Note this must be run within msys2 mingw64
pacman -Suy mingw-w64-x86_64-gtk3 mingw-w64-x86_64-python3 mingw-w64-x86_64-python3-gobject mingw-w64-x86_64-python-pip mingw-w64-x86_64-python-sounddevice mingw-w64-x86_64-portaudio mingw-w64-x86_64-cmake mingw-w64-x86_64-gcc mingw-w64-x86_64-toolchain git mingw-w64-x86_64-zlib zlib mingw-w64-x86_64-python-pyopengl mingw-w64-x86_64-glade mingw-w64-x86_64-ffmpeg mingw-w64-x86_64-python-ffmpeg-python python-devel mingw-w64-x86_64-python-psutil

# Unused Packages
# mingw-w64-x86_64-opencv mingw-w64-x86_64-gstreamer mingw-w64-x86_64-python-opencv

# Remove opencv
# pacman -R mingw-w64-x86_64-x264 mingw-w64-x86_64-ffms2 mingw-w64-x86_64-ffmpeg mingw-w64-x86_64-frei0r-plugins mingw-w64-x86_64-opencv
# pacman -R mingw-w64-x86_64-gstreamer mingw-w64-x86_64-gst-plugins-base mingw-w64-x86_64-gst-plugins-bad-libs mingw-w64-x86_64-gst-plugins-bad mingw-w64-x86_64-gst-plugins-good
# pacman -R  mingw-w64-x86_64-opencv mingw-w64-x86_64-python-opencv

# Install Debugpy
pip install debugpy

# Install PyInstaller
pip install pyinstaller

# Copy PortAudio DLL as a workaround for python sounddevice import
cp /mingw64/bin/libportaudio.dll /mingw64/bin/portaudio.dll