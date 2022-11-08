import numpy as np
import random

random.seed(42)

def simulation(n, policy = 1):
    # create a dict with n keys and all default values set to 0
    bins = dict.fromkeys(range(n), 0)
    possible_choices = np.arange(n)
    if policy == 1: # if policy == random dropping
        for _ in range(n):
            choice = random.choice(possible_choices)
            bins[choice] =  bins[choice] + 1
    elif policy != 1: # else if policy == random load balancing
        for _ in range(n):
            # choose d possible bins where i can drop the _-th ball
            chosen = random.choices(possible_choices, k = policy)
            min_ = n
            for idx in chosen:
                if bins[idx] <= min_:
                    # compute the minimum occupancy level among all the selected bins
                    min_ = bins[idx] 
            # create a list which contains the indexes of the bins whose occupancy level is equal to the min
            idxs = [idx for idx in chosen if bins[idx] == min_]
            # in case of tie select a random index among the ones who has the same lowest occupancy level
            luckiest = random.choice(idxs)
            bins[luckiest] = bins[luckiest] + 1
    # compute the metrics
    min_occ = min(bins.values())
    max_occ = max(bins.values())
    avg_occ = sum(bins.values())/n
    return max_occ, min_occ, avg_occ, bins