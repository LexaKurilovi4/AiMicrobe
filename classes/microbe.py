import random
import time
from math import sqrt, sin

from classes.genome import Genome
from classes.queue import Queue


def generate_vector(start=False):
    if start:
        return [random.randint(-50, 50) / 10, random.randint(-50, 50) / 10]
    return [random.randint(-10, 10) / 10, random.randint(-10, 10) / 10]


class Microbe:

    def __init__(self, canvas, size, max_speed, parent=None):
        self.canvas = canvas
        self.x = random.randint(size * 5, self.canvas.size[0] - size * 5)
        self.y = random.randint(size * 5, self.canvas.size[1] - size * 5)
        self.size = int(size)
        self.genome = Genome(parent)
        self.calories = 70
        self.max_calories = 100
        self.queue = Queue()
        if 1 in self.genome.code and 3 not in self.genome.code:
            self.color = '#0f0'
        elif 1 not in self.genome.code and 3 in self.genome.code:
            self.color = '#f00'
        elif 1 in self.genome.code and 3 in self.genome.code:
            self.color = '#ff0'
        else:
            self.color = '#00f'
        self.bot = canvas.create_oval(self.x - self.size,
                                      self.y - self.size,
                                      self.x + self.size,
                                      self.y + self.size, fill=self.color, outline=self.color)
        self.speed = generate_vector(start=True)
        # self.speed_vector = canvas.create_line(self.x,
        #                                        self.y,
        #                                        self.x + self.speed[0] * 10,
        #                                        self.y + self.speed[1] * 10,
        #                                        fill="#fff",
        #                                        arrow="last")
        self.max_speed = max_speed

    def generate_speed(self):
        vector = generate_vector()
        self.speed[0] += vector[0]
        self.speed[1] += vector[1]
        collide = self.check_collision()
        if collide is not None:
            self.speed[0] += collide[0]
            self.speed[1] += collide[1]
        speed_len = sqrt(self.speed[0] ** 2 + self.speed[1] ** 2)
        if speed_len > self.max_speed:
            self.speed[0] = self.speed[0] * self.max_speed / speed_len
            self.speed[1] = self.speed[1] * self.max_speed / speed_len
        if self.x + self.speed[0] <= 0 or self.x + self.speed[0] >= self.canvas.size[0]:
            self.speed[0] = -self.speed[0]
        if self.y + self.speed[1] <= 0 or self.y + self.speed[1] >= self.canvas.size[1]:
            self.speed[1] = -self.speed[1]
        return self.speed

    def imitate_move(self, speed):
        self.x = round(self.x + speed[0], 2)
        self.y = round(self.y + speed[1], 2)
        self.calories -= round(sqrt((speed[0]) ** 2 + (speed[1]) ** 2) / 4, 2)
        self.canvas.coords(self.bot,
                           self.x - self.size,
                           self.y - self.size,
                           self.x + self.size,
                           self.y + self.size)
        # self.canvas.coords(self.speed_vector,
        #                    self.x,
        #                    self.y,
        #                    self.x + speed[0] * 10,
        #                    self.y + speed[1] * 10)

    def die(self):
        self.canvas.delete(self.bot)
        self.canvas.microbes.remove(self)
        del self

    def attack(self, damage):
        attack_range = 1.5
        coll = self.canvas.find_overlapping(self.x - self.size * attack_range,
                                            self.y - self.size * attack_range,
                                            self.x + self.size * attack_range,
                                            self.y + self.size * attack_range)
        coll = list(coll)
        coll.remove(self.bot)
        if len(coll) == 0:
            return
        self.canvas.itemconfigure(self.bot, fill='#fff', outline='#fff')
        self.change_color()
        for other in self.canvas.microbes:
            if other.bot in coll:
                other.calories -= damage
                self.calories += damage / 3
                # other.die()

    def check_collision(self):
        coll = self.canvas.find_overlapping(self.x - self.size - 0.1,
                                            self.y - self.size - 0.1,
                                            self.x + self.size + 0.1,
                                            self.y + self.size + 0.1)
        coll = list(coll)
        vector = None
        coll.remove(self.bot)
        for other in self.canvas.microbes:
            if other.bot in coll:
                vector = [(self.x - other.x), (self.y - other.y)]
            return vector

    def generate_queue(self):
        next_gen = True
        test_run = 0
        try:
            while next_gen:
                test_run += 1
                match self.genome.code[self.genome.cur_gene]:
                    case 1:
                        # self.calories += 6
                        # self.imitate_move()
                        self.queue.add_synthesis(5)
                        self.genome.cur_gene += 1
                        next_gen = False
                    case 2:
                        # self.calories -= 1
                        self.queue.add_skip(5)
                        self.genome.cur_gene += 2
                    case 3:  # attack
                        # self.attack()
                        # self.calories -= 2
                        self.queue.add_attack(15)
                        self.genome.cur_gene += 3
                        next_gen = False
                    case 4:
                        self.genome.cur_gene += 4
                        self.queue.add_move(self.generate_speed())
                        # self.imitate_move()
                    case 5:
                        self.genome.cur_gene += 5
                        next_gen = False
                        self.queue.add_skip(5)
                        # self.imitate_move()
                    case 6:
                        self.genome.cur_gene += 6
                        next_gen = False
                        self.queue.add_move(self.generate_speed())
                        # self.imitate_move()
                    case 7:
                        self.genome.cur_gene += 7
                        next_gen = False
                        self.queue.add_skip(5)
                        # self.imitate_move()
                    case 0:
                        self.genome.cur_gene += random.randint(0, len(self.genome.code)-1)
                        next_gen = False
                        self.queue.add_move(self.generate_speed())
                        # self.imitate_move()
                if self.genome.cur_gene > 7:
                    self.genome.cur_gene = self.genome.cur_gene % 8
                if test_run > 16:
                    break
        except Exception as e:
            print(e)
        if self.calories > 100:
            self.calories = 100
        if self.calories <= 0:
            self.die()

    def execute_queue(self):
        for action in self.queue.queue:
            if "synthesis" in action:
                self.calories += action["synthesis"]
            elif "attack" in action:
                self.attack(action["attack"])
            elif "move" in action:
                self.imitate_move(action["move"])
            elif "skip" in action:
                self.calories -= action["skip"]

    async def change_color(self):
        time.sleep(0.3)
        await self.canvas.itemconfigure(self.bot, fill=self.color, outline='#fff')
