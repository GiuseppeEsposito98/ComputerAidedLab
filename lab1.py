from client import *
import random
from event import *
mu = 3
lam = 4
users = 0
queue = []
FES = []
time = 0.0
SIM_TIME = 30
e0 = Event(0,"arrival")
FES.append(e0)
# consider a multiserver queue
# compute the statistics
# prova a fare con le tuple
def arrival(time, FES, queue):
    global users
    t_ia = random.expovariate(1.0/mu)
    e = Event(time +t_ia, "arrival")
    FES.append(e)
    users +=1
    client = Client("arrival", time)
    queue.append(client)
    # if users == 1 significa "if the server is idle" perchè significa che users è stato appena incrementato quindi significa che il server era idle
    if(users == 1):
        service_time = random.expovariate(1/lam)
        e1 = Event(time + service_time, "departure")
        FES.append(e1)


def departure(time, FES, queue):
    global users
    client = queue.pop(0)
    users -=1
    # are there more client in line?
    if users > 0:
        service_time = random.expovariate(1/lam)
        e2 = Event(time + service_time, "departure")
        FES.append(e2)


while time < SIM_TIME:
    event = FES.pop(0)
    time += event.duration
    if(event.typ == "arrival"):
        arrival(time, FES, queue)
    elif(event.typ == "departure"):
        departure(time, FES, queue)
    # pensa che qua stai stampando t_ia e t_service perchè tu gli stai salvando quello nell'oggetto, forse quello che dovresti salvare è il tempo corrente
    FES.sort()
    print(event)