# pyinstaller --onedir pyinstallerbug.py
import gi
gi.require_version("Gtk", "3.0")
from gi.repository import Gtk, GdkPixbuf

pixbuf = GdkPixbuf.Colorspace.RGB

win = Gtk.Window()
win.show_all()
Gtk.main()