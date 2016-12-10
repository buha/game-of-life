from life import *

class Universe():
    def __init__(self, state):
        '''
        Initialize the game with the initial state (the only input to the original Game of Life)
        :param state: 2D list of booleans
        '''
        self._age = 0
        self.seed(state)

    def seed(self, state):
        # create all the Lifeforms and store them into the Universe's state
        self._state = [[Lifeform(i) for i in row] for row in state]  # 2D list of Lifeforms
        self.updateNeighbors()

    def getNeighbors(self, col, row):
        neighbors = []
        # iterate each cell in the 3x3 square centered on self
        for j in range(row - 1, row + 2):
            for i in range(col - 1, col + 2):
                if (i, j) != (col, row):
                    # wrap around - this is not really standard Conway GOL but it's more elegant
                    # than board where cells die because they reached the edge of the universe
                    if i == len(self._state[0]):
                        i = 0 # wrap around horizontally
                    if j == len(self._state):
                        j = 0 # wrap around vertically
                    neighbors.append(self._state[j][i])
        return neighbors

    def updateNeighbors(self):
        '''
        Specify neighbors to each lifeform in the universe
        :return:
        '''
        [life.specifyNeighbors(self.getNeighbors(lifei, rowi)) \
            for rowi, row in enumerate(self._state) \
                for lifei, life in enumerate(row)]

    def evolve(self):
        '''
        At each time tick, the universe evolves and updates its lifeforms.
        '''
        self._age += 1

        for row in self._state:
            for life in row:
                life.play()


        for row in self._state:
            for life in row:
                life.updateState()


    def state(self):
        '''
        Get a 2D boolean representation of the Universe's state
        :return: 2D list of booleans
        '''
        return [[life.alive() for life in row] for row in self._state]

    def toggleLifeform(self, col, row):
        try:
            l = self._state[row][col]
        except IndexError:
            return # ignore clicks that are not on the grid (not sure how this would be possible)

        if l.alive():
            l.kill()
        else:
            l.resurrect()
