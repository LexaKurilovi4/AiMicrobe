import random
import tkinter as tk
import time
from classes.microbe import Microbe


class World(tk.Canvas):

    def __init__(self, master, size, microbes_count, microbes_size):
        super().__init__(master=master, width=size[0], height=size[1], bg='#000')
        self.pack(expand=True, fill=tk.BOTH)
        self.size = size
        self.number_of_population = 1
        self.microbes = []
        self.microbes_dict = {}
        self.microbes_count = microbes_count
        self.microbes_size = microbes_size
        self.step_id = None
        self.iterations = 0
        self.counter = self.create_text(50, 50, text=0, font='Arial 20', fill='#fff')
        self.generate_queue = True
        self.death_count_check = 0
        self.previous = microbes_count
        self.generate_population()
        # time.sleep(10)
        self.step()

    def step(self):
        self.itemconfigure(self.counter, text=len(self.microbes))
        if self.previous == len(self.microbes) or len(self.microbes) < int(self.microbes_count * 0.2):
            self.death_count_check += 1
            if self.death_count_check > 75:
                print(f'Population number : {self.number_of_population - 1}')
                print(f'Microbes count : {len(self.microbes)}')
                print(f'Iterations: {self.iterations}')
                print('_' * 20)
                self.death_count_check = 0
                self.generate_population()
        else:
            self.death_count_check = 0
        if self.generate_queue:
            for microbe in self.microbes:
                microbe.generate_queue()
            self.step_id = self.after(50, self.step)
            self.generate_queue = False
        else:
            for microbe in self.microbes:
                microbe.execute_queue()
                microbe.queue.clear()
            self.previous = len(self.microbes)
            self.iterations += 1
            self.step_id = self.after(5, self.step)
            self.generate_queue = True

    def generate_population(self):
        if self.number_of_population == 1:
            for i in range(self.microbes_count):
                self.microbes.append(Microbe(canvas=self, size=self.microbes_size, max_speed=10))
            self.number_of_population += 1
        else:
            self.after_cancel(self.step_id)
            self.iterations = 0
            parents_code = []
            for microbe in self.microbes:
                parents_code.append(microbe.genome.code)
            for microbe in self.microbes:
                self.delete(microbe.bot)
                del microbe
            self.microbes.clear()
            for i in range(self.microbes_count):
                self.microbes.append(Microbe(canvas=self, size=self.microbes_size, max_speed=10, parent=random.choice(parents_code)))
            self.number_of_population += 1
            self.step()
