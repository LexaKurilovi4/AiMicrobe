class Queue:

    def __init__(self):
        self.queue = []
        self.synthesis = 1
        self.attack = 1
        self.move = 1
        self.skip = 1
    
    def clear(self):
        self.__init__()

    def add_synthesis(self, call):
        self.queue.append({"synthesis": call/self.synthesis})
        self.synthesis += 1

    def add_attack(self, damage):
        self.queue.append({"attack": damage/self.attack})
        self.attack += 1

    def add_move(self, vector):
        self.queue.append({"move": [vector[0]/self.move**2, vector[1]/self.move**2]})
        self.move += 1

    def add_skip(self, call):
        self.queue.append({"skip": call/self.skip})
        self.skip += 1
