from client import Client
from event import *
#import random
from scipy.stats import t
import matplotlib.pyplot as plt
import numpy as np
from show_results import *
import csv
from simulation import *

"""
In this laboratory we were asked to simulate a single server queue system (queue discipline: FIFO).
It is a system where the arrival time of the client is scheduled and if the server is already busy the client 
is added to the queue: that job will start when the server will not be busy. If the server is idle we check if the queue is empty, 
in this case interrupt the cycle otherwise schedule a new departure event for the inline client. 
(For debugging purposes I also kept track of the client to which each event is referred)
"""

def arrival(time, FES, queue_, mu, lam, users, hyper= False):

    global id_client
    t_ia = np.random.exponential(mu)
    e = Event(time +t_ia, "arrival")
    # id_client is used to check whether a specific client has just one arrival and one departure (debugging purposes)
    id_client = id_client + 1 
    client_arr = Client("arrival", time, id_client)
    e.assignClient(client_arr)
    FES.append(e)
    users = users +1
    queue_.append(client_arr)
    if(users == 1):
        if hyper:
            service_time = generate_hyperexponential()
        else:
            service_time = np.random.exponential(lam)
        client_dep = Client("departure", time+ service_time, id_client)
        e1 = Event(time + service_time, "departure")
        e1.assignClient(client_dep)
        FES.append(e1)
    return users

# Departure function
def departure(time, FES, queue_, lam, users, delays):

    users = users - 1
    client_dep = queue_.pop(0)
    delays.append(time-client_dep.arrival_time)
    if users > 0:
        service_time = np.random.exponential(lam)
        e2 = Event(time + service_time, "departure")
        client_dep.set_("departure")
        e2.assignClient(client_dep)
        FES.append(e2)
    return users, delays


utilizations = [0.1, 0.2, 0.4, 0.7, 0.8, 0.9, 0.95, 0.99]
# utilization = mu / lambda 
# Main loop

    
for u in utilizations:
    # Initializations
    id_client = 0
    users = 0
    delays = list()
    queue_ = list()
    FES = list()
    time = 0.0
    e0 = Event(time,"arrival")
    c0 = Client("arrival", time, id_client)
    e0.assignClient(c0)
    FES.append(e0)
    queue_.append(c0)
    avgs_per_window = list()

        

    # Simulation parameters
    np.random.seed(4899)
    
    confidence = 0.95
    SIM_TIME = 100000
    # mu must be more than lambda 
    mu = 1/u
    lam = 1
    users = 0
    while time < SIM_TIME:
        FES.sort()
        event = FES.pop(0)
        time = event.time
        if(event.typ == "arrival"):
            users = arrival(time, FES, queue_,mu,lam, users)
        elif(event.typ == "departure"):
            users, delays = departure(time, FES, queue_,lam, users, delays)

    cum_mean_per_event = cum_mean(delays)
    without_transient, idx = remove_transient(cum_mean_per_event, u)
    fig2, ax2 = plt.subplots(1,1)
    plot_metric(fig2, ax2, cum_mean_per_event , 'delay')
    ax2.axvline(x = idx, ymin=0, ymax=5, c = 'r',  label = 'end of transient')
    ax2.set_title(f'Event VS avg_delay_or_avg_length with u: {u}', fontsize=14)
    plt.show()


    correct_n = find_number_of_batches(without_transient, u, 10, 0.95)
    means, ci_lower, ci_upper = perform_batch_means(without_transient, correct_n=correct_n)
    fig3, ax3 = plt.subplots(1,1)
    plot_metric_with_ci(ax3, means, 'delays', ci_lower, ci_upper)
    ax3.set_title(f'Batch means result for u: {u}')
    plt.show()






# the utilization is lambda time the average service time. 
# for infinite queue the utilization should be always less than one otherwise
# the system is not stable. 
# utilization is the average amount of work requested to the server from customers arriving in the time unit
# lambda = 3 3 person per unit for time
# if the service time is 10 units of time it means that you need to work 30 units of time on average.
# utilization for single server queue cannot exceed 1

# devide in batch and evaluate the mean if the mean is less then the one of the previous one, that is the transient

# commentare il codice
# eventualmente capire perchè non funziona il confidence interval
# eventualmente capire che significa deterministic
