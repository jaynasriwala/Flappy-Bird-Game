import pygame
from pygame.locals import *
import sys
from random import randint

# Global Var and Constants


SCREEN_WIDTH = 1400
SCREEN_HEIGHT = 700
SCREEN=pygame.display.set_mode([SCREEN_WIDTH, SCREEN_HEIGHT]) # creating Display
GAME_IMAGES = {}
GAME_SOUNDS = {}
FPS = 30
initial_volume = 0.2
initial_volume2 = 0.2

playerX = SCREEN_WIDTH/6
playerY = SCREEN_HEIGHT/6

# gap = playerH * 3


# Functions
def welcomeScreen():
    while True:
        SCREEN.blit(GAME_IMAGES["background"],(0,0))
        SCREEN.blit(GAME_IMAGES["base"],(baseX,baseY))
        SCREEN.blit(GAME_IMAGES["player"],(playerX,playerY))
        SCREEN.blit(GAME_IMAGES["message"],(messageX,messageY))
        GAME_SOUNDS["backgroung_start"].set_volume(initial_volume)
        GAME_SOUNDS["backgroung_start"].play()
        pygame.display.update()
        
        for x in pygame.event.get():
            if x.type == KEYDOWN and x.key == K_ESCAPE:
                pygame.quit()
                sys.exit()
            if x.type == KEYDOWN and x.key == K_SPACE:
                GAME_SOUNDS["backgroung_start"].stop()
                return
def getRandomPipe():
    gap = GAME_IMAGES["player"].get_height()*3
    y2 = randint(gap,SCREEN_HEIGHT - GAME_IMAGES["base"].get_height())
    y1 = y2 - gap - GAME_IMAGES["pipe"][0].get_height()
    pipeX = SCREEN_WIDTH
    pipe = [
        {"x":pipeX,"y":y1},
        {"x":pipeX,"y":y2},
    ]
    return pipe

def gameLoop():
    GAME_SOUNDS["backgroung_play_time"].set_volume(initial_volume2)
    GAME_SOUNDS["backgroung_play_time"].play()
    newPipe1 = getRandomPipe()
    newPipe2 = getRandomPipe()
    newPipe3 = getRandomPipe()

    # list of upper pipes
    upperPipes = [
        {"x":SCREEN_WIDTH,"y":newPipe1[0]["y"] },
        {"x":SCREEN_WIDTH * 1.33 ,"y":newPipe2[0]["y"] },
        {"x":SCREEN_WIDTH * 1.66 ,"y":newPipe3[0]["y"] }
    ]
    lowerPipes = [
        {"x":SCREEN_WIDTH,"y":newPipe1[1]["y"] },
        {"x":SCREEN_WIDTH + SCREEN_WIDTH/3,"y":newPipe2[1]["y"] },
        {"x":SCREEN_WIDTH + SCREEN_WIDTH/0.75,"y":newPipe3[1]["y"] }
    ]

    score = 0
    pipeSpeedX = -20
    playerSpeedY = -9
    playerMaxSpeed = 10
    playerFlyingSpeed = -5
    playerAccY = 1
    playerFlying = False
    
    playerX = SCREEN_WIDTH/6
    playerY = SCREEN_HEIGHT/6

    while True:
        for x in pygame.event.get():
            if x.type == KEYDOWN and x.key == K_ESCAPE:
                pygame.quit()
                sys.exit()
            if x.type == KEYDOWN and (x.key == K_UP or x.key == K_w):
                if playerY > 0:
                    playerSpeedY = playerFlyingSpeed
                    playerFlying = True
                    GAME_SOUNDS["fly"].play()
        
        # moving player up
        playerY = playerY + playerSpeedY
        if playerFlying == True:
            playerFlying = False

        # pulling player down
        
        if playerSpeedY < playerMaxSpeed and not playerFlying:
            playerSpeedY = playerSpeedY + playerAccY

        # moving pipes
        for upperPipe , lowerPipe in zip(upperPipes,lowerPipes):
            upperPipe["x"] =upperPipe["x"] + pipeSpeedX
            lowerPipe["x"] =lowerPipe["x"] + pipeSpeedX
            
        # adding new pipes
        if upperPipes[0]["x"] < 0 :
            newPipe = getRandomPipe()
            upperPipes.append(newPipe[0])
            lowerPipes.append(newPipe[1])
        

        # removing old pipe
        if upperPipes[0]["x"] < 0:
            upperPipes.pop(0)
            lowerPipes.pop(0)

        # change in score
        playerCenterX = playerX + GAME_IMAGES["player"].get_width()/2
        for pipe in upperPipes:
            pipeCenterX = pipe["x"] + GAME_IMAGES["pipe"][0].get_width()/2
            if pipeCenterX <= playerCenterX < pipeCenterX + abs(pipeSpeedX):
                score = score + 1
                GAME_SOUNDS["point"].play()
        
        # player die
        if ishit(playerX,playerY,upperPipes,lowerPipes):
            GAME_SOUNDS["die"].play()
            
            pygame.time.wait(2000)
            return

        # bluiting up everythig
        SCREEN.blit(GAME_IMAGES["background"],(0,0))
        SCREEN.blit(GAME_IMAGES["player"],(playerX,playerY))
        for upperPipe , lowerPipe in zip(upperPipes,lowerPipes):
            SCREEN.blit(GAME_IMAGES["pipe"][0],(upperPipe["x"],upperPipe["y"]))
            SCREEN.blit(GAME_IMAGES["pipe"][1],(lowerPipe["x"],lowerPipe["y"]))
        SCREEN.blit(GAME_IMAGES["base"],(baseX,baseY))

        # blittin the score
        scoreDigits = [int(x) for x in list(str(score))]

        scoreX = 0
        scoreY = 0
        for digit in scoreDigits:
            SCREEN.blit(GAME_IMAGES["numbers"][digit], (scoreX,scoreY))
            scoreX += GAME_IMAGES["numbers"][digit].get_width()
        pygame.display.update()
        pygame.time.Clock().tick(FPS)


    

