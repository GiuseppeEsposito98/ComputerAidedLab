import random
import numpy as np
from first_task.first_task import HawkessProcess as HP_1
import os
from utils import *
from collections import Counter
from scipy.stats import t
from collections import OrderedDict, defaultdict

import math 
SIM_TIME = 10
t_curr = 0
counter_anc = 0


# Assume that 2% of individuals that gets infected,  die after a while, while the others  recover.
# This holds because the 'a while' is the end of the simulation so after the simulation you see what is the 2%


def main():

    # input parameter
    RUNS = 2
    distributions = ['uniform', 'exponential']
    seed = 302179 

    # set the seed
    np.random.seed(seed)
    random.seed(seed)

    # initializations
    if not os.path.exists('./graphs'):
        os.mkdir('graphs')
    result_dict_exp = defaultdict(list)
    result_dict_unif = defaultdict(list)

    for distr in distributions:
        for _ in range(RUNS):
            # initialize the simualator
            simulator = HP_1(302179, infection_time_distribution = distr)

            # perform the simulation
            inf_times_dict, counter = simulator.execute()
            print('number of deaths: ',math.floor(counter * 0.02))

            inf_times_dict =[math.floor(t) for lst in inf_times_dict.values() for t in lst]
            count_infect = Counter(inf_times_dict)
            count_infect = OrderedDict(count_infect)

            if distr == 'uniform':
                for key in count_infect.keys():
                    result_dict_unif[key].append(count_infect[key])

            if distr == 'exponential':
                for key in count_infect.keys():
                    result_dict_exp[key].append(count_infect[key])

    fig, ax = plt.subplots(1,1)
    
    plot_avgs(ax, fig, result_dict_exp.keys(), result_dict_exp.values(), x_label='days', y_label='#infected', need_ci=True, label_='exponential', save_flag=False)
    plot_avgs(ax, fig, result_dict_unif.keys(), result_dict_unif.values(), x_label='days', y_label='#infected', need_ci=True, label_='uniform', filename='#infected per day')
        
    
if __name__ == '__main__':
    main()

