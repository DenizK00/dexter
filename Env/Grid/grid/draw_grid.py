import tkinter as tk
from grid.grid_environment import GridEnvironment

class DrawGrid:
    def __init__(self, root, width=10, height=10, cell_size=20):
        self.env = GridEnvironment(width, height, cell_size)
        self.cell_size = cell_size

        self.canvas = tk.Canvas(root, width=width * cell_size, height=height * cell_size)
        self.canvas.pack()

        self.canvas.bind("<Button-1>", self.on_click)
        self.render()

    def on_click(self, event):
        x = event.x // self.cell_size
        y = event.y // self.cell_size
        self.env.set_cell(x, y, 1)
        self.render()

    def render(self):
        self.canvas.delete("all")
        grid_repr = self.env.draw_grid()
        for y, row in enumerate(grid_repr.split("\n")):
            for x, cell in enumerate(row):
                color = "green" if cell == "A" else "white"
                self.canvas.create_rectangle(
                    x * self.cell_size, y * self.cell_size,
                    (x + 1) * self.cell_size, (y + 1) * self.cell_size,
                    fill=color, outline="black"
                )

def start():
    root = tk.Tk()
    app = DrawGrid(root)
    root.mainloop()
