# Compile OpenCV with GStreamer

## MSYS2 Method
1. Download [Gstreamer MSCV 64bit](https://gstreamer.freedesktop.org/data/pkg/windows/1.22.0/msvc/gstreamer-1.0-devel-msvc-x86_64-1.22.0.msi) or [Latest Release](https://gstreamer.freedesktop.org/download/) and do a full install
2. Download [OpenCV 4.7.0](https://github.com/opencv/opencv/archive/4.7.0.zip) or [Latest Source Release](https://opencv.org/releases/)
3. Edit the "C:\tools\msys64\home\USER\.bash_profile" to add PATH=/f/gstreamer/1.0/msvc_x86_64/bin:$PATH
4. Open Msys2 CMD Window (MINGW64)
5. Extract source to ~/opencv-4.7.0
6. mkdir ~/opencv-4.7.0/build && cd ~/opencv-4.7.0/build
7. cmake-gui
8. Where is the source code: C:/Users/USER/git/opencv-4.7.0
9. Where to build the binaries: C:/Users/USER/git/opencv-4.7.0/build
10. Click Configure and select MSYS2 Makefiles
11. Select Generate and close cmake-gui
12. run mingw32-make install [Compile OpenCV with Gstreamer in MinGW](https://medium.com/csmadeeasy/opencv-c-installation-on-windows-with-mingw-c0fc1499f39)

## MSCV Method - Does not Compile
1. Download and do a complete install of [Gstreamer for MinGW Development](https://gstreamer.freedesktop.org/download/)
2. Follow this guide to [Compile OpenCV for MinGW Windows](https://galaktyk.medium.com/how-to-build-opencv-with-gstreamer-b11668fa09c)
3. For step 5 CmakeGUI & Visual Studio use these for gstreamer
```
F:/gstreamer/1.0/msvc_x86_64/lib/gstapp-1.0.lib
F:/gstreamer/1.0/msvc_x86_64/lib/gstaudio-1.0.lib
F:/gstreamer/1.0/msvc_x86_64/lib/gstbase-1.0.lib
F:/gstreamer/1.0/msvc_x86_64/include/glib-2.0
F:/gstreamer/1.0/msvc_x86_64/lib/glib-2.0.lib
F:/gstreamer/1.0/msvc_x86_64/lib/glib-2.0/include
F:/gstreamer/1.0/msvc_x86_64/lib/gobject-2.0.lib
F:/gstreamer/1.0/msvc_x86_64/include/gstreamer-1.0
F:/gstreamer/1.0/msvc_x86_64/lib/gstreamer-1.0.lib
F:/gstreamer/1.0/msvc_x86_64/lib/gstpbutils-1.0.lib
F:/gstreamer/1.0/msvc_x86_64/lib/gstriff-1.0.lib
F:/gstreamer/1.0/msvc_x86_64/lib/gstvideo-1.0.lib
```

Also, you may need these paths from the [Official OpenCV Windows Build Guide](https://docs.opencv.org/4.x/d5/de5/tutorial_py_setup_in_windows.html)
```
C:/tools/msys64/mingw64/include/python3.10
C:/tools/msys64/mingw64/lib/libpython3.10.dll.a
C:/tools/msys64/mingw64/lib/python3.10/site-packages
```

And from this document, you may need to uncheck the following:
```
BUILD_TESTS
BUILD_opencv_highgui
ENABLE_SOLUTION_FOLDERS
```
