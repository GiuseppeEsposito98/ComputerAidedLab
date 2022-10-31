import numpy as np
import random
from collections import Counter
import matplotlib.pyplot as plt

#n = int(input("Number of balls and bins: "))

def simulation(n, d = None):
    bins = dict.fromkeys(range(n), 0)
    if d == 1:
        for i in range(n):
            choice = random.choice(range(n))
            bins[choice] =  bins[choice] +1
    elif d != 1:
        #d = int(input("Number of selected bins"))
        for _ in range(n):
            chosen = random.choices(np.arange(n), k = d)
            min_ = n
            for idx in chosen:
                if bins[idx] <= min_:
                    min_ = bins[idx]
            idxs = [idx for idx in chosen if bins[idx] == min_]
            luckiest = random.choice(idxs)
            bins[luckiest] = bins[luckiest] + 1
    counter = Counter(bins.values())
    #print(counter)
    min_occ = min([val for val in bins.values() if val !=0])
    print(min_occ)
    max_occ = max([val for val in bins.values() if val !=0])
    print(max_occ)
    avg_occ = sum(bins.values())/(n-counter[0])
    print(avg_occ)
    return max_occ, min_occ, avg_occ


max_occs = list()
min_occs = list()
avg_occs = list()
N = [100,1000,10000,10**5, 10**6]
for n in N:
    print(n)
    max_occ, min_occ, avg_occ = simulation(n, 2)
    max_occs.append(max_occ)
    min_occs.append(min_occ)
    avg_occs.append(avg_occ)
fig = plt.figure()
plt.plot(N, max_occs)
plt.plot(N, min_occs)
plt.plot(N, avg_occs)
plt.ylabel("occupancy levels")
plt.xlabel("N")
plt.show()


        
        

                
         
