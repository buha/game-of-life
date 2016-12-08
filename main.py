import sys
from PyQt5.QtWidgets import QApplication, QMainWindow
# from PyQt5.QtCore import (QThread, QSize, pyqtSignal, pyqtSlot)
import design

class MainWindow(QMainWindow):
    def __init__(self, screen_width, screen_height):
        super().__init__()

        # build ui
        self.ui = design.Ui_MainWindow()
        self.ui.setupUi(self)

        self.resize(screen_width / 2, screen_height / 2)

        # create the universe
        self.ui.graphicsView.start(screen_width, screen_height)

if __name__ == '__main__':
    # set up graphics
    app = QApplication(sys.argv)

    # get screen resolution and create the main window
    screen_resolution = app.desktop().screenGeometry()
    main = MainWindow(screen_resolution.width(), screen_resolution.height())

    # draw
    main.show()
    s = app.exec_()

    # finish properly
    sys.exit(s)


