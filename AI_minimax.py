from board import Board
from copy import deepcopy

# based on a scoring mechanism for the best moves, the computer checks all possible future boards
# to a certain number of moves ahead
class Minimax:
    def __init__(self, board, height):
        self.player = 2
        # pass in the board object
        self.b = deepcopy(board)
        self.root = self.Node(board, None, None)  # current board
        self.height = height
        self.buildTree(self.root, self.height, self.b)

# --- builds a game tree using Nodes ---
    def buildLevel(self, node, board, player):
        for moves in range(7):
            a = deepcopy(board)  # copys so theres no reference
            if a.doTreeMove(moves, player):  # if the move is possible its added to the tree
                node.addChild(self.Node(a, node, moves))

    # recursively builds count levels
    def buildTree(self, root, count, board):
        if count <= 0:
            return 0
        else:
            self.player = (count % 2)+1 # gives either 1 or 2
            self.buildLevel(root, board, self.player)
            for x in range(len(root.children)):
                return self.buildTree(root.children[x], count-1, root.children[x].data)

    # just for testing
    def printTree(self, root):
        print("Score:  ", root.score, "\nboard:  \n", root.data.board,"move:  ", root.colOfMove)
        print("Parent: ", root.parent, "\n")
        for x in range(len(root.children)):
            self.printTree(root.children[x])


# --- finds best Node in tree ---
    def getBestNode(self, node, depth, isMax):
        if depth == 0:
            return node.score
        if isMax:
            best = -5000
            for childNode in node.children:
                score = self.getBestNode(childNode, depth-1, False)
                best = max(score, best)  # gets max between all children
                #print("best:", best)
                node.score = best
            print("Best:", best)
            return best
        else:
            worst = 5000
            for childNode in node.children:
                score = self.getBestNode(childNode, depth-1, True)
                worst = min(worst, score)  # gets max between all children
                #print("worst:", worst)
                node.score = worst
            print("Worst:", worst)
            return worst

    def getMove(self):
        n = self.getBestNode(self.root, self.height, True)
        print("best score: ", n)
        score = -6000
        move = 0
        for x in self.root.children:
            #print("children scores", x.score)
            # determines which move should be made based on highest score
            if x.score >= score:
                move = x.colOfMove
                score = x.score
                print("Current move:", move, "Score:", score)
        print("Move:", move)
        return move

    class Node:
        def __init__(self, obj, parent, col):
            self.data = obj
            self.score = obj.checkScore() # AI is player 2
            self.parent = parent
            self.children = []
            self.colOfMove = col  # stores the move in first level so it can actually be done

        def addChild(self, obj):
            self.children.append(obj)

'''
#testing only
b = Board()
print(b.board)
m = Minimax(b, 3) # must give odd number or looks ahead
#m.buildTree(m.root, m.height, m.b)
#m.printTree(m.root)
#m.getBestNode(m.root, m.height, True)
m.getMove()
m.printTree(m.root)
'''











