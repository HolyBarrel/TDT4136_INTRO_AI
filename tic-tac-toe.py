from copy import deepcopy
from search_algortihms import minimax_search
from search_algortihms import alpha_beta_search
import time

State = tuple[int, list[list[int | None]]]  # Tuple of player (whose turn it is),
                                            # and board
Action = tuple[int, int]  # Where to place the player's piece

# Version of the game that uses alpha-beta pruning and also prints the minimax search result
# The search methods are compared, in terms of time taken to find the solution

class Game:
    def initial_state(self) -> State:
        return (0, [[None, None, None], [None, None, None], [None, None, None]])

    def to_move(self, state: State) -> int:
        player_index, _ = state
        return player_index

    def actions(self, state: State) -> list[Action]:
        _, board = state
        actions = []
        for row in range(3):
            for col in range(3):
                if board[row][col] is None:
                    actions.append((row, col))
        return actions

    def result(self, state: State, action: Action) -> State:
        _, board = state
        row, col = action
        next_board = deepcopy(board)
        next_board[row][col] = self.to_move(state)
        return (self.to_move(state) + 1) % 2, next_board

    def is_winner(self, state: State, player: int) -> bool:
        _, board = state
        for row in range(3):
            if all(board[row][col] == player for col in range(3)):
                return True
        for col in range(3):
            if all(board[row][col] == player for row in range(3)):
                return True
        if all(board[i][i] == player for i in range(3)):
            return True
        return all(board[i][2 - i] == player for i in range(3))

    def is_terminal(self, state: State) -> bool:
        _, board = state
        if self.is_winner(state, (self.to_move(state) + 1) % 2):
            return True
        return all(board[row][col] is not None for row in range(3) for col in range(3))

    def utility(self, state, player):
        assert self.is_terminal(state)
        if self.is_winner(state, player):
            return 1
        if self.is_winner(state, (player + 1) % 2):
            return -1
        return 0

    def print(self, state: State):
        _, board = state
        print()
        for row in range(3):
            cells = [
                ' ' if board[row][col] is None else 'x' if board[row][col] == 0 else 'o'
                for col in range(3)
            ]
            print(f' {cells[0]} | {cells[1]} | {cells[2]}')
            if row < 2:
                print('---+---+---')
        print()
        if self.is_terminal(state):
            if self.utility(state, 0) > 0:
                print(f'P1 won')
            elif self.utility(state, 1) > 0:
                print(f'P2 won')
            else:
                print('The game is a draw')
        else:
            print(f'It is P{self.to_move(state)+1}\'s turn to move')



if __name__ == '__main__':
    print('Tic-tac-toe with alpha-beta pruning')
    game = Game()
    state = game.initial_state()
    start_time = time.time()
    while not game.is_terminal(state):
        game.print(state)
        action = alpha_beta_search(game, state, True)
        state = game.result(state, action)
    end_time = time.time()
    elapsed_time_ab = end_time - start_time
    game.print(state)
    


    print('Tic-tac-toe with minimax, competitive version')
    game = Game()
    state = game.initial_state()
    start_time = time.time()
    while not game.is_terminal(state):
        game.print(state)
        action = minimax_search(game, state, True)
        state = game.result(state, action)
    end_time = time.time()
    elapsed_time_minimax = end_time - start_time
    game.print(state)
    
    print(f'Minimax took {elapsed_time_minimax:.4f} seconds')
    print(f'Alpha-Beta Pruning took {elapsed_time_ab:.4f} seconds\n')

