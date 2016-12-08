from PyQt5.QtWidgets import QGraphicsView, QGraphicsScene, QGraphicsRectItem
from PyQt5.QtCore import Qt, QTimer, QPointF, QLineF, QRectF
from PyQt5.QtGui import QBrush, QPen, QColor
from random import randint
from universe import Universe

class constants():
    CellToScreenRatio = 0.001
    AtomicTick = 0.2
    background = QColor(60, 60, 60)
    grid = QColor(20, 20, 20)
    cell = QColor(84, 158, 39)

class UniverseView(QGraphicsView):
    def __init__(self, parent=None):
        super().__init__(parent)

        # visuals
        self.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)

        # set up the graphics
        self.scene = QGraphicsScene()
        self.setScene(self.scene)

        # set up time
        self.timer = QTimer()
        self.timer.timeout.connect(self.rePaint)

    def start(self, wscene, hscene):
        # set a sensible value for the cell size relative to screen size
        self.cell_size = int(wscene * constants.CellToScreenRatio) # in pixels
        if self.cell_size < 10:
            self.cell_size = 10

        # screen size is most certainly not a multiple of our cell size, so cut the extra
        wscene = int(self.parent().parent().width() / self.cell_size) * self.cell_size
        hscene = int(self.parent().parent().height() / self.cell_size) * self.cell_size

        # set the scene size
        self.scene.setSceneRect(QRectF(0, 0, wscene, hscene))

        # compute the number of rows/columns that are needed to fit items of cellsize into the scene
        self.rows = int(self.scene.height() / self.cell_size)
        self.cols = int(self.scene.width() / self.cell_size)

        # create a random initial state for the universe
        initial = [[(randint(0, 10) == 9) for i in range(self.cols)] for j in range(self.rows)]
        '''initial = [[False for i in range(self.cols)] for j in range(self.rows)]
        initial[0][0] = True
        initial[0][1] = True
        initial[1][2] = True
        initial[2][2] = True
        initial[3][2] = True
        '''

        # create the universe
        self.universe = Universe(initial)

        # the fun begins here
        self.timer.start(constants.AtomicTick * 1000)

    def stop(self):
        self.timer.stop()

    def drawCell(self, x, y):
        item = QGraphicsRectItem(x * self.cell_size,
                                 y * self.cell_size,
                                 self.cell_size,
                                 self.cell_size)
        item.setBrush(QBrush(constants.cell))
        item.setPen(constants.grid)
        self.scene.addItem(item)

    def draw(self, state):
        '''
        Draw the scene.
        :param state: 2D list of booleans
        '''
        for rowi, row in enumerate(state):
            for celli, cell in enumerate(row):
                if cell:
                    self.drawCell(celli, rowi)

    def rePaint(self):
        print("Drawing Universe of age {}".format(self.universe._age))

        # delete everything on the canvas
        self.scene.clear()

        # draw the background
        self.scene.setBackgroundBrush(constants.background)

        # repaint grid
        for row in range(self.rows - 1):
            line = self.scene.addLine(0, (row + 1) * self.cell_size, self.scene.width(), (row + 1) * self.cell_size)
            line.setPen(QPen(QBrush(constants.grid), 1))
        for col in range(self.cols - 1):
            line = self.scene.addLine((col + 1) * self.cell_size, 0, (col + 1) * self.cell_size, self.scene.height())
            line.setPen(QPen(QBrush(constants.grid), 1))

        # draw the universe
        state = self.universe.state()
        self.draw(state)

        # evolve
        self.universe.evolve()

    def keyPressEvent(self, QKeyEvent):
        # delete selected items when pressing the keyboard's delete key
        if QKeyEvent.key() == Qt.Key_Space:
            if self.timer.isActive():
                self.stop()
            else:
                self.timer.start(constants.AtomicTick * 1000)