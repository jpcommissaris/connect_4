import numpy as np
from board import Board
from copy import deepcopy
import random
import math

class Learner:

    def __init__(self):
        b = Board()
        self.root = self.Node(b, None) # sets up first level (no pieces on board)
        #self.root.children.append(self.Node(b, self.root))
        self.player = 2
        self.exploit = 50 # percent chance of picking favorable move versus random one

    # adds node during a game
    def connectNodes(self, parent, child):
        # makes a connection between nodes
        child.parent = parent
        parent.children.append(child)
        return child
    # checks if move is legal
    def isMoveLegal(self, node, col):
        if node.obj.board[0][col] == 0:
            return True
        else:
            return False

    def printScores(self, root):
        print(root.score, end=" ")
        for x in range(len(root.children)):
            self.printScores(root.children[x])

    def play(self, root):
        level = 0
        positionsPlayed = []
        while (not root.obj.checkWin()) and level < 42:
            self.switchPlayer() # switches player
            level += 1 # increments level
            child = self.Node(deepcopy(root.obj), None) # creates new child (not connected yet)
            child.obj.doBotMove(self.getMove(child), self.player) # does a move
            positionsPlayed.append(child) # adds move to list of nodes
            newNode = self.findPosition(root, child) # finds child node with board, if none exist, adds new node
            root = newNode
            print(root.obj.board)

        # checks for tied game
        if level == 42:
            winner = 0
        else:
            winner = self.player
        print("The winner is: ", winner)
        self.scorePositions(winner, positionsPlayed) # scores positions based on who won

    # changes the score of all positions after a game
    def scorePositions(self, winner, pos):
        # positive scores are good for player 1, negative scores are good for player 2
        for x in pos:
            if winner == 1:
                print(1)
                x.score += 1
            elif winner == 2:
                print(2)
                x.score -= 1

    def findPosition(self, root, child):  # need to get a list of legal moves
        # returns node with current board
        for x in root.children:
            if x.obj.board.all() == child.obj.board.all():
                return x
        # else, add position and return it
        return self.connectNodes(root, child)

    def getMove(self, node):
        # gets starting score
        # were gonna pick moves with better scores, this way the machine starts learning
        # gather a legal move
        legalMoves = []
        for x in range(7):
            if self.isMoveLegal(node, x):
                legalMoves.append(x)
        move = random.randint(0, len(legalMoves) - 1)
        return move
        # percentage 0-100
        rand = random.randint(0, 100)
        # pick a move, not always the highest score
        if 0 <= rand <= self.exploit:
            if self.player == 1:
                base = -math.inf
                # chooses move based on scoring
                for item in node.children:
                    if item.score > base:
                        move = item.score
            else:
                base = math.inf
                # chooses move
                for item in node.children:
                    if item.score < base:
                        move = item.score
            return move
        else:
            return move

    def switchPlayer(self):
        if self.player == 1:
            self.player = 2
        else:
            self.player = 1

    def train(self, games):
        gamesPlayed = 0
        while gamesPlayed < games:
            b = Board()
            self.root = self.Node(b, None)
            self.play(self.root)
            gamesPlayed += 1
            if gamesPlayed % 10 == 0:
                print("\nNumber of games completed: ", gamesPlayed)
                if self.exploit < 98:
                    self.exploit += 1


            '''
            print("scores: ")
            self.printScores(self.root)
            print('\n')'''


        # this is where the positions need to be stored into a pickle file of sorts


    class Node:

        def __init__(self, boardOBJ, parent):
            self.obj = boardOBJ
            self.parent = parent
            self.score = 0 # keeps track of how good the board is
            self.children = [] # next set of possible moves

#testing
l = Learner()
l.train(10)
print(l.root.children)
l.printScores(l.root)




