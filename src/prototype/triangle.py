import gi

gi.require_version("Gtk", "3.0")
from gi.repository import Gtk
import numpy as np
from OpenGL.GL import *
VERTEX_SOURCE = '''
#version 330
in vec2 position;
void main()
{
    gl_Position = vec4(position, 0.0, 1.0);
}
'''

FRAGMENT_SOURCE ='''
#version 330
out vec4 outColor;
void main()
{
    outColor = vec4(1.0, 1.0, 1.0, 1.0);
}'''

def on_realize(self, area):        
    # We need to make the context current if we want to
    # call GL API
    area.make_current()

def on_render(area, context):
    print("%s\n", glGetString(GL_VERSION))
    area.make_current()

    # Load Shaders, Create program, Setup Graphics
    vertexShader = glCreateShader(GL_VERTEX_SHADER)
    glShaderSource(vertexShader, VERTEX_SOURCE)
    glCompileShader(vertexShader)
    status = glGetShaderiv(vertexShader, GL_COMPILE_STATUS)
    print("Compile vertexShader status: " + str(status == GL_TRUE))

    pixelShader = glCreateShader(GL_FRAGMENT_SHADER)
    glShaderSource(pixelShader, FRAGMENT_SOURCE)
    glCompileShader(pixelShader)
    status = glGetShaderiv(pixelShader, GL_COMPILE_STATUS)
    print("Compile vertexShader status: " + str(status == GL_TRUE))

    shaderProgram = glCreateProgram()
    glAttachShader(shaderProgram, vertexShader)
    glAttachShader(shaderProgram, pixelShader)
    glLinkProgram(shaderProgram)
    glBindFragDataLocation(shaderProgram, 0, "outColor")
    positionHandle = glGetAttribLocation(shaderProgram, "position")

    w = area.get_allocated_width()
    h = area.get_allocated_height()
    glViewport(0, 0, w, h)

    # Setup Buffers
    vertices = np.array([
     0.0,  0.0, # Vertex 1 (X, Y)
     0.0, -0.0, # Vertex 2 (X, Y)
    -0.0, -0.0 # Vertex 3 (X, Y)
    ], dtype=np.float32) 
    vbo = glGenBuffers(1)
    glBindBuffer(GL_ARRAY_BUFFER, vbo)
    glBufferData(GL_ARRAY_BUFFER, len(vertices), vertices, GL_STATIC_DRAW)
    vao = glGenVertexArrays(1)

    # inside this function it's safe to use GL; the given
    # Gdk.GLContext has been made current to the drawable
    # surface used by the Gtk.GLArea and the viewport has
    # already been set to be the size of the allocation
    # we can start by clearing the buffer        
    # glClearColor(0, 1, 1, 0)
    # glClear(GL_COLOR_BUFFER_BIT)

    # Setup Texture
    tex = glGenTextures(1)
    glBindTexture(GL_TEXTURE_2D, tex)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_REPEAT)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_REPEAT)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)
    pixels = [
        0.0, 0.0, 0.0,   1.0, 1.0, 1.0,
        1.0, 1.0, 1.0,   0.0, 0.0, 0.0]

    glTexImage2D(GL_TEXTURE_2D, 0, GL_RGB, 2, 2, 0, GL_RGB, GL_FLOAT, pixels)
    glGenerateMipmap(GL_TEXTURE_2D)

    # draw your object
    glUseProgram(shaderProgram)
    posAttrib = glGetAttribLocation(shaderProgram, "position")
    glEnableVertexAttribArray(posAttrib)
    glBindVertexArray(vao)
    glDrawArrays(GL_TRIANGLES, 0, 3)

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