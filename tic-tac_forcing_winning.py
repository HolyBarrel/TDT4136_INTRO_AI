from copy import deepcopy
from search_algortihms import alpha_beta_search

State = tuple[int, list[list[int | None]]]  # Tuple of player (whose turn it is),
                                            # and board
Action = tuple[int, int]  # Where to place the player's piece

# Version of the game that uses alpha-beta pruning and attempts to solve the 
# problem with avoiding stupid moves for player 1
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
                    next_board = deepcopy(board)
                    next_board[row][col] = self.to_move(state)
                    if self.is_winner((self.to_move(state), next_board), self.to_move(state)):
                        return [(row, col)]
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

    def heuristic(state: State, player: int) -> int:
        _, board = state
        score = 0

        # Define the opponent
        opponent = (player + 1) % 2

        # Prioritize center (1, 1)
        if board[1][1] == player:
            score += 3
        elif board[1][1] == opponent:
            score -= 3

        # Prioritize corners (0,0), (0,2), (2,0), (2,2)
        corners = [(0, 0), (0, 2), (2, 0), (2, 2)]
        for corner in corners:
            row, col = corner
            if board[row][col] == player:
                score += 2
            elif board[row][col] == opponent:
                score -= 2

        # Standard row/column/diagonal counting (as before)
        for row in range(3):
            if board[row].count(opponent) == 0:  # If opponent isn't blocking
                score += board[row].count(player)  # Reward based on how many of player's marks
        for col in range(3):
            col_values = [board[row][col] for row in range(3)]
            if col_values.count(opponent) == 0:
                score += col_values.count(player)

        diag1 = [board[i][i] for i in range(3)]
        if diag1.count(opponent) == 0:
            score += diag1.count(player)
        diag2 = [board[i][2 - i] for i in range(3)]
        if diag2.count(opponent) == 0:
            score += diag2.count(player)

        return score



    def utility(self, state, player):
        if self.is_terminal(state):
            if self.is_winner(state, player):
                return 10
            if self.is_winner(state, (player + 1) % 2):
                return -10
            return 0

        return self.heuristic(state, player)

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
    game = Game()
    state = game.initial_state()
    while not game.is_terminal(state):
        game.print(state)
        action = alpha_beta_search(game, state)
        state = game.result(state, action)
    game.print(state)

