import tkinter as tk
from grid.draw_grid import DrawGrid

def draw(width=10, height=10, cellsize=30):
    root = tk.Tk()
    root.title("Grid Environment Drawer")
    app = DrawGrid(root, width=width, height=height, cell_size=cellsize)
    root.mainloop()
