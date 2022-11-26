
import numpy as np
import random
import itertools
from useful_classes import *
from sympy import symbols, Eq, solve

# possible parameters of distributions
# arrival
# for both high and low_priority


#service
# case a
# for both high and low priority
one_over_mu_a = 1

# case b
# 0.5 for low_priority, 1.5 for high_priority
one_over_mu_P = (0.5, 1.5)


def arrival(time, FES, queue_, server_dict, users, id_client, distribution= 'exponential'):
    '''
    This function computes a random instance of time,
    add an even to the FES (Future Event Set),
    add a client to the queue whose label is 'arrival' and whose id is a constantly increasing counter
    '''
    if distribution == 'hyperexponential':
        lam = generate_hyperexponential()
    elif distribution == 'deterministic_process':
        lam = 1
    elif distribution == 'exponential':
        lam=1

    # inter arrival time
    t_ia = np.random.exponential(lam)
    e = Event(time +t_ia, "arrival")
    # id_client is used to check whether a specific client has just one arrival and one departure (debugging purposes)
    id_client = id_client + 1 
    client_arr = Client("arrival", time, id_client)
    # i'm taking track of the corresponding client in the event object
    e.assignClient(client_arr)
    FES.append(e)
    # increase the counter of users in the system
    #users = users +1
    # if all the servers are busy
    if all(server.status == 'busy' for server in server_dict.values()):    
        queue_.client_list.append(client_arr)
    # otherwise if there is at least one that is idle
    else:
        for server in server_dict.values():
            if server.status == 'idle':
                # the distribution can be either ['hyperexponential', 'exponential']
                if distribution == 'hyperexponential':
                    service_time = generate_hyperexponential()
                elif distribution == 'deterministic_process':
                    service_time = 1
                elif distribution == 'exponential':
                    service_time = np.random.exponential(1)
                server.set_client(client_arr)
                server.set_status('busy')
                client_dep = Client(status = "departure", arrival_time= t_ia, id_client = id_client)
                e1 = Event(time + service_time, "departure")
                e1.assignClient(client_dep)
                FES.append(e1)
                break      
    return id_client


# Departure function
def departure(time, FES, queue_, server_dict, users, delays, distribution= 'exponential'):
    # is the queue counter is greater than 0 make the server busy
    if len(queue_.client_list) > 0:
        # remove the first client added in the queue (FIFO policy)
        client_dep = queue_.client_list.pop(0)
        # delays are time the client just popped from the queue has spent in the queue
        delays.append(time-client_dep.arrival_time)
        # the distribution can be either ['hyperexponential', 'uniform']
        if distribution == 'hyperexponential':
            service_time = generate_hyperexponential()
        elif distribution == 'deterministic_process':
            service_time = 1
        elif distribution == 'exponential':
            service_time = np.random.exponential(1)
        e2 = Event(time + service_time, "departure")
        # set the label of the client just popped to 'departure'
        client_dep.set_status("departure")
        e2.assignClient(client_dep)
        FES.append(e2)
    else:
        server_dict['server0'].set_status('idle')
        server_dict['server1'].set_status('idle')
    return delays



def generate_hyperexponential(params):
    '''
    Generate numbers from an hyperexponential distribution
    '''
    # this value is to garantee the same probability to choose the l1 or l2
    x, y = symbols('x y')
    eq1 = Eq(0.5*x + 0.5*y - params[0])
    eq2 = Eq(x**2 - y**2 - (params[1]*10)**2)
    freq1, freq2 = solve([eq1,eq2])[0]
    u = np.random.uniform(0,1)
    if u <= 0.5:
        service = np.random.exponential(1/freq1)
    else:
        service = np.random.exponential(1/freq2)

    return service

def cum_mean(arr):
    '''
    This function compute the cumulative mean weighted on the number of events. The structure of the resulting array is
    the following:
    [
        cum_mean_1 = delay1 / 1,
        cum_mean_2 = (delay1 + delay2) / 2,
        ...
        cum_mean_n =(delay1 + delay2 + delay3 + ... + delay_n) / total_number_of_departure
    ]
    '''
    cum_sum = np.cumsum(arr,axis=0)
    for i in range(cum_sum.shape[0]):
        if i == 0:
            continue
        cum_sum[i] = cum_sum[i]/(i+1)
    return cum_sum

def plot_metric_with_ci(ax,
                list_per_event: list,
                label_: str,
                ci_lower: list,
                ci_upper: list,
                x_label = 'Event',
                marker: str = None,
                log_scale: bool = False
                ):
    '''
        This function plot a generic array of delays with standard functions of matplotlib.pyplot
        when a confidence interval is requested
    '''
    ax.plot(list_per_event, label = label_, marker = marker)
    ax.set_xlabel(x_label)
    ax.set_ylabel('Delays (time unit)')
    ax.grid(True)
    # plot confidence interval
    ax.fill_between([x for x in range(len(list_per_event))], ci_lower, ci_upper, alpha = .5, label = f'{label_} confidence interval 95%')
    if log_scale:
        ax.xscale("log")
        ax.yscale("log")
    ax.legend()

def plot_metric(fig,
                ax,
                list_per_event: list,
                label: str,
                marker: str = None,
                log_scale: bool = False,
                x_label = 'Event'
                ):
    
    '''
    This function plot a generic array of delays with standard functions of matplotlib.pyplot when a confidence interval 
    is not requested
    '''
    ax.plot(list_per_event, label = label, marker = marker)
    ax.set_xlabel(x_label)
    ax.set_ylabel('Delays (time unit)')
    ax.grid(True)
    if log_scale:
        ax.xscale("log")
        ax.yscale("log")
    ax.legend()




"""def arrival(time, FES, queue_dict, id_client, params = None, freq_arr = None, distribution= 'exponential'):
    '''
    This function computes a random instance of time,
    add an even to the FES (Future Event Set),
    add a client to the queue whose label is 'arrival' and whose id is a constantly increasing counter
    '''

    if distribution == 'hyperexponential':
        lam = generate_hyperexponential(params)
    elif distribution == 'deterministic_process':
        lam = 1
    elif distribution == 'exponential':
        lam = 1/freq_arr

    # inter arrival time
    t_ia = np.random.exponential(lam)
    e = Event(time +t_ia, "arrival")
    # id_client is used to check whether a specific client has just one arrival and one departure (debugging purposes)
    id_client = id_client + 1 
    priority_type = random.choice(['low', 'high'])
    client_arr = Client("arrival", time, id_client, priority_type)
    queue_dict[priority_type].add_client(client_arr)
    # i'm taking track of the corresponding client in the event object
    e.assignClient(client_arr)
    FES.append(e)
    # is there is exactly one user in the queue make the server busy
    if any(server.status == 'idle' for server in server_dict.values()):
        # the distribution can be either ['hyperexponential', 'uniform']
        if distribution == 'hyperexponential':
            service_time = generate_hyperexponential(params)
        elif distribution == 'deterministic_process':
            service_time = 1
        elif distribution == 'exponential':
            service_time = np.random.exponential(1)
        client_dep = Client("departure", time+ service_time, id_client)
        e1 = Event(time + service_time, "departure")
        e1.assignClient(client_dep)
        FES.append(e1)
    elif all(server.status == 'busy' for server in server_dict.values()) and client_arr.typ == 'high' and any(server.client.typ == 'low' for server in server_dict.values()):
        for server in server_dict.values():
            if server.client.typ == 'low':
                pass"""