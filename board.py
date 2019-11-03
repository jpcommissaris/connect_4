import pygame
import numpy as np
import random
import math



BLACK = (0,0,0)
BLUE = (20,40,250)
RED = (255, 0, 0)
YELLOW = (250, 248, 57)
WHITE = (255,255,255)


class Board():

    def __init__(self):
        # board constant
        self.rows = 6
        self.cols = 7
        self.board = np.zeros((self.rows, self.cols))  # sets inital 2d array filled with zeros
        # logic
        self.player = 1
        self.winner = 0
        self.p1Score = 0
        self.p2Score = 0
        # graphics
        self.size = 75
        self.radius = (int)(self.size * .38)

    # --- graphics ---
    def drawBoard(self, win):
        offset = 40
        for c in range(self.cols):
            for r in range(self.rows):
                rect = (offset+c * self.size, (r + 1) * self.size-offset, self.size, self.size)
                pygame.draw.rect(win, YELLOW, rect)
                posCircle = (offset+int((c + 0.5) * self.size), int((r + 1.5) * self.size)-offset)
                # determines color of circle
                if self.board[r][c] == 1:
                    color = RED
                elif self.board[r][c] == 2:
                    color = BLACK
                else:
                    color = WHITE
                pygame.draw.circle(win, color, posCircle, self.radius)

    def drawTexts(self, win):
        myfont = pygame.font.SysFont('helvetica', 20)
        redScore = myfont.render("P1: "+str(self.p1Score), False, (0, 0, 0))
        blackScore = myfont.render("P2: "+str(self.p2Score), False, (0, 0, 0))
        if self.winner == 1 or self.winner == 2:
            winFont = pygame.font.SysFont('helvetica', 42)
            theWinner = winFont.render("Player " + str(self.winner) + " wins!!", False, (0,255,0))
            win.blit(theWinner, (172,166))
        win.blit(redScore, (50, 490))
        win.blit(blackScore, (505, 490))

    def newGameButton(self, win):
        pygame.draw.rect(win, (40, 250, 40), (250, 520, 106, 30))
        pygame.draw.rect(win,BLACK,(250,520,106,30),1)
        myfont = pygame.font.SysFont('helvetica', 18)
        buttonText = myfont.render("New Game", False, (0, 0, 0))
        win.blit(buttonText, (259, 526))




    # --- logic ---
    def getMoves(self):
        # checks each column for space
        moves = [False, False, False, False, False, False, False]
        for m in range(self.cols):
            if self.board[0][m] == 0:
                moves[m] = True
        return moves
    def getNumMoves(self):
        moves = []
        for m in range(7):
            if self.getMoves()[m]:
                moves.append(m)
        return moves
    def isMoveLegal(self, col):
        if self.board[0][col] == 0:
            return True
        else:
            return False


    def isBoardFull(self):
        if self.getMoves() == [False, False, False, False, False, False, False]:
            return True
        else:
            return False

    def doMove(self, event):
        # get column to drop piece
        mouseX = event.pos[0] + 40
        mouseY = event.pos[1]
        move = int(math.floor(mouseX / self.size))-1
        if self.getMoves()[move] and 30 < mouseY < 490: # checks if its at the top, and if inside bpard
            # loops up until it find empty space
            for r in range(self.rows-1, -1, -1): # start, stop, step_size
                if self.board[r][move] == 0:
                    self.board[r][move] = self.player
                    # checks for winning move
                    self.setWin()
                    # switch turns
                    if self.player == 1:
                        self.player = 2
                    else:
                        self.player = 1
                    break

    def doTreeMove(self, col, player):
        if self.getMoves()[col]:
            for r in range(self.rows-1, -1, -1): # start, stop, step_size
                if self.board[r][col] == 0:
                    self.board[r][col] = player
                    return True
        return False

    def setWin(self):
        if self.checkWin():
            if self.player == 1:
                self.winner = 1
                self.p1Score += 1
            else:
                self.winner = 2
                self.p2Score += 1

    # self.rows = 6, self.cols = 7
    def checkWin(self):
        # check vertical spaces
        for r in range(self.rows-3):
            for c in range(self.cols):
                if self.board[r][c] == self.player and self.board[r + 1][c] == self.player and self.board[r + 2][c] == self.player and self.board[r + 3][c] == self.player:
                    return True

        # check horizontal spaces
        for r in range(self.rows):
            for c in range(self.cols-3):
                if self.board[r][c] == self.player and self.board[r][c + 1] == self.player and self.board[r][c + 2] == self.player and self.board[r][c + 3] == self.player:
                    return True

        # check left diagonal spaces
        for r in range(3, self.rows):
            for c in range(self.cols-3):
                if self.board[r][c] == self.player and self.board[r - 1][c + 1] == self.player and self.board[r - 2][c + 2] == self.player and self.board[r - 3][c + 3] == self.player:
                    return True

        # check right diagonal spaces
        for r in range(self.rows-3):
            for c in range(self.cols-3):
                if self.board[r][c] == self.player and self.board[r + 1][c + 1] == self.player and self.board[r + 2][c + 2] == self.player and self.board[r + 3][c + 3] == self.player:
                    return True
        return False

