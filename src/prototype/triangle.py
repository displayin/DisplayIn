import gi

gi.require_version("Gtk", "3.0")
from gi.repository import Gtk
import numpy as np
from OpenGL.GL import *
from OpenGL.GL import shaders

FRAGMENT_SOURCE ='''
#version 330
in vec4 inputColor;
out vec4 outputColor;
void main(){
outputColor = vec4(1.0,0.0,0.0,1.0);//constant red. I know it's a poor shader
};'''

VERTEX_SOURCE = '''
#version 330
in vec4 position;
void main(){
gl_Position =  position;
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
    shader_prog = shaders.compileProgram(VERTEX_SHADER_PROG, FRAGMENT_SHADER_PROG)
    
    ############################################
    # Init Buffers
    ############################################
    # Create a new VAO (Vertex Array Object) and bind it
    vertex_array_object = glGenVertexArrays(1)
    glBindVertexArray(vertex_array_object)
    # Generate buffers to hold our vertices
    vertex_buffer = glGenBuffers(1)
    glBindBuffer(GL_ARRAY_BUFFER, vertex_buffer)
    # Get the position of the 'position' in parameter of our shader and bind it.
    position = glGetAttribLocation(shader_prog, 'position')
    glEnableVertexAttribArray(position)
    # Describe the position data layout in the buffer
    glVertexAttribPointer(position, 3, GL_FLOAT, False, 0, ctypes.c_void_p(0))
    # Send the data over to the buffer
    vertices = np.array([
        # Positions        
        1.0,  1.0, 0.0,   # Top Right       0
        1.0, -1.0, 0.0,   # Bottom Right    1
        -1.0, -1.0, 0.0,  # Bottom Left     2
        -1.0,  1.0, 0.0,  # Top Left        3
        1.0,  1.0, 0.0,   # Top Right       4
                            ], dtype=np.float32)
    
    size = sizeof(GLfloat) * len(vertices)
    glBufferData(GL_ARRAY_BUFFER, size, vertices, GL_STATIC_DRAW)

    ebo = glGenBuffers(1) # Generate EBO
    indices = np.array([
        0, 1, 3, # First Triangle
        1, 2, 3  # Second Triangle
    ])
    glBindBuffer(GL_ELEMENT_ARRAY_BUFFER, ebo) # Bind the indices for information about drawing sequence
    glBufferData(GL_ELEMENT_ARRAY_BUFFER, sizeof(GLint64) * len(indices), indices, GL_STATIC_DRAW)

    # Unbind the VAO first (Important)
    glBindVertexArray(0)
    # Unbind other stuff
    glDisableVertexAttribArray(position)

    ############################################
    # Render
    ############################################
    glBindBuffer(GL_ARRAY_BUFFER, 0)
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glUseProgram(shader_prog)
    glBindVertexArray(vertex_array_object)
    glDrawArrays(GL_TRIANGLES, 0, 3)
    glDrawArrays(GL_TRIANGLES, 2, 3)
    #glDrawElements(GL_TRIANGLES, 3, GL_UNSIGNED_INT, 0)
    glBindVertexArray(0)
    glUseProgram(0)

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