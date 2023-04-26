#!/bin/bash

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