import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk
from OpenGL.GL import *
from OpenGL.GL import shaders
import numpy as np

FRAGMENT_SOURCE ='''
#version 330
in vec3 ourColor;
in vec2 TexCoord;
out vec4 color;
uniform sampler2D ourTexture;
void main(){
color = texture(ourTexture , TexCoord);
};'''

VERTEX_SOURCE = '''
#version 330
layout (location=0) in vec3 position;
layout (location=1) in vec3 color;
layout (location=2) in vec2 texCoord;
out vec3 ourColor;
out vec2 TexCoord;
void main()
{
gl_Position = vec4(position,1.0);
ourColor = color;
TexCoord= vec2(texCoord.x,1.0-texCoord.y);
}'''

recVertices = np.array([
    # Positions           Colors           Texture Coords
    0.5,  0.5, 0.0,   1.0, 0.0, 0.0,    1.0, 1.0,   # Top Right
    0.5, -0.5, 0.0,   0.0, 1.0, 0.0,    1.0, 0.0,   # Bottom Right
    -0.5, -0.5, 0.0,   0.0, 0.0, 1.0,   0.0, 0.0,   # Bottom Left
    -0.5,  0.5, 0.0,   1.0, 1.0, 0.0,   0.0, 1.0    # Top Left
                    ], dtype=np.float32)
indices = np.array([
    0, 1, 3, # First Triangle
    1, 2, 3  # Second Triangle
])

# Based on examples:
# https://stackoverflow.com/questions/42153819/how-to-load-and-display-an-image-in-opengl-es-3-0-using-c
# https://stackoverflow.com/questions/47565884/use-of-the-gtk-glarea-in-pygobject-gtk3
class OpenGLRenderer(Gtk.GLArea):
    def __init__(self):
        Gtk.GLArea.__init__(self)
        self.connect("realize", self.onRealize)
        self.connect("render", self.onRender)
        self.ctx = None
        self.frame = None
        self.area = None
        self.shaderProgram = None
        self.positionHandle = None
        self.textureId = None
        self.vao = None

    def onRealize(self, area):

        error = area.get_error()
        if error != None:
            print("your graphics card is probably too old : ", error)
        else:
            print(area, "realize... fine so far")

        self.ctx = self.get_context()
        self.ctx.make_current()

        print("OpenGL realized", self.ctx)

    def onRender(self, area, ctx):
        
        self.render(self.frame)
        return True

    def setupGraphics(self, width, height):

        if self.shaderProgram is None:
            # Load Shaders, Create program, Setup Graphics
            VERTEX_SHADER_PROG = shaders.compileShader(VERTEX_SOURCE, GL_VERTEX_SHADER)
            FRAGMENT_SHADER_PROG = shaders.compileShader(FRAGMENT_SOURCE, GL_FRAGMENT_SHADER)
            self.shaderProgram = shaders.compileProgram(VERTEX_SHADER_PROG, FRAGMENT_SHADER_PROG)
            self.positionHandle = glGetAttribLocation(self.shaderProgram, "position")

        glViewport(0, 0, width, height)
    
    def initBuffers(self):
        # Initialize an buffer to store all the verticles and transfer them to the GPU
        self.vao = glGenVertexArrays(1) # Generate VAO
        vbos = glGenBuffers(1) # Generate VBO
        ebo = glGenBuffers(1) # Generate EPBO
        glBindVertexArray(self.vao) # Bind the Vertex Array

        glBindBuffer(GL_ARRAY_BUFFER, vbos) # Bind verticles array for OpenGL to use
        glBufferData(GL_ARRAY_BUFFER, len(recVertices), recVertices, GL_STATIC_DRAW)

        glBindBuffer(GL_ELEMENT_ARRAY_BUFFER, ebo) # Bind the indices for information about drawing sequence
        glBufferData(GL_ELEMENT_ARRAY_BUFFER, len(indices), indices, GL_STATIC_DRAW)
        
        # 1. set the vertex attributes pointers
        # Position Attribute
        glVertexAttribPointer(0, 3, GL_FLOAT, GL_FALSE, 8 * sizeof(GLfloat), ctypes.c_void_p(0))
        glEnableVertexAttribArray(0)
        # Color Attribute
        glVertexAttribPointer(1, 3, GL_FLOAT, GL_FALSE, 8 * sizeof(GLfloat), ctypes.c_void_p(3 * sizeof(GLfloat)))
        glEnableVertexAttribArray(1)
        # Texture Coordinate Attribute
        glVertexAttribPointer(2, 2, GL_FLOAT, GL_FALSE, 8 * sizeof(GLfloat), ctypes.c_void_p(6 * sizeof(GLfloat)))
        glEnableVertexAttribArray(2)

        glBindVertexArray(0) # 3. Unbind VAO

        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        glUseProgram(self.shaderProgram)
        glBindVertexArray(self.vao)

        glBindVertexArray(0)
    
    def generateTexture(self, frame):
        # Update Frame
        self.frame = frame

        # If we have a frame to display
        if frame is not None:
            # extract array from Image
            h, w, d = frame.shape

            # Generate Texture
            self.textureId = glGenTextures(1)
            glBindTexture(GL_TEXTURE_2D, self.textureId) # Bind our 2D texture so that following set up will be applied

            # Set texture wrapping parameter
            glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_MIRRORED_REPEAT)
            glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_MIRRORED_REPEAT)

            # Set texture Filtering parameter
            glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_NEAREST)
            glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_NEAREST)

            glTexImage2D(GL_TEXTURE_2D, 0, GL_RGB , w , h, 0, GL_RGB, GL_UNSIGNED_BYTE, frame)
            glGenerateMipmap(GL_TEXTURE_2D)
            glBindTexture(GL_TEXTURE_2D,0) # Unbind 2D textures

    def render(self, frame):

        # Set OpenGL Render Context
        if self.ctx is not None and frame is not None:
            self.ctx.make_current()

            # extract array from Image
            h, w, d = frame.shape

            # Initialize Graphics
            self.setupGraphics(w, h)

            # Generate Texture
            self.generateTexture(frame)

            # Clear Screen
            glClearColor(0, 0, 1, 1)
            glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

            # Render Frame
            glUseProgram(self.shaderProgram)
            # checkGlError("glUseProgram")

            # glVertexAttribPointer(self.positionHandle, 2, GL_FLOAT, GL_FALSE, 0, recVertices)
            # checkGlError("glVertexAttribPointer")
            # glEnableVertexAttribArray(self.positionHandle)
            # checkGlError("glEnableVertexAttribArray")
            # glDrawArrays(GL_TRIANGLE_FAN, 0, 4)
            # checkGlError("glDrawArrays")
            glActiveTexture(GL_TEXTURE0)
            # checkGlError("glActiveTexture")
            glBindTexture(GL_TEXTURE_2D, self.textureId)
            #checkGlError("glBindTexture")
            mlocation = glGetUniformLocation(self.shaderProgram, "ourTexture")
            #checkGlError("glGetUniformLocation")
            glUniform1i(mlocation, 0)
            #checkGlError("glUniform1i")
            self.initBuffers()
            glBindVertexArray(self.vao)
            #checkGlError("glBindVertexArray")
            glDrawElements(GL_TRIANGLES, 6, GL_UNSIGNED_INT, 0)
            
            # Queue Draw
            glFlush()
            self.queue_draw()