# --- different types of bots ---
    def doRandomMove(self):
        move = random.randint(0, 6)
        if self.getMoves()[move]:
            for r in range(self.rows - 1, -1, -1):  # start, stop, step_size
                if self.board[r][move] == 0:
                    self.board[r][move] = self.player
                    # checks for winning move
                    self.setWin()
                    self.player = 1
                    break
        else:
            for x in range(6):
                if self.getMoves()[x]:
                    for r in range(self.rows - 1, -1, -1):  # start, stop, step_size
                        if self.board[r][x] == 0:
                            self.board[r][x] = self.player
                            # checks for winning move
                            self.setWin()
                            self.player = 1
                            break
                    break

    def doMinimaxMove(self, move):
        for r in range(self.rows - 1, -1, -1):  # start, stop, step_size
            if self.board[r][move] == 0:
                self.board[r][move] = self.player
                # checks for winning move
                self.setWin()
                self.player = 1
                break

    def doBotMove(self, col, p):
        for r in range(self.rows - 1, -1, -1):  # start, stop, step_size
            if self.board[r][col] == 0:
                self.board[r][col] = p
                break


# checks score of the board, must use on a new board where a possible move is player

    def checkScore(self): # p is player, c is column of move
        score = 0
        # center
        for r in range(self.rows):
            if self.board[r][3] == 2:
                score += 2
            if self.board[r][2] == 2:
                score += 1
            if self.board[r][4] == 2:
                score += 1
        # vertical
        for cols in range(self.cols):
            slice = []
            for x in list(self.board[:, cols]): # list of one row all columns
                slice.append(x)
            for rows in range(self.rows - 3): # checks all squares for moves
                square = slice[rows:rows + 4]
                score += self.checkSquare(square)
        # horizontal
        for rows in range(self.rows):
            slice = []
            for x in list(self.board[rows, :]):  # list of one row all columns
                slice.append(x)
            for cols in range(self.cols - 3):  # checks all squares for moves
                square = slice[cols:cols + 4]
                score += self.checkSquare(square)
        # forward slash '/'
        for rows in range(self.rows - 3):
            for cols in range(self.cols - 3):
                square = []
                for x in range(4):
                    square.append(self.board[rows+x][cols+x]) # 1 up and 1 right
                score += self.checkSquare(square)
        # backward slash '\'
        for rows in range(3, self.rows):
            for cols in range(self.cols - 3):
                square = []
                for x in range(4):
                    square.append(self.board[rows - x][cols + x])  # 1 down and 1 right
                score += self.checkSquare(square)
        # returns score of board
        print(score)
        return score



    def checkSquare(self, sq):
        score = 0
        # determine whose who
        me = 2
        them = 1
        # defense
        if sq.count(them) == 4:
            score -= 100
        elif sq.count(them) == 3 and sq.count(0) == 1:
            score -= 10
        elif sq.count(them) == 2 and sq.count(0) == 2:
            score -= 3
        # offense
        if sq.count(me) == 4:
            score += 1000
        elif sq.count(me) == 3 and sq.count(0) == 1:
            score += 7
        elif sq.count(me) == 2 and sq.count(0) == 2:
            score += 1
        return score



