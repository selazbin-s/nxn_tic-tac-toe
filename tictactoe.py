from games import *
import time
import matplotlib.pyplot as plt
import numpy as np
import random
import sys

def alpha_beta_IDS(state, game, depth, eval_fn=None):
    start = time.time()
    player = game.to_move(state)

    def alphabeta(state,alpha, beta, depth):

        def max_value(state, alpha, beta, depth):
            if game.terminal_test(state):
                return game.utility(state, player)
            if time.time() - start > 10 or 0 >= depth: return eval_fn(state)
            v = -np.inf
            for a in game.actions(state):
                v = max(v, min_value(game.result(state, a), alpha, beta, depth - 1))
                if v >= beta:
                    return v
                alpha = max(alpha, v)
            return v

        def min_value(state, alpha, beta, depth):
            if game.terminal_test(state):
                return game.utility(state, player)
            if time.time() - start > 10 or 0 >= depth: return eval_fn(state)
            v = np.inf
            for a in game.actions(state):
                v = min(v, max_value(game.result(state, a), alpha, beta, depth - 1))
                if v <= alpha:
                    return v
                beta = min(beta, v)
            return v
        
        return max_value(state, alpha, beta, depth) if state.to_move == 'X' else min_value(state, alpha, beta, depth)

    best_action = None
    for d in range(1, depth):
        if time.time() - start > 10: break
        eval_fn = eval_fn or (lambda state: game.utility(state, player))
        best_score = -np.inf
        beta = np.inf
        for a in game.actions(state):
            v = alphabeta(game.result(state, a), best_score, beta, d)
            if v > best_score:
                best_score = v
                best_action = a
    return best_action

def minmax_decision(state, game, depth, eval_fn = None):
    """Given a state in a game, calculate the best move by searching
    forward all the way to the terminal states."""

    player = state.to_move

    def max_value(state, depth):
        if game.terminal_test(state):
            return game.utility(state, player)
        if depth <= 0: return eval_fn(state)
        v = -np.inf
        for a in game.actions(state):
            v = max(v, min_value(game.result(state, a), depth - 1))
        return v

    def min_value(state, depth):
        if game.terminal_test(state):
            return game.utility(state, player)
        if depth <= 0: return eval_fn(state)
        v = np.inf
        for a in game.actions(state):
            v = min(v, max_value(game.result(state, a), depth - 1))
        return v

    # Body of minmax_decision:
    for d in range(1, depth):
        eval_fn = eval_fn or (lambda state: game.utility(state, player))
        v = max(game.actions(state), key=lambda a: min_value(game.result(state, a), d))
    return v



class NxNTicTacToe(Game):
    """Play TicTacToe on an h x v board, with Max (first player) playing 'X'.
    A state has the player to move, a cached utility, a list of moves in
    the form of a list of (x, y) positions, and a board, in the form of
    a dict of {(x, y): Player} entries, where Player is 'X' or 'O'."""

    def __init__(self, h, v):
        self.h = h
        self.v = v
        self.k = 3
        moves = [(x, y) for x in range(1, h + 1)
                 for y in range(1, v + 1)]
        self.initial = GameState(to_move='X', utility=0, board={}, moves=moves)

    def actions(self, state):
        """Legal moves are any square not yet taken."""
        return state.moves

    def result(self, state, move):
        if move not in state.moves:
            return state  # Illegal move has no effect
        board = state.board.copy()
        board[move] = state.to_move
        moves = list(state.moves)
        moves.remove(move)
        return GameState(to_move=('O' if state.to_move == 'X' else 'X'),
                         utility=self.compute_utility(board, move, state.to_move),
                         board=board, moves=moves)

    def utility(self, state, player):
        """Return the value to player; 1 for win, -1 for loss, 0 otherwise."""
        return state.utility if player == 'X' else -state.utility

    def terminal_test(self, state):
        """A state is terminal if it is won or there are no empty squares."""
        return state.utility != 0 or len(state.moves) == 0

    def display(self, state):
        board = state.board
        for x in range(1, self.h + 1):
            for y in range(1, self.v + 1):
                print(board.get((x, y), '.'), end=' ')
            print()

    def compute_utility(self, board, move, player):
        """If 'X' wins with this move, return 1; if 'O' wins return -1; else return 0."""
        if (self.k_in_row(board, move, player, (0, 1)) or
                self.k_in_row(board, move, player, (1, 0)) or
                self.k_in_row(board, move, player, (1, -1)) or
                self.k_in_row(board, move, player, (1, 1))):
            return +1 if player == 'X' else -1
        else:
            return 0


    def k_in_row(self, board, move, player, delta_x_y):
        """Return true if there is a line through move on board for player."""
        (delta_x, delta_y) = delta_x_y
        x, y = move
        n = 0  # n is number of moves in row
        while board.get((x, y)) == player:
            n += 1
            x, y = x + delta_x, y + delta_y
        x, y = move
        while board.get((x, y)) == player:
            n += 1
            x, y = x - delta_x, y - delta_y
        n -= 1  # Because we counted move itself twice
        return n >= self.k

