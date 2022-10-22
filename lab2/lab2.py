from Player import Player
import numpy as np
import random
from board import Board
from Action import Action
from time import time, sleep
import csv

# SETTING CONSTANT VALUES
NUM_ROW = 200
players = 20
def simulation(ROWS, fixed_speed, num_of_players):
    id = 0
    RANDOM_SEED = 9
    THR = 1
    random.seed(RANDOM_SEED)


    # INITIALIZATIONS
    board = Board((ROWS, ROWS))
    for n in range(1, num_of_players +1):
        coordinates = (random.randint(0, ROWS-1), random.randint(0, ROWS-1))
        player = Player(coordinates, fixed_speed,n)
        board.save_players(player)

    time_ = 0

    while True:
        for player in board.list_of_players:
            for other in board.list_of_players:
                if (player.check_distance(other, THR) and player.id_ != other.id_):
                    Action.compute_local_winner(board, player, other)

        board.update_matrix()
        #print(board.matrix)
        if len(board.list_of_players)== 1:
            break
        time_ = time_ +1
   # print(len(board.killed))
    return time_, board.list_of_players[0], board.killed

time_, winner, killed_list = simulation(NUM_ROW, 1,players)


print("kill_winner:", winner.kill_counter)
print("time: ", time_)
# the fact that a player at random is killed is an assumption
# the game session is manages by a single virtual machine (assumption 2)
# people moves at random (assumption 3)
# initial conditions: where does the person starts?
# it's up to us
# of course create a class player that takes track of all the killed components
# in case of pair what happens?
# what does mean that they meet eachother ?
# what does happen if three player meet eachother?
# how is the speed encoded?
# we have to implement a clock that makes the time flowing in a discrete way
# work with timeslots(?)
# extension: powerups that spawn randomly on the map and are like: speed augmentation, increasing probability to win..
# coordinates or discrete movement?