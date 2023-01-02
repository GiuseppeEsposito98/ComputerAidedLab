import random
import numpy as np
from first_task import *
import math 
SIM_TIME = 10
t_curr = 0
counter_anc = 0

np.random.seed(302179)
random.seed(302179)
RUNS = 100
# while t_curr < SIM_TIME:
#     tau = np.random.exponential(1/20)
#     t_curr = t_curr + tau
#     counter_anc = counter_anc +1
# print(counter_anc)
# class SeedGenerator:
#     def __init__(
#             self,
#             k: int,
#             seed: int):
#         self.generator = np.random.default_rng(seed=seed)
#         self.low = k
#         self.high = k**3
    
#     def __call__(self) -> int:
#         return self.generator.integers(
#             low=self.low,
#             high=self.high
#             )
        
# get_seed = SeedGenerator(
#         seed=42,
#         k = RUNS
#         )

simulator = HawkessProcess(302179, infection_time_distribution = 'exponential')
time_list = simulator.execute()

# Assume that 2% of individuals that gets infected,  die after a while, while the others  recover.
# This holds because the 'a while' is the end of the simulation so after the simulation you see what is the 2%
print('number of deaths: ',math.floor(len(time_list) * 0.02))


