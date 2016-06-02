from tic_tac_tree import *
from game_methods import *
from numpy import zeros

print("Let's play, biatch.")

#get board size and simulation runtime from the user:
board_dimension = get_board_dimension()
simulation_runtime = get_simulation_runtime(board_dimension)

#create head node (empty board) by constructing a node with: parent node = None,
#board = array of zeros, child nodes = [], and turn = -1 (the human player):
current = node(None, zeros([board_dimension, board_dimension]), [], -1)

#construct the simulator for the current (head) node:
sim = simulator(current)

#simulate one game by passing the parent of the current node, which is None, to the
#simulator, so the tree is initialized and the list of current child nodes is populated
sim.simulate_one_game(None)

print_board(current.board)

#main game loop:
while current.check_board() == 0:
	player_move_x = input("Enter the x dimension of your move: ")
	player_move_y = input("Enter the y dimension of your move: ")
	
	#determine which node.child the player chose
	player_move_index = child_node_from_move_coordinates(current.board, player_move_x, player_move_y)
	
	#advance current to that node (now consider the board corresponding to player's move):
	current = current.children[player_move_index]
	print_board(current.board)
	
	#check if the player won (this condition should never be met...):
	if current.check_board() == -1:
		print("How can this be...?!? You've won!!")
		break
	#check if the game was tied:
	if current.check_board() == -10:
		print("Tie game. You are a formidable adversary.")
		break

	print("Now my turn: ")

	#advance the simulator to the current node
	sim.current_node = current

	#in the allowed runtime, simulate games from this board. at the end of each game simulated, backtrack 
	#through all visited nodes and log result (weighted by game length) in that node's record.
	#choose the best move based on total records (include simulations from previous turns) of child nodes
	current = sim.find_best_move(current, simulation_runtime)
	print_board(current.board)
	
	#check for program win:
	if current.check_board() == 1:
		print("It's seems I've won again.")
		break



