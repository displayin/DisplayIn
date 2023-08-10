#!/bin/bash

# Experimental Paths
#  --paths "../../../opencv-4.7.0/build/install/x64/mingw/bin/" --paths "../../../opencv-4.7.0/build/install/x64/mingw/lib/" --paths "/mingw64/lib/python3.11/site-packages/cv2/python-3.11/"

# Clean Build Folders
[ -d "build" ] && rm -rf build
[ -d "dist" ] && rm -rf dist
[ -f "displayin.spec" ] && rm displayin.spec

# Set GSTREAMER ROOT
GSTREAMER_ROOT=/c/gstreamer
[ -d "/f/gstreamer" ] && GSTREAMER_ROOT=/f/gstreamer

# Run Pyinstaller
pyinstaller --add-data="resource/ui/maingui.glade;resource/ui" --splash "resource/images/DisplayInSplash.png" --icon="resource/images/DisplayInIcon.ico" --onedir displayin.py \
--add-binary "C:\tools\msys64\mingw64\lib\gdk-pixbuf-2.0\2.10.0\loaders\libpixbufloader-png.dll;lib\gdk-pixbuf\loaders" \
--add-binary "C:\tools\msys64\mingw64\bin\libGLESv2.dll;lib\opencv\bin" \
--add-binary "C:\tools\msys64\mingw64\bin\libEGL.dll;lib\opencv\bin" \
--add-binary "C:\tools\msys64\mingw64\bin\libIex-3_1.dll;lib\opencv\bin" \
--add-binary "C:\tools\msys64\mingw64\bin\libIlmThread-3_1.dll;lib\opencv\bin" \
--add-binary "C:\tools\msys64\mingw64\bin\libImath-3_1.dll;lib\opencv\bin" \
--add-binary "C:\tools\msys64\mingw64\bin\libOpenEXR-3_1.dll;lib\opencv\bin" \
--add-binary "F:\gstreamer\1.0\msvc_x86_64\bin\gstapp-1.0-0.dll;lib\opencv\bin" \
--add-binary "F:\gstreamer\1.0\msvc_x86_64\bin\gstaudio-1.0-0.dll;lib\opencv\bin" \
--add-binary "F:\gstreamer\1.0\msvc_x86_64\bin\gstbase-1.0-0.dll;lib\opencv\bin" \
--add-binary "F:\gstreamer\1.0\msvc_x86_64\bin\gstpbutils-1.0-0.dll;lib\opencv\bin" \
--add-binary "F:\gstreamer\1.0\msvc_x86_64\bin\gstreamer-1.0-0.dll;lib\opencv\bin" \
--add-binary "F:\gstreamer\1.0\msvc_x86_64\bin\gstriff-1.0-0.dll;lib\opencv\bin" \
--add-binary "F:\gstreamer\1.0\msvc_x86_64\bin\gsttag-1.0-0.dll;lib\opencv\bin" \
--add-binary "F:\gstreamer\1.0\msvc_x86_64\bin\gstvideo-1.0-0.dll;lib\opencv\bin" \
--add-binary "F:\gstreamer\1.0\msvc_x86_64\bin\gstd3d11-1.0-0.dll;lib\opencv\bin" \
--add-binary "F:\gstreamer\1.0\msvc_x86_64\bin\orc-0.4-0.dll;lib\opencv\bin" \
--add-binary "F:\gstreamer\1.0\msvc_x86_64\lib\gstreamer-1.0\gstapp.dll;lib\opencv\lib\gstreamer-1.0" \
--add-binary "F:\gstreamer\1.0\msvc_x86_64\lib\gstreamer-1.0\gstmediafoundation.dll;lib\opencv\lib\gstreamer-1.0" \
--add-binary "F:\gstreamer\1.0\msvc_x86_64\lib\gstreamer-1.0\gstvideoconvertscale.dll;lib\opencv\lib\gstreamer-1.0" \
--add-binary "C:\Windows\System32\vcruntime140_1.dll;lib\opencv\bin"


