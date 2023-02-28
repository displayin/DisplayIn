from util.exceptionhandler import ExceptionHandler
from util.logger import Logger
from ui.mainwindow import MainWindow

import gi
gi.require_version("Gtk", "3.0")
from gi.repository import Gdk

class UIHandler:
    def __init__(self) -> None:
        self.window: MainWindow = None
        self.exHandler: ExceptionHandler = None
        self.logger: Logger = None

    def setWindow(self, window: MainWindow) -> None:
        self.window: MainWindow = window
        self.exHandler: ExceptionHandler = self.window.exHandler
        self.logger: Logger = self.window.logger

    def handleException(self, e: Exception):
        if self.exHandler:
            self.exHandler.handle(e)

    def onSelectDisplay(self, combo):
        try:
            selected = combo.get_active()
            if selected is not None and selected != -1:
                self.window.selectedDisplay = selected
                self.window.startVideo()
                self.logger.log("Video Started!")
        except Exception as e:
            self.handleException(e)

    def onSelectAudioIn(self, combo):
        try:
            selected = combo.get_active()
            if selected is not None:
                model = combo.get_model()
                self.window.selectedAudioIn = model[selected][1]
                self.window.startAudio()
                self.logger.log("Audio Started!")
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

    def onDisplayResize(self, widget, allocation):
        try:
            if self.window is not None and self.window.videoStream is not None and self.window.videoStream.config is not None and self.window.glArea is None:
                # TODO create option to maintain aspect ratio
                self.window.videoStream.config.width = allocation.width
                self.window.videoStream.config.height = allocation.height
        except Exception as e:
            self.handleException(e)
    
    def onWindowKeyPress(self, widget, event):
        try:
            # check the event modifiers (can also use SHIFTMASK, etc)
            ctrl = (event.state & Gdk.ModifierType.CONTROL_MASK)

            # TODO: Have buttons for these
            if ctrl and event.keyval == Gdk.KEY_f:
                self.window.fullscreen()
            elif ctrl and event.keyval == Gdk.KEY_h:
                actionBar = self.getGtkObject("actionBar")
                actionBar.set_reveal_child(not actionBar.get_reveal_child())
        except Exception as e:
            self.handleException(e)

    def onWindowStateEvent(self, widget, ev):
        try:
            self.window.isFullscreen = bool(
                ev.new_window_state & Gdk.WindowState.FULLSCREEN)
        except Exception as e:
            self.handleException(e)
    
    def getGtkObject(self, objectId: str):
        return self.window.builder.get_object(objectId)

    def onExit(self, obj):
        try:
            self.window.exit()
        except Exception as e:
            self.handleException(e)
