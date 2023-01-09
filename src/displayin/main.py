
from config.videostreamconfig import VideoStreamConfig
from config.audiostreamconfig import AudioStreamConfig
from engine.videostream import VideoStream
from engine.audiostream import AudioStream
from ui.mainwindow import MainWindow



if __name__ == '__main__':

    # videoConfig = VideoStreamConfig(0)
    # audioConfig = AudioStreamConfig(10, 15)

    # video = VideoStream(videoConfig)
    # audio = AudioStream(audioConfig)

    # video.start()
    # audio.start()

    ui = MainWindow()
    ui.show()
