#!/bin/bash

# Clean Build Folders
[ -d "build" ] && rm -rf build/*
[ -d "dist" ] && rm -rf dist/*

# Run Pyinstaller
pyinstaller --noconsole --add-data="resource/ui/maingui.glade:resource/ui" --splash "resource/images/DisplayInSplash.png" --icon="resource/images/DisplayInIcon.ico" --onedir displayin.py