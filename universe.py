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
        return True if self._state in [LifeformState.alive, LifeformState.dying] else False

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

        if (nc < 2 or nc > 3) and self.alive():
            self._state = LifeformState.dying
        if nc == 3 and not self.alive():
            self._state = LifeformState.resurrecting

        if self.alive():
            self._age += 1

    def updateState(self):
        if self._state == LifeformState.dying:
            self._state = LifeformState.dead

        if self._state == LifeformState.resurrecting:
            self._state = LifeformState.alive


class Universe():
    def __init__(self, state):
        '''
        Initialize the game with the initial state (the only input to the original Game of Life)
        :param state: 2D list of booleans
        '''

        self._age = 0

        # create all the Lifeforms and store them into the Universe's state
        self._state = [[Lifeform(i) for i in row] for row in state]  # 2D list of Lifeforms

    def updateNeighbors(self):
        # repass over the Universe's state to specify neighbors
        for rowi, row in enumerate(self._state):
            for lifei, life in enumerate(row):
                neighbors = []
                for j in range(rowi - 1, rowi + 2):
                    for i in range(lifei - 1, lifei + 2):
                        if (i, j) != (lifei, rowi):
                            if i == len(row):
                                i = 0
                            if j == len(self._state):
                                j = 0
                            # print('attempt to access _state[{}][{}]'.format(j,i))
                            neighbors.append(self._state[j][i])
                life.specifyNeighbors(neighbors)

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
