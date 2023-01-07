from first_task.first_task import HawkessProcess as HP_1
from utils import *
from second_task.second_task import HawkessProcess as HP_2
import math


simulator = HP_1(302179, infection_time_distribution = 'exponential')

# perform the simulation
inf_time_dict, counter = simulator.execute()
#print('number of deaths: ',math.floor(len(time_list) * 0.02))

#simulator2 = HP_2(302179)
#simulator2.execute()