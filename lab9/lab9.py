import matplotlib.pyplot as plt
import numpy as np
from simulation import *

"""
In this laboratory we were asked to simulate a single server queue system (queue discipline: FIFO).
It is a system where the arrival time of the client is scheduled and if the server is already busy the client 
is added to the queue: that job will start when the server will not be busy. If the server is idle we check if the queue is empty, 
in this case interrupt the cycle otherwise schedule a new departure event for the inline client. 
(For debugging purposes I also kept track of the client to which each event is referred)
"""

def arrival(time, FES, queue_, users, u, distribution= 'exponential'):
    '''
    This function computes a random instance of time,
    add an even to the FES (Future Event Set),
    add a client to the queue whose label is 'arrival' and whose id is a constantly increasing counter
    '''
    global id_client
    # inter arrival time
    if distribution == 'hyperexponential':
        lam = generate_hyperexponential()
    elif distribution == 'deterministic_process':
        lam = 1
    elif distribution == 'exponential':
        service_time = generate_exponential_service_time()
        lam=1
    else:
        service_time = generate_service_time()

    t_ia = generate_arrival_time(lam/u)
    e = Event(time +t_ia, "arrival")
    # id_client is used to check whether a specific client has just one arrival and one departure (debugging purposes)
    id_client = id_client + 1 
    client_arr = Client("arrival", time, id_client)
    # i'm taking track of the corresponding client in the event object
    e.assignClient(client_arr)
    FES.append(e)
    # increase the counter of users in the system
    users = users +1
    queue_.append(client_arr)
    # is there is exactly one user in the queue make the server busy
    if(users == 1):
        # the distribution can be either ['hyperexponential', 'uniform']
        if distribution == 'hyperexponential':
            service_time = generate_hyperexponential()
        elif distribution == 'deterministic_process':
            service_time = 1
        elif distribution == 'exponential':
            service_time = generate_exponential_service_time()
        else:
            service_time = generate_service_time()
        client_dep = Client("departure", time+ service_time, id_client)
        e1 = Event(time + service_time, "departure")
        e1.assignClient(client_dep)
        FES.append(e1)
    return users

# Departure function
def departure(time, FES, queue_, users, delays, distribution= 'exponential'):
    # when a user is leaving decrease the user counter
    users = users - 1
    # remove the first client added in the queue (FIFO policy)
    client_dep = queue_.pop(0)
    # delays are time the client just popped from the queue has spent in the queue
    delays.append(time-client_dep.arrival_time)
    # is the queue counter is greater than 0 make the serve busy
    if users > 0:
        # the distribution can be either ['hyperexponential', 'uniform']
        if distribution == 'hyperexponential':
            service_time = generate_hyperexponential()
        elif distribution == 'deterministic_process':
            service_time = 1
        elif distribution == 'exponential':
            service_time = generate_exponential_service_time()
        else:
            service_time = generate_service_time()
        e2 = Event(time + service_time, "departure")
        # set the label of the client just popped to 'departure'
        client_dep.set_("departure")
        e2.assignClient(client_dep)
        FES.append(e2)
    return users, delays

np.random.seed(30179)
utilizations = [0.1, 0.2, 0.4, 0.7, 0.8, 0.9, 0.95, 0.99]

mean_exp = list()
lower_bounds_exp = list()
upper_bounds_exp = list()  

mean_hyperexp = list()
lower_bounds_hyperexp = list()
upper_bounds_hyperexp = list()  

mean_det = list()
lower_bounds_det = list()
upper_bounds_det = list()   
# Main loop
for distribution in ['exponential', 'hyperexponential', 'deterministic_process']:     
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
        
        confidence = 0.95
        SIM_TIME = 100000

        
        users = 0

        while time < SIM_TIME:
            # the FES is sorted such that we have a FIFO service policy, so it is sorted with respect to the event with the 
            # least time the event has occurred
            FES.sort()
            event = FES.pop(0)
            # update the current time
            time = event.time
            if(event.typ == "arrival"):
                users = arrival(time, FES, queue_, users, u, distribution)
            elif(event.typ == "departure"):
                users, delays = departure(time, FES, queue_, users, delays, distribution)
        cum_mean_per_event = cum_mean(delays)
        without_transient, idx = remove_transient(cum_mean_per_event, u, distribution)

        # plot average delays per departure event (end of warm-up transient detection)
        fig2, ax2 = plt.subplots(1,1)
        plot_metric(fig2, ax2, cum_mean_per_event , 'delay')
        # plot a vertical line when the transient has ended
        ax2.axvline(x = idx, ymin=0, ymax=5, c = 'r',  label = 'end of transient')
        ax2.set_title(f'#departure_event VS cumulative_average_delay \nUtilization_level: {u}\nDistribution: {distribution}', fontsize=14)
        fig2.savefig(f'graphs/{distribution}/with u: {u}, (transient detection) #departure_event VS cumulative_average_delay.png')
        plt.close()


        # compute the correct number of batches
        correct_num_batches = find_batches(without_transient, u, 10, confidence)

        #compute the mean for each batch and consequently the confidence interval
        means, ci_lower_bounds, ci_upper_bounds = batch_means(without_transient, correct_num_batches = correct_num_batches)
        # plot the average delays per departure event as result of batch means algorithm 
        fig3, ax3 = plt.subplots(1,1)
        plot_metric_with_ci(ax3, means, 'delays', ci_lower_bounds, ci_upper_bounds)
        ax3.set_title(f'#departure_event VS cumulative_average_delay\nUtilization_level: {u}\nDistribution: {distribution}')
        fig3.savefig(f'graphs/{distribution}/with u: {u}, (batch mean) #departure_event VS cumulative_average_delay.png')
        plt.close()

        if distribution == 'hyperexponential':
            mean_hyperexp.append(np.mean(means))
            ci_hyperexp = t.interval(0.95, len(means)-1, np.mean(means), np.std(means))
            lower_bounds_hyperexp.append(ci_hyperexp[0])
            upper_bounds_hyperexp.append(ci_hyperexp[1]) 
        elif distribution == 'deterministic_process':
            mean_det.append(np.mean(means))
            ci_det = t.interval(0.95, len(means)-1, np.mean(means), np.std(means))
            lower_bounds_det.append(ci_det[0])
            upper_bounds_det.append(ci_det[1])
        elif distribution == 'exponential':
            mean_exp.append(np.mean(means))
            ci_exp = t.interval(0.95, len(means)-1, np.mean(means), np.std(means))
            lower_bounds_exp.append(ci_exp[0])
            upper_bounds_exp.append(ci_exp[1])


