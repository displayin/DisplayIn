#!/bin/bash

# Experimental Paths
#  --paths "../../../opencv-4.7.0/build/install/x64/mingw/bin/" --paths "../../../opencv-4.7.0/build/install/x64/mingw/lib/" --paths "/mingw64/lib/python3.10/site-packages/cv2/python-3.10/"

# Run Pyinstaller
pyinstaller --noconsole --add-data="resource/ui/maingui.glade;resource/ui" --onedir displayin.py

# Workaround to manually copy cv2 standalone python to dynamic-load library modules
cp ../../../opencv-4.7.0/build/lib/python3/cv2*.pyd dist/displayin/lib-dynload/