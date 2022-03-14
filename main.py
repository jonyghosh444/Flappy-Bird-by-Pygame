# Hare Krishna
import random
import sys
import pygame
from pygame.locals import *

# Global variables for the game
FPS = 30
SCREENWIDTH = 800
SCREENHEIGHT = 930
SCREEN = pygame.display.set_mode((SCREENWIDTH, SCREENHEIGHT))
GROUND_Y = SCREENHEIGHT * 0.8
GAME_SPRITES = {}
GAME_SOUNDS = {}
PLAYER = 'Gallery/sprites/bird.png'
BACKGROUND = 'Gallery/sprites/background.jpg'
PIPE = 'Gallery/sprites/pipe.png'


def welcomeScreen():
    player_x = int(SCREENWIDTH / 5)
    player_y = int((SCREENHEIGHT - GAME_SPRITES['player'].get_height()) / 2)
    message_x = int((SCREENWIDTH - GAME_SPRITES['message'].get_width()) / 2)
    message_y = int(SCREENHEIGHT * 0.01)
    base_x = 0
    while True:
        for event in pygame.event.get():
            if event.type == QUIT or (event.type == KEYDOWN and event.key == K_ESCAPE):
                pygame.quit()
                sys.exit()

            elif event.type == KEYDOWN and (event.key == K_SPACE or event.key == K_UP):
                return
            else:
                SCREEN.blit(GAME_SPRITES['background'], (0, 0))
                SCREEN.blit(GAME_SPRITES['player'], (player_x, player_y))
                SCREEN.blit(GAME_SPRITES['message'], (message_x, message_y))
                SCREEN.blit(GAME_SPRITES['base'], (base_x, GROUND_Y))
                pygame.display.update()
                FPS_CLOCK.tick(FPS)


def mainGame():
    score = 0
    player_x = int(SCREENWIDTH / 5)
    player_y = int(SCREENWIDTH / 2)
    base_x = 0

    # create 2 pipes
    newPipe1 = getRandomPipe()
    newPipe2 = getRandomPipe()

    # list of upper pipes
    upperPipes = [
        {'x': SCREENWIDTH + 200, 'y': newPipe1[0]['y']},
        {'x': SCREENWIDTH + 200 + (SCREENWIDTH / 2), 'y': newPipe2[0]['y']},
    ]

    # list of lower pipes
    lowerPipes = [
        {'x': SCREENWIDTH + 200, 'y': newPipe1[1]['y']},
        {'x': SCREENWIDTH + 200 + (SCREENWIDTH / 2), 'y': newPipe2[1]['y']},
    ]

    # velocity
    pipeVel_x = -4
    playerVel_y = -9
    playerMaxVel_y = 10
    # playerMinVel_y = -8
    playerAcc_y = 1

    playerFlapAccV = -8  # velocity while flapping
    playerFlapped = False  # It is true only when the bird is flapping

    while True:
        for event in pygame.event.get():
            if event.type == QUIT or (event.type == KEYDOWN and event.key == K_ESCAPE):
                pygame.quit()
                sys.exit()

            if event.type == KEYDOWN and (event.key == K_SPACE or event.key == K_UP):
                if player_y > 0:
                    playerVel_y = playerFlapAccV
                    playerFlapped = True
                    GAME_SOUNDS['wing'].play()

        crashTest = isCollide(player_x, player_y, upperPipes,
                              lowerPipes)  # This function will return true if the player is crashed
        if crashTest:
            return

        # check for score
        playerMidPos = player_x + GAME_SPRITES['player'].get_width() / 2
        for pipe in upperPipes:
            pipeMidpos = pipe['x'] + GAME_SPRITES['pipe'][0].get_width() / 2
            if pipeMidpos <= playerMidPos < pipeMidpos + 4:
                score += 1
                print(f'Your score is {score}')
                GAME_SOUNDS['point'].play()

        if playerVel_y < playerMaxVel_y and not playerFlapped:
            playerVel_y += playerAcc_y

        if playerFlapped:
            playerFlapped = False
        playerHeight = GAME_SPRITES['player'].get_height()
        player_y = player_y + min(playerVel_y, GROUND_Y - player_y - playerHeight)

        # move pipes to the left
        for upperPipe, lowerPipe in zip(upperPipes, lowerPipes):
            upperPipe['x'] += pipeVel_x
            lowerPipe['x'] += pipeVel_x

        # Add a new pipe when the first pipe about to cross the leftmost part of the screen
        if 0 < upperPipes[0]['x'] < 5:
            newPipe = getRandomPipe()
            upperPipes.append(newPipe[0])
            lowerPipes.append(newPipe[1])

        # if the pipe is out of the screen, remove it
        if upperPipes[0]['x'] < -GAME_SPRITES['pipe'][0].get_width():
            upperPipes.pop(0)
            lowerPipes.pop(0)

        # lets blit our sprites now
        SCREEN.blit(GAME_SPRITES['background'], (0, 0))

        for upperPipe, lowerPipe in zip(upperPipes, lowerPipes):
            SCREEN.blit(GAME_SPRITES['pipe'][0], (upperPipe['x'], upperPipe['y']))
            SCREEN.blit(GAME_SPRITES['pipe'][1], (lowerPipe['x'], lowerPipe['y']))

        SCREEN.blit(GAME_SPRITES['base'], (base_x, GROUND_Y))
        SCREEN.blit(GAME_SPRITES['player'], (player_x, player_y))
        myDigits = [int(x) for x in list(str(score))]
        width = 0
        for digit in myDigits:
            width += GAME_SPRITES['numbers'][digit].get_width()
        XOffSet = (SCREENWIDTH - width) / 2

        for digit in myDigits:
            SCREEN.blit(GAME_SPRITES['numbers'][digit], (XOffSet, SCREENHEIGHT * 0.12))
            XOffSet += GAME_SPRITES['numbers'][digit].get_width()
        pygame.display.update()
        FPS_CLOCK.tick(FPS)


