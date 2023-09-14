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

from ui.mainwindow import MainWindow
from ui.uihandler import UIHandler
from ui.dialogexceptionhandler import DialogExceptionHandler
from util.resource import Resource as res

if __name__ == '__main__':
    exHandler = DialogExceptionHandler()
    try:
        # Close Splash Window
        res.closeSpash()

        # Request Camera Authorization for MacOS
        res.macAuthorizeCamera()

        # Show Main Program Window
        ui = MainWindow(exHandler)
        uiHandler = UIHandler()
        uiHandler.setWindow(ui)
        ui.setUiHandler(uiHandler)
        ui.show()
    except Exception as e:
        exHandler.handle(e)
