import math

def minimax_search(game,state, competitive = False):
    player = game.to_move(state)
    if competitive:
        _, move = max_value(game, state, player=player)
    else:
        _, move = max_value(game, state, player=0)
    return move

def max_value(game, state, player):
    if game.is_terminal(state):
        return game.utility(state, player=player), None
    value, move = -math.inf, None
    for action in game.actions(state):
        value2, action2 = min_value(game, game.result(state, action), player)
        if value2 > value:
            value, move = value2, action
    return value, move

def min_value(game, state, player):
    if game.is_terminal(state):
        return game.utility(state, player=player), None
    value, move = math.inf, None
    for action in game.actions(state):
        value2, action2 = max_value(game, game.result(state, action), player)
        if value2 < value:
            value, move = value2, action
    return value, move