class Lifeform():
    def __init__(self, state=False):
        '''
        Create a lifeform
        :param state: True stands for alive, False stands for dead.
        '''
        self._age = 0
        self._state = state
        self._neighbors = []

    def alive(self):
        '''
        Is this cell alive?
        '''
        return self._state

    def specifyNeighbor(self, neighbor):
        '''
        Tell the lifeform whom its neighbor is.
        :param neighbor: another lifeform
        '''
        self._neighbors.append(neighbor)

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
            self.kill()
        elif nc == 3 and not self.alive():
            self.resurrect()
        return 0

    def kill(self):
        self._state = False

    def resurrect(self):
        self._state = True



class Universe():
    def __init__(self, state):
        '''
        Initialize the game with the initial state (the only input to the original Game of Life)
        :param state: 2D list of booleans
        '''

        self._age = 0

        # create all the Lifeforms and store them into the Universe's state
        self._state = [[Lifeform(i) for i in row] for row in state]  # 2D list of Lifeforms

        # repass over the Universe's state to specify neighbors (there must be a better way!)
        for rowi, row in enumerate(self._state):
            for lifei, life in enumerate(row):
                for j in range(rowi - 1, rowi + 2):
                    for i in range(lifei - 1, lifei + 2):
                        if (i, j) != (lifei, rowi) \
                                and i >= 0 \
                                and j >= 0 \
                                and i < len(row) \
                                and j < len(self._state):
                            #print('attempt to access _state[{}][{}]'.format(j,i))
                            life.specifyNeighbor(self._state[j][i])
                '''
                try:
                    print('attempt to access _state[{}][{}]'.format(rowi - 1, lifei - 1))
                    life.specifyNeighbor(self._state[rowi - 1][lifei - 1])
                    print('attempt to access _state[{}][{}]'.format(rowi - 1, lifei))
                    life.specifyNeighbor(self._state[rowi - 1][lifei    ])
                    print('attempt to access _state[{}][{}]'.format(rowi - 1, lifei + 1))
                    life.specifyNeighbor(self._state[rowi - 1][lifei + 1])
                    print('attempt to access _state[{}][{}]'.format(rowi, lifei -1))
                    life.specifyNeighbor(self._state[rowi    ][lifei - 1])
                    print('attempt to access _state[{}][{}]'.format(rowi, lifei + 1))
                    life.specifyNeighbor(self._state[rowi    ][lifei + 1])
                    print('attempt to access _state[{}][{}]'.format(rowi + 1, lifei - 1))
                    life.specifyNeighbor(self._state[rowi + 1][lifei - 1])
                    print('attempt to access _state[{}][{}]'.format(rowi + 1, lifei))
                    life.specifyNeighbor(self._state[rowi + 1][lifei    ])
                    print('attempt to access _state[{}][{}]'.format(rowi + 1, lifei + 1))
                    life.specifyNeighbor(self._state[rowi + 1][lifei + 1])
                except Exception as e:
                    pass
                    '''
    def evolve(self):
        '''
        At each time tick, the universe evolves and updates its lifeforms.
        '''
        self._age += 1
        [[life.play() for life in row] for row in self._state]

    def state(self):
        '''
        Get a 2D boolean representation of the Universe's state
        :return: 2D list of booleans
        '''
        return [[life.alive() for life in row] for row in self._state]