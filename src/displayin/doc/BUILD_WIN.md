# Compile OpenCV with GStreamer

## MSYS2 Method
1. Download [Gstreamer MSCV 64bit](https://gstreamer.freedesktop.org/data/pkg/windows/1.22.0/msvc/gstreamer-1.0-devel-msvc-x86_64-1.22.0.msi) or [Latest Release](https://gstreamer.freedesktop.org/download/) and do a full install
2. Download [OpenCV 4.7.0](https://github.com/opencv/opencv/archive/4.7.0.zip) or [Latest Source Release](https://opencv.org/releases/)
3. Edit the `C:\tools\msys64\home\USER\.bash_profile` to add `PATH=/f/gstreamer/1.0/msvc_x86_64/bin:$PATH`
4. Open Msys2 CMD Window (MINGW64)
5. Extract source to `~/opencv-4.7.0`
6. `mkdir ~/opencv-4.7.0/build && cd ~/opencv-4.7.0/build`
7. `cmake-gui`
8. Where is the source code: `C:/Users/USER/git/opencv-4.7.0`
9. Where to build the binaries: `C:/Users/USER/git/opencv-4.7.0/build`
10. Click Configure and select MSYS2 Makefiles
11. Uncheck the following: `WITH_OBSENSOR`, `BUILD_SHARED_LIBS`, `BUILD_TESTS`, `BUILD_PERF_TESTS`, `BUILD_opencv_python_tests`, `INSTALL_TESTS`, `BUILD_ZLIB`,
12. Set `PYTHON3_PACKAGES_PATH` to `C:/tools/msys64/mingw64/lib/python3.10/site-packages`
13. Select Generate and close cmake-gui
14. run `mingw32-make install` 
15. Instructions based on [Compile OpenCV with Gstreamer in MinGW](https://medium.com/csmadeeasy/opencv-c-installation-on-windows-with-mingw-c0fc1499f39)

### Post Install - Binplace OpenCV binaries and OpenCV Python Module - Only if binaries are missing
1. Copy `C:\Users\cley\git\opencv-4.7.0\build\install\x64\mingw\bin` to `C:\tools\msys64\mingw64\bin`
2. Copy `C:\Users\cley\git\opencv-4.7.0\build\install\x64\mingw\lib` to `C:\tools\msys64\mingw64\lib`
3. Move `C:\tools\msys64\mingw64\lib\python3.11\site-packages\cv2` to `C:\tools\msys64\temp` if it exists
4. Copy `C:\Users\cley\git\opencv-4.7.0\build\lib\python3\cv2.cp311-mingw_x86_64.pyd` to `C:\tools\msys64\mingw64\lib\python3.11\site-packages\cv2`


