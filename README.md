# DisplayIn
DisplayIn App for streaming your display input using OpenCV written in Python.

## Dependent Libraries
- [OpenCV Python](https://docs.opencv.org/3.4/dd/d43/tutorial_py_video_display.html)
- [python-sounddevice](https://python-sounddevice.readthedocs.io/en/0.3.12/api.html)
- [Python GTK+3](https://python-gtk-3-tutorial.readthedocs.io/en/latest/introduction.html)

## IDEs
- [VSCode](https://code.visualstudio.com/)
- [Glade GTK](https://glade.gnome.org/)

# Setup Windows Dev Environment
1. Install [Chocolatey](https://chocolatey.org/)
2. Open Powershell in Administrator Window and run 
```
Set-ExecutionPolicy Unrestricted
```
3. Then install msys2
```
choco install msys2
```
4. Add these to the PATH system environment variable
```
C:\tools\msys64\mingw64
```
5. Open msys2 terminal
```
C:\tools\msys64\mingw64.exe
```
6. Now run the setup script
```
scripts/setup_devenv_windows_msys2.sh
```
7. The first run will close the window, repeat steps 5 and 6 again to finish

## Compile OpenCV with GStreamer
1. Download and do a complete install of [Gstreamer for MinGW Development](https://gstreamer.freedesktop.org/download/)
2. Follow this guide to [Compile OpenCV for MinGW Windows](https://galaktyk.medium.com/how-to-build-opencv-with-gstreamer-b11668fa09c)
3. For step 5 CmakeGUI & Visual Studio use these for gstreamer
```
F:/gstreamer/1.0/mingw_x86_64/lib/gstapp-1.0.lib
F:/gstreamer/1.0/mingw_x86_64/lib/gstaudio-1.0.lib
F:/gstreamer/1.0/mingw_x86_64/lib/gstbase-1.0.lib
F:/gstreamer/1.0/mingw_x86_64/include/glib-2.0
F:/gstreamer/1.0/mingw_x86_64/lib/glib-2.0.lib
F:/gstreamer/1.0/mingw_x86_64/lib/glib-2.0/include
F:/gstreamer/1.0/mingw_x86_64/lib/gobject-2.0.lib
F:/gstreamer/1.0/mingw_x86_64/include/gstreamer-1.0
F:/gstreamer/1.0/mingw_x86_64/lib/gstreamer-1.0.lib
F:/gstreamer/1.0/mingw_x86_64/lib/gstpbutils-1.0.lib
F:/gstreamer/1.0/mingw_x86_64/lib/gstriff-1.0.lib
F:/gstreamer/1.0/mingw_x86_64/lib/gstvideo-1.0.lib
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

# Documentation

## Windows Tools
- [MSYS2 Pacman](https://www.msys2.org/)
- [PyObject for Windows](https://sourceforge.net/projects/pygobjectwin32/)
- [GitHub CLI](https://cli.github.com/)

## Windows Documentation
- [Install GTK3 using gvsbuild](https://github.com/wingtk/gvsbuild/)

## Windows Misc Documentation
- [Install GTK in Windows](https://pygobject.readthedocs.io/en/latest/getting_started.html#windows-getting-started)
- [Setting up GTK for Windows](https://www.gtk.org/docs/installations/windows)
- [Using GCC with MinGW](https://code.visualstudio.com/docs/cpp/config-mingw)
- [Create Symlink in Windows](https://www.maketecheasier.com/create-symbolic-links-windows10/)
- [Install PyGObject in Windows](https://stackoverflow.com/questions/33862049/python-cannot-install-pygobject)
- [Pip on MinGW64](https://stackoverflow.com/questions/56930492/pip-on-mingw64)
- [Install GCC in MinGW64](https://www.devdungeon.com/content/install-gcc-compiler-windows-msys2-cc)
- [Setting up Python in Windows](https://stackoverflow.com/questions/51787630/setting-up-developement-environment-pycharm-python-gtk-windows/51959831#51959831)