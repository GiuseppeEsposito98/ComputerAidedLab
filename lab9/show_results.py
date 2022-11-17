import matplotlib.pyplot as plt
import pandas as pd


# before removing transient
plt.plot(avg_lenghts_per_event)
plt.title('Event VS Avg_Delay', fontsize=14)
plt.xlabel('Event')
plt.ylabel('DELAYS')
plt.grid(True)
plt.show()

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

# after removing the transient
plt.plot(avg_lenghts_per_event)
plt.title('Event VS Avg_Delay', fontsize=14)
plt.xlabel('Event')
plt.ylabel('DELAYS')
plt.grid(True)
plt.show()