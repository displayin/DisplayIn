from util.resource import Resource as res
import ffmpeg

class VideoExporter:
    def __init__(self, window):
        self.window = window
        pass

    def exportVideo(recordedFps, videoFileName="temp.avi", audioFileName="temp.wav"):
        videoFile = ffmpeg.input(videoFileName , r=recordedFps)
        audioFile = ffmpeg.input(audioFileName)
        outFileName = res.saveFileDialog()
        if outFileName != None:
            ffmpeg.output(videoFile, audioFile, outFileName).run(
                overwrite_output=True)
        res.deleteFileIfExists(videoFileName)
        res.deleteFileIfExists(audioFileName)
        pass
