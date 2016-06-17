# tic_tac_tree

Program that will not lose to you in tic tac toe, on an arbitrarily sized board.

To run, clone the repository and run tic_tac_toe.py. Enter a board size (2 - 7) and time for the program to run simulations at each turn. Enter the x and y coordinates of your moves (indexed to the right and downward on the board, from 0).

Classes and functions are described in docstrings.

This program uses a dynamic tree structure relating possible game-states, and traverses that tree to simulate game outcomes. The results of all simulations resulting from a given game state are stored and updated as the game progresses. At the end of the allotted runtime, the best available move is selected by analyzing the simulation results corresponding to each available move. The aggressiveness/defensiveness parameters for the move selection can be adjusted in tic_tac_tree.py.
