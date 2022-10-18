from Player import Player
import numpy as np
import random
from board import Board
# SETTING CONSTANT VALUES
id = 0
ROWS = 8
COLS = 8
fixed_speed = 3
NUMBER_OF_PLAYERS = 4
RANDOM_SEED = 31 
THR = 1
#np.random.seed(RANDOM_SEED)
distance_matrix = np.zeros((NUMBER_OF_PLAYERS, NUMBER_OF_PLAYERS), dtype=object)

# INITIALIZATIONS
board = Board((ROWS, COLS))
for n in range(NUMBER_OF_PLAYERS):
    coordinates = (np.random.randint(0, ROWS), np.random.randint(0, ROWS))
    player = Player(coordinates, fixed_speed, id)
    board.save_players(player)
    id += 1

# these nested for are to control if the just spawned players are already under the threshold
for player in sorted(board.list_of_players, key=lambda a: a.id_):
    for other in sorted(board.list_of_players, key=lambda a: a.id_):
        if(player.id_ != other.id_):
            while player.check_distance(other, THR):
                player.coordinates = (np.random.randint(0, ROWS), np.random.randint(0, COLS))
        distance_matrix[player.get_id(), other.get_id()] = player.compute_distance(other)


print(distance_matrix)




# the fact that a player at random is killed is an assumption
# the game session is manages by a single virtual machine (assumption 2)
# people moves at random (assumption 3)
# initial conditions: where does the person starts?
#  it's up to us
# of course create a class player that takes track of all the killed components
# in case of pair what happens?
# what does mean that they meet eachother ?
# what does happen if three player meet eachother?
# how is the speed encoded?
# we have to implement a clock that makes the time flowing in a discrete way
# work with timeslots(?)
# extension: powerups that spawn randomly on the map and are like: speed augmentation, increasing probability to win..
# coordinates or discrete movement?