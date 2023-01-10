
from ui.mainwindow import MainWindow
from ui.dialogexceptionhandler import DialogExceptionHandler

if __name__ == '__main__':
    exHandler = DialogExceptionHandler()
    try:
        # Show Main Program Wino
        ui = MainWindow(exHandler)
        ui.show()
    except Exception as e:
        exHandler.handle(e)