def check_input(user_input, board_size):
    # Strip parentheses from the input
    user_input = user_input.strip("()")

    # Split the input into a and b strings
    a_str, b_str = user_input.split(",")

    if not a_str.isdigit() or not b_str.isdigit():
        return False

    a, b = int(a_str), int(b_str)

    # Check if either a or b is greater than the board size
    if a > board_size or b > board_size:
        return False

    return True

def human_computer(game, state):
    print("\nStart game!\n")
    game.display(state)
    while not game.terminal_test(state):
        player = state.to_move
        print(f"\n{player}'s turn.")

        if player == 'X':  # User's turn
            move_input = input("Enter your move as (x, y): ")
            if(check_input(move_input,board_size)):
                move = eval(move_input)
                state = game.result(state, move)
            else:
                print("Invalid input!\n")
        else:  # Algorithm's turn
            depth = 5  # Set the search depth
            eval_fn = None  # Use the default evaluation function
            move = alpha_beta_IDS(state, game, depth, eval_fn)
            state = game.result(state, move)
            print(f"The algorithm chooses {move}.")

        game.display(state)
    print("\nGame over.")
    if state.utility == 1:
        print("X wins!")
    elif state.utility == -1:
        print("O wins!")
    else:
        print("It's a tie!")
        


def computer_computer(game, state, algo_type):
    print("\nStart game!\n")
    game.display(state)
    
    results = {'X': 0, 'O': 0, 'Tie': 0}
    total_time = 0
    total_branching = 0

    for _ in range(3):
        state = game.initial  # Reset the game state
        
        start_time = time.time()
        branching_count = 0
        while not game.terminal_test(state):
            player = state.to_move
            print(f"\n{player}'s turn.")
            if player == 'X':
                #depth = 5
                #move = alpha_beta_IDS(state, game, d=depth)
                moves = game.actions(state)
                move = random.choice(moves)
                branching_count += len(moves)  # Count the number of possible moves
            else:
                # Generate a random move
                #moves = game.actions(state)
                depth = 10
                eval_fn = None
                if algo_type=='a':
                    move = alpha_beta_IDS(state, game, depth, eval_fn)
                else:
                    move = minmax_decision(state, game, depth = 5)

            state = game.result(state, move)
            game.display(state)
        
        print("New game")
        
        game_time = time.time() - start_time
        total_time += game_time
        
        total_branching += branching_count
        

        if state.utility == 1:
            results['X'] += 1
        elif state.utility == -1:
            results['O'] += 1
        else:
            results['Tie'] += 1
    average_branching = total_branching / 10  # Calculate the average branching factor
    
    # Print the results
    print("\nResults:")
    print(f"X Wins: {results['X']}")
    print(f"O Wins: {results['O']}")
    print(f"Ties: {results['Tie']}")
    print(f"Total time taken: {total_time:.2f} seconds")
    print(f"Average Branching Factor: {average_branching:.2f}")
    return results


def human_human(game, state):
    print("\nStart game!\n")
    game.display(state)
    while not game.terminal_test(state):
        player = state.to_move
        print(f"\n{player}'s turn.")
        move_input = input("Enter your move as (x, y): ")
        if(check_input(move_input,board_size)):
            move = eval(move_input)
            state = game.result(state, move)
        else:
            print("Invalid input!\n")
        game.display(state)
    print("\nGame over.")
    if state.utility == 1:
        print("X wins!")
    elif state.utility == -1:
        print("O wins!")
    else:
        print("It's a tie!")


if __name__ == "__main__":
    user_input = input("Please enter a single number greater than 3 to represent the size of your board in terms of squares, such as '3' for a 3x3 board or '4' for a 4x4 board.\n")
    if user_input.isdigit():
        board_size = int(user_input)
    else:
        print("Invalid input")
        sys.exit(0)
    if board_size<3 or board_size>9:
        print("Invalid input")
        sys.exit(0)
    game = NxNTicTacToe(board_size, board_size)
    state = game.initial

    game_type = input("Please enter 'a' to play against another player, 'b' to play against alpha beta algorithm, or 'c' to watch the algorithm play against itself.\n" )
    if game_type=="a":
        human_human(game,state)
    elif game_type=="b":
        human_computer(game, state)
    elif game_type=="c":
        algo_type=input("Please enter 'a' for alpha beta iterative deepening algorithm or 'b' for min max algorithm.\n")
        if algo_type == 'a' or algo_type == 'b':
            results = computer_computer(game, state, algo_type)
            # Plot the results
            labels = ['X Wins', 'O Wins', 'Ties']
            values = [results['X'], results['O'], results['Tie']]

            plt.bar(labels, values)
            plt.xlabel('Results')
            plt.ylabel('Count')
            plt.title('Computer vs. Computer Results')
            plt.show()
        
    else:
        print("Invalid input")
        sys.exit(0)

    print("Thanks for playing!\n")