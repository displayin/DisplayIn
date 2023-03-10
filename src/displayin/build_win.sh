#!/bin/bash

# Experimental Paths
#  --paths "../../../opencv-4.7.0/build/install/x64/mingw/bin/" --paths "../../../opencv-4.7.0/build/install/x64/mingw/lib/" --paths "/mingw64/lib/python3.10/site-packages/cv2/python-3.10/"

# Clean Build Folders
[ -d "build" ] && rm -rf build/*
[ -d "dist" ] && rm -rf dist/*

# Run Pyinstaller
pyinstaller --noconsole --add-data="resource/ui/maingui.glade;resource/ui" --onedir displayin.py

# Workaround to manually copy cv2 standalone python and module config files to library modules output
mkdir dist/displayin/cv2/python-3.10/
cp install/patch/*py dist/displayin/cv2/
cp ../../../opencv-4.7.0/build/lib/python3/cv2*.pyd dist/displayin/cv2/python-3.10/