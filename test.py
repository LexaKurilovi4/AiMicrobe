import tkinter as tk
from classes.world import World


root = tk.Tk()
root.geometry('1000x900')
world = World(master=root, size=(1000, 900,), microbes_count=100, microbes_size=2)

root.mainloop()