# Workaround to manually copy cv2 standalone python and module config files to library modules output
[ ! -d "dist/displayin/cv2/python-3.11/" ] && mkdir dist/displayin/cv2/python-3.11/
cp install/patch/*py dist/displayin/cv2/
cp ../../../opencv-4.7.0/build/lib/python3/cv2*.pyd dist/displayin/cv2/python-3.11/

# Make Binary Path
# mkdir dist/displayin/lib/opencv/
# mkdir dist/displayin/lib/opencv/bin/
# mkdir dist/displayin/lib/opencv/lib/
# mkdir dist/displayin/lib/opencv/lib/gstreamer-1.0/

# Copy mingw64 dependencies
# cp /mingw64/bin/libEGL.dll dist/displayin/lib/opencv/bin/
# cp /mingw64/bin/libGLESv2.dll dist/displayin/lib/opencv/bin/
# cp /mingw64/bin/libIex-3_1.dll dist/displayin/lib/opencv/bin/
# cp /mingw64/bin/libIlmThread-3_1.dll dist/displayin/lib/opencv/bin/
# cp /mingw64/bin/libImath-3_1.dll dist/displayin/lib/opencv/bin/
# cp /mingw64/bin/libOpenEXR-3_1.dll dist/displayin/lib/opencv/bin/

# Copy gstreamer dependencies
# cp $GSTREAMER_ROOT/1.0/msvc_x86_64/bin/*.dll dist/displayin/lib/opencv/bin/
# cp $GSTREAMER_ROOT/1.0/msvc_x86_64/bin/gstapp-1.0-0.dll dist/displayin/lib/opencv/bin/
# cp $GSTREAMER_ROOT/1.0/msvc_x86_64/bin/gstaudio-1.0-0.dll dist/displayin/lib/opencv/bin/
# cp $GSTREAMER_ROOT/1.0/msvc_x86_64/bin/gstbase-1.0-0.dll dist/displayin/lib/opencv/bin/
# cp $GSTREAMER_ROOT/1.0/msvc_x86_64/bin/gstpbutils-1.0-0.dll dist/displayin/lib/opencv/bin/
# cp $GSTREAMER_ROOT/1.0/msvc_x86_64/bin/gstreamer-1.0-0.dll dist/displayin/lib/opencv/bin/
# cp $GSTREAMER_ROOT/1.0/msvc_x86_64/bin/gstriff-1.0-0.dll dist/displayin/lib/opencv/bin/
# cp $GSTREAMER_ROOT/1.0/msvc_x86_64/bin/gsttag-1.0-0.dll dist/displayin/lib/opencv/bin/
# cp $GSTREAMER_ROOT/1.0/msvc_x86_64/bin/gstvideo-1.0-0.dll dist/displayin/lib/opencv/bin/
# cp $GSTREAMER_ROOT/1.0/msvc_x86_64/bin/gstd3d11-1.0-0.dll dist/displayin/lib/opencv/bin/
# cp $GSTREAMER_ROOT/1.0/msvc_x86_64/bin/orc-0.4-0.dll dist/displayin/lib/opencv/bin/

# Copy gstreamer lib dependencies
# cp $GSTREAMER_ROOT/1.0/msvc_x86_64/lib/gstreamer-1.0/*.dll dist/displayin/lib/opencv/lib/gstreamer-1.0/
# cp $GSTREAMER_ROOT/1.0/msvc_x86_64/lib/gstreamer-1.0/gstapp.dll dist/displayin/lib/opencv/lib/gstreamer-1.0/
# cp $GSTREAMER_ROOT/1.0/msvc_x86_64/lib/gstreamer-1.0/gstmediafoundation.dll dist/displayin/lib/opencv/lib/gstreamer-1.0/
# cp $GSTREAMER_ROOT/1.0/msvc_x86_64/lib/gstreamer-1.0/gstvideoconvertscale.dll dist/displayin/lib/opencv/lib/gstreamer-1.0/

# Copy Visual Studio Redistributable Binary - 14.34.31938.0
# https://aka.ms/vs/17/release/vc_redist.x64.exe 
# https://learn.microsoft.com/en-us/cpp/windows/latest-supported-vc-redist?view=msvc-170
# cp /c/Windows/System32/vcruntime140_1.dll dist/displayin/lib/opencv/bin/

# Remove any gstreamer dependencies copied into the build directory (they may be the wrong version)
rm dist/displayin/gst*.dll