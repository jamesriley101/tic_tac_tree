#main game methods

from numpy import reshape

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

def child_node_from_move_coordinates(board, x_dim, y_dim):
	player_move_index = 0
	linear_board = reshape(board, [1, len(board[0]) ** 2])[0]
	for j in range(y_dim * len(board[0]) + x_dim):
		if linear_board[j] == 0:
			player_move_index += 1
	return player_move_index