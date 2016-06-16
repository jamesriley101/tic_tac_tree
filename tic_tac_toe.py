from tic_tac_tree import Board, Simulator

print("Let's play, biatch.")

# create head Board (empty board):
currentBoard = Board()

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
	simulator.simulateGamesForSimTime()

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


