# main game methods

from numpy import reshape

def get_board_dimension():
	board_dimension = 0
	while board_dimension < 3 or board_dimension > 6:
		board_dimension = input("What size board (3 - 6)? ")
	return board_dimension

def get_simulation_runtime(board_dimension):
	simulation_runtime  = 0
	while simulation_runtime < board_dimension - 2:
		simulation_runtime = float(input("How long do you want me to think about each move (seconds)? "))
		if simulation_runtime < board_dimension - 2:
			print("I need a little more time than that for a board of size %s") % board_dimension
	return simulation_runtime

