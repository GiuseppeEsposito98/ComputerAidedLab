from client import Client
from event import Event
from server import Server
import random
from scipy.stats import t
import matplotlib.pyplot as plt
import numpy as np

"""
In this laboratory we were asked to simulate a single server queue system (queue discipline: FIFO).
It is a system where the arrival time of the client is scheduled and if the server is already busy the client 
is added to the queue: that job will start when the server will not be busy. If the server is idle we check if the queue is empty, 
in this case interrupt the cycle otherwise schedule a new departure event for the inline client. 
(For debugging purposes I also kept track of the client to which each event is referred)
"""

# Initializations
id_client = 0
users = 0
list_of_instances_of_time = list()
# i need this because in case of arrival the service time with which i update the delay time must me 0
#service_time = 0
delays = list()
len_queue = list()
queue_ = []
FES = []
time = 0.0
seeds = [ 1232,1341, 5346, 3732]
e0 = Event(time,"arrival")
c0 = Client("arrival", time, id_client)
e0.assignClient(c0)
FES.append(e0)
queue_.append(c0)
random.seed(42)
np.random.seed(4899)

# Arrival function
def arrival(time, FES, queue_):
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
        #client_dep.set_("departure")
        e1.assignClient(client_dep)
        FES.append(e1)

# Departure function
def departure(time, FES, queue_):
    global users
    users = users - 1
    client_dep = queue_.pop(0)
    len_queue.append(len(queue_))
    delays.append(time-client_dep.arrival_time)
    if users > 0:
        service_time = np.random.exponential(lam)
        e2 = Event(time + service_time, "departure")
        client_dep.set_("departure")
        e2.assignClient(client_dep)
        FES.append(e2)
    

# Simulation parameters
SIM_TIME = 1_000
# mu must be more than lambda 
mu = 1/0.99
lam = 1
# utilization = mu / lambda 
# Main loop
while time < SIM_TIME:
    FES.sort()
    event = FES.pop(0)
    time = event.time
    if(event.typ == "arrival"):
        arrival(time, FES, queue_)
    elif(event.typ == "departure"):
        departure(time, FES, queue_)
    list_of_instances_of_time.append(time)
    #print(delay)


plt.plot(len_queue)
plt.title('CURRENT_TIME VS DELAYS', fontsize=14)
plt.xlabel('i')
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