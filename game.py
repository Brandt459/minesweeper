import random
import numpy as np
from itertools import islice
import pygame

class Game:
    def __init__(self, gamemode):
        self.gamemode = None
        self.board = []     # [row, column, mine neighbors, visible?, flagged?]
        self.rows = 0
        self.columns = 0
        self.mineSquares = []
        self.gameover = False
        self.generateBoard(gamemode)
        self.flags = 0
        self.mines = 0

    def generateBoard(self, gamemode=-1, screen=None):
        oldGamemode = self.gamemode
        self.gamemode = gamemode if gamemode != -1 else self.gamemode
        self.board = []
        self.gameover = False
        if self.gamemode == 0:
            self.rows = 9
            self.columns = 9
            self.mines = 10
        elif self.gamemode == 1:
            self.rows = 16
            self.columns = 16
            self.mines = 40
        elif self.gamemode == 2:
            self.rows = 16
            self.columns = 30
            self.mines = 99
        if self.gamemode != oldGamemode:
            width = 30 * self.columns + 20
            height = 30 * self.rows + 120
            screen = pygame.display.set_mode(size=(width, height))
        
        population = []
        for tup in np.ndindex((self.rows, self.columns)):
            population.append(tup)
        mineSquares = sorted(random.sample(population, self.mines))

        input = iter(population)
        rows = [list(islice(input, self.rows)) for _ in range(self.columns)]

        for row in rows:
            newRow = []
            for square in row:
                square = list(square)
                if tuple(square) in mineSquares:
                    square.append(-1)
                else:
                    mineNeighbors = 0
                    for i in range(square[0] - 1, square[0] + 2):
                        for j in range(square[1] - 1, square[1] + 2):
                            if (i, j) in mineSquares:
                                mineNeighbors += 1
                    square.append(mineNeighbors)
                square.append(False)
                square.append(False)
                newRow.append(square)
            self.board.append(newRow)
    
    def findVoidBorder(self, row, col):
        rowMin = 0 if row == 0 else row - 1
        rowMax = self.rows if not row + 1 < self.rows else row + 2
        colMin = 0 if col == 0 else col - 1
        colMax = self.columns if not col + 1 < self.columns else col + 2

        for i in range(rowMin, rowMax):
            for j in range(colMin, colMax):
                if self.board[i][j][2] == 0 and not self.board[i][j][3] and not self.board[i][j][4]:
                    self.board[i][j][3] = True
                    self.findVoidBorder(i, j)
                if not self.board[i][j][4]:
                    self.board[i][j][3] = True

    def chordPreCheck(self, rowMin, rowMax, colMin, colMax):
        flags = 0
        for i in range(rowMin, rowMax):
            for j in range(colMin, colMax):
                if self.board[i][j][4]:
                    flags += 1
        return flags
    
    def chord(self, row, col):
        rowMin = 0 if row == 0 else row - 1
        rowMax = self.rows if not row + 1 < self.rows else row + 2
        colMin = 0 if col == 0 else col - 1
        colMax = self.columns if not col + 1 < self.columns else col + 2

        if self.board[row][col][2] == self.chordPreCheck(rowMin, rowMax, colMin, colMax):
            for i in range(rowMin, rowMax):
                for j in range(colMin, colMax):
                    self.board[i][j][3] = True
                    if self.board[i][j][2] == -1 and not self.board[i][j][4]:
                        self.gameover = True
                    if self.board[i][j][2] == 0 and not self.board[i][j][4]:
                        self.findVoidBorder(i, j)
