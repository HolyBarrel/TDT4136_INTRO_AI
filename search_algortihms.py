import math

def minimax_search(game,state, competitive = False):
    """
    Perform minimax search to find the best move in a given game state.

    This function implements the minimax algorithm, a decision rule used for minimizing the possible loss 
    in a worst-case scenario. It operates by recursively exploring the game tree and evaluating the utility 
    of terminal states, assuming that the opponent plays optimally.

    :param game: A game object that provides the interface for game-specific operations such as checking terminal 
                states, retrieving available actions, and calculating utilities.
    :param state: The current state of the game from which the search will begin.
    :param competitive: Boolean indicating if the search should be competitive. If True, the algorithm optimizes for 
                        the player who is currently to move; if False, it optimizes for player 0.
    :return: The best action to take in the current state.
    """

    def max_value(game, state, player):
        """
        Compute the maximum utility value for the current player by simulating the game and minimizing the opponent's utility.

        :param game: A game object that allows interaction with the game state.
        :param state: The current state of the game.
        :param player: The player for whom we are maximizing the utility.
        :return: A tuple of (maximum utility value, action) for the current player.
        """
        if game.is_terminal(state):
            return game.utility(state, player), None
        value, move = -math.inf, None
        for action in game.actions(state):
            value2, action2 = min_value(game, game.result(state, action), player)
            if value2 > value:
                value, move = value2, action
        return value, move

    def min_value(game, state, player):
        """
        Compute the minimum utility value for the current player by simulating the game and maximizing the opponent's utility.

        :param game: A game object that allows interaction with the game state.
        :param state: The current state of the game.
        :param player: The player for whom we are minimizing the utility.
        :return: A tuple of (minimum utility value, action) for the current player.
        """
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
    """
    Perform alpha-beta pruning to find the best move in a given game state.

    This function implements alpha-beta pruning, which is an optimization of the minimax algorithm. It reduces the 
    number of nodes that are evaluated by the minimax algorithm in the search tree, effectively speeding up the search 
    by eliminating branches that cannot influence the final decision.

    :param game: A game object that provides the interface for game-specific operations such as checking terminal states, 
                 retrieving available actions, and calculating utilities.
    :param state: The current state of the game from which the search will begin.
    :param competitive: Boolean indicating if the search should be competitive. If True, the algorithm optimizes for 
                        the player who is currently to move; if False, it optimizes for player 0.
    :return: The best action to take in the current state.
    """

    def max_value(game, state, alpha, beta, player):
        """
        Compute the maximum utility value for the current player, using alpha-beta pruning to cut off branches that will not be selected.

        :param game: A game object that allows interaction with the game state.
        :param state: The current state of the game.
        :param alpha: The best value that the maximizer can guarantee.
        :param beta: The best value that the minimizer can guarantee.
        :param player: The player for whom we are maximizing the utility.
        :return: A tuple of (maximum utility value, action) for the current player.
        """
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
        """
        Compute the minimum utility value for the current player, using alpha-beta pruning to cut off branches that will not be selected.

        :param game: A game object that allows interaction with the game state.
        :param state: The current state of the game.
        :param alpha: The best value that the maximizer can guarantee.
        :param beta: The best value that the minimizer can guarantee.
        :param player: The player for whom we are minimizing the utility.
        :return: A tuple of (minimum utility value, action) for the current player.
        """
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

