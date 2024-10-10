import math

def minimax_search(game,state, competitive = False):

    def max_value(game, state, player):
        if game.is_terminal(state):
            return game.utility(state, player), None
        value, move = -math.inf, None
        for action in game.actions(state):
            value2, action2 = min_value(game, game.result(state, action), player)
            if value2 > value:
                value, move = value2, action
        return value, move

    def min_value(game, state, player):
        if game.is_terminal(state):
            return game.utility(state, player), None
        value, move = math.inf, None
        for action in game.actions(state):
            value2, action2 = max_value(game, game.result(state, action), player)
            if value2 < value:
                value, move = value2, action
        return value, move
    
    player = game.to_move(state)
    if competitive:
        _, move = max_value(game, state, player=player)
    else:
        _, move = max_value(game, state, player=0)
    return move




def alpha_beta_search(game, state, competitive = False):

    def max_value(game, state, alpha, beta, player):
        if game.is_terminal(state):
            return game.utility(state, player), None
        v = float('-inf')
        for action in game.actions(state):
            v2, _ = min_value(game, game.result(state, action), alpha, beta, player)
            if v2 > v:
                v = v2
                move = action
            if v >= beta:
                return v, move
            alpha = max(alpha, v)
        return v, move

    def min_value(game, state, alpha, beta, player = 0):
        if game.is_terminal(state):
            return game.utility(state, player), None
        v = float('inf')
        for action in game.actions(state):
            v2, _ = max_value(game, game.result(state, action), alpha, beta, player)
            if v2 < v:
                v = v2
                move = action
            if v <= alpha:
                return v, move
            beta = min(beta, v)
        return v, move

    player = game.to_move(state)
    if competitive:
        _, move = max_value(game, state, float('-inf'), float('inf'), player=player)
    else:
        _, move = max_value(game, state, float('-inf'), float('inf'), player = 0)
    return move

