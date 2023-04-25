'''
Created on Apr 23, 2022

@author: Adam Seals
'''
from random import choice, randint
import pygame


class Block():
    #this is basically just holds data about color and wether the block is hollow or not
    def __init__(self, hollow = True, color = (0,0,0,0)):

        self.hollow = hollow

        self.color = color

        if not hollow:
            self.color = color
        



class Piece():

    def __init__(self, gameBoard, gameWindow):

        self.ROTATION_LOCATION_MAP = ( ((1,4), (2,4), (3,4), (4,4)) , ((1,3), (2,3), (3,3), (4,3)) , ((1,2), (2,2), (3,2), (4,2)) , ( (1,1), (2,1), (3,1), (4,1)) )
        self.gameWindow = gameWindow
        self.gameBoard = gameBoard
        self.pieceX = 11.45
        self.pieceY = -2
        self.blockSize = gameBoard.blockSize
        self.tickCounter = 0
        self.expired = False
        

        self._generatePieceData()
    

    def setMain(self):

        self.pieceX = 3
        self.pieceY = -4
        self.tickCounter = 0


    def setHold(self):

        self.pieceX = 11.45
        self.pieceY = 9



    def _isClear(self, LocationData , movementOffsets = (0,0)):
        #checks if a future location is clear
        clearness = True

        newPieceX = self.pieceX + movementOffsets[0]
        newPieceY = self.pieceY + movementOffsets[1]
        
        for (rowNum, row) in enumerate(LocationData):

            for (colNum, block) in enumerate(row):
                
                blockX = newPieceX + colNum
                blockY = newPieceY + rowNum 

                if not block.hollow:

                    if blockY < 0:#handles blocks above the buffer line
                        if (blockX > self.gameBoard.XMax-1) or (blockX < 0):
                            clearness = False

                    else:
                        if ((blockX > self.gameBoard.XMax-1) or (blockX < 0)):
                            #checks if piece is out of bounds
                            clearness = False
                        try:
                            if not self.gameBoard.boardData[blockY][blockX].hollow:
                                #checks if a piece on the board interferes with the movement
                                clearness = False
                        except IndexError:
                            clearness = False
        return clearness
    

    def _generatePieceData(self):
        '''
        - selects a random piece and sets up the piece data to be manipulated by the other methods
        - I chose to hard-code the initial piece and rotate the piece instead of hard coding every possible rotation, 
        this also allows you to add new pieces easily if you want to spice the game up,
        but unfortunately you cant make pieces that dont fit in a 4x4 square, at least not without a lot of trouble. 
        '''

        pieceType = choice(('I','O','L','J','T','Z','S'))
        
        #self.pieceData = ( ( , , , ) , ( , , , ) , ( , , , ) , ( , , , ) ) 4x4 list matrix
        
        if pieceType == 'I':
            
            self.pieceData = list(( (Block(),Block(),Block(hollow = False, color = (0,255,255)),Block()) ,  (Block(),Block(),Block(hollow = False, color = (0,255,255)),Block()) , (Block(),Block(),Block(hollow = False, color = (0,255,255)),Block()) , (Block(),Block(),Block(hollow = False, color = (0,255,255)),Block()) ))
            return
        
        if pieceType == 'O':

            self.pieceData = list(( ( Block() , Block() , Block() , Block() ) , ( Block() , Block(hollow = False, color = (255, 233, 0)) , Block(hollow = False, color = (255, 233, 0)) , Block() ) , ( Block() , Block(hollow = False, color = (255, 233, 0)) , Block(hollow = False, color = (255, 233, 0)) , Block() ) , ( Block() , Block() , Block() , Block() ) ))
            return

        if pieceType == 'L':

            self.pieceData = list(( (Block() ,Block(hollow = False, color = (255, 126, 0)) ,Block() ,Block() ) , (Block() ,Block(hollow = False, color = (255, 126, 0)) ,Block() ,Block() ) , (Block() ,Block(hollow = False, color = (255, 126, 0)) ,Block(hollow = False, color = (255, 126, 0)) ,Block() ) , (Block() ,Block() ,Block() ,Block() ) ))
            return
    
        if pieceType == 'J':

            self.pieceData = list(( (Block() ,Block() ,Block(hollow = False, color = (3, 65, 174)) ,Block() ) , (Block() ,Block() ,Block(hollow = False, color = (3, 65, 174)) ,Block() ) , (Block() ,Block(hollow = False, color = (3, 65, 174)) ,Block(hollow = False, color = (3, 65, 174)) ,Block() ) , (Block() ,Block() ,Block() ,Block() ) ))
            return
        
        if pieceType == 'T':

            self.pieceData = list(( (Block() ,Block() ,Block() ,Block() ) , (Block() ,Block(hollow = False, color = (153,51,255)) ,Block() ,Block() ) , (Block() ,Block(hollow = False, color = (153,51,255)) ,Block(hollow = False, color = (153,51,255)) ,Block() ) , (Block() ,Block(hollow = False, color = (153,51,255))  ,Block() ,Block() ) ))
            return
        
        if pieceType == 'Z':
            
            self.pieceData = list(( (Block() ,Block() ,Block() ,Block() ) , (Block() , Block(hollow = False, color = (255, 50, 19)), Block(hollow = False, color = (255, 50, 19)),Block() ) , ( Block(), Block(), Block(hollow = False, color = (255, 50, 19)), Block(hollow = False, color = (255, 50, 19))) , ( Block(),Block() ,Block() ,Block() ) ))
            return
        
        if pieceType == 'S':

            self.pieceData = list(( ( Block(), Block(), Block(), Block()) , ( Block(), Block(hollow = False, color = (44, 249, 0)), Block(hollow = False, color = (44, 249, 0)), Block()) , ( Block(hollow = False, color = (44, 249, 0)), Block(hollow = False, color = (44, 249, 0)), Block(), Block()) , ( Block(), Block(), Block(), Block()) ))
            return


    def _place(self):

        #writes data from the piece to the game board
        for rowNum, row in enumerate(self.pieceData):
            
            for colNum, block in enumerate(row):

                if not block.hollow:
                    if (self.pieceY + rowNum) < 0:
                        self.gameBoard.expired = True

                    else:
                        self.gameBoard.boardData[self.pieceY+rowNum][self.pieceX+colNum] = block

        self.expired = True
        self.gameBoard.score += 5
        self.gameBoard.checkForClears()


    def draw(self):
        #draws the piece
        for (rowNum, row) in enumerate(self.pieceData):

            for (colNum, block) in enumerate(row):
                
                blockPixelStartX = (self.pieceX * self.blockSize) + (colNum * self.blockSize)
                blockPixelStartY = (self.pieceY * self.blockSize) + (rowNum * self.blockSize) + (4 * self.blockSize)
                
                blockColor = block.color
                
                if not block.hollow:
                    pygame.draw.rect( self.gameWindow , blockColor , pygame.Rect( blockPixelStartX , blockPixelStartY , self.blockSize , self.blockSize ), border_radius = 3)


    def moveDown(self):
        #move the down if the pieces below are clear, if not clear, place down the piece
        if self._isClear(self.pieceData, (0,1)):
            self.pieceY += 1
        else:
            self._place()


    def moveLeft(self):
        if self._isClear(self.pieceData, (-1,0)):
            self.pieceX -= 1
        return


    def moveRight(self):
        if self._isClear(self.pieceData, (1,0)):
            self.pieceX += 1

        return


    def rotate(self):
        '''
        Im using a tuple 'location map' that has the coordinates of each block posiotion after 1 rotation, 
        trust me this is the best way to do it for a small matrix of a set size.
        there may be another way to do it but i have already spent too long making this class and this was the simplest and fastest way
        the offset map can be found in __init__
        '''
        tempData = [ ['','','',''] , ['','','',''] , ['','','',''] , ['','','',''] ]

        for rowNum in range(4):
            for colNum in range(4):

                tempData[(self.ROTATION_LOCATION_MAP[rowNum][colNum][0])-1][(self.ROTATION_LOCATION_MAP[rowNum][colNum][1])-1] = self.pieceData[rowNum][colNum]

        if self._isClear(tempData):

            self.pieceData = tempData

        return


    def tick(self, tps, allowMoveDown): #moves the piece down after a changing interval

        self.tickCounter += 1
        tickPerDrop = tps - self.gameBoard.speed
        
        if self.tickCounter == tickPerDrop:
            self.tickCounter = 0
            if allowMoveDown:
                self.moveDown()


    def isExpired(self):
        return self.expired

