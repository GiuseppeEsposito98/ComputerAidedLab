# Simulation of pop game

## OVERVIEW
The idea of the game is that initially a P number of player are randomly generated in a grid N x N and a clock start flowing. At each increment of the virtual time the position of each player is updated by a random movement, the distance between one player and all the others are computed. If two players’ distance is below the given threshold Thr, one of the two players at random is killed and the inner kill counter of the player is updated. The simulation will stop only when the number of players is just one. 

## ASSUMPTIONS
Before going into the deatail of the development it is noteworthy to specify the assumption i made in order to make the simulation meaningful:
    1. If after a new update of the position 3 players' distance is below the threshold, they will "fight" sorted by their id
    2. The movement of the players are discrete cell by cell and they can move in all directions, also diagonal
    3. Two player see eachother if they are below a threshold that is set to 1
    4. The initial position of the players are randomly computed
    5. There is no SIMULATION TIME beause one of the metrics i had to study was the time to win and since all my simulation converged even though some of them took a lot of time i decided to let them run
    6. The speed is set equal for all the players 
    7. We assume that all the players have at least one kill so that we can compute the average kills per player as (#initial_players-1)/#initial_players

## SIMULATION PARAMTER
In order to understand the behaviour of some metrics we tried different values of the following simulation parameter: 
    - Board edge (ROWS) = [10,50,100,200,500,700,1000,1500] 
    - Number of players (N) = [2,10,50,100,500]
    - Random seed = 9 to make the simulations repetable 

To make the simulations more balanced we tried the combinations of values that you can see in the file "results.csv"

## METRICS
With these simulations we wanted to compute the folloqing metrics: 
    - Time to win
    - Number of killed opponents for the winner
    - Average number of killed opponents fo all players

## DATA STRUCTURES
I created 3 custom classes which are:
    - Player: which contains the coordinates of each player, the kill counter, an incremental id which is unique.
    - Board: which contains the matrix where the player are placed, the list of players and the killed players.
    - Action: which is a class without attributes that i need to computw the new coordinates at each iteration and the winner of each fight.

## MAIN ALGORITHM 
begin
- initialize the board
- generate the N random player
- save them in a list
- compute the initial random position of the N players 
- for player in list_of_players:
    - for other in list_of_players:
        - compute the distance among all the players:
        - if this is below the threshold:
            - let the close players fight and choose the winner
            - increase the kill_counter of the winner
            - remove the beaten player from the board
- generate a random move between the 9 avilable
- if it is a valid one (the new coordinates of the players does not contain 0 and they are not greater than the board edge):  
    - update the position of the players.
end

## RUN INSTRUCTION
To run the script it is required to have all the files in the same folder and to have installed the numpy, pandas and matplotlib libraries and then run the file lab2.py. Then to try all the input parameter you just need to change the input parameter (which are defined at the begining of the file lab2.py) to the function "simulation" where the first is the numeber of rows, the second is the speed that is equal for each player and the last one is the number of players.

## GRAPHS
The graphs can be visualized by just running the file "show_results.py" which will plot the results that are already collected in the csv file of the folder and will save the png file in the folder called "graphs". 

## FUTURE IMPROVEMENT
Another interesting case study could be the use of some power ups. One of them could increase the probability of a player to win a fight for a given amount of time he meets any other player, in this way the metrics of average number of kill per player and kill of the winner could change accordingly. 
