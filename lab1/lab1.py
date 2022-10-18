from client import Client
from event import Event
from server import Server
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
queue_ = []
FES = []
time = 0.0
e0 = Event(time,"arrival")
c0 = Client("arrival", time, id_client)
e0.assignClient(c0)
FES.append(e0)
queue_.append(c0)


# Arrival function
def arrival(time, FES, queue_):
    global users 
    global id_client
    t_ia = np.random.exponential(1/mu)
    e = Event(time +t_ia, "arrival")
    users = users +1
    # id_client is used to check whether a specific client has just one arrival and one departure (debugging purposes)
    id_client = id_client + 1 
    client_arr = Client("arrival", time, id_client)
    e.assignClient(client_arr)
    FES.append(e)
    queue_.append(client_arr)
    if(users == 1):
        client_dep = queue_.pop(0)
        service_time = np.random.exponential(1/lam)
        e1 = Event(time + service_time, "departure")
        client_dep.set_("departure")
        e1.assignClient(client_dep)
        FES.append(e1)

# Departure function
def departure(time, FES, queue_):
    global users
    users = users - 1
    if users > 0:
        client_dep = queue_.pop(0)
        service_time = np.random.exponential(1/lam)
        e2 = Event(time + service_time, "departure")
        client_dep.set_("departure")
        e2.assignClient(client_dep)
        FES.append(e2)

# Simulation parameters
num_servers = 2
SIM_TIME = 100
mu = 3
lam = 4

# Main loop
while time < SIM_TIME:
    event = FES.pop(0)
    time = event.time
    if(event.typ == "arrival"):
        arrival(time, FES, queue_)
    elif(event.typ == "departure"):
        departure(time, FES, queue_)
    queue_.sort()
    FES.sort()
    print(event)



