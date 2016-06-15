# i prefer direct imports - asterix makes it harder to read. If the name is there,
# i know exactly which file it's in
# for imports:
# 	- alphabetize
#   - there should be three sections with a blank line in between:
# 		- native packages e.g. from date import datetime (you dont have any)
# 		- third party libraries e.g. from numpy import zeros
# 		= your libraries
# 		reformatted to how it should look

from tic_tac_tree import Board, Simulator
from game_methods import get_board_dimension, get_simulation_runtime

print("Let's play, biatch.")

# everything here should be inside a run method, they shouldn't be accesible by other modules
#  e.g. this part could be part of Game.game_setup() or something, then the instance of game can hold the game state
# get board size and simulation runtime from the user:
board_dimension = get_board_dimension()
simulation_runtime = get_simulation_runtime(board_dimension)

# create head Board (empty board) by constructing a Board with: parent Board = None,
# board = array of zeros, nextBoards = [], and turn = -1 (the human player):
currentBoard =  Board(None, None, -1, board_dimension)

# construct the simulator for the current (empty) Board. The simulator simulates game outcomes
# by traversing from current Board to end-game Boards and back, logging outcome of simulation:
simulator = Simulator(currentBoard)

# simulate one game by passing the parent of the current Board, which is None, to the
# simulator, so the tree is initialized and the list of current nextBoards is populated
simulator.simulateOneGame()

currentBoard.printBoard()

# main game loop:
while currentBoard.checkForGameOver() == 0:
	# prompt user for their move, checking for validity. advance currentBoard to Board 
	# corresponding to player's move):
	currentBoard = currentBoard.get_player_move()
	currentBoard.printBoard()

	# check if the player won (this condition should never be met...):
	if currentBoard.checkForGameOver() == -1:
		print("How can this be...?!? You've won!!")
		break
	# check if the game was tied:
	if currentBoard.checkForGameOver() == -10:
		print("Tie game. You are a formidable adversary.")
		break

	# advance the simulator to the current Board
	simulator.homeBoard = currentBoard

	print("Now my turn: ")

	# in the allowed runtime, simulate games from the current Board:
	simulator.simulateGamesForTimeN(simulation_runtime)

	# chose the best move and advance to that Board:
	currentBoard = currentBoard.pickBestMove()

	currentBoard.printBoard()

	# check for computer win:
	if currentBoard.checkForGameOver() == 1:
		print("It's seems I've won again.")
		break
	# check for tie:
	if currentBoard.checkForGameOver() == -10:
		print("Tie game. You are a formidable adversary.")
		break


