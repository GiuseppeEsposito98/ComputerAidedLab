import numpy as np
from .Node import Node



class HawkessProcess:
    def __init__(self, seed, MAX_SIM_TIME = 100, ancestor_generation_parameter = 20, poisson_parameter = 2, ancestor_time_bound = 10, infection_time_parameter =1/10, infection_time_distribution = 'uniform', upper_bound_uniform = 20) -> None:
        self.seed = seed
        # max simulation time
        self.MAX_SIM_TIME = MAX_SIM_TIME
        # instant of time until when the ancestors can be generated
        self.ancestor_time_bound = ancestor_time_bound
        # Period parameter (sigma) of the exponential that will be used to generate the ancestors
        self.ancestor_generation_parameter = ancestor_generation_parameter
        # function to generate the ancestors
        self.generate_ancestor_time = lambda: np.random.exponential(1/ancestor_generation_parameter)
        # parameter of the distribution from which I extract the number of children per node
        self.poisson_parameter = poisson_parameter
        # parameter of the distribution that generates the time of infection
        self.infection_time_parameter = infection_time_parameter
        # distribution from which we extract the infection time instants
        self.infection_time_distribution = infection_time_distribution
        self.upper_bound_uniform = upper_bound_uniform
        # each ancestor corresponds to tree that could be managed at class level (so independently for each ancestor)
        self.trees = dict()

    
    def execute(self):
        counter = 0
        t_curr = 0
        id_ = 0
        inf_times_dict = dict()
        while t_curr < self.ancestor_time_bound:
            tau = self.generate_ancestor_time()
            t_curr += tau
            self.trees[id_] = Node(t_curr, self.poisson_parameter, self.MAX_SIM_TIME, self.infection_time_parameter , self.infection_time_distribution , self.upper_bound_uniform)
            id_ += 1
        for id_node in self.trees.keys():
            inf_times = list()
            self.trees[id_node].generate_age()
            inf_times_dict[id_node] = self.trees[id_node].group_infection_times(inf_times)
            counter += len(self.trees[id_node].group_infection_times(inf_times))
        return inf_times_dict, counter

    # a questo punto abbiamo generato un albero dove ogni nodo riporta il corrispondente tempo di infezione

    



# descrivere più di una politica nel report mostrando sia costi che morti

