from enum import Enum

class LifeformState(Enum):
    dead = 0,
    alive = 1,
    dying = 2,
    resurrecting = 3

class Lifeform():
    def __init__(self, c1, c2, state=False):
        '''
        Create a lifeform
        :param state: True stands for alive, False stands for dead.
        '''
        self._age = 0
        self._state = LifeformState.alive if state else LifeformState.dead
        self._neighbors = []
        self._c1 = c1
        self._c2 = c2


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

        if (nc < self._c1 or nc > self._c2) and self.alive():
            self._state = LifeformState.dying
        if nc == self._c2 and not self.alive():
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
