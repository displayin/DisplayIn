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

# Make Binary Path
mkdir dist/displayin/lib/opencv/
mkdir dist/displayin/lib/opencv/bin/
mkdir dist/displayin/lib/opencv/lib/
mkdir dist/displayin/lib/opencv/lib/gstreamer-1.0/

# Copy mingw64 dependencies
cp /mingw64/bin/libEGL.dll dist/displayin/lib/opencv/bin/
cp /mingw64/bin/libGLESv2.dll dist/displayin/lib/opencv/bin/
cp /mingw64/bin/libIex-3_1.dll dist/displayin/lib/opencv/bin/
cp /mingw64/bin/libIlmThread-3_1.dll dist/displayin/lib/opencv/bin/
cp /mingw64/bin/libImath-3_1.dll dist/displayin/lib/opencv/bin/
cp /mingw64/bin/libOpenEXR-3_1.dll dist/displayin/lib/opencv/bin/

# Copy gstreamer dependencies
cp /f/gstreamer/1.0/msvc_x86_64/bin/gstapp-1.0-0.dll dist/displayin/lib/opencv/bin/
cp /f/gstreamer/1.0/msvc_x86_64/bin/gstaudio-1.0-0.dll dist/displayin/lib/opencv/bin/
cp /f/gstreamer/1.0/msvc_x86_64/bin/gstbase-1.0-0.dll dist/displayin/lib/opencv/bin/
cp /f/gstreamer/1.0/msvc_x86_64/bin/gstpbutils-1.0-0.dll dist/displayin/lib/opencv/bin/
cp /f/gstreamer/1.0/msvc_x86_64/bin/gstreamer-1.0-0.dll dist/displayin/lib/opencv/bin/
cp /f/gstreamer/1.0/msvc_x86_64/bin/gstriff-1.0-0.dll dist/displayin/lib/opencv/bin/
cp /f/gstreamer/1.0/msvc_x86_64/bin/gsttag-1.0-0.dll dist/displayin/lib/opencv/bin/
cp /f/gstreamer/1.0/msvc_x86_64/bin/gstvideo-1.0-0.dll dist/displayin/lib/opencv/bin/
cp /f/gstreamer/1.0/msvc_x86_64/bin/orc-0.4-0.dll dist/displayin/lib/opencv/bin/

# Copy gstreamer lib dependencies
cp /f/gstreamer/1.0/msvc_x86_64/lib/gstreamer-1.0/gstapp.dll dist/displayin/lib/opencv/lib/gstreamer-1.0/
cp /f/gstreamer/1.0/msvc_x86_64/lib/gstreamer-1.0/gstmediafoundation.dll dist/displayin/lib/opencv/lib/gstreamer-1.0/
cp /f/gstreamer/1.0/msvc_x86_64/lib/gstreamer-1.0/gstvideoconvertscale.dll dist/displayin/lib/opencv/lib/gstreamer-1.0/
