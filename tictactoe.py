from games import *


if __name__ == "__main__":
    game = TicTacToe()
    state = game.initial

    print("Let's play TicTacToe!\n")
    game.display(state)

    while not game.terminal_test(state):
        player = state.to_move
        print(f"\n{player}'s turn.")
        move = eval(input("Enter your move as (x, y): "))
        state = game.result(state, move)
        game.display(state)

    print("\nGame over.")
    if state.utility == 1:
        print("X wins!")
    elif state.utility == -1:
        print("O wins!")
    else:
        print("It's a tie!")