from random import randint
from numpy import copy
from time import time

#definition of node. this class represents a given state of the game. The board itself
#is a member that is an array with each element representing a square (0 = no move yet, 
#-1 = human move, and 1 = computer move). the parent is the node representing the previous
#game state. children is a list of nodes representing all the possible next-turn states of 
#the game. the record is the weighted record of game simulations that passed through that 
#game state in all previous turns' simulations:
class node():
	def __init__(self, parent, board, children, turn):
		self.board = board
		self.parent = parent
		self.children = children
		self.turn = turn
		self.record = [0,0,0]
		self.dim = len(self.board[0])

	#internal class method checking for a winner or tie-game in self.board:
	def check_board(self):
		for i in range(self.dim):
			if sum(self.board[:,i]) == -(self.dim) or sum(self.board[i,:]) == -(self.dim):
				return -1
			if sum(self.board[:,i]) == self.dim or sum(self.board[i,:]) == self.dim:
				return 1
		diag1_sum = 0
		diag2_sum = 0
		for i in range(self.dim):
			diag1_sum += self.board[i][i] 
			diag2_sum += self.board[(self.dim) - 1 - i][i]
		if diag1_sum == -(self.dim) or diag2_sum == -(self.dim):
			return -1
		if diag1_sum == self.dim or diag2_sum == self.dim:
			return 1
		for i in range(self.dim):
			for j in range(self.dim):
				if self.board[i][j] == 0:
					return 0
		return -10

#definition of simulator class. in the allotted runtime, the simulator traverses the 
#tree structure of possible game states, from the current state to all possible end-game 
#states, determines the outcome, then traverses back to the current game state while logging 
#that result in the record of each node along the way. the simulated record of each node,
#retained and updated throughout the game, is used to evaluate the best possible move:

class simulator():
	def __init__(self, current_node):
		self.current_node = current_node

	#method to create the board for a child node. copies the current board, and adds the 
	#move, passed as x_dim and y_dim, to that board:
	def make_move(self, x_dim, y_dim, board, player):
		out_board = copy(board)
		if player == 1:
			out_board[x_dim][y_dim] = 1
		else:
			out_board[x_dim][y_dim] = -1
		return out_board

	#method to log the result of a game simulation at each node that was in the game sequence.
	#the impact of a result on the record is inversely weighted by sequence length.
	def log_game(self, result, game_moves):
		if result == -1:
			self.current_node.record[2] += 1 / float(game_moves)
		if result == 1:
			self.current_node.record[0] += 1 / float(game_moves)
		if result == -10:
			self.current_node.record [1] += 1 / float(game_moves)
		return

	#method to create the child nodes representing all possible moves from a given game state.
	#called when a node is visited in a simulation for the first time.  
	def create_child_nodes(self, turn):
		for i in range(self.current_node.dim):
			for j in range(self.current_node.dim):
				if self.current_node.board[i,j] == 0:
					child_board = self.make_move(i, j, self.current_node.board, turn)
					self.current_node.children.append(node(self.current_node, child_board, [], turn * -1))
		return

	#method to simulate a game sequence from a given game state. moves for both players are chosen 
	#arbitrarily and the simulator advances to that node. the outcome of the sequence is determined, 
	#then the simulator backtracks to the actual game state node, updating the records of the nodes 
	#comprising that sequence along the way. the parent of the current node is used as a backstop:
	def simulate_one_game(self, current_parent):
		turn = self.current_node.turn
		game_sequence = []
		game_moves = 1
		while self.current_node.check_board() == 0:
			game_moves += 1
			if self.current_node.children == []:
				self.create_child_nodes(turn)
			game_sequence.append(self.current_node)
			self.current_node = self.current_node.children[randint(0, len(self.current_node.children) - 1)]
			turn = turn * -1
		sim_outcome = self.current_node.check_board()
		
		while self.current_node.parent != current_parent:
			self.log_game(sim_outcome, game_moves)
			self.current_node = self.current_node.parent
		return

	#method to determine best available move at a given game state. games are simulated for the allotted runtime, 
	#and the best available move is determined by calculating a rating from the accumlated win/loss records of 
	#all simulated games that passed through each of the child nodes representing the available moves

	def find_best_move(self, this_node, sim_time):
		#for the allowed time, simulate games, updating the record of each node:
		stop_time = time() + sim_time
		while time() < stop_time:
			self.simulate_one_game(this_node.parent)
		#decide best move based on record of each child node (available moves), and strategy parameters multiplying
		#the impact of simulated wins/losses on the record of each node:
		aggressiveness = 3
		defensiveness = 5
		best_move = None
		best_rating = 0
		for i in this_node.children:
			move_rating = float(i.record[0] * aggressiveness + i.record[1]) / (sum(i.record) + i.record[-1] * defensiveness)
			#print("%s : %s") % (i.record, this_rating)
			if move_rating > best_rating:
				best_rating = move_rating
				best_move = i
		return best_move





