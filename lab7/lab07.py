import numpy as np
import random
from collections import Counter
import matplotlib.pyplot as plt

def simulation(n, d = None):
    bins = dict.fromkeys(range(n), 0)
    if d == 1:
        for i in range(n):
            choice = random.choice(range(n))
            bins[choice] =  bins[choice] +1
    elif d != 1:
        possible_choices = np.arange(n)
        for _ in range(n):
            chosen = random.choices(possible_choices, k = d)
            min_ = n
            for idx in chosen:
                if bins[idx] <= min_:
                    min_ = bins[idx]
            idxs = [idx for idx in chosen if bins[idx] == min_]
            luckiest = random.choice(idxs)
            bins[luckiest] = bins[luckiest] + 1
    counter = Counter(bins.values())
    min_occ = min([val for val in bins.values() if val !=0])
    #print(min_occ)
    max_occ = max([val for val in bins.values() if val !=0])
    #print(max_occ)
    avg_occ = sum(bins.values())/(n-counter[0])
    #print(avg_occ)
    return max_occ, min_occ, avg_occ


max_occs = list()
N = [100,1000,10000,10**5]
D = [1,2,3,4]
values = list()
for d in D:
    for n in N:
        #print(n)
        max_occ, min_occ, avg_occ = simulation(n, d)
        max_occs.append(max_occ)
    values.append(max_occs)
    max_occs = list()
#print("len(values) ", len(values))
fig = plt.figure()
for val in values: 
    plt.plot(N, val)
plt.ylabel("occupancy levels")
plt.xlabel("N")
plt.show()
plt.savefig("N-occupancy level.png")


        
        

                
         
