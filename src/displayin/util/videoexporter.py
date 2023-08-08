from util.resource import Resource as res
from threading import Thread
import ffmpeg
import time
import os

import gi
gi.require_version("Gtk", "3.0")
from gi.repository import Gtk, GLib

class VideoExporter:
    def __init__(self, window):
        self.window = window
        self.running = False
        pass

    def exportVideo(self, recordedFps, videoFileName="temp.avi", audioFileName="temp.wav"):
        videoFile = ffmpeg.input(videoFileName , r=recordedFps)
        audioFile = ffmpeg.input(audioFileName)
        
        videoInfo = ffmpeg.probe(videoFileName)
        totalFrames = int(videoInfo['streams'][0]['nb_frames'])

        # Create Progress Window
        progressWindow = Gtk.Window(title="Exporting Video File...")
        progressWindow.set_border_width(10)
        vbox = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=6)
        progressWindow.add(vbox)
        progressBar = Gtk.ProgressBar()
        vbox.pack_start(progressBar, True, True, 0)
        progressWindow.show_all()

        outFileName = res.saveFileDialog()
        if outFileName != None:
            saveThread = Thread(target=self.ffmpegExport, args=(
                videoFileName, audioFileName, videoFile, audioFile, outFileName))
            saveThread.start()
            progressThread = Thread(target=self.displayProgress, args=(totalFrames, progressWindow, progressBar))
            progressThread.start()
        
        pass

    def ffmpegExport(self, videoFileName, audioFileName, videoFile, audioFile, outFileName):
        self.window.buttonRecord.set_sensitive(False)
        self.running = True
        (ffmpeg
            .output(videoFile, audioFile, outFileName)
            .global_args('-progress', 'progress.txt')
            .run(overwrite_output=True, capture_stdout=True, capture_stderr=True))
        
        res.deleteFileIfExists(videoFileName)
        res.deleteFileIfExists(audioFileName)
        self.running = False
        self.window.buttonRecord.set_sensitive(True)

    def displayProgress(self, totalFrames, progressWindow, progressBar):
        
        while self.running:
            time.sleep(0.1)
            if os.path.exists("progress.txt"):
                progressfile = open("progress.txt", "r")
                data = progressfile.read()
                progressfile.close()

        progressWindow.destroy()

        pass
