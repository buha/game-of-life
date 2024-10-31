import sys
from PyQt5.QtWidgets import QApplication, QMainWindow
from PyQt5.QtCore import Qt, QSize
import design
from random import randint

class MainWindow(QMainWindow):
    def __init__(self, screen_width, screen_height, c1, c2):
        super().__init__()

        # build ui
        self.ui = design.Ui_MainWindow()
        self.ui.setupUi(self)

        # resize the main window to a sensible value
        self.resize(QSize(int(screen_width / 2), int(screen_height / 2)))

        # resize the graphics scene to match the window
        uv = self.ui.graphicsView
        uv.resize(screen_width, screen_height)

        # create a random initial state for the universe
        initial = [[(randint(0, 10) == 9) for i in range(uv.cols)] for j in range(uv.rows)]
        uv.initialize(initial, c1, c2)

        # start the animation directly
        uv.start()

    def resizeEvent(self, QResizeEvent):
        # resize the graphics scene to match the window
        self.ui.graphicsView.resize(screen_resolution.width(), screen_resolution.height())

    def keyPressEvent(self, QKeyEvent):
        if QKeyEvent.key() == Qt.Key_F11:
            if self.windowState() == Qt.WindowFullScreen:
                self.showNormal()
            else:
                self.showFullScreen()

if __name__ == '__main__':
    c1 = 2
    c2 = 3
    try:
        c1 = int(sys.argv[1])
        if not (c1 > 0 and c1 < 10):
            raise ValueError
        c2 = int(sys.argv[2])
        if not (c2 > 0 and c2 < 10):
            raise ValueError
    except IndexError:
        pass
    except ValueError:
        print("c1 and c2 must be positive integers between 1 and 9\ngame-of-life [c1 c2]")
        sys.exit(0)

    # set up graphics
    app = QApplication(sys.argv)

    # get screen resolution and create the main window
    screen_resolution = app.desktop().screenGeometry()
    main = MainWindow(screen_resolution.width(), screen_resolution.height(), c1, c2)

    # draw, launch qt app
    main.show()
    s = app.exec_()

    # finish properly
    sys.exit(s)



