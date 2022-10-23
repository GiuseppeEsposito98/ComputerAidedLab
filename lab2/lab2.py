from Player import Player
import random
from board import Board
from Action import Action
from time import time, sleep

# SETTING CONSTANT VALUES
NUM_ROW = 100
players = 10
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

    # Main
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
    return time_, board.list_of_players[0], board.killed
    # I return also the only existring element of the list_of_players that at the end will contain only the winner

time_, winner, killed_list = simulation(NUM_ROW, 1,players)


print("kill_winner:", winner.kill_counter)
print("time: ", time_)