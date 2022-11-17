from client import Client
from event import *
#import random
from scipy.stats import t
import matplotlib.pyplot as plt
import numpy as np
import csv

"""
In this laboratory we were asked to simulate a single server queue system (queue discipline: FIFO).
It is a system where the arrival time of the client is scheduled and if the server is already busy the client 
is added to the queue: that job will start when the server will not be busy. If the server is idle we check if the queue is empty, 
in this case interrupt the cycle otherwise schedule a new departure event for the inline client. 
(For debugging purposes I also kept track of the client to which each event is referred)
"""

def arrival(time, FES, queue_, mu, lam):
    global users 
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
        service_time = np.random.exponential(lam)
        client_dep = Client("departure", time+ service_time, id_client)
        e1 = Event(time + service_time, "departure")
        e1.assignClient(client_dep)
        FES.append(e1)

# Departure function
def departure(time, FES, queue_, lam):
    global users
    users = users - 1
    client_dep = queue_.pop(0)
    delays.append(time-client_dep.arrival_time)
    if users > 0:
        service_time = np.random.exponential(lam)
        e2 = Event(time + service_time, "departure")
        client_dep.set_("departure")
        e2.assignClient(client_dep)
        FES.append(e2)


# Initializations
id_client = 0
users = 0
delays = list()
len_queue = list()
queue_ = []
FES = []
time = 0.0
e0 = Event(time,"arrival")
c0 = Client("arrival", time, id_client)
e0.assignClient(c0)
FES.append(e0)
queue_.append(c0)
avgs_per_window = list()

    

# Simulation parameters
np.random.seed(4899)
seeds = [1232,1341, 5346, 3732]
utilizations = [0.1, 0.2, 0.4, 0.7, 0.8, 0.9, 0.95, 0.99]
confidence = 0.95
SIM_TIME = 500
# mu must be more than lambda 
mu = 1/0.99
lam = 1
# utilization = mu / lambda 
# Main loop
with open("results.csv", "w") as csvf:
    header="queue length,avg length per event(incremental mean),CAPIRE COSA METTERCI, AKA COSA PLOTTARCI\n"
    csvf.write(header)
    
with open("results.csv", "a") as csvf:
    # DA QUI IN POI PROBABILMENTE VA TUTTO INDENTATO
    while time < SIM_TIME:
        FES.sort()
        event = FES.pop(0)
        time = event.time
        if(event.typ == "arrival"):
            arrival(time, FES, queue_,mu,lam)
        elif(event.typ == "departure"):
            departure(time, FES, queue_,lam)
        csvf.write(f"{len(queue_)}")
        len_queue.append(len(queue_))

# quindi prima calcoliamo la lunghezza media della coda ogni evento
# tu stai facendo la lunghezza della coda diviso l'indice dell'evento a cui ti trovi.
avg_lenghts_per_event = [l/(e+1) for e,l in enumerate(len_queue)] ##
# questa cosa può essere fatta nel while con un counter al posto di "e" e i valori di len al posto di l

plt.plot(avg_lenghts_per_event)
plt.title('Event VS Avg_Delay', fontsize=14)
plt.xlabel('Event')
plt.ylabel('DELAYS')
plt.grid(True)
plt.show()
# quindi definiamo una window di 10 eventi 
# e calcoliamo la media delle medie delle persone nella coda ad ogni evento
avgs_per_window = list()
for i in range(len(avg_lenghts_per_event)):
    if i % 5 == 0:
        avg = sum([avg_lenghts_per_event[j] for j in range(i-10,i)])/10
        avgs_per_window.append(avg)




thr = 0.010
for i in range(len(avgs_per_window)):
    if abs(avgs_per_window[i-1] - avgs_per_window[i]) > thr:
    # these i's corresponds to a window of 10 events so if i multiply it by 20, we will get the steady state on the original graph
    # one idea to make it adaptable to different cases so that it becomes automatic, is to tune the lenght of the window with respect to the period of the steady state wave function
    # and the threshold which idk.
      for j in range((i-1)*5, i*5):
        avg_lenghts_per_event.pop(j)

# scrivere anche la avg_lenghts_per_event di nuovo perchè qui ho rimosso il transiente


plt.plot(avgs_per_window, marker = "o")
plt.title('Event VS Avg', fontsize=14)
plt.xlabel('Event')
plt.ylabel('Avg')
plt.grid(True)
plt.show()

plt.plot(delays)
plt.title('Event VS Delay', fontsize=14)
plt.xlabel('Event')
plt.ylabel('Delay_per_client_which_is_in_departure')
plt.grid(True)
plt.show()

plt.plot(len_queue)
plt.title('Event VS length_of_the_queue', fontsize=14)
plt.xlabel('Event')
plt.ylabel('length of the queue')
plt.grid(True)
plt.show()


plt.plot(avg_lenghts_per_event)
plt.title('Event VS Avg_Delay', fontsize=14)
plt.xlabel('Event')
plt.ylabel('DELAYS')
plt.grid(True)
plt.show()



# the utilization is lambda time the average service time. 
# for infinite queue the utilization should be always less than one otherwise
# the system is not stable. 
# utilization is the average amount of work requested to the server from customers arriving in the time unit
# lambda = 3 3 person per unit for time
# if the service time is 10 units of time it means that you need to work 30 units of time on average.
# utilization for single server queue cannot exceed 1

# devide in batch and evaluate the mean if the mean is less then the one of the previous one, that is the transient


# new_lst = list()
# for i in range(len(delays)):
#     new_lst.append(delays[i])
#     if i % 100 == 0:
#         new_list = list()