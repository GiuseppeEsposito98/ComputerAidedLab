import numpy as np

class Node:

    def __init__(self, time_born, poisson_parameter, MAX_SIM_TIME, infection_time_parameter = 1/10 , infection_time_distribution = 'uniform' , upper_bound_uniform = 20) -> None:
        self.time_born = time_born
        self.infection_time_parameter = infection_time_parameter
        self.infection_time_distribution = infection_time_distribution
        self.upper_bound_uniform = upper_bound_uniform
        self.poisson_parameter = poisson_parameter
        self.generate_num_of_children = lambda: np.random.poisson(poisson_parameter)
        self.MAX_SIM_TIME = MAX_SIM_TIME
        #self.has_generated = False
        self.children = list()
    
    def generate_age(self):
        num_children = self.generate_num_of_children()
        #self.has_generated = True
        for _ in range(num_children):
            tau = self.h()
            time_abs = self.time_born + tau 
            if time_abs > self.MAX_SIM_TIME: # stopping condition of the current branch of the tree 
                break  
            child = Node(time_abs, self.poisson_parameter, self.MAX_SIM_TIME, self.infection_time_parameter, self.infection_time_distribution, self.upper_bound_uniform) 
            self.children.append(child) 
            child.generate_age()
    
    def group_infection_times(self, inf_times):
        inf_times.append(self.time_born)  
        for child in self.children: 
            inf_times = child.group_infection_times(inf_times)
        return inf_times
    
    def h(self):
        if self.infection_time_distribution == 'exponential':
            tau = np.random.exponential(1/self.infection_time_parameter)
            print(tau)
            return tau 

        elif self.infection_time_distribution == 'uniform':
            return np.random.uniform(low=0, high=self.upper_bound_uniform)