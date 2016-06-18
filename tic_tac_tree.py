from random import choice
from time import time
from numpy import copy, zeros

class Board():
    """
    represents a game state.
    Board.allMovesMade is a 2d array where each element represents a space on the Board
    (0 = no move yet, -1 = human move, and 1 = computer move).

    args:
        previousBoard: Board - previous game state.
        allMovesMade: numpy array - all moves the on Board (0 = no move yet, 1 = computer, -1 = human)
        current player: int - which player is about to move. -1 = human, 1 = computer
        boardSize: int - size of the board. only designated when instanting the empty board

    """
    def __init__(self, previousBoard = None, allMovesMade = None, currentPlayer = -1):

        self.previousBoard = previousBoard
        self.allMovesMade = allMovesMade
        self.currentPlayer = currentPlayer
        self.nextBoards = {}
        self.simRecordWeighted = {
                                    "wins_weighted": 0.1,
                                    "ties_weighted": 0.1,
                                    "loses_weighted": 0.1,
        }
        #if allMovesMade == None we are instantiating an empty board:
        if allMovesMade == None:
            self.boardSize = 0
            while self.boardSize < 2 or self.boardSize > 6:
                self.boardSize = input("What size board (2 - 6)? ")
            self.allMovesMade = zeros([self.boardSize, self.boardSize])
        else:
            self.boardSize = len(allMovesMade[0])

    def printBoard(self):
        print_board = list(self.allMovesMade)
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

    def check_player_move(self, player_move):
        for i in player_move:
            if i < 0 or i >= len(self.allMovesMade):
                return False
            if self.allMovesMade[player_move[1]][player_move[0]]:
                return False
        return True

    def get_player_move(self):
        player_move_x = None
        player_move_y = None
        while not self.check_player_move((player_move_x, player_move_y)):
            player_move_x = input("Enter the x dimension of your move: ")
            player_move_y = input("Enter the y dimension of your move: ")
        return self.nextBoards[(player_move_x, player_move_y)]

    def checkForGameOver(self):
        """
        check for a winner or tie-game in self.allMovesMade. return 1 for computer win,
        -1 for player win, 0 for an ongoing game and -10 for a tie.
        """
        player_win = self.boardSize * -1
        computer_win = self.boardSize
        for coordinate in xrange(self.boardSize):
            # check for computer win along horizontals and verticals:
            if (sum(self.allMovesMade[:, coordinate]) == computer_win or
                    sum(self.allMovesMade[coordinate, :]) == computer_win):
                return 1
            # check for player win along horizontals and verticals:
            if (sum(self.allMovesMade[:, coordinate]) == player_win or
                    sum(self.allMovesMade[coordinate, :]) == player_win):
                return -1
        # check for winner along diagonals
        diag1_sum = 0
        diag2_sum = 0
        for coordinate in xrange(self.boardSize):
            diag1_sum += self.allMovesMade[coordinate][coordinate]
            diag2_sum += self.allMovesMade[(self.boardSize) - 1 - coordinate][coordinate]
        # check for player in along diagonals:
        if diag1_sum == computer_win or diag2_sum == computer_win:
            return 1
        # check for computer win along diagonals:
        if diag1_sum == player_win or diag2_sum == player_win:
            return -1
        # check if for any empty spaces:
        for row in range(self.boardSize):
            for column in range(self.boardSize):
                if self.allMovesMade[row][column] == 0:
                    return 0
        # if here, return -10 indicating an ongoing game:
        return -10

    def createNextBoards(self):
        """
        Create the nextBoards representing all possible moves from the current Board.
        Called when a Board is visited in a simulation for the first time.
        """
        for row in range(self.boardSize):
            for column in range(self.boardSize):
                if self.allMovesMade[column, row] == 0:
                    nextBoardMoves = copy(self.allMovesMade)
                    nextBoardMoves[column, row] = self.currentPlayer
                    self.nextBoards[(row, column)] = Board(self, nextBoardMoves, self.currentPlayer * -1)
        return

    def logGame(self, result, weight):
        """
        Logs the result of a game simulation at a Board that was a step in that simulation
        the impact of a result on the simRecordWeighted is inversely weighted by number
        of turns from the actual current board simulated before reaching that result.
        """
        if result == -1:
            self.simRecordWeighted['loses_weighted'] += 1 / float(weight) ** 2
        if result == 1:
            self.simRecordWeighted['wins_weighted'] += 1 / float(weight) ** 2
        if result == -10:
            self.simRecordWeighted['ties_weighted'] += 1 / float(weight) ** 2
        return

    def pickBestMove(self):
        """
        Chooses the best available move, based on the simulated records of the Board associated with
        each available move.
        """
        aggressiveness = 3
        defensiveness = 5
        best_option = None
        best_option_rating = 0
        for option in self.nextBoards.values():
            option_rating_numerator = option.simRecordWeighted['wins_weighted'] * aggressiveness + option.simRecordWeighted['ties_weighted']
            option_rating_denominator = option.simRecordWeighted['loses_weighted'] * defensiveness
            option_rating = option_rating_numerator / option_rating_denominator
            if option_rating > best_option_rating:
                best_option = option
                best_option_rating = option_rating
        return best_option

class Simulator():
    """
    the simulator traverses the tree structure of possible Boards, from the actual Board to a random outcome,
    determines the outcome, then traverses back to the actual Board while logging that result in simRecordWeighted
    of each Board along the way.

    args:
        homeBoard: Board - The actual game state. Simulator traverses out from this Board and returns.
    """

    def __init__(self, homeBoard):
        self.homeBoard = homeBoard
        self.currentBoard = None
        self.simTime = 0
        while self.simTime < self.homeBoard.boardSize - 2:
            self.simTime = float(input("How long do you want me to think about each move (seconds)? "))
            if self.simTime < self.homeBoard.boardSize - 2:
                print("I need a little more time than that for a board of size %s") % board_dimension

    def simulateOneGame(self):
        """
        Simulates a game from a given Board. In a given simulation, a member of nextBoards is chosen randomly
        and the simulator advances to that Board. The eventual outcome of the simulation is determined, and
        the simulator backtracks to homeBoard (the actual game state), updating the simRecordWeighted
        of each Board comprising that simluation along the way back to homeBoard.
        """
        game_moves = 1
        self.currentBoard = self.homeBoard
        while self.currentBoard.checkForGameOver() == 0:
            if self.currentBoard.nextBoards == {}:
                self.currentBoard.createNextBoards()
            self.currentBoard = choice(list(self.currentBoard.nextBoards.values()))
            game_moves += 1
        sim_outcome = self.currentBoard.checkForGameOver()

        while self.currentBoard != self.homeBoard:
            self.currentBoard.logGame(sim_outcome, game_moves)
            self.currentBoard = self.currentBoard.previousBoard
        return

    def simulateGamesForSimTime(self):
        """
        For simTime seconds, simulates games, updating the simRecordWeighted of each Board.
        """
        stop_time = time() + self.simTime
        while time() < stop_time:
            self.simulateOneGame()
        return
