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
                self.window.setDisplay(selected)
                self.window.settings.set('displayDevice', selected)
        except Exception as e:
            self.handleException(e)

    def onSelectAudioIn(self, combo):
        try:
            selected = combo.get_active()
            if selected is not None:
                model = combo.get_model()
                self.window.setAudioIn(model[selected][1], selected)
                self.window.settings.set('audioIn', selected)

        except Exception as e:
            self.handleException(e)

    def onSelectAudioOut(self, combo):
        try:
            selected = combo.get_active()
            if selected is not None:
                model = combo.get_model()
                self.window.setAudioOut(model[selected][1], selected)
                self.window.settings.set('audioOut', selected)

        except Exception as e:
            self.handleException(e)

    def onSelectResolution(self, combo):
        selected = combo.get_active()
        if selected is not None and selected != -1:
            model = combo.get_model()
            self.window.settings.set('resolution', model[selected][0])
            self.window.startVideo()
        pass

    def onSelectFps(self, combo):
        selected = combo.get_active()
        if selected is not None and selected != -1:
            model = combo.get_model()
            self.window.settings.set('fps', model[selected][1])
            self.window.startVideo()
        pass

    def onSettingsReset(self, widget, ev=None):
        self.window.stopVideo()
        self.window.stopAudio()
        self.window.initialize(True)
        self.window.startVideo()
        self.window.startAudio()
        pass

    def onSelectVolume(self, widget, ev=None):
        try:
            volume = widget.get_value()
            self.window.audioStream.setVolume(volume)
            self.window.settings.set('volume', volume)
        except Exception as e:
            self.handleException(e)


    def onHideToolBarOnStart(self, widget):
        pass

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

    def onDisplayHover(self, widget, event):

        allocation = widget.get_allocation()
        revealHeight = allocation.height - 5

        if event.y >= revealHeight:
            actionBar = self.getGtkObject("actionBar")
            actionBar.set_reveal_child(True)

        pass

    def onHideTaskbar(self, widget):
        actionBar = self.getGtkObject("actionBar")
        actionBar.set_reveal_child(False)

    def onFullscreen(self, widget):
        self.window.fullscreen()

    def onPreferences(self, widget):
        settingsWindow = self.getGtkObject('settings')
        settingsWindow.show_all()

    def onAbout(self, widget):
        aboutWindow = self.getGtkObject('about')
        aboutWindow.show()

    def onCloseHide(self, widget, ev):
        widget.hide()
        return True

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
