# i prefer direct imports - asterix makes it harder to read. If the name is there,
# i know exactly which file it's in
# for imports:
# 	- alphabetize
#   - there should be three sections with a blank line in between:
# 		- native packages e.g. from date import datetime (you dont have any)
# 		- third party libraries e.g. from numpy import zeros
# 		= your libraries
# 		reformatted to how it should look

from tic_tac_tree import *
from game_methods import *

print("Let's play, biatch.")

# everything here should be inside a run method, they shouldn't be accesible by other modules
#  e.g. this part could be part of Game.game_setup() or something, then the instance of game can hold the game state
# get board size and simulation runtime from the user:
board_dimension = get_board_dimension()
simulation_runtime = get_simulation_runtime(board_dimension)

# create head node (empty board) by constructing a node with: parent node = None,
# board = array of zeros, child nodes = [], and turn = -1 (the human player):
current =  Node(None, board_dimension, [], -1)

# construct the simulator for the current (head) node:
# this is why not to use asterix imports - wtf is simulator?
simulator = Simulator(current)

# simulate one game by passing the parent of the current node, which is None, to the
# simulator, so the tree is initialized and the list of current child nodes is populated
simulator.simulate_one_game(None)

print_board(current.board)

# main game loop:
while current.check_board() == 0:
	# prompt user for their move, checking for validity:
	player_move = get_player_move(current.board[0])

	# determine which node.child the player chose
	player_move_index = child_node_from_move_coordinates(current.board, player_move)

	# advance current to that node (now consider the board corresponding to player's move):
	current = current.children[player_move_index]
	print_board(current.board)

	# check if the player won (this condition should never be met...):
	if current.check_board() == -1:
		print("How can this be...?!? You've won!!")
		break
	# check if the game was tied:
	if current.check_board() == -10:
		print("Tie game. You are a formidable adversary.")
		break

	print("Now my turn: ")

	# advance the simulator to the current node
	simulator.current_node = current

	# in the allowed runtime, simulate games from this board. at the end of each game simulated, backtrack
	# through all visited nodes and log result (weighted by game length) in that node's record.
	# choose the best move based on total records (include simulations from previous turns) of child nodes
	current = simulator.find_best_move(current, simulation_runtime)
	print_board(current.board)

	# check for program win:
	if current.check_board() == 1:
		print("It's seems I've won again.")
		break