def ishit(playerX,playerY,upperPipes,lowerPipes):
    pipeHight = GAME_IMAGES["pipe"][0].get_height()
    pipeWidth = GAME_IMAGES["pipe"][0].get_width()
    playerWidth = GAME_IMAGES["player"].get_width() 
    playerHight = GAME_IMAGES["player"].get_height()

    # hit with base celling
    if playerY < 0 or playerY + playerHight  > SCREEN_HEIGHT - GAME_IMAGES["base"].get_height():
        return True
    
    
    # hit with upper pipes
    for pipe in upperPipes:
        if (playerY < pipe["y"] + pipeHight ) and (pipe["x"] - playerWidth < playerX < pipe["x"] + pipeWidth):
            return True

    

    # hit with lower pipes
        
    for pipe in lowerPipes:
        if (playerY + playerWidth >pipe["y"] ) and (pipe["x"] - playerWidth < playerX < pipe["x"] + pipeWidth):
            return True


    return False

# Main program
pygame.init()
pygame.display.set_caption("Flappy Bird --- By Jay Nasriwala")

GAME_IMAGES["background"]= pygame.image.load("images/bg2.jpg").convert_alpha()
GAME_IMAGES["base"] = pygame.image.load("images/base_3.png").convert_alpha()
GAME_IMAGES["player"] = pygame.image.load("images/bird.png").convert_alpha()
GAME_IMAGES["message"] = pygame.image.load("images/message.png").convert_alpha()
GAME_IMAGES["numbers"] = (
    pygame.image.load("images/0.png").convert_alpha()
    ,pygame.image.load("images/1.png").convert_alpha()
    ,pygame.image.load("images/2.png").convert_alpha()
    ,pygame.image.load("images/3.png").convert_alpha()
    ,pygame.image.load("images/4.png").convert_alpha()
    ,pygame.image.load("images/5.png").convert_alpha()
    ,pygame.image.load("images/6.png").convert_alpha()
    ,pygame.image.load("images/7.png").convert_alpha()
    ,pygame.image.load("images/8.png").convert_alpha()
    ,pygame.image.load("images/9.png").convert_alpha()

)
GAME_IMAGES["pipe"] = (
    pygame.image.load("images/pipe1_u.png").convert_alpha(),
    pygame.image.load("images/pipe1_d.png").convert_alpha()
)

GAME_SOUNDS["die"] = pygame.mixer.Sound("sound/die.wav")
GAME_SOUNDS["fly"] = pygame.mixer.Sound("sound/fly.wav")
GAME_SOUNDS["point"] = pygame.mixer.Sound("sound/point.wav")
GAME_SOUNDS["backgroung_start"] = pygame.mixer.Sound("sound/playback1.mp3")
GAME_SOUNDS["backgroung_play_time"] = pygame.mixer.Sound("sound/playback2.mp3")
#              (x, y)
# background = (0, 0)
# base       = (0, SCREEN_HEIGHT- base_height)
# player     = (SCREEN_WIDTH/5, SCREEN_HEIGHT/2)
# message    = (SCREEN_WIDTH/2-IMG_WIDTH, SCREEN_HEIGHT/2-IMG-HEIGHT)

baseX = 0
baseY = SCREEN_HEIGHT-GAME_IMAGES["base"].get_height()

messageX = SCREEN_WIDTH/2 - GAME_IMAGES["message"].get_width()/2
messageY = SCREEN_HEIGHT/2 - GAME_IMAGES["message"].get_height()/2

while True:

    welcomeScreen()
    gameLoop()
    
