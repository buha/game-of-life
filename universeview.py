from PyQt5.QtWidgets import QGraphicsView, QGraphicsScene, QGraphicsRectItem
from PyQt5.QtCore import Qt, QTimer, QPointF, QLineF, QRectF
from PyQt5.QtGui import QBrush, QPen, QColor
from random import randint
from universe import Universe
from time import perf_counter

class constants():
    CellToScreenRatio = 0.01
    AtomicTick = 0.01
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
        self._scene = QGraphicsScene()
        self.setScene(self._scene)

        # set up time
        self._timer = QTimer()
        self._timer.timeout.connect(self.timeTick)

        # defaults
        self._showStatus = False
        self._showGrid = False
        self._mousePosition = (0,0)

    def resize(self, wscene, hscene):
        # set a sensible value for the cell size relative to screen size
        self.cell_size = int(wscene * constants.CellToScreenRatio) # in pixels
        if self.cell_size < 2:
            self.cell_size = 2

        # screen size is most certainly not a multiple of our cell size, so cut the extra
        wscene = int(self.parent().parent().width() / self.cell_size) * self.cell_size
        hscene = int(self.parent().parent().height() / self.cell_size) * self.cell_size

        # set the scene size
        self._scene.setSceneRect(QRectF(0, 0, wscene, hscene))

        # compute the number of rows/columns that are needed to fit items of cellsize into the scene
        self.rows = int(self._scene.height() / self.cell_size)
        self.cols = int(self._scene.width() / self.cell_size)

        # create a random initial state for the universe
        initial = [[(randint(0, 10) == 9) for i in range(self.cols)] for j in range(self.rows)]

        # create the universe
        self.universe = Universe(initial)

    def start(self):
        self._timer.start(constants.AtomicTick * 1000)
        self.frame_timestamps = []

    def stop(self):
        self._timer.stop()

    def drawCell(self, x, y):
        item = QGraphicsRectItem(x * self.cell_size,
                                 y * self.cell_size,
                                 self.cell_size,
                                 self.cell_size)
        item.setBrush(QBrush(constants.cell))
        item.setPen(constants.grid)
        self._scene.addItem(item)

    def draw(self, state):
        '''
        Draw the scene.
        :param state: 2D list of booleans
        '''
        for rowi, row in enumerate(state):
            for celli, cell in enumerate(row):
                if cell:
                    self.drawCell(celli, rowi)

    def status(self):
        value = self._scene.addText('FPS: {:.2f}'.format(self._FPS))
        value.setDefaultTextColor(Qt.white)
        value.setPos(0, 0)

        age = self._scene.addText('Universe age: {}'.format(self.universe._age))
        age.setDefaultTextColor(Qt.white)
        age.setPos(0, 15)

        age = self._scene.addText('Mouse at x {}, y {}'.format(self._mousePosition[0], self._mousePosition[1]))
        age.setDefaultTextColor(Qt.white)
        age.setPos(0, 30)

    def drawGrid(self):
        for row in range(self.rows - 1):
            line = self._scene.addLine(0, (row + 1) * self.cell_size, self._scene.width(), (row + 1) * self.cell_size)
            line.setPen(QPen(QBrush(constants.grid), 1))
        for col in range(self.cols - 1):
            line = self._scene.addLine((col + 1) * self.cell_size, 0, (col + 1) * self.cell_size, self._scene.height())
            line.setPen(QPen(QBrush(constants.grid), 1))

    def reDraw(self):
        # delete everything on the canvas
        self._scene.clear()

        # draw the background
        self._scene.setBackgroundBrush(constants.background)

        # grid
        if self._showGrid:
            self.drawGrid()

        # draw the universe
        state = self.universe.state()
        self.draw(state)

        # status
        if self._showStatus:
            self.status()

    def timeTick(self):
        start_t = perf_counter()

        self.reDraw()

        # evolve
        self.universe.evolve()

        end_t = perf_counter()
        time_taken = end_t - start_t
        start_t = end_t
        self.frame_timestamps.append(time_taken)
        self.frame_timestamps = self.frame_timestamps[-30:]
        self._FPS = len(self.frame_timestamps) / sum(self.frame_timestamps)

    def keyPressEvent(self, QKeyEvent):
        # delete selected items when pressing the keyboard's delete key
        if QKeyEvent.key() == Qt.Key_Space:
            if self._timer.isActive():
                self.stop()
            else:
                self._timer.start(constants.AtomicTick * 1000)

        elif QKeyEvent.key() == Qt.Key_S:
            self._showStatus = not self._showStatus

        elif QKeyEvent.key() == Qt.Key_G:
            self._showGrid = not self._showGrid

        self.reDraw()
        QGraphicsView.keyPressEvent(self, QKeyEvent)

    def mousePressEvent(self, QMouseEvent):
        self.universe.toggleLifeform(int(QMouseEvent.x() / self.cell_size),
                                     int(QMouseEvent.y() / self.cell_size))
        self.reDraw()
        QGraphicsView.mousePressEvent(self, QMouseEvent)


    def mouseMoveEvent(self, QMouseEvent):
        self._mousePosition = (int(QMouseEvent.x() / self.cell_size), int(QMouseEvent.y() / self.cell_size))

