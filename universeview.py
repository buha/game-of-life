from PyQt5.QtWidgets import QGraphicsView, QGraphicsScene, QGraphicsRectItem
from PyQt5.QtCore import Qt, QTimer, QPointF, QLineF, QRectF
from PyQt5.QtGui import QBrush, QPen, QColor
from random import randint

class constants():
    CellToScreenRatio = 0.01
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

        # the fun begins here
        self.timer.start(300)
        self.generation = 0

    def stop(self):
        self.timer.stop()

    def drawCell(self, row, col):
        item = QGraphicsRectItem(col * self.cell_size,
                                 row * self.cell_size,
                                 self.cell_size,
                                 self.cell_size)
        item.setBrush(QBrush(constants.cell))
        item.setPen(constants.grid)
        self.scene.addItem(item)

    def rePaint(self):
        # grow older
        self.generation += 1

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

        # cells
        self.drawCell(randint(0,  self.rows - 1) , randint(0, self.cols - 1))
        self.drawCell(randint(0, self.rows - 1), randint(0, self.cols - 1))
        self.drawCell(randint(0, self.rows - 1), randint(0, self.cols - 1))
        self.drawCell(randint(0, self.rows - 1), randint(0, self.cols - 1))
        self.drawCell(randint(0, self.rows - 1), randint(0, self.cols - 1))
        self.drawCell(randint(0, self.rows - 1), randint(0, self.cols - 1))
        self.drawCell(randint(0, self.rows - 1), randint(0, self.cols - 1))
        self.drawCell(randint(0, self.rows - 1), randint(0, self.cols - 1))
        self.drawCell(randint(0, self.rows - 1), randint(0, self.cols - 1))
        self.drawCell(randint(0, self.rows - 1), randint(0, self.cols - 1))