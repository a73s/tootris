import pygame
from sys import exit

WIDTH = 500
HEIGHT = 720
WHITE = (255,255,255)
BACKGROUNDCOLOR = (31,9,75)
PIECESIZE = 30


def startMenu(window,icon):
    sentinel = True

    while sentinel:
        window.fill(BACKGROUNDCOLOR)
        window.blit(icon, (53,20))

        #draw messages
        font = pygame.font.Font('freesansbold.ttf', 15)
        temp = font.render('Press any key to start', True, WHITE)
        window.blit(temp,(175,380))

        #if you hit any key, the game starts
        for event in pygame.event.get():

            if event.type == pygame.QUIT:
                    
                pygame.quit()
                exit()

            if event.type == pygame.KEYDOWN:
                
                sentinel = False

        pygame.display.flip()


def pauseMenu(window):
    sentinel = True
    while sentinel:
        window.fill(BACKGROUNDCOLOR)

        #draw pause messages
        font = pygame.font.Font('freesansbold.ttf', 25)
        temp = font.render('Paused', True, WHITE)
        window.blit(temp, (200,300))

        font = pygame.font.Font('freesansbold.ttf', 15)
        temp = font.render('Press escape to resume', True, WHITE)
        window.blit(temp,(165,330))

        #if you hit escape, the pause menu closes
        for event in pygame.event.get():

                if event.type == pygame.QUIT:
                    
                    pygame.quit()
                    exit()

                if event.type == pygame.KEYDOWN:
                
                    if event.key == pygame.K_ESCAPE:
                        
                        sentinel = False

        pygame.display.flip()



def displayText(window, XY = (10,10), Font = 'freesansbold.ttf', size = 14, color = WHITE, XY2 = (10,10)):
    
    font = pygame.font.Font(Font, size)
    temp = font.render('Up Next:', True, color)
    window.blit(temp, XY)

    font = pygame.font.Font(Font, size)
    temp = font.render('Holding:', True, color)
    window.blit(temp, XY2)


def renderStuff(window, gameBoard, gamePiece, upNextPiece, heldPiece):
    #just general display stuff
    window.fill(BACKGROUNDCOLOR)
    gameBoard.draw()
    gamePiece.draw()
    gameBoard.displayScore(XY = (315,10))
    displayText(XY = (375,44), window = window, XY2 = (375, 374))
    upNextPiece.draw()
    try:
        heldPiece.draw()
    except:
        None
    
    pygame.draw.line(window,WHITE,(0,4*PIECESIZE), (PIECESIZE*10,4*PIECESIZE))
    pygame.draw.line(window,WHITE,(PIECESIZE*10,0), (PIECESIZE*10,HEIGHT))


def endMenu(score,window):
    sentinel = True

    while sentinel:
        window.fill(BACKGROUNDCOLOR)

        #draw pause messages
        font = pygame.font.Font('freesansbold.ttf', 25)
        temp = font.render('Game Over', True, WHITE)
        window.blit(temp, (185,300))

        font = pygame.font.Font('freesansbold.ttf', 15)
        temp = font.render('Press escape to restart', True, WHITE)
        window.blit(temp,(175,355))

        temp = font.render('Score: ' + str(score), True, (0,255,0))
        window.blit(temp,(215,330))

        for event in pygame.event.get():

                if event.type == pygame.QUIT:
                    
                    pygame.quit()
                    exit()

                if event.type == pygame.KEYDOWN:
                
                    if event.key == pygame.K_ESCAPE:
                        
                        sentinel = False

        pygame.display.flip()
