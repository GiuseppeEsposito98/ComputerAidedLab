import random
import numpy as np
from first_task import *
import math 
SIM_TIME = 10
t_curr = 0
counter_anc = 0



# while t_curr < SIM_TIME:
#     tau = np.random.exponential(1/20)
#     t_curr = t_curr + tau
#     counter_anc = counter_anc +1
# print(counter_anc)


simulator = HawkessProcess(302179)
time_list = simulator.execute()

# Assume that 2% of individuals that gets infected,  die after a while, while the others  recover.
# This holds because the 'a while' is the end of the simulation so after the simulation you see what is the 2%
print('number of deaths: ',math.floor(len(time_list) * 0.02))


