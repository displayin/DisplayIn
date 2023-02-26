import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk
from OpenGL.GL import *
from OpenGL.GL import shaders
import numpy as np

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

class OpenGLRenderer(Gtk.GLArea):
    def __init__(self):
        Gtk.GLArea.__init__(self)
        self.connect("realize", self.onRealize)
        self.connect("render", self.onRender)
        self.ctx = None
        self.frame = None
        self.area = None

    def onRealize(self, area):

        error = area.get_error()
        if error != None:
            print("your graphics card is probably too old : ", error)
        else:
            print(area, "realize... fine so far")

        self.ctx = self.get_context()

        print("OpenGL realized", self.ctx)

    def onRender(self, area, ctx):
        
        self.updateFrame(self.frame)
        return True

    def updateFrame(self, frame):
        # Update Frame
        self.frame = frame

        # Set OpenGL Render Context
        if self.ctx is not None:
            self.ctx.make_current()

            # If we have a frame to display
            if frame is not None:
                # extract array from Image
                h, w, d = frame.shape

                if self.area is not None:
                    w = self.area.get_allocated_width()
                    h = self.area.get_allocated_height()

                glClearColor(0, 0, 0, 1)
                glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
                VERTEX_SHADER_PROG = shaders.compileShader(VERTEX_SOURCE, GL_VERTEX_SHADER)
                FRAGMENT_SHADER_PROG = shaders.compileShader(FRAGMENT_SOURCE, GL_FRAGMENT_SHADER)
                self.shader_prog = shaders.compileProgram(VERTEX_SHADER_PROG, FRAGMENT_SHADER_PROG)
                
                # Create a new VAO (Vertex Array Object) and bind it
                vertex_array_object = glGenVertexArrays(1)
                glBindVertexArray(vertex_array_object)
                # Generate buffers to hold our vertices
                vertex_buffer = glGenBuffers(1)
                glBindBuffer(GL_ARRAY_BUFFER, vertex_buffer)
                # Get the position of the 'position' in parameter of our shader and bind it.
                position = glGetAttribLocation(self.shader_prog, 'position')
                glEnableVertexAttribArray(position)
                # Describe the position data layout in the buffer
                glVertexAttribPointer(position, 3, GL_FLOAT, False, 0, ctypes.c_void_p(0))
                # Send the data over to the buffer
                vertices = np.array([-0.6, -0.6, 0.0,
                                    0.0, 0.6, 0.0,
                                    0.6, -0.6, 0.0,
                                    0.7, -0.1, 0.0,
                                    0.8, 0.1, 0.0,
                                    0.9, -0.1, 0.0
                                    ], dtype=np.float32)
                glBufferData(GL_ARRAY_BUFFER, 96, vertices, GL_STATIC_DRAW)
                # Unbind the VAO first (Important)
                glBindVertexArray(0)
                # Unbind other stuff
                glDisableVertexAttribArray(position)

                glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
                glUseProgram(self.shader_prog)
                glBindVertexArray(vertex_array_object)
                glDrawArrays(GL_TRIANGLES, 0, 3)
                glDrawArrays(GL_TRIANGLES, 4, 3)

                glBindVertexArray(0)
                glUseProgram(0)

                return True

                

                # Initialize
                textureId = glGenTextures(1)
                glBindTexture(GL_TEXTURE_2D, textureId)
                glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_NEAREST)
                glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_NEAREST)
                glTexImage2D(GL_TEXTURE_2D, 0, GL_RGB, w, h, 0, GL_RGB, GL_UNSIGNED_BYTE, None)
                glBindTexture(GL_TEXTURE_2D, 0)
                glFinish()

                # Setup Viewport
                glViewport(0, 0, w, h)
                glMatrixMode(GL_PROJECTION)
                glLoadIdentity()
                glOrtho(0, w, 0, h, 0, 1)
                glMatrixMode(GL_MODELVIEW)
                glLoadIdentity()

                # Clear Screen
                glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
                glClearColor(0.0, 0.0, 0.0, 1.0)
                glLoadIdentity()

                glBindTexture(GL_TEXTURE_2D, textureId)
                glTexSubImage2D(GL_TEXTURE_2D, 0, 0, 0, w, h,  GL_RGB, GL_UNSIGNED_BYTE, frame)

                # Draw textured Quads
                self.drawQuad(w, h)

        pass

    def drawQuad(self, width, height):
        glBegin(GL_QUADS)
        glTexCoord2f(0.0, 1.0)
        glVertex3f(0, 0, 0.0)
        glTexCoord2f(1.0, 1.0)
        glVertex3f(width, 0.0, 0.0)
        glTexCoord2f(1.0, 0.0)
        glVertex3f(width, height,  0.0)
        glTexCoord2f(0.0, 0.0)
        glVertex3f(0,  height,  0.0)
        glEnd

        glFlush()