'''
Created on Mar 24, 2022

@author: Adam Seals
'''
import pygame
from Display import *
from Piece import Piece
from Board import *

TPS = 30
PIECESIZE = 30


def main():

    pygame.init()
    window = pygame.display.set_mode((WIDTH, HEIGHT))
    
    pygame.display.set_caption('Tootris')
    icon = pygame.image.load('tootris.png')
    pygame.display.set_icon(icon)
    clock = pygame.time.Clock()
    newPieceCheck = True
    heldPiece = None
    swapPiece = 0
    canSwap = 1

    #the main game loop
    while True:
        allowMoveDownThisTick = True

        if swapPiece:
            heldPiece,gamePiece = gamePiece,heldPiece
                    
            heldPiece.setHold()
            newPieceCheck = True

            try:
                gamePiece.setMain()
            except AttributeError:
                newPieceCheck = True
            
            swapPiece = 0
            canSwap = 0


        try: #check if the game ends
            newGame = gameBoard.isExpired()
            endOfGame = True
        except UnboundLocalError:
            newGame = True


        if newGame: #start a new game if the game is done
            try:
                if endOfGame:
                    endMenu(gameBoard.score,window)
            except UnboundLocalError: 
                startMenu(window, icon)

            gameBoard = Board(gameWindow = window, boardXYMax = (10,20), blockSize = PIECESIZE)
            upNextPiece = Piece(gameBoard = gameBoard, gameWindow = window)
            heldPiece = None
            newGame = False
        

        try: #check if a new piece is required
            newPieceCheck = gamePiece.isExpired()
        except (UnboundLocalError, AttributeError): #attribute error exception is required if the piece is put on hold
            newPieceCheck = True


        if newPieceCheck: #move the next piece in and create a new piece to be next up
            gamePiece = upNextPiece
            gamePiece.setMain()
            upNextPiece = Piece(gameBoard = gameBoard, gameWindow = window)
            dropStopper = True
            newPieceCheck = False
            canSwap = 1

        
        for event in pygame.event.get():
            '''
            this loop checks if you hit the x button
            also checks for keypresses
            '''
            if event.type == pygame.QUIT:
                
                pygame.quit()
                exit()
            
            if event.type == pygame.KEYDOWN:

                if event.key == pygame.K_UP:
                    gamePiece.rotate()

                if event.key == pygame.K_LEFT:
                    gamePiece.moveLeft()

                if event.key == pygame.K_RIGHT:
                    gamePiece.moveRight()
                
                if event.key == pygame.K_ESCAPE:
                    pauseMenu(window)
                
                if event.key == pygame.K_RCTRL:
                    if canSwap:
                        swapPiece = 1


        pressed = pygame.key.get_pressed()

        if dropStopper:

            if not pressed[pygame.K_DOWN]:
                #this in addition to drop stopper allows the piece to be moved down fast but the input does not apply to the next piece
                dropStopper = False
        else:
            if pressed[pygame.K_DOWN]:
                gamePiece.moveDown()
                allowMoveDownThisTick = False

    
        gamePiece.tick(tps = TPS, allowMoveDown = allowMoveDownThisTick)
        
        renderStuff(window, gameBoard, gamePiece, upNextPiece, heldPiece)
        pygame.display.flip()
        clock.tick(TPS)
        
      
main()
