from util.exceptionhandler import ExceptionHandler
from ui.mainwindow import MainWindow


class UIHandler:
    def __init__(self) -> None:
        self.window: None
        self.exHandler: None

    def setWindow(self, window: MainWindow) -> None:
        self.window: MainWindow = window
        self.exHandler: ExceptionHandler = self.window.exHandler

    def handleException(self, e: Exception):
        if self.exHandler:
            self.exHandler.handle(e)

    def onSelectDisplay(self, combo):
        try:
            selected = combo.get_active()
            if selected is not None:
                self.window.selectedDisplay = selected
                self.window.startVideo()
        except Exception as e:
            self.handleException(e)

    def onSelectAudioIn(self, combo):
        try:
            selected = combo.get_active()
            if selected is not None:
                model = combo.get_model()
                self.window.selectedAudioIn = model[selected][1]
                self.window.startAudio()
        except Exception as e:
            self.handleException(e)

    def onSelectAudioOut(self, combo):
        try:
            selected = combo.get_active()
            if selected is not None:
                model = combo.get_model()
                self.window.selectedAudioOut = model[selected][1]
                self.window.startAudio()
        except Exception as e:
            self.handleException(e)

    def onExit(self, obj):
        try:
            self.window.exit()
        except Exception as e:
            self.handleException(e)
