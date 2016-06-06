# these are functions, but should be methods of a Board class,
# main game methods

from numpy import reshape

# this should be a method of board
def check_player_move(player_move, board):
	for i in player_move:
		if i < 0 or i > len(board) - 1 or board[i] != 0:
			return False
	return True

def get_player_move(board):
	player_move = [None, None]
	while not check_player_move(player_move, board):
		player_move[0] = input("Enter the x dimension of your move: ")
		player_move[1] = input("Enter the y dimension of your move: ")
	return player_move

#identify the node in the list children that corresponds to the coordinates of the player move (the
#list children was populated by creating a node for every available move, ordered as they appear row-wise)
def child_node_from_move_coordinates(board, player_move):
	player_move_index = 0
    # ?
	linear_board = reshape(board, [1, len(board[0]) ** 2])[0]
	for j in range(player_move[1] * len(board[0]) + player_move[0]):
		if linear_board[j] == 0:
			player_move_index += 1
	return player_move_index

def print_board(board):
	print_board = list(board)
	for i in range(len(print_board)):
		print_board[i] = list(print_board[i])
	for n in print_board:
		for i,j in enumerate(n):
			if j == 0:
				n[i] = ' '
			if j == -1:
				n[i] = 'X'
			if j == 1:
				n[i] = 'O'
	for i in print_board:
		print(i)

def get_board_dimension():
	board_dimension = 0
	while board_dimension < 3 or board_dimension > 10:
		board_dimension = input("What size board (3 - 10)? ")
	return board_dimension

def get_simulation_runtime(board_dimension):
	simulation_runtime  = 0
	while simulation_runtime < board_dimension - 2:
		simulation_runtime = float(input("How long do you want me to think about each move (seconds)? "))
		if simulation_runtime < board_dimension - 2:
			print("I need a little more time than that for a board of size %s") % board_dimension
	return simulation_runtime

