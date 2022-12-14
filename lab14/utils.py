
import numpy as np


class GWProcess: 
    def __init__(self, max_nodes, lam, seed):
        self.max_nodes = max_nodes
        self.lam = lam
        self.extract_num_children = lambda: np.random.poisson(lam=lam)
        self.seed = seed
        self.children_per_generations= [1,]
        self.generation_counter = 0



    def execute(self):
        while self.children_per_generations[-1] > 0 and self.children_per_generations[-1] <  self.max_nodes:
            counter_children = 0
            child_prev = self.children_per_generations[-1]
            for _ in range(child_prev):
                counter_children = counter_children + self.extract_num_children()
            self.children_per_generations.append(counter_children)
            self.generation_counter = self.generation_counter + 1 
        return (self.generation_counter-1, self.children_per_generations) if self.children_per_generations[-1] == 0 else (-1, self.children_per_generations)

