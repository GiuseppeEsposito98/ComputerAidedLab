# OVERVIEW
The idea of the simulation is: at the beginning N bins and N balls are generated and the until the number of balls has expired it keeps dropping the balls in the bins. The dropping policies are the following:
The balls are dropped in a random bin 
“D” bins are randomly chosen and the ball will be dropped in the least occupied bin.
The aim of this simulation is to study the variation in the occupancy level with respect to the dropping policy.

# FOLDER CONTENTS
- A main script that runs the simulation (lab07.py),
- A processing script that performs the bins and balls experiments with different parameters
- A file where are stored all the results for each policy and for each number of bins and balls
- A report where all the requested issues are addressed

# INSTRUCTION TO RUN
To run the file you have to install the numpy and matplotlib packages and then run the script lab07.py keeping it in the same folder of dropping_policy.py

# POSSIBLE EXTENSIONS
- The simulation can be run different times in order to compute the average of the requested metrics and than compare it with the theoretical boundaries of the confidence intervals.
- It could be interesting to study the cases in which the number of balls is different from the number of bins