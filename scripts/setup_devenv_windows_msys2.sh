#!/bin/bash
# Note this must be run within msys2 mingw64
pacman -Suy mingw-w64-x86_64-gtk3 mingw-w64-x86_64-python3 mingw-w64-x86_64-python3-gobject mingw-w64-x86_64-python-pip mingw-w64-x86_64-python-sounddevice mingw-w64-x86_64-portaudio mingw-w64-x86_64-cmake mingw-w64-x86_64-gcc mingw-w64-x86_64-toolchain git mingw-w64-x86_64-zlib zlib mingw-w64-x86_64-python-pyopengl mingw-w64-x86_64-glade mingw-w64-x86_64-ffmpeg mingw-w64-x86_64-python-ffmpeg-python python-devel

# Unused Packages
# mingw-w64-x86_64-opencv mingw-w64-x86_64-gstreamer mingw-w64-x86_64-python-opencv

# Remove opencv
# pacman -R mingw-w64-x86_64-x264 mingw-w64-x86_64-ffms2 mingw-w64-x86_64-ffmpeg mingw-w64-x86_64-frei0r-plugins mingw-w64-x86_64-opencv

# Install Debugpy
pip install debugpy

# Install PyInstaller
pip install pyinstaller

# Copy PortAudio DLL as a workaround for python sounddevice import
cp /mingw64/bin/libportaudio.dll /mingw64/bin/portaudio.dll