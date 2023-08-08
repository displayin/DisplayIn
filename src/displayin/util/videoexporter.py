from util.resource import Resource as res
from threading import Thread
import ffmpeg

class VideoExporter:
    def __init__(self, window):
        self.window = window
        pass

    def exportVideo(self, recordedFps, videoFileName="temp.avi", audioFileName="temp.wav"):
        videoFile = ffmpeg.input(videoFileName , r=recordedFps)
        audioFile = ffmpeg.input(audioFileName)
        outFileName = res.saveFileDialog()
        if outFileName != None:
            saveThread = Thread(target=self.ffmpegExport, args=(
                videoFileName, audioFileName, videoFile, audioFile, outFileName))
            saveThread.start()
        
        pass

    def ffmpegExport(self, videoFileName, audioFileName, videoFile, audioFile, outFileName):
        self.window.buttonRecord.set_sensitive(False)
        ffmpeg.output(videoFile, audioFile, outFileName).run(
            overwrite_output=True)
        
        res.deleteFileIfExists(videoFileName)
        res.deleteFileIfExists(audioFileName)
        self.window.buttonRecord.set_sensitive(True)
