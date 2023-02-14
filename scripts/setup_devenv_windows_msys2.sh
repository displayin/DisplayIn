#!/bin/bash
pacman -Suy mingw-w64-x86_64-gtk3 mingw-w64-x86_64-python3 mingw-w64-x86_64-python3-gobject mingw-w64-x86_64-python-pip mingw-w64-x86_64-python-sounddevice mingw-w64-x86_64-portaudio mingw-w64-x86_64-opencv mingw-w64-x86_64-python-opencv mingw-w64-x86_64-gstreamer

# Install Debugpy
pip install debugpy

# Install PyInstaller
pip install pyinstaller