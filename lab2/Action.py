import random
from copy import deepcopy
random.seed(302179)
class Action: 
    

    def move(coord:tuple, board_size):
        possible_move = [(0,0), (0,1), (0,-1),
                         (1,0), (1, 1), (1,-1), 
                         (-1,0), (-1,1), (-1,-1)]

        move_ = random.choice(possible_move)
        while move_[0] + coord[0] < 0 or move_[0] + coord[0] > board_size-1 or move_[1] + coord[1] < 0 or move_[1] + coord[1] > board_size-1:
            
            moves_ = possible_move[:]
            moves_.remove(move_)
            move_ = random.choice(moves_)
        return move_[0] + coord[0], move_[1] + coord[1]

    def compute_local_winner(board, player, other):
            winner = random.choice([0,1])
            if winner == 1:
                board.remove_player(other)
                board.matrix[other.coordinates] = 0
                player.increase_kill()
                return player.id_
            else:
                board.matrix[player.coordinates] = 0
                board.remove_player(player)
                other.increase_kill()
                return other.id_
        #return dist