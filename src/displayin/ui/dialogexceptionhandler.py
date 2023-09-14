#
# Copyright (c) 2023 Tekst LLC.
#
# This file is part of DisplayIn 
# (see https://github.com/displayin).
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program. If not, see <http://www.gnu.org/licenses/>.#
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
        errorMessage = self.getErrorMessage(ex)
        
        # Log message
        self.logErrorMessage(errorMessage)

        dialog.format_secondary_text(str(errorMessage))
        dialog.run()

        dialog.destroy()
        pass

    def getErrorMessage(self, ex: Exception):
        errorMessage = "We have encountered an error!"
        if len(ex.args) > 0:
            errorMessage = ex.args[0]

        if len(ex.args) > 1 and ex.args[1] is not None:
            errorMessage = errorMessage + "\nError Code: " + str(ex.args[1])

        return errorMessage
    

    def logErrorMessage(self, errorMessage):
        # Log message
        errorMessageWithStackTrace = '[Exception] ' + \
            errorMessage + traceback.format_exc()
        self.logger.log(errorMessageWithStackTrace)

    def logException(self, ex):
        # Print Error Message
        errorMessage = self.getErrorMessage(ex)

        # Log message
        self.logErrorMessage(errorMessage)