def isCollide(player_x, player_y, upperPipes, lowerPipes):
    if player_y > GROUND_Y  or player_y < 0:
        GAME_SOUNDS['hit'].play()
        return True
    #
    for pipe in upperPipes:
        pipeHeight = GAME_SPRITES['pipe'][0].get_height()
        if player_y < pipeHeight + pipe['y'] and abs(player_x - pipe['x']) < GAME_SPRITES['pipe'][0].get_width():
            GAME_SOUNDS['hit'].play()
            return True
    #
    for pipe in lowerPipes:
        if (player_y + GAME_SPRITES['player'].get_height() > pipe['y']) and abs(player_x - pipe['x']) < GAME_SPRITES['pipe'][0].get_width():
            GAME_SOUNDS['hit'].play()
            return True
    return False


def getRandomPipe():
    """
    Generate positions of two pipes(one bottom straight and one top rotated) for blitting on the screen
    """
    offset = SCREENHEIGHT / 3
    y2 = offset + random.randrange(0, int(SCREENHEIGHT - GAME_SPRITES['base'].get_height() - 1.2 * offset))
    print(y2)
    pipe_x = SCREENWIDTH
    y1 = SCREENHEIGHT - y2 - 70
    pipe = [
        {'x': pipe_x, 'y': -y1},  # upper pipe
        {'x': pipe_x, 'y': y2}  # lower pipe
    ]
    return pipe


if __name__ == '__main__':
    pygame.init()
    FPS_CLOCK = pygame.time.Clock()
    pygame.display.set_caption('Flappy Bird by Jony')
    GAME_SPRITES['numbers'] = (
        pygame.image.load('Gallery/sprites/0.png').convert_alpha(),
        pygame.image.load('Gallery/sprites/1.png').convert_alpha(),
        pygame.image.load('Gallery/sprites/3.png').convert_alpha(),
        pygame.image.load('Gallery/sprites/4.png').convert_alpha(),
        pygame.image.load('Gallery/sprites/5.png').convert_alpha(),
        pygame.image.load('Gallery/sprites/6.png').convert_alpha(),
        pygame.image.load('Gallery/sprites/7.png').convert_alpha(),
        pygame.image.load('Gallery/sprites/8.png').convert_alpha(),
        pygame.image.load('Gallery/sprites/9.png').convert_alpha()
    )
    GAME_SPRITES['message'] = pygame.transform.scale((pygame.image.load('Gallery/sprites/home.png')), (1000, 620))
    GAME_SPRITES['base'] = pygame.image.load('Gallery/sprites/ground.png').convert_alpha()
    GAME_SPRITES['pipe'] = (pygame.transform.rotate(pygame.image.load(PIPE).convert_alpha(), 180),
                            pygame.image.load(PIPE).convert_alpha()
                            )
    GAME_SPRITES['background'] = pygame.image.load(BACKGROUND).convert()
    GAME_SPRITES['player'] = pygame.image.load(PLAYER).convert_alpha()

    # Game sounds
    GAME_SOUNDS['die'] = pygame.mixer.Sound('Gallery/audio/die.wav')
    GAME_SOUNDS['hit'] = pygame.mixer.Sound('Gallery/audio/hit.wav')
    GAME_SOUNDS['point'] = pygame.mixer.Sound('Gallery/audio/point.wav')
    GAME_SOUNDS['swoosh'] = pygame.mixer.Sound('Gallery/audio/swooshing.wav')
    GAME_SOUNDS['wing'] = pygame.mixer.Sound('Gallery/audio/wing.wav')

    while True:
        welcomeScreen()
        mainGame()
