from client import *
import numpy as np
from event import *
id_client = 0
mu = 3
lam = 4
users = 0
#num_servers = 2
#servers = []
queue_ = []
FES = []
time = 0.0
SIM_TIME = 30
e0 = Event(time,"arrival")
c0 = Client("arrival", time, id_client)
e0.assignClient(c0)
FES.append(e0)
queue_.append(c0)
# consider a multiserver queue
# compute the statistics
def arrival(time, FES, queue_):
    global users
    global id_client
    t_ia = np.random.exponential(1/mu)
    e = Event(time +t_ia, "arrival")
    users = users +1
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


while time < SIM_TIME:
    event = FES.pop(0)
    time = event.time
    if(event.typ == "arrival"):
        arrival(time, FES, queue_)
        queue_.sort()
    elif(event.typ == "departure"):
        departure(time, FES, queue_)
    FES.sort()
    print(event)