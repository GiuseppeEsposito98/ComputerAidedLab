import random
random.seed(302179)
class Action: 
    

    def move(player, board_size):
        '''Generate a random and ADMISSIBLE movement'''
        possible_move = [(0,0), (0,1), (0,-1),
                         (1,0), (1, 1), (1,-1), 
                         (-1,0), (-1,1), (-1,-1)]

        move_ = random.choice(possible_move)
        coord = player.coordinates[:]
        speed = player.speed
        while speed*(move_[0] + coord[0]) < 0 or speed*(move_[0] + coord[0]) > board_size-1 or speed*(move_[1] + coord[1]) < 0 or speed*(move_[1] + coord[1]) > board_size-1:
            # we remove only from the deep copy of the possible_move list otherwise the moves 
            # previously classified as invalid will still be considered invalid
            moves_ = possible_move[:]
            moves_.remove(move_)
            move_ = random.choice(moves_)
        return speed*(move_[0] + coord[0]), speed*(move_[1] + coord[1])

    def compute_local_winner(board, player, other):
            '''Manage the fight between two players'''
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