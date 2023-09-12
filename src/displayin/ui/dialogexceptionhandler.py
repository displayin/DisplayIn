import traceback
import gi

gi.require_version("Gtk", "3.0")
from gi.repository import Gtk
from util.exceptionhandler import ExceptionHandler
from util.logger import Logger

class DialogExceptionHandler(ExceptionHandler):

    def __init__(self, logger = None):
        self.logger = logger
        if self.logger == None:
            self.logger = Logger()

    def handle(self, ex: Exception):
        # TODO: Localize Message Dialog
        dialog = Gtk.MessageDialog(
            flags=0,
            message_type=Gtk.MessageType.ERROR,
            buttons=Gtk.ButtonsType.OK,
            text="Error",
        )

        # Print Error Message
        errorMessage = "We have encountered an error!"
        if len(ex.args) > 0:
            errorMessage = ex.args[0]
        
        if len(ex.args) > 1 and ex.args[1] is not None:
            errorMessage = errorMessage + "\nError Code: " + str(ex.args[1])
        
        # Log message
        errorMessageWithStackTrace = '[Exception] ' + errorMessage + traceback.format_exc()
        self.logger.log(errorMessageWithStackTrace)

        dialog.format_secondary_text(str(errorMessage))
        dialog.run()

        dialog.destroy()
        pass