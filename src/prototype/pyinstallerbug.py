# pyinstaller --onedir pyinstallerbug.py
import gi
gi.require_version("Gtk", "3.0")
from gi.repository import Gtk, GdkPixbuf

if False:
    h, w, d = frame.shape
    pixbuf = GdkPixbuf.Pixbuf.new_from_data(
        frame.tostring(), GdkPixbuf.Colorspace.RGB, False, 8, w, h, w*d)

win = Gtk.Window()
win.show_all()
Gtk.main()