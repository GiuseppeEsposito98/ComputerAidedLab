import numpy as np
from scipy.stats import norm, t

def cum_mean(arr):
    cum_sum = np.cumsum(arr,axis=0)
    for i in range(cum_sum.shape[0]):
        if i == 0:
            continue
        cum_sum[i] = cum_sum[i]/(i+1)
    return cum_sum

def remove_transient(arr, u):
    len_window = int(u*10000)
    #len_window = int(len(arr)/n_window)
    n_window = int(len(arr)/len_window)
    thr = 0.95
    if u == 0.9 or u == 0.95:
        thr = 0.98
    elif u == 0.99:
        thr = 0.995
    for i in range(n_window):
        if i*len_window >= len(arr):
            break
        else:
            window1 = arr[i*len_window: (i+1)*len_window]
            #window2 = arr[(i+1)*len_window: (i+2)*len_window]
            if window1 != []:
                max1, min1 = min(window1), max(window1)
                normalized = min1/max1
            if normalized > thr:
                arr = arr[(i+1)*len_window:]
                return arr, len_window*(i+1)

def find_number_of_batches(delays, u, n, confidence=.95):
    # delays è senza transient
    delays = np.array(delays)
    while True:
        batches = np.array_split(delays, n)
        for batch in batches:
            x = np.mean(batch)
            ci = t.interval(confidence, len(batches)-1, x, np.std(batch))
            z = ci[1] - x
            if (2*z/x) > u:
                print('interval too large')
                n += 1
                break
            else: 
                print('interval ok')
                return n

def perform_batch_means(delays, correct_n, confidence=.95):
    means = list()
    ci_lower = list()
    ci_upper = list()
    delays = np.array(delays)
    batches = np.array_split(delays, correct_n)
    for batch in batches:
        x = np.mean(batch)
        ci = t.interval(confidence, len(batches)-1, x, np.std(batch))
        print(ci, x)
        ci_lower.append(ci[0])
        ci_upper.append(ci[1])
        means.append(x)
    
    return means, ci_lower, ci_upper

def generate_hyperexponential():
    p = .5
    l1 = 1/6
    l2 = 1/8
    u1 = np.random.random()
    if u1 <= p:
        scale = l1
    else:
        scale = l2
    u2 = np.random.random()
    service = -np.log(u2)/scale
    return service