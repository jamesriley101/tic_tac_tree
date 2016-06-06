from random import choice
from time import time

from numpy import copy, zeros

# for help commenting, use package DocBlockr
# I would call this something more descriptive than node...maybe Board? because
# each node represents a unique board?
# Node gives me no info about what it is


class Node():
    """
    represents a game state.
    Node.board is a 2d array each element represents a square
    0 = no move yet, -1 = human move, and 1 = computer move).
    # you dont have to use this pattern, but each arg in init should be noted
    args:
        parent: Node - previous game state.
        children: list([Node]) - all possible next-turn states.
        # note the units for record what is [0-0-0]
        record: is the weighted record of game simulations that passed through
        thatgame state in all previous turns' simulations
        turn: ???
    """

    def __init__(self, parent, board, children, turn):
        # replace the board parameter with dimension,
        # then do `zeros([board_dimension, board_dimension])` here.
        # i've refactored.
        # no need to save self.dimension
        # later... actually, i think this should just take a board,
        # then calculate children based on the board.
        # board should actually be its own class, with has make children
        self.board = board
        self.turn = turn
        # why do we ever need Node.parent?
        self.parent = parent
        #  these should be more descriptive
        # - all nodes have parents and children
        # - what are they? previous_move, next_moves?
        # self.children = self.create_child_nodes?
        # also, children could be a 'map' - a dict of nodes by coordinates,
        # to more easily find a child node in child_node_from_move_coordinates
        in game_methods
        self.children = children
        # should this be a tuple?
        self.record = [0, 0, 0]

    def check_board(self):
        # better to use docstrings, because in many ides, it will show you
        # the docstring when you highlight a class - total nitpick
        """check for a winner or tie-game in self.board"""
        for i in xrange(self.dimension):
            # could split this into private methods:
            # _check_horizontal, _check_vertical, _check_diagonal,
            if (sum(self.board[:, i]) == -(self.dimension) or
                    sum(self.board[i, :]) == -(self.dimension)):
                return -1
            if (sum(self.board[:, i]) == self.dimension or
                    sum(self.board[i, :]) == self.dimension):
                return 1

        diag1_sum = 0
        diag2_sum = 0
        for i in xrange(self.dimension):
            diag1_sum += self.board[i][i]
            diag2_sum += self.board[(self.dimension) - 1 - i][i]

        if diag1_sum == -(self.dimension) or diag2_sum == -(self.dimension):
            return -1

        if diag1_sum == self.dimension or diag2_sum == self.dimension:
            return 1

        for i in range(self.dimension):
            for j in range(self.dimension):
                if self.board[i][j] == 0:
                    return 0
        # -10?
        return -10


class Simulator():
    """
    in the allotted runtime, the simulator traverses the
    tree structure of possible game states, from the current state to
    all possible end-game states, determines the outcome, then traverses back
    to the current game state while logging that result in the record
    of each node along the way. the simulated record of each node,
    retained and updated throughout the game, is used to evaluate the best
    possible move
    """

    def __init__(self, current_node):
        self.current_node = current_node

    # docstring
    # method to create the board for a child node. copies the current board,
    # and adds the move, passed as x_dim and y_dim, to that board:
    # also, you could pass the same board around and modify it,
    # instead of copy(board), just modify the board in place,
    # there are arguments and proponents of both,
    # but it *might* help your runtime to not have to create new boards
    def make_move(self, x_dim, y_dim, board, player):
        out_board = copy(board)
        if player == 1:
            out_board[x_dim][y_dim] = 1
        else:
            out_board[x_dim][y_dim] = -1
        return out_board

    # method to log the result of a game simulation at each node that was in the game sequence.
    # the impact of a result on the record is inversely weighted by sequence
    # length.
    def log_game(self, result, game_moves):
        # to make this more readable, i might make record a
        # dict with wins, ties, loses, or a namedtuple
        if result == -1:
            self.current_node.record[2] += 1 / float(game_moves)
        if result == 1:
            self.current_node.record[0] += 1 / float(game_moves)
        if result == -10:
            self.current_node.record[1] += 1 / float(game_moves)
        return

    # create the child nodes representing all possible moves
    # from the current game state.
    # called when a node is visited in a simulation for the first time.
    def create_child_nodes(self, turn):
        for i in range(self.current_node.dim):
            for j in range(self.current_node.dim):
                if self.current_node.board[i, j] == 0:
                    child_board = self.make_move(
                        i, j, self.current_node.board, turn)
                    self.current_node.children.append(
                        node(self.current_node, child_board, [], turn * -1))
        return

    # method to simulate a game sequence from a given game state. moves for both players are chosen
    # arbitrarily and the simulator advances to that node. the outcome of the sequence is determined,
    # then the simulator backtracks to the actual game state node, updating the records of the nodes
    # comprising that sequence along the way. the parent of the current node
    # is used as a backstop:
    # isn't current _parent always self.parent?
    def simulate_one_game(self, current_parent):
        turn = self.current_node.turn
        # do you use game_sequence, aside from adding to it?
        game_sequence = []
        game_moves = 1
        while self.current_node.check_board() == 0:
            game_moves += 1
            # children should be created based on the passed in board
            if self.current_node.children == []:
                self.create_child_nodes(turn)
            game_sequence.append(self.current_node)
            # might try to make this gaurauntee that it goes
            # down paths it has least explored
            # use the native random package
            self.current_node = choice(self.current_node.children)
            turn = turn * -1
        sim_outcome = self.current_node.check_board()

        # i don't really get why we have to compare parents?
        # later... ah - got it - cause we need to tell them if we won
        # how about Node.update_parent, which calls itself recursively, until parent is None
        # i think the Nodes should be operating on themselves
        while self.current_node.parent != current_parent:
            self.log_game(sim_outcome, game_moves)
            self.current_node = self.current_node.parent
        return

    # method to determine best available move at a given game state. games are simulated for the allotted runtime,
    # and the best available move is determined by calculating a rating from the accumlated win/loss records of
    # all simulated games that passed through each of the child nodes
    # representing the available moves

    def find_best_move(self, this_node, sim_time):
        # for the allowed time, simulate games, updating the record of each
        # node:
        stop_time = time() + sim_time
        while time() < stop_time:
            # why is this parent? why is this_node not self?
            self.simulate_one_game(this_node.parent)
            # decide best move based on record of each child node (available moves), and strategy parameters multiplying
            # the impact of simulated wins/losses on the record of each node:
            aggressiveness = 3
            defensiveness = 5
            best_move = None
            best_rating = 0
        for child in this_node.children:
            # don't use \ - if a line is that long,
            # you should probably split the logic up.
            # it would be easier to understand what the numerator and operator represent
            # if you have to, you can enclose it in parentheses
            # and break at operators, like so - still ugly though
            move_rating = (float(child.record[0] *
                           aggressiveness + child.record[1]) /
                           (sum(child.record) + i.record[-1] * defensiveness))

        if move_rating > best_rating:
            best_rating = move_rating
            best_move = child

        return best_move
