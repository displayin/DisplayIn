#
# Copyright (c) 2023 Tekst LLC.
#
# This file is part of DisplayIn 
# (see https://github.com/displayin).
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program. If not, see <http://www.gnu.org/licenses/>.#

# pyinstaller --onedir pyinstallerbug.py --splash "splash.png" --add-binary "C:\tools\msys64\mingw64\lib\gdk-pixbuf-2.0\2.10.0\loaders\libpixbufloader-png.dll;lib\gdk-pixbuf\loaders"
import gi
gi.require_version("Gtk", "3.0")
from gi.repository import Gtk, GdkPixbuf

import numpy as np

frame = np.array([[[0, 0, 0]]], dtype=np.uint8)
h, w, d = frame.shape
pixbuf = GdkPixbuf.Pixbuf.new_from_data(
    frame.tostring(), GdkPixbuf.Colorspace.RGB, False, 8, w, h, w*d)

print(pixbuf)

icon = Gtk.Image.new_from_icon_name("gtk-fullscreen", size=Gtk.IconSize.BUTTON)
print(icon)

win = Gtk.Window()
win.show_all()
Gtk.main()