
import numpy as np
import random
from utils import *
import matplotlib.pyplot as plt

# INPUT PARAMETERS
confidence = 0.95
SIM_TIME = 100000
k = 2

## Initializations  for each distribution type

# Initial time
time = 0.0

# List of delays of the clients
delays_low = list()
delays_high = list()
delays = list()


# Queues
# queue_dict= dict()
# for typ in ['low', 'high']:
#     queue_dict[typ] = Queue(typ)
queue_ = Queue()
id_client = 0
#priority_type = random.choice(['low', 'high'])
c0 = Client("arrival", time, id_client)#, priority=priority_type)
#queue_dict[priority_type].add_client(c0)
queue_.add_client(c0)
users = 0



# Servers
server_dict = dict()
for i in range(k):
    server_dict[f'server{i}'] = Server()

# Events
FES = list()
# first deault event
e0 = Event(time,"arrival")
e0.assignClient(c0)
FES.append(e0)
arr = 0
dep = 0

#freq_arrs = [0.2, 0.4, 0.8, 1.4, 2.0, 2.4, 2.8]
#possible_config = itertools.product([1, 0.5, 3.5], repeat = 2)
#for freq_arr in freq_arrs:
    #for params in possible_config:
while time < SIM_TIME:
    # the FES is sorted such that we have a FIFO service policy, so it is sorted with respect to the event with the 
    # least time the event has occurred
    FES.sort()
    event = FES.pop(0)
    # update the current time
    time = event.time
    if(event.typ == "arrival"):
        arr += 1
        id_client = arrival(time, FES, queue_, server_dict, users, id_client)
    elif(event.typ == "departure"):
        dep +=1
        delays = departure(time, FES, queue_, server_dict, users, delays)
    #print(event)
# print(arr)
# print(dep)
cum_avg = cum_mean(delays)
fig2, ax2 = plt.subplots(1,1)
plot_metric(fig2, ax2, cum_avg , 'Delay', x_label='#departure_event')
fig2.savefig('prova_delays')
# da riscrivere nellottica che quello che sto simulando è la FES sostanzialmente
# quindi quando vado in arrival calcola che quando genero un tempo di servizio posso salvare il tempo di servizio nell'
# oggetto cliente e tenere traccia lì dentro così quando mi serve ce l'ho.
# il cliente arriva,
# si controlla se i server sono idle
# se almeno uno dei due non lo è
#   aggiungi il cliente al server 
#   imposta lo status del server a busy
# altrimenti
#   controlla il cliente che i due server stanno servendo
#   se entrambi sono high priority
#       aggiungi il cliente appena arrivato alla queue (high priority)
#   altrimenti
#       ferma il processo del server che sta servendo il cliente con low_priority
#       in caso di parità scegli un server a caso dal quale rimuovere il cliente
#       estrai il relativo cliente
#       se c'è spazio nella coda:
#           aggiungilo alla coda che gli spetta di modo che sia il primo servito 
#               (probabilmente non ce ne sarà bisogno perchè sarà quello con il tempo di interarrival time minore)
#       altrimenti:
#           non aggiungere alla cosa e lascialo stare
#       e definisci un tempo di servizio rimanente che sarà il tempo corrente meno il tempo di servizio 
#           precentemente generato per quel cliente meno l'interarrival time del cliente che deve essere servito probabilmente questo sarà da registrare nei delay
#       aggiorna lo stato del server a busy_high
#       estrai randomicamente un tempo di servizio per il nuovo cliente
#       crea un evento departure a tempo_corrente + service_time



## obiettivi a piccoli passi:
# implementare la coda come classe
# testare

# implementare un server come classe
# testare

# implementare 1 coda, 2 server
# testare

# implmenetare 2 code, 2 server
# testare
