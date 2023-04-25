import pygame
from piece import Block
from math import log

class Board():

    #stores data about the game board and draws the gameboard
    def __init__(self, boardXYMax = (10,20), blockSize = 50, gameWindow = None):

        self.gameWindow = gameWindow
        self.speed = 4
        self.score = 0
        self.blockSize = blockSize
        self.expired = False
        
        self.removedRows = 0
        self.totalRemovedRows = 1
        self.XMax = boardXYMax[0]
        self.YMax = boardXYMax[1]

        self.boardData = [['' for i in range(self.XMax)] for j in range(self.YMax)]

        #fills board with empty blocks
        for row in range(self.YMax):
            for column in range(self.XMax):
                self.boardData[row][column] = Block()
            

    def checkForClears(self):
        #checks for full rows
        for rowNum, row in enumerate(self.boardData):
            lineFull = True

            for block in row:

                if block.hollow:
                    lineFull = False

            
            if lineFull:
                #deletes full row
                self.boardData.pop(rowNum)
                #inserts new row at the top
                self.boardData.insert(0, [Block() for j in range(self.XMax)])
                self.removedRows += 1
                self.totalRemovedRows += 1

        self.score += 10 * self.removedRows * self.removedRows

        #removing more rows at once gives exponentially more points

        #increases the speed when you clear 2 rows
        if self.speed < 30:
            if self.removedRows > 0:
                #I was using a graphing calculator to find a good equation here, I though this looked good
                #the starting speed can be adjusted with the starting value of totalRemovedRows
                self.speed = round(14*log(self.totalRemovedRows,10) +2)

        self.removedRows = 0


    def isExpired(self):
        return self.expired


    def displayScore(self, XY = (10,10), Font = 'freesansbold.ttf', size = 14, color = (255,255,255)):
        font = pygame.font.Font(Font, size)
        temp = font.render('Score: ' + str(self.score), True, color)
        self.gameWindow.blit(temp, XY)

        '''
        font = pygame.font.Font(Font, size)
        temp = font.render('Speed: ' + str(self.speed), True, color)
        self.gameWindow.blit(temp, (10,15))

        font = pygame.font.Font(Font, size)
        temp = font.render('rows: ' + str(self.totalRemovedRows), True, color)
        self.gameWindow.blit(temp, (2,0))
        '''

    def draw(self):
        if not self.expired:
            for (rowNum, row) in enumerate(self.boardData):

                for (colNum, block) in enumerate(row):

                    blockPixelStartX = colNum * self.blockSize
                    blockPixelStartY = (rowNum * self.blockSize) + (4 * self.blockSize)
                    
                    blockColor = block.color
                    
                    if not block.hollow:
                        pygame.draw.rect( self.gameWindow , blockColor , pygame.Rect( blockPixelStartX , blockPixelStartY , self.blockSize , self.blockSize ), border_radius = 3)

