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

        progressWindow = Gtk.Window(title="Exporting Video File...")
        progressWindow.set_border_width(10)
        progressWindow.set_deletable(False)
        vbox = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=6)
        progressWindow.add(vbox)
        progressBar = Gtk.ProgressBar()
        vbox.pack_start(progressBar, True, True, 0)

        self.progressWindow = progressWindow
        self.progressBar = progressBar
        self.logger = self.window.logger
        pass

    def exportVideo(self, recordedFps, videoFileName="temp.avi", audioFileName="temp.wav"):
        videoFile = ffmpeg.input(videoFileName , r=recordedFps)
        audioFile = ffmpeg.input(audioFileName)
        
        videoInfo = ffmpeg.probe(videoFileName)
        totalFrames = int(videoInfo['streams'][0]['nb_frames'])

        # Create Progress Window
        progressWindow = self.progressWindow
        progressBar = self.progressBar
        progressWindow.show_all()

        outFileName = res.saveFileDialog(
            res.getRecordingFileName(), self.window.videoDir)
        if outFileName != None:

            # FFmpeg video saving thread
            saveThread = Thread(target=self.ffmpegExport, args=(
                videoFileName, audioFileName, videoFile, audioFile, outFileName))
            saveThread.start()

            # Progress bar thread
            progressThread = Thread(target=self.displayProgress, args=(totalFrames, progressWindow, progressBar))
            progressThread.start()
        
        pass

    def ffmpegExport(self, videoFileName, audioFileName, videoFile, audioFile, outFileName):
        self.window.buttonRecord.set_sensitive(False)
        self.running = True

        overlayFileName = "DisplayInLogoWatermark.png"
        overlayFile = ffmpeg.input(os.path.join(
            'resource', 'images', overlayFileName))
        (ffmpeg
            .output(videoFile, audioFile, overlayFile, outFileName)
            .global_args('-filter_complex', 'overlay=30:30', '-progress', 'progress.txt', '-async', '1')
            .run(overwrite_output=True, capture_stdout=True, capture_stderr=True))
        self.logger.log("Saved recording to " + outFileName)

        res.deleteFileIfExists(videoFileName)
        self.logger.log("Deleted " + videoFileName)
        res.deleteFileIfExists(audioFileName)
        self.logger.log("Deleted " + audioFileName)
        self.running = False
        self.window.buttonRecord.set_sensitive(True)

    def displayProgress(self, totalFrames, progressWindow, progressBar):
        
        while self.running:
            time.sleep(0.1)
            if os.path.exists("progress.txt"):

                # Read current progress
                progressfile = open("progress.txt", "r")
                data = progressfile.read()
                progressfile.close()

                # Parse out current frame
                lines = data.splitlines()
                indicies = reversed(range(len(lines) - 1))
                for i in indicies:
                    currentLine = lines[i]
                    if currentLine.startswith("frame="):
                        frame = int(currentLine.partition('=')[-1])
                        progressPercent = frame / totalFrames
                        progressBar.set_fraction(progressPercent)
                        break

        progressWindow.hide()

        pass
