
import random
from lab14.utils import *
import matplotlib.pyplot as plt

# INPUT PARAMETERS
confidence = 0.95
SIM_TIME = 100000
k = 2


# possible distirbutions 
distributions = ['exponential', 'hyperexponential', 'deterministic_process']

# 2 possible case studies defined for different values of utilization

freq_arrs = [0.2, 0.4, 0.8, 1.4, 2.0, 2.4, 2.8]
case = input("Choose the case among a (E[S]_HP = E[S]_LP = 1), b (E[S]_HP = 1/2, E[S]_LP = 3/2): ")
for freq in freq_arrs:
    for distribution in distributions:
        ## Initializations 

        # Initial time
        time = 0.0

        # List of delays of the clients
        delays_low = list()
        delays_high = list()
        delays = list()



        # Queue
        max_size = 1000
        queue = list()
        

        # Initialization first client
        id_client = 0
        priority_type = random.choice(['low', 'high'])
        c0 = Client("arrival", time, id_client, priority=priority_type)
        queue.append(c0)
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

        while time < SIM_TIME:
            # the FES is sorted such that we have a FIFO service policy, so it is sorted with respect to the event with the 
            # least time the event has occurred
            FES.sort()
            event = FES.pop(0)
            # update the current time
            time = event.time

            if event.time < time:  
                event.time = time
            t_curr = event.time

            if event.typ == "arrival":
                for i in range(k-1):
                    # If the first server is idle
                    if server_dict[f'server{i}'].status == 'idle':
                        # make it busy
                        users, id_client = arrival(1/freq, 1/freq, distribution, case, queue, max_size, FES, server_dict[f'server{i}'], time, id_client, users)
                        arr = arr+1
                    # If the second server is idle
                    elif server_dict[f'server{i+1}'].status == 'idle':
                        # make it busy
                        users, id_client = arrival(1/freq, 1/freq, distribution, case, queue, max_size, FES, server_dict[f'server{i+1}'], time, id_client, users)
                        arr = arr+1
                    # If both the servers are busy but a HP arrives
                    elif event.client.priority == "high":
                        # if the servers are both busy with an HP
                        if server_dict[f'server{i}'].client.priority == "high" and server_dict[f'server{i+1}'].client.priority == "high":
                            # then treat it as a normal arrival
                            users, id_client = arrival(1/freq, 1/freq, distribution, case, queue, max_size, FES, server_dict[f'server{i}'], time, id_client, users)
                        else:
                            # otherwise, stop a service to start the HP one.
                            users, id_client = high_arrival(server_dict, users, time, FES, queue, distribution, case, 1/freq, 1/freq, max_size, id_client)
                        arr = arr+1
            elif event.typ == "departure":
                users= departure(users,time, FES, queue, distribution, case, 1/freq, 1/freq, delays_low, delays_high, delays)
                dep = dep+1


cum_avg_low = cum_mean(delays_low)
cum_avg_high = cum_mean(delays_high)
fig2, ax2 = plt.subplots(1,1)
plot_metric(fig2, ax2, cum_avg_low , 'Delay low', x_label='#departure_event')
plot_metric(fig2, ax2, cum_avg_high , 'Delay high', x_label='#departure_event')
fig2.savefig('prova_delays')

