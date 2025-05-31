import random


class Genome:

    def __init__(self, parent):
        self.code = []
        self.cur_gene = 0
        self.generate_code(parent)

    def inversion(self, parent):
        inverted_gene = None
        gene_index = random.randint(0, 7)
        gene = parent[gene_index]
        match gene:
            case 0:
                inverted_gene = 7
            case 1:
                inverted_gene = 6
            case 2:
                inverted_gene = 5
            case 3:
                inverted_gene = 4
            case 4:
                inverted_gene = 3
            case 5:
                inverted_gene = 2
            case 6:
                inverted_gene = 1
            case 7:
                inverted_gene = 0
        parent[gene_index] = inverted_gene
        self.code = parent.copy()

    def change_order(self, parent):
        indexes = range(len(parent))
        f_id = random.choice(indexes)
        s_id = random.choice(indexes)
        while f_id == s_id:
            s_id = random.choice(indexes)
        parent[f_id], parent[s_id] = parent[s_id], parent[f_id]
        self.code = parent.copy()

    def change_value(self, parent):
        gene_index = random.randint(0, 7)
        parent[gene_index] = random.randint(0, 7)
        self.code = parent.copy()

    def change_expression(self, parent):
        parent.pop(len(parent) - 1)
        self.code = parent.copy()

    def generate_code(self, parent):
        if not parent:
            for i in range(8):
                self.code.append(random.randint(0, 7))
            if 4 or 6 not in self.code:
                self.code[random.randint(0, 7)] = 0

        else:
            if random.random() < 0.8:
                self.code = parent.copy()
                return
            match random.randint(1, 3):
                case 1:
                    self.inversion(parent)
                case 2:
                    self.change_order(parent)
                case 3:
                    self.change_value(parent)
