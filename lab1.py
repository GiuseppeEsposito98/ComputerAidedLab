from client import *
import numpy as np
from event import *
id_client = 0
mu = 3
lam = 4
users = 0
queue = []
FES = []
time = 0.0
SIM_TIME = 30
e0 = Event(0,"arrival")
c0 = Client("arrival", 0, id_client)
e0.assignClient(c0)
FES.append(e0)
queue.append(c0)
# consider a multiserver queue
# compute the statistics
# prova a fare con le tuple
def arrival(time, FES, queue):
    global users
    global id_client
    t_ia = np.random.exponential(1.0/mu)
    e = Event(time +t_ia, "arrival")

    users = users +1
    id_client+=1
    client_arr = Client("arrival", time, id_client)
    e.assignClient(client_arr)
    FES.append(e)
    queue.append(client_arr)
    # if users == 1 significa "if the server is idle" perchè significa che users è stato appena incrementato quindi significa che il server era idle
    if(users == 1):
        service_time = np.random.exponential(1/lam)
        e1 = Event(time + service_time, "departure")
        client_arr.set_("departure")
        e1.assignClient(client_arr)
        FES.append(e1)


def departure(time, FES, queue):
    global users
    users = users - 1
    # are there any client in line?
    if users > 0:
        client_dep = queue.pop(0)
        service_time = np.random.exponential(1/lam)
        e2 = Event(time + service_time, "departure")
        client_dep.set_("departure")
        e2.assignClient(client_dep)
        FES.append(e2)


while time < SIM_TIME:
    event = FES.pop(0)
    time += event.time
    if(event.typ == "arrival"):
        arrival(time, FES, queue)
        queue.sort()
    elif(event.typ == "departure"):
        departure(time, FES, queue)
    # pensa che qua stai stampando t_ia e t_service perchè tu gli stai salvando quello nell'oggetto, forse quello che dovresti salvare è il tempo corrente
    FES.sort()
    print(event)