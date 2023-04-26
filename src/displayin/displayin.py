
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
