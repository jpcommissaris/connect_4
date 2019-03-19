import pygame
import numpy as np
import random
import math

rand = random.Random()
BLACK = (0,0,0)
BLUE = (0,0,255)
RED = (255, 0, 0)
YELLOW = (255, 255, 0)

class Board():


    def __init__(self):
        # const
        self.rows = 6
        self.cols = 7
        #logic
        self.board = np.zeros((self.rows, self.cols)) #sets inital 2d array filled with zeros
        # graphics
        self.size = 100
        self.radius = (int)(self.size/3)
        self.player = 1
        self.winner = 0

    def __str__(self):
        str_board = "\n\n" + str(self.board).replace("0.", "_").replace("-1.", " O").replace("1.", "X")
        str_board = str_board.replace("[", " ").replace("]", " ")
        return str_board
    # --- graphics ---
    def drawBoard(self, win):
        for c in range(self.cols):
            for r in range(self.rows):
                rect = (c * self.size, (r + 1) * self.size, self.size, self.size)
                pygame.draw.rect(win, BLUE, rect)
                circle = (int((c + 0.5) * self.size), int((r + 1.5) * self.size))
                pygame.draw.circle(win, BLACK, circle, self.radius)

        for c in range(self.cols):
            for r in range(self.rows):
                if self.board[r][c] == 1:
                    circle = (int((c + 0.5) * self.size), int((r + 1.5) * self.size))
                    pygame.draw.circle(win, RED, circle, self.radius)
                elif self.board[r][c] == 2:
                    circle = (int((c + 0.5) * self.size), int((r + 1.5) * self.size))
                    pygame.draw.circle(win, YELLOW, circle, self.radius)

    def highlight(self, win, event):
        pygame.draw.rect(win, BLACK, (0, 0, self.width, self.size))
        mouseX = event.pos[0]  # checks x-position of the mouse on the screen
        if self.player == 1:
            pygame.draw.circle(win, RED, (mouseX, int(self.size / 2)), self.radius)
        else:
            pygame.draw.circle(win, YELLOW, (mouseX, int(self.size / 2)), self.radius)


    # --- logic ---
    def getMoves(self):
        # checks each column for space
        moves = [False, False, False, False, False, False, False]
        for m in range(self.rows):
            if self.board[0][m] == 0:
                moves[m] = True
        return moves

    def doMove(self, event):
        # get column to drop piece
        mouseX = event.pos[0]
        move = int(math.floor(mouseX / self.size))
        # loops down column until it finds a place with a piece
        for j in range(self.rows-1):
            if self.board[j][move] != 0:
                self.board[j-1][move] = self.player
                break
        # checks for winning move
        self.setWin()
        # switch turns
        if self.player == 1:
            self.player = 2
        else:
            self.player = 1

    def setWin(self):
        if self.checkWin():
            if self.player == 1:
                self.winner = 1
            else:
                self.winner = 2

    def checkWin(self):
        # check horizontal spaces
        for r in range(self.rows):
            for c in range(self.cols - 3):
                if self.board[r][c] == self.player and self.board[r + 1][c] == self.player and self.board[r + 2][c] == self.player and self.board[r + 3][c] == self.player:
                    return True

        # check vertical spaces
        for c in range(self.cols):
            for r in range(self.rows - 3):
                if self.board[r][c] == self.player and self.board[r][c + 1] == self.player and self.board[r][c + 2] == self.player and self.board[r][c + 3] == self.player:
                    return True

        # check left diagonal spaces
        for c in range(self.cols-3):
            for r in range(3, self.rows):
                if self.board[r][c] == self.player and self.board[r + 1][c - 1] == self.player and self.board[r + 2][c - 2] == self.player and self.board[r + 3][c - 3] == self.player:
                    return True

        # check right diagonal spaces
        for c in range(self.cols-3):
            for r in range(self.rows-3):
                if self.board[r][c] == self.player and self.board[r + 1][c + 1] == self.player and self.board[r + 2][c + 2] == self.player and self.board[r + 3][c + 3] == self.player:
                    return True
        return False



