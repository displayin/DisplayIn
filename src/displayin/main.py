
from ui.mainwindow import MainWindow
from ui.uihandler import UIHandler
from ui.dialogexceptionhandler import DialogExceptionHandler

if __name__ == '__main__':
    exHandler = DialogExceptionHandler()
    try:
        # Show Main Program Window
        ui = MainWindow(exHandler)
        uiHandler = UIHandler()
        uiHandler.setWindow(ui)
        ui.setUiHandler(uiHandler)
        ui.show()
    except Exception as e:
        exHandler.handle(e)
