import numpy as np
from .Node import Node
import math



class HawkessProcess:
    def __init__(self, seed, ancestor_time_bound=10, time_no_pharms=20, MAX_SIM_TIME=365, infection_parameter=20, poisson_parameter=2, infection_distribution = 'exponential', uniform_bound = 20) -> None:
        self.seed = seed
        self.ancestor_time_bound = ancestor_time_bound
        self.time_no_pharm = time_no_pharms
        self.MAX_SIM_TIME = MAX_SIM_TIME 
        self.infection_parameter = infection_parameter
        self.poisson_parameter = poisson_parameter
        self.infection_distribution = infection_distribution,
        self.uniform_bound = uniform_bound
        self.trees = dict()
        self.infections = dict()

        
    def sigma(self, t_curr, poisson_intensity):
        # qua posso passare la classe nodo che creo ogni volta, così ritorno l'ultimo tempo generato
        if t_curr < self.ancestor_time_bound:
            return self.infection_parameter
        else: 
            return 0#poisson_intensity
    
    def h_func(self, t):
        if t<=self.ancestor_time_bound:
            return 1/self.infection_parameter
        else: 
            return 0
    
    def execute(self):
        '''
        qui non funziona 'n cazzo
        '''
        counter = 0
        t_curr = 0
        rho = 0.95
        poisson_intensity = 0
        inf_times_dict = dict()
        raugh_times = list()
        # ricordati che bisogna distinguere per ogni albero e fino a che non finisce ancestor_time_bound
        while t_curr < self.MAX_SIM_TIME:
            #print(self.infection_distribution)
            print(t_curr)
            new_t = np.random.exponential(1/self.infection_parameter)
            #h = self.h_func()
            print('new_t: ', new_t)
            t_curr += new_t
            if len(self.infections.keys())==0 or list(self.infections.keys())[-1]<self.time_no_pharm:
                stoch_intensity = self.sigma(t_curr, poisson_intensity) + self.poisson_parameter * sum(self.h_func(t) for t in raugh_times)
                poisson_intensity = stoch_intensity
            else:
                print('im out')
                stoch_intensity = self.sigma(t_curr, poisson_intensity) + self.poisson_parameter * sum(self.h_func(t_curr-t) for t in raugh_times if t < t_curr-20)
            #print('im stoc:', stoch_intensity)
            #print('poi: ', poisson_intensity)

            raugh_times.append(t_curr)
            new_key = math.floor(t_curr)
            if new_key in self.infections.keys():
                self.infections[new_key] += 1
            else:
                self.infections[new_key] = 1

            raugh_times.append(t_curr)
            u = np.random.uniform(0,1)
            # e poi è sbagliato il rapporto perchè è una probabilità e ad un certo punto va sopra 1 (il problema è principalmente questo)
            if t_curr >= 10:
                #print(self.infection_parameter)
                self.infection_parameter /= rho
            print(f'{sum(list(self.infections.values()))} total infected at time {list(self.infections.keys())[-1]}')

        # while t_curr < self.ancestor_time_bound:
        #     tau = self.generate_ancestor_time()
        #     t_curr += tau
        #     self.trees[id_] = Node(t_curr, self.poisson_parameter, self.MAX_SIM_TIME_without_int, self.infection_time_parameter , self.infection_time_distribution , self.upper_bound_uniform)
        #     id_ += 1
        # while t_curr < self.MAX_SIM_TIME:
        #     for node in self.trees.values():
        #         poisson_intensity = 0
        #         t_curr = node.time_born
                
        #         while t_curr < self.MAX_SIM_TIME:
        #             h = np.random.exponential(1/self.infection_parameter)
        #             t_curr += h
        #             if len(self.infections)==0 or self.infections.keys()[-1]<self.time_no_pharm:
        #                 stoch_intensity = self.sigma(t_curr) + sum([h(t_curr- t_i) for t_i in self.infections.keys()])
        #                 poisson_intensity = stoch_intensity
        #             else:
        #                 s = 0
        #                 stoch_intensity = self.sigma(t_curr) + self.poisson_parameter * sum([h(t) for t in self.infections.keys()])
                    
        #             u = np.random.uniform(0,1)

        #             new_key = math.floor(t_curr)
        #             self.infections[new_key] += 1

        #             if u > stoch_intensity/poisson_intensity:
        #                 self.infection_parameter /= rho
        #             print(sum(f'{sum(self.infections.values())/new_key} total infected at time {list(self.infections.keys())[-1]}'))
       
            
            # qui prova a non usare la classe che ti sei creato.

        return inf_times_dict, counter




# descrivere più di una politica nel report mostrando sia costi che morti

