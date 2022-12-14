
import numpy as np


class GWProcess: 
    '''
    Simulator class:
    this class manages every tree generated by the Galton-Watson process returning the last detected generation 
    before the extinction and also the number of individuals per generation. This is performed under the following conditions.
    '''
    def __init__(self, max_nodes, lam, seed):
        self.max_nodes = max_nodes
        self.lam = lam
        # function to randomly extract the number of children per individual
        self.extract_num_children = lambda: np.random.poisson(lam=lam)
        self.seed = seed
        self.children_per_generations= [1,]
        self.generation_counter = 0



    def execute(self):
        while self.children_per_generations[-1] > 0 and self.children_per_generations[-1] <  self.max_nodes:
            counter_children = 0
            child_prev = self.children_per_generations[-1]
            # for each individual of the previous generation
            for _ in range(child_prev):
                # generate the number of children from a poisson distribution
                counter_children = counter_children + self.extract_num_children()
            self.children_per_generations.append(counter_children)
            self.generation_counter = self.generation_counter + 1 
        return (self.generation_counter, self.children_per_generations[:self.generation_counter]) if self.children_per_generations[-1] == 0 else (-1, [])

