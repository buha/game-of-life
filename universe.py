from enum import Enum

class LifeformState(Enum):
    dead = 0,
    alive = 1,
    dying = 2,
    resurrecting = 3

class Lifeform():
    def __init__(self, state=False):
        '''
        Create a lifeform
        :param state: True stands for alive, False stands for dead.
        '''
        self._age = 0
        self._state = LifeformState.alive if state else LifeformState.dead
        self._neighbors = []

    def alive(self):
        '''
        Is this cell alive?
        '''
        return True if self._state in \
            [LifeformState.alive, LifeformState.dying] else False

    def specifyNeighbors(self, neighbors):
        '''
        Tell the lifeform whom its neighbor is.
        :param neighbor: another lifeform
        '''
        self._neighbors = neighbors

    def aliveNeighbors(self):
        '''
        Count how many naighbors are alive
        :return: numeric
        '''
        return sum(neighbor.alive() for neighbor in self._neighbors)

    def play(self):
        '''
        This is where the Game of Life rules get implemented
        '''
        nc = self.aliveNeighbors()

        if self.alive():
            self._age += 1

        if (nc < 2 or nc > 3) and self.alive():
            self._state = LifeformState.dying
        if nc == 3 and not self.alive():
            self._state = LifeformState.resurrecting

    def updateState(self):
        if self._state == LifeformState.dying:
            self.kill()

        if self._state == LifeformState.resurrecting:
            self.resurrect()

    def kill(self):
        self._state = LifeformState.dead

    def resurrect(self):
        self._state = LifeformState.alive


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

    def getNeighbors(self, col, row):
        neighbors = []
        for j in range(row - 1, row + 2):
            for i in range(col - 1, col + 2):
                if (i, j) != (col, row):
                    if i == len(self._state[0]):
                        i = 0
                    if j == len(self._state):
                        j = 0
                    neighbors.append(self._state[j][i])
        return neighbors

    def updateNeighbors(self):
        # repass over the Universe's state to specify neighbors
        for rowi, row in enumerate(self._state):
            for lifei, life in enumerate(row):
                life.specifyNeighbors(self.getNeighbors(lifei, rowi))

    def evolve(self):
        '''
        At each time tick, the universe evolves and updates its lifeforms.
        '''
        self._age += 1

        self.updateNeighbors()

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
            return

        if l.alive():
            l.kill()
        else:
            l.resurrect()

        self.updateNeighbors()
