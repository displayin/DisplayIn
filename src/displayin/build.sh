#!/bin/bash
##
## Copyright (c) 2023 Tekst LLC.
##
## This file is part of DisplayIn 
## (see https://github.com/displayin).
##
## This program is free software: you can redistribute it and/or modify
## it under the terms of the GNU General Public License as published by
## the Free Software Foundation, either version 3 of the License, or
## (at your option) any later version.
##
## This program is distributed in the hope that it will be useful,
## but WITHOUT ANY WARRANTY; without even the implied warranty of
## MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
## GNU General Public License for more details.
##
## You should have received a copy of the GNU General Public License
## along with this program. If not, see <http://www.gnu.org/licenses/>.##


# Clean Build Folders
[ -d "build" ] && rm -rf build
[ -d "dist" ] && rm -rf dist
[ -f "displayin.spec" ] && rm displayin.spec

# Run Pyinstaller
pyinstaller --noconsole --add-data="resource/ui/maingui.glade:resource/ui" --add-data "resource/images:resource/images" --splash "resource/images/DisplayInSplash.png" --icon="resource/images/DisplayInIcon.ico" --hidden-import "OpenGL.platform.egl" --onedir displayin.py