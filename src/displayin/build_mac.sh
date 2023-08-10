#!/bin/bash

# Clean Build Folders
[ -d "build" ] && rm -rf build
[ -d "dist" ] && rm -rf dist
[ -f "displayin.spec" ] && rm displayin.spec

# Run Pyinstaller
pyinstaller --noconsole --add-data="resource/ui/maingui.glade:resource/ui" --icon="resource/images/DisplayInIcon.ico" --onedir displayin.py

# Patch Info.plist - Needed for security to tell the OS that we need camera access otherwise it will crash
plistPatch="	<key>NSCameraUsageDescription</key>\n	<string>DisplayIn uses Cameras</string>\n</dict>"
dictString="</dict>"
sed -i '' "s|$dictString|$plistPatch|gi" "dist/displayin.app/Contents/Info.plist"
echo "Patched NSCameraUsageDescription into Info.plist"

# Rename app
mv dist/displayin.app dist/DisplayIn.app