# Initial test of Video Capture
# See https://docs.opencv.org/3.4/dd/d43/tutorial_py_video_display.html
import numpy as np
import cv2 as cv
from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *
from threading import Thread

class VideoStream:
    def __init__(self):
        self.video_capture = cv.VideoCapture(0)
        ret, frame = self.video_capture.read()
        self.current_frame = frame
           
    # create thread for capturing images
    def start(self):
        Thread(target=self._update_frame, args=()).start()
   
    def _update_frame(self):
        while(True):
            ret, frame = self.video_capture.read()
            self.current_frame = frame
                   
    # get the current frame
    def get_current_frame(self):
        return self.current_frame

class Program:
 
    def __init__(self):
        self.video = VideoStream()
        self.video.start()
         
        self.x_axis = 0.0
        self.y_axis = 0.0
        self.z_axis = 0.0
     
    def _update_image(self):
        # get image from webcam 
        frame = self.video.get_current_frame()

        frame = cv.cvtColor(frame, cv.COLOR_BGR2RGB)
        h, w, d = frame.shape
         
        # apply texture
        glTexImage2D(GL_TEXTURE_2D, 0, GL_RGBA, w, h, 0, GL_RGBA, GL_UNSIGNED_BYTE, frame)
 
    def _draw_image(self, textureID):
        # draw image
        verts = ((1, 1), (1,-1), (-1,-1), (-1,1))
        texts = ((1, 0), (1, 1), (0, 1), (0, 0))
        surf = (0, 1, 2, 3)

        glEnable(GL_TEXTURE_2D)
        glBindTexture(GL_TEXTURE_2D, textureID)

        glBegin(GL_QUADS)
        for i in surf:
            glTexCoord2f(texts[i][0], texts[i][1])
            glVertex2f(0 + verts[i][0], 0 + verts[i][1])
        glEnd()
        
        glDisable(GL_TEXTURE_2D)
 
    def _init_gl(self, Width, Height):
        self.textID = glGenTextures(1)
        # initialize incl. texture
        glClearColor(0.0, 0.0, 0.0, 0.0)
        glClearDepth(1.0)
        gluPerspective(45, (640 / 480), 0.1, 50.0)
        glTranslatef(0.0, 0.0, -5)
        glPixelStorei(GL_UNPACK_ALIGNMENT, 1)
        glBindTexture(GL_TEXTURE_2D, self.textID)
        glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_NEAREST)
        glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_NEAREST)
        glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_CLAMP_TO_BORDER)
        glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_CLAMP_TO_BORDER)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_BASE_LEVEL, 0)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAX_LEVEL, 0)
 
    def _draw_scene(self):
        # update texture image
        self._update_image()
        
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        glLoadIdentity()
        self._draw_image(self.textID)
 
        glutSwapBuffers()
 
    def main(self):
        # setup and run OpenGL
        glutInit()
        glutInitDisplayMode(GLUT_RGBA | GLUT_DOUBLE | GLUT_DEPTH)
        glutInitWindowSize(640, 480)
        glutInitWindowPosition(0, 0)
        glutCreateWindow(b'OpenGL Render')
        glutDisplayFunc(self._draw_scene)
        glutIdleFunc(self._draw_scene)
        self._init_gl(640, 480)
        glutMainLoop()
 
# run instance of Lego Tracker 
program = Program()
program.main()