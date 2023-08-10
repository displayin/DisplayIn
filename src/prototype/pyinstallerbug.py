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