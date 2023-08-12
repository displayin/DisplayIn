#!/bin/bash

# Clean Build Folders
[ -d "build" ] && rm -rf build
[ -d "dist" ] && rm -rf dist
[ -f "displayin.spec" ] && rm displayin.spec

# Run Pyinstaller
pyinstaller --noconsole --add-data="resource/ui/maingui.glade:resource/ui" --add-data "resource/images:resource/images" --splash "resource/images/DisplayInSplash.png" --icon="resource/images/DisplayInIcon.ico" --hidden-import "OpenGL.platform.egl" --onedir displayin.py