fig4, ax4 = plt.subplots(1,1)
fig4.suptitle(distribution)
ax4.plot(utilizations, mean_exp, label = 'exponential')
ax4.plot(utilizations, mean_hyperexp, label = 'hyperexponential')
ax4.plot(utilizations, mean_det, label = 'deterministic')
ax4.fill_between(utilizations, lower_bounds_exp, upper_bounds_exp, alpha = .5)
ax4.fill_between(utilizations, lower_bounds_hyperexp, upper_bounds_hyperexp, alpha = .5)
ax4.fill_between(utilizations, lower_bounds_det, upper_bounds_det, alpha = .5)
ax4.set_xlabel('Utilization level')
ax4.set_ylabel('Delays')
ax4.grid(True)
ax4.legend()
plt.savefig(f'graphs/Utilization VS delays.png')

'''for u in utilizations:
    # Initializations
    id_client = 0
    users = 0
    # list of delays of the clients
    delays = list()
    # list of clients
    queue_ = list()
    FES = list()
    # initial time 
    time = 0.0
    e0 = Event(time,"arrival")
    c0 = Client("arrival", time, id_client)
    # setup the initial values of the lists
    e0.assignClient(c0)
    FES.append(e0)
    queue_.append(c0)
    avgs_per_window = list()

        

    # Simulation parameters
    np.random.seed(42)
    
    confidence = 0.95
    SIMULATION_TIME = 100000

    # parameter for the inter arrival time generator in function of u
    mu = 1/u
    # parameter for the inter arrival time generators
    lam = 1
    users = 0
    while time < SIMULATION_TIME:
        # the FES is sorted such that we have a FIFO service policy, so it is sorted with respect to the event with the least
        # time the event has occurred
        FES.sort()
        event = FES.pop(0)
        # update the current time
        time = event.time
        if(event.typ == "arrival"):
            users = arrival(time, FES, queue_,mu,lam, users, distribution)
        elif(event.typ == "departure"):
            users, delays = departure(time, FES, queue_,lam, users, delays, distribution)

    #cumulative mean of delays per event
    cum_mean_per_event = cum_mean(delays)

    # detect and remove transient
    without_transient, idx = remove_transient(cum_mean_per_event, u)

    # plot delays per event
    fig2, ax2 = plt.subplots(1,1)
    plot_metric(fig2, ax2, cum_mean_per_event , 'delay')
    # plot a vertical line when the transient has ended
    ax2.axvline(x = idx, ymin=0, ymax=5, c = 'r',  label = 'end of transient')
    ax2.set_title(f'Event VS cumulative_average_delay with u: {u}', fontsize=14)
    fig2.savefig(f'graphs/{distribution}/Event VS cumulative_average_delay (transient detection) with u: {u}.png')
    plt.close()

    # compute the correct number of batches
    correct_num_batches = find_batches(without_transient, u, 10, confidence)

    #compute the mean for each batch and consequently the confidence interval
    means, ci_lower_bounds, ci_upper_bunds = batch_means(without_transient, correct_num_batches = correct_num_batches)
    # plot delays per event on a smoothed graph using batch means
    fig3, ax3 = plt.subplots(1,1)
    plot_metric_with_ci(ax3, means, 'delays', ci_lower_bounds, ci_upper_bunds)
    ax3.set_title(f'Batch means result for u: {u}')
    fig3.savefig(f'graphs/{distribution}/Event VS cumulative_average_delay (batch mean) with u: {u}.png')
    plt.close()
'''









# the utilization is lambda time the average service time. 
# for infinite queue the utilization should be always less than one otherwise
# the system is not stable. 
# utilization is the average amount of work requested to the server from customers arriving in the time unit
# lambda = 3 3 person per unit for time
# if the service time is 10 units of time it means that you need to work 30 units of time on average.
# utilization for single server queue cannot exceed 1


