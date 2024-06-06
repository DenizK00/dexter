import numpy as np

class GridEnvironment:
    def __init__(self, width=10, height=10, cell_size=20):
        self.width = width
        self.height = height
        self.cell_size = cell_size
        self.grid = np.zeros((height, width), dtype=int)
        self.agent_pos = None

    def draw_grid(self):
        grid_representation = np.full((self.height, self.width), " ")
        for y in range(self.height):
            for x in range(self.width):
                if self.grid[y, x] == 1:
                    grid_representation[y, x] = "A"
                else:
                    grid_representation[y, x] = "."

        return "\n".join("".join(row) for row in grid_representation)

    def set_cell(self, x, y, value):
        self.grid[y, x] = value

    def set_agent(self, x, y):
        if self.agent_pos:
            self.set_cell(*self.agent_pos, 0)
        self.agent_pos = (x, y)
        self.set_cell(x, y, 1)
