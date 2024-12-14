from flags import flags


class Animation:
    def __init__(self):
        self.canvas = [[[0, 0, 0] for y in range(6)] for x in range(6)]
        # run initializing step
        self.tick()

    def tick(self):
        pass


class TestAnimation(Animation):
    coord = [0, 0]

    def tick(self):
        self.canvas[self.coord[0]][self.coord[1]] = [0, 0, 0]
        self.coord[0] += 1
        self.coord[0] %= 6
        if self.coord[0] == 0:
            self.coord[1] += 1
            self.coord[1] %= 6
        self.canvas[self.coord[0]][self.coord[1]] = [8, 8, 8]


class FlagCycleAnimation(Animation):
    flag_idx = 0

    flag_list = list(flags.values())

    def tick(self):
        for x in range(len(self.canvas)):
            for y in range(len(self.canvas[x])):
                self.canvas[x][y] = self.flag_list[self.flag_idx][x]
        self.flag_idx = (self.flag_idx + 1) % len(self.flag_list)


class GameOfLife(Animation):
    cells = [
        [
            0,
            0,
            0,
            0,
            0,
            0,
        ],
        [
            0,
            0,
            1,
            0,
            0,
            0,
        ],
        [
            0,
            0,
            0,
            1,
            0,
            0,
        ],
        [
            0,
            1,
            1,
            1,
            0,
            0,
        ],
        [
            0,
            0,
            0,
            0,
            0,
            0,
        ],
        [
            0,
            0,
            0,
            0,
            0,
            0,
        ],
    ]

    def is_alive(self, x, y):
        return self.cells[x % len(self.cells)][y % len(self.cells[0])]

    def get_neighs_alive(self, x, y):
        alive = sum(
            [self.is_alive(a, b) for b in range(y - 1, y + 2) for a in [x - 1, x + 1]]
        )
        alive += self.is_alive(x, y - 1) + self.is_alive(x, y + 1)
        return alive

    def tick(self):
        new_cells = [
            [
                0,
            ]
            * 6,
            [
                0,
            ]
            * 6,
            [
                0,
            ]
            * 6,
            [
                0,
            ]
            * 6,
            [
                0,
            ]
            * 6,
            [
                0,
            ]
            * 6,
        ]

        for x in range(len(self.cells)):
            for y in range(len(self.cells[0])):
                neighs_alive = self.get_neighs_alive(x, y)
                if (self.cells[x][y] == 1 and neighs_alive == 2) or (neighs_alive == 3):
                    new_cells[x][y] = 1
                self.canvas[x][y] = [8, 8, 8] if new_cells[x][y] else [0, 0, 0]

        self.cells = new_cells
