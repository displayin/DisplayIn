import gi

gi.require_version("Gtk", "3.0")
from gi.repository import Gtk
import numpy as np
from OpenGL.GL import *
from OpenGL.GL import shaders

FRAGMENT_SOURCE ='''
#version 330
in vec3 Color;
in vec2 Texcoord;
out vec4 outColor;
uniform sampler2D imageTexture;
void main()
{
    outColor = texture(imageTexture, Texcoord);
}'''

VERTEX_SOURCE = '''
#version 330
layout (location=0) in vec3 position;
layout (location=1) in vec3 color;
layout (location=2) in vec2 texcoord;
out vec3 Color;
out vec2 Texcoord;
void main()
{
    Color = color;
    Texcoord = texcoord;
    gl_Position = vec4(position, 1.0);
}'''

def on_realize(self, area):        
    # We need to make the context current if we want to
    # call GL API
    area.make_current()

def on_render(area, context):
    print("%s\n", glGetString(GL_VERSION))
    area.make_current()

    ############################################
    # Init Shaders
    ############################################
    glClearColor(0, 0, 0, 1)
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    VERTEX_SHADER_PROG = shaders.compileShader(VERTEX_SOURCE, GL_VERTEX_SHADER)
    FRAGMENT_SHADER_PROG = shaders.compileShader(FRAGMENT_SOURCE, GL_FRAGMENT_SHADER)
    shaderProgram = shaders.compileProgram(VERTEX_SHADER_PROG, FRAGMENT_SHADER_PROG)
    
    ############################################
    # Init Buffers
    ############################################
    # Create a new VAO (Vertex Array Object) and bind it
    vao = glGenVertexArrays(1)
    glBindVertexArray(vao)
    # Generate buffers to hold our vertices
    vertex_buffer = glGenBuffers(1)
    glBindBuffer(GL_ARRAY_BUFFER, vertex_buffer)
    # Send the data over to the buffer
    vertices = np.array([
        # Positions      Color           Texchords 
        1.0,  1.0, 0.0,  0.0, 1.0, 0.0,  1.0, 0.0, # Top Right       0
        1.0, -1.0, 0.0,  0.0, 0.0, 1.0,  1.0, 1.0, # Bottom Right    1
        -1.0, -1.0, 0.0, 1.0, 1.0, 1.0,  0.0, 1.0, # Bottom Left     2
        -1.0,  1.0, 0.0, 1.0, 0.0, 0.0,  0.0, 0.0, # Top Left        3
        1.0,  1.0, 0.0,  0.0, 1.0, 0.0,  1.0, 0.0, # Top Right       4
    ], dtype=np.float32)
    
    size = sizeof(GLfloat) * len(vertices)
    glBufferData(GL_ARRAY_BUFFER, size, vertices, GL_STATIC_DRAW)

    # Specify the layout of the vertex data
    posAttrib = glGetAttribLocation(shaderProgram, "position")
    glEnableVertexAttribArray(posAttrib)
    glVertexAttribPointer(posAttrib, 3, GL_FLOAT, GL_FALSE, 8 * sizeof(GLfloat), ctypes.c_void_p(0))

    colAttrib = glGetAttribLocation(shaderProgram, "color")
    glEnableVertexAttribArray(colAttrib)
    glVertexAttribPointer(colAttrib, 3, GL_FLOAT, GL_FALSE, 8 * sizeof(GLfloat), ctypes.c_void_p(3 * sizeof(GLfloat)))

    texAttrib = glGetAttribLocation(shaderProgram, "texcoord")
    glEnableVertexAttribArray(texAttrib)
    glVertexAttribPointer(texAttrib, 2, GL_FLOAT, GL_FALSE, 8 * sizeof(GLfloat), ctypes.c_void_p(6 * sizeof(GLfloat)))

    # Unbind the VAO first (Important)
    glBindVertexArray(0)

    ############################################
    # Render
    ############################################
    glBindBuffer(GL_ARRAY_BUFFER, 0)
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glUseProgram(shaderProgram)
    glBindVertexArray(vao)

    # Load Textures
    width = 2
    height = 2
    textureId = glGenTextures(1)
    glActiveTexture(GL_TEXTURE0)
    glBindTexture(GL_TEXTURE_2D, textureId)

    # Black/white checkerboard
    pixels = [
        0,   0,   0,     255, 255, 255,
        255, 255, 255,   0,   0,   0
    ]

    glTexImage2D(GL_TEXTURE_2D, 0, GL_RGB, width, height, 0, GL_RGB, GL_UNSIGNED_BYTE, pixels)
    glUniform1i(glGetUniformLocation(shaderProgram, "imageTexture"), 0)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_CLAMP_TO_EDGE)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_CLAMP_TO_EDGE)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)

    glDrawArrays(GL_TRIANGLES, 0, 3)
    glDrawArrays(GL_TRIANGLES, 2, 3)
    glBindVertexArray(0)
    glUseProgram(0)

    # we completed our drawing; the draw commands will be
    # flushed at the end of the signal emission chain, and
    # the buffers will be drawn on the window
    return True

win = Gtk.Window()
area = Gtk.GLArea()
#area.set_required_version(2, 1)
#major, minor = area.get_required_version()
#print("Version " + str(major) + "." + str(minor))
area.connect('render', on_render)
area.connect('realize', on_realize)
win.connect("destroy", Gtk.main_quit)
win.add(area)
win.show_all()
Gtk.main()