from PyQt5.QtWidgets import QGraphicsView, QGraphicsScene, QGraphicsRectItem
from PyQt5.QtCore import Qt, QTimer, QRectF
from PyQt5.QtGui import QBrush, QPen, QColor
from universe import Universe
from time import perf_counter

class constants():
    DefaultCellToScreenRatio = 0.005
    DefaultAtomicTick = 0.1
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
        self._timerTickPeriod = constants.DefaultAtomicTick

        # defaults
        self._showStatus = False
        self._showGrid = False
        self._mousePosition = (0,0)
        self._CellToScreenRatio = 0.01

    def initialize(self, initialState):
        self.universe = Universe(initialState)

    def seed(self, state):
        self.universe.seed(state)

    def start(self):
        self._timer.start(constants.DefaultAtomicTick * 1000)
        self.frame_timestamps = []
        self.start_t = perf_counter()

    def stop(self):
        self._timer.stop()

    def rows(self):
        return self.rows

    def cols(self):
        return self.colss

    def resize(self, wscreen, hscreen):
        # set a sensible value for the cell size relative to screen size
        self.cell_size = int(wscreen * self._CellToScreenRatio)
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

        # resize the 2D boolean representation of the universe according to grid size
        s = None
        try:
            s = self.universe.state()
        except:
            return

        s = s[:self.rows] # in case we grew smaller, cut extra rows
        while self.rows > len(s):
            s.append([False] * self.cols)

        for rowi, row in enumerate(s):
            s[rowi] = s[rowi][:self.cols] # in case we grew smaller, cut extra items in row
            for coli, col in enumerate(range(self.cols)):
                try:
                    s[rowi][coli] # try to access the indexes
                except:
                    s[rowi].append(False) # if we grew bigger, previous index access will generate an exception.
                                          # it's about time to add False items (dead cells) to the row

        # feed the new universe representation to it as if we were starting all anew
        self.universe.seed(s)

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

        value = self._scene.addText('Desired FPS: {:.2f}'.format(1/self._timerTickPeriod))
        value.setDefaultTextColor(Qt.white)
        value.setPos(0, 15)

        age = self._scene.addText('Universe age: {}'.format(self.universe._age))
        age.setDefaultTextColor(Qt.white)
        age.setPos(0, 30)

        age = self._scene.addText('Mouse at x {}, y {}'.format(self._mousePosition[0], self._mousePosition[1]))
        age.setDefaultTextColor(Qt.white)
        age.setPos(0, 45)

        age = self._scene.addText('Universe size {}x{}'.format(self.rows, self.cols))
        age.setDefaultTextColor(Qt.white)
        age.setPos(0, 60)

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
        end_t = perf_counter()
        time_taken = end_t - self.start_t
        self.start_t = end_t
        self.frame_timestamps.append(time_taken)
        self.frame_timestamps = self.frame_timestamps[-5:]
        self._FPS = len(self.frame_timestamps) / sum(self.frame_timestamps)

        self.reDraw()

        # evolve
        self.universe.evolve()

    def keyPressEvent(self, QKeyEvent):
        if QKeyEvent.key() == Qt.Key_Space:
            if self._timer.isActive():
                self.stop()
            else:
                self._timer.start(self._timerTickPeriod  * 1000)

        elif QKeyEvent.key() == Qt.Key_S:
            self._showStatus = not self._showStatus

        elif QKeyEvent.key() == Qt.Key_G:
            self._showGrid = not self._showGrid

        elif QKeyEvent.key() == Qt.Key_Minus:
            self._timerTickPeriod *= 1.05
            self._timer.setInterval(self._timerTickPeriod * 1000)

        elif QKeyEvent.key() == Qt.Key_Plus:
            self._timerTickPeriod /= 1.05
            self._timer.setInterval(self._timerTickPeriod * 1000)

        self.reDraw()
        QGraphicsView.keyPressEvent(self, QKeyEvent)

    def mousePressEvent(self, QMouseEvent):
        self.universe.toggleLifeform(int(QMouseEvent.x() / self.cell_size),
                                     int(QMouseEvent.y() / self.cell_size))
        self.reDraw()
        QGraphicsView.mousePressEvent(self, QMouseEvent)


    def mouseMoveEvent(self, QMouseEvent):
        self._mousePosition = (int(QMouseEvent.x() / self.cell_size), int(QMouseEvent.y() / self.cell_size))

    def wheelEvent(self, QWheelEvent):
        # adjust the cell to screen ratio with input from mouse wheel
        if QWheelEvent.angleDelta().y() > 0:
            self._CellToScreenRatio *= 1.05
        else:
            self._CellToScreenRatio /= 1.05

        # resize the grid accordingly
        self.resize(self.parent().parent().width(), self.parent().parent().height())

