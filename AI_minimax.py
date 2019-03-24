from board import Board
from copy import copy

# based on a scoring mechanism for the best moves, the computer checks all possible future boards
# to a certain number of moves ahead
class Minimax:
    def __init__(self, board, height):
        self.b = board # pass in the board object
        self.root = self.Node(board, None, None)  # current board
        self.height = height
        self.buildTree(self.root, self.height)

# --- builds a game tree using Nodes ---
    def buildLevel(self, node):
        for moves in range(7):
            a = copy(node.data)  # copys so theres no reference
            if a.doTreeMove(moves):  # if the move is possible its added to the tree
                node.addChild(self.Node(a, node, moves))

    # recursively builds count levels
    def buildTree(self, root, count):
        if count <= 0:
            return 0
        else:
            self.buildLevel(root)
            for x in range(len(root.children)):
                self.buildTree(root.children[x], count-1)

    # just for testing
    def printTree(self, root):
        print("score:  ", root.score, "parent:  ", root.parent,"move:  ", root.colOfMove)
        for x in range(len(root.children)):
            self.printTree(root.children[x])


# --- finds best Node in tree ---
    def getBestNode(self, node, height, MAX):
        if height == 0:
            node.score = node.data.checkScore(1, node.colOfMove)
            print("Node score: ", node.score)
            return node.data.checkScore(1, node.colOfMove)  # base case returns boards score
        if MAX:
            best = -5000
            for childNode in node.children:
                score = self.getBestNode(childNode, height-1, False)
                best = max(score, best)  # gets max between all children
            node.score = best
            return best
        else:
            worst = 5000
            for childNode in node.children:
                score = self.getBestNode(childNode, height-1, True)
                worst = min(worst, score)  # gets max between all children
            node.score = worst
            return worst

    def getMove(self):
        n = self.getBestNode(self.root, self.height, True)
        print("best score: ", n)
        score = -6000
        move = 0
        for x in self.root.children:
            print("children scores", x.score)
            # determines which move should be made based on highest score
            if x.score > score:
                move = x.colOfMove
                score = x.score
                print("current: ", move)
        print(move)
        return move

    class Node:
        def __init__(self, obj, parent, col):
            self.data = obj
            self.score = 0
            self.parent = parent
            self.children = []
            self.colOfMove = col  # stores the move in first level so it can actually be done

        def addChild(self, obj):
            self.children.append(obj)



b = Board()
m = Minimax(b, 4)
m.getMove()
m.printTree(m.root)














