import sys
from PyQt5.QtWidgets import QApplication, QMainWindow
from PyQt5.QtCore import Qt
import design
from random import randint

class MainWindow(QMainWindow):
    def __init__(self, screen_width, screen_height):
        super().__init__()

        # build ui
        self.ui = design.Ui_MainWindow()
        self.ui.setupUi(self)

        # resize the main window to a sensible value
        self.resize(screen_width / 2, screen_height / 2)

        # resize the graphics scene to match the window
        uv = self.ui.graphicsView
        uv.resize(screen_width, screen_height)

        # create a random initial state for the universe
        initial = [[(randint(0, 10) == 9) for i in range(uv.cols)] for j in range(uv.rows)]
        uv.initialize(initial)

        # start the animation directly
        uv.start()

    def resizeEvent(self, QResizeEvent):
        # resize the graphics scene to match the window
        self.ui.graphicsView.stop()
        self.ui.graphicsView.resize(screen_resolution.width(), screen_resolution.height())
        self.ui.graphicsView.start()

    def keyPressEvent(self, QKeyEvent):
        if QKeyEvent.key() == Qt.Key_F11:
            if self.windowState() == Qt.WindowFullScreen:
                self.showNormal()
            else:
                self.showFullScreen()
        

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



