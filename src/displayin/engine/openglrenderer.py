import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk
from OpenGL.GL import *
import numpy as np

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

FRAGMENT_SOURCE ='''
#version 330
in vec3 ourColor;
in vec2 TexCoord;
out vec4 color;
uniform sampler2D ourTexture;
void main(){
color = texture(ourTexture, TexCoord);
};'''

recVertices = np.array([
    # Positions           Colors           Texture Coords
    1.0,  1.0, 0.0,   1.0, 0.0, 0.0,    1.0, 1.0,   # Top Right    0
    1.0, -1.0, 0.0,   0.0, 1.0, 0.0,    1.0, 0.0,   # Bottom Right 1
    -1.0, -1.0, 0.0,   0.0, 0.0, 1.0,   0.0, 0.0,   # Bottom Left  2
    -1.0,  1.0, 0.0,   1.0, 1.0, 0.0,   0.0, 1.0,   # Top Left     3
    1.0,  1.0, 0.0,   1.0, 0.0, 0.0,    1.0, 1.0,   # Top Right    4
], dtype=np.float32)

def checkGlError(op: str):
    error = glGetError()
    if error is not None and error != 0:
        print("after %s() glError (0x%x)", op, error)

# Based on examples:
# https://stackoverflow.com/questions/42153819/how-to-load-and-display-an-image-in-opengl-es-3-0-using-c
# https://stackoverflow.com/questions/47565884/use-of-the-gtk-glarea-in-pygobject-gtk3
class OpenGLRenderer(Gtk.GLArea):
    def __init__(self):
        Gtk.GLArea.__init__(self)
        self.connect("realize", self.onRealize)
        self.connect("render", self.onRender)
        self.ctx = None
        self.frame = self.createBlankScreenFrame()
        self.area = None
        self.shaderProgram = None
        self.positionHandle = None
        self.textureId = None
        self.vao = None
        self.vbos = None
        self.version = None

    def getVersion(self):
        major = glGetIntegerv(GL_MAJOR_VERSION)
        minor = glGetIntegerv(GL_MINOR_VERSION)
        version = glGetString(GL_VERSION)

        return major, minor, version
    
    def createBlankScreenFrame(self):
        frame = np.array([[[0, 0, 0]] * 640] * 480, dtype=np.uint8)
        return frame

    def onRealize(self, area):

        error = area.get_error()
        if error != None:
            print("your graphics card is probably too old : ", error)
        else:
            print(area, "realize... fine so far")

        self.ctx = self.get_context()
        self.ctx.make_current()

        major, minor, self.version = self.getVersion()
        print("OpenGL realized", self.ctx)
        print("%s\n", self.version)

    def onRender(self, area, ctx):
        
        self.render(self.frame)
        return True

    def setupGraphics(self):

        if self.shaderProgram is None:
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

            self.shaderProgram = glCreateProgram()
            glAttachShader(self.shaderProgram, vertexShader)
            glAttachShader(self.shaderProgram, pixelShader)
            glLinkProgram(self.shaderProgram)
            glBindFragDataLocation(self.shaderProgram, 0, "color")
            self.positionHandle = glGetAttribLocation(self.shaderProgram, "position")

            # Initalize Vertex Buffers
            self.initBuffers()
    
    def initBuffers(self):
        # Initialize an buffer to store all the verticles and transfer them to the GPU
        self.vao = glGenVertexArrays(1) # Generate VAO
        self.vbos = glGenBuffers(1) # Generate VBO
        glBindVertexArray(self.vao) # Bind the Vertex Array

        glBindBuffer(GL_ARRAY_BUFFER, self.vbos) # Bind verticles array for OpenGL to use
        glBufferData(GL_ARRAY_BUFFER, sizeof(GLfloat) * len(recVertices), recVertices, GL_STATIC_DRAW)
        
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
    
    def generateTexture(self, frame):
        # Update Frame
        self.frame = frame

        # Delete previous textures to avoid memory leak
        if self.textureId is not None:
            glDeleteTextures(1, [self.textureId])

        # If we have a frame to display
        if frame is not None:
            # extract array from Image
            h, w, d = frame.shape

            # Frame is a 3 dimentional array where shape eg. (1920, 1080, 3)
            # Where it is w, h, and 3 values for color
            # https://www.educba.com/numpy-flatten/
            pixels = frame.flatten(order = 'C')

            # Generate Texture
            self.textureId = glGenTextures(1)
            glBindTexture(GL_TEXTURE_2D, self.textureId) # Bind our 2D texture so that following set up will be applied

            # Set texture wrapping parameter
            glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_CLAMP_TO_EDGE)
            glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_CLAMP_TO_EDGE)

            # Set texture Filtering parameter
            glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR)
            glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)

            glTexImage2D(GL_TEXTURE_2D, 0, GL_RGB, w, h, 0, GL_RGB, GL_UNSIGNED_BYTE, pixels)
            glGenerateMipmap(GL_TEXTURE_2D)
            glBindTexture(GL_TEXTURE_2D, 0) # Unbind 2D textures

    def render(self, frame):

        # Set OpenGL Render Context
        if self.ctx is not None and frame is not None:
            self.ctx.make_current()

            # Initialize Graphics
            self.setupGraphics()

            # Generate Texture
            self.generateTexture(frame)

            # Clear Screen
            glClearColor(0, 0, 1, 1)
            glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

            # Use Shader Program, Bind Vertex Array and Texture
            glUseProgram(self.shaderProgram)
            checkGlError("glUseProgram")
            glActiveTexture(GL_TEXTURE0)
            checkGlError("glActiveTexture")
            glBindTexture(GL_TEXTURE_2D, self.textureId)
            checkGlError("glBindTexture")
            mlocation = glGetUniformLocation(self.shaderProgram, "ourTexture")
            checkGlError("glGetUniformLocation")
            glUniform1i(mlocation, 0)
            checkGlError("glUniform1i")
            glBindVertexArray(self.vao)
            checkGlError("glBindVertexArray")

            # Render Frame
            glDrawArrays(GL_TRIANGLES, 0, 3)
            glDrawArrays(GL_TRIANGLES, 2, 3)
            
            # Queue Draw
            glFlush()
            self.queue_draw()
