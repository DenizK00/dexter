import tkinter as tk
from grid.draw_grid import DrawGrid

def start():
    root = tk.Tk()
    root.title("Grid Environment Drawer")
    app = DrawGrid(root)
    root.mainloop()
