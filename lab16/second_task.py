
import numpy as np

# class Ancestor:
#     def __init__(self, time_born, ) -> None:
#         pass

class Node:

    def __init__(self, time_born, MAX_SIM_TIME,  poisson_parameter, infection_time_parameter = 1/10 , infection_time_distribution = 'uniform' , upper_bound_uniform = 20, pause_generation = 20) -> None:
        self.time_born = time_born
        self.MAX_SIM_TIME = MAX_SIM_TIME
        self.infection_time_parameter = infection_time_parameter
        self.infection_time_distribution = infection_time_distribution
        self.upper_bound_uniform = upper_bound_uniform
        self.generate_infection_time = lambda: np.random.exponential(1/infection_time_parameter) if infection_time_distribution == 'exponential' else lambda: np.random.uniform(low=0, high=upper_bound_uniform)
        self.poisson_parameter = poisson_parameter
        self.generate_num_of_children = lambda: np.random.poisson(poisson_parameter)
        self.pause_generation = pause_generation,
        self.has_generated = False
        self.children = list()
    
    def generate_age(self):
        if not self.has_generated:
            num_children = self.generate_num_of_children()
            self.has_generated = True
            for _ in range(num_children): 
                tau = np.random.uniform(0,20) ######## devi cambiare
                time_assolute = self.time_born + tau  
                if time_assolute > self.pause_generation:  
                    return          
                child = Node(time_assolute, self.poisson_parameter, self.infection_time_parameter, self.infection_time_distribution, self.upper_bound_uniform, self.pause_generation) 
                self.children.append(child) 
                child.generate_age()
        else: 
            pass
    
    
    
    def group_infection_times(self, inf_times, low_day, upper_day):
        if self.time_born <= upper_day and self.time_born >= low_day:
            inf_times.append(self.time_born)  
            for child in self.children: 
                inf_times = child.group_infection_times(inf_times)
            return inf_times

class HawkessProcess:
    def __init__(self, seed, MAX_SIM_TIME = 365, initial_time = 0, ancestor_generation_parameter = 20, poisson_parameter = 2, ancestor_time_bound = 10, infection_time_parameter =1/10, infection_time_distribution = 'uniform', upper_bound_uniform = 20, pause_generation = 20) -> None:
        self.seed = seed
        self.MAX_SIM_TIME = MAX_SIM_TIME
        self.initial_time = initial_time
        # instant of time until when the ancestors can be generated
        self.ancestor_time_bound = ancestor_time_bound #### 10
        # Period parameter (sigma) of the exponential that will be used to generate the ancestors
        self.ancestor_generation_parameter = ancestor_generation_parameter ##### 20
        # function to generate the ancestors
        self.generate_ancestor_time = lambda: np.random.exponential(1/ancestor_generation_parameter)
        # parameter of the distribution from which I extract the number of children per node
        self.poisson_parameter = poisson_parameter
        # parameter of the distribution that generates the time of infection
        self.infection_time_parameter = infection_time_parameter
        # distribution from which we extract the infection time instants
        self.infection_time_distribution = infection_time_distribution
        self.upper_bound_uniform = upper_bound_uniform
        self.pause_generation = pause_generation
        # function to generate the infection time with respect to the given distribution
        #self.generate_infection_time = lambda: np.random.exponential(1/infection_time_parameter) if infection_time_distribution == 'exponential' else lambda: np.random.uniform(low=0, high=upper_bound_uniform)
        # each ancestor corresponds to tree that could be managed at class level (so independently for each ancestor)
        self.trees = dict()
    
    def generate_uncontrolled(self):
        for ancestor in self.trees.values(): 
            ancestor.generate_age()
        

    
    def execute(self):
        t_curr = self.initial_time
        id = 0
        inf_times = list()
        while t_curr <= self.ancestor_time_bound:
            tau = self.generate_ancestor_time()
            t_curr += tau
            self.trees[id] = Node(t_curr, self.MAX_SIM_TIME, self.poisson_parameter, self.infection_time_parameter , self.infection_time_distribution , self.upper_bound_uniform, self.pause_generation)
            id += 1
        self.generate_uncontrolled()
        t_curr = self.pause_generation
        for day in range(t_curr, self.MAX_SIM_TIME):

        return inf_times





# descrivere più di una politica nel report mostrando sia costi che morti

