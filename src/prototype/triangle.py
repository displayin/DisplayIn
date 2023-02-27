import gi

gi.require_version("Gtk", "3.0")
from gi.repository import Gtk

from OpenGL.GL import *

def on_realize(self, area):        
    # We need to make the context current if we want to
    # call GL API
    area.make_current()

def on_render(area, context):
    print("%s\n", glGetString(GL_VERSION))
    area.make_current()

    w = area.get_allocated_width()
    h = area.get_allocated_height()
    glViewport(0, 0, w, h)

    # inside this function it's safe to use GL; the given
    # Gdk.GLContext has been made current to the drawable
    # surface used by the Gtk.GLArea and the viewport has
    # already been set to be the size of the allocation
    # we can start by clearing the buffer        
    glClearColor(1, 1, 1, 0)
    glClear(GL_COLOR_BUFFER_BIT)

    # draw your object  
    glColor3f(0, 0, 0)           
    glBegin(GL_TRIANGLES)
    glVertex3f ( 0.0, 1.0, 0.0)
    glVertex3f (-1.0,-1.0, 0.0)
    glVertex3f ( 1.0,-1.0, 0.0)
    glEnd()

    # we completed our drawing; the draw commands will be
    # flushed at the end of the signal emission chain, and
    # the buffers will be drawn on the window
    return True

win = Gtk.Window()
area = Gtk.GLArea()
area.set_required_version(2, 1)
major, minor = area.get_required_version()
print("Version " + str(major) + "." + str(minor))
area.connect('render', on_render)
area.connect('realize', on_realize)
win.connect("destroy", Gtk.main_quit)
win.add(area)
win.show_all()
Gtk.main()