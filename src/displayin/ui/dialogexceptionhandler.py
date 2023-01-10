import gi

gi.require_version("Gtk", "3.0")
from gi.repository import Gtk
from util.exceptionhandler import ExceptionHandler

class DialogExceptionHandler(ExceptionHandler):
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
        
        if len(ex.args) > 1:
            errorMessage += "\nError Code: " + str(ex.args[1])     
            
        dialog.format_secondary_text(errorMessage)
        dialog.run()

        dialog.destroy()
        pass