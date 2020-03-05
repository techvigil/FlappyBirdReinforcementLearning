from itertools import cycle
import random
import sys

import datetime
from IPython import display
import numpy as np

import gym
from gym import error, spaces, utils

import pandas as pd
import itertools
import sys
import os
import string
import matplotlib.pyplot as plt
plt.style.use('seaborn-whitegrid')

from matplotlib.cbook import MatplotlibDeprecationWarning
import matplotlib.colors as mcolors
import matplotlib.patches as patches
import matplotlib as mpl
from matplotlib.pylab import rcParams
rcParams['figure.figsize'] = 12, 4

from pylab import rc
import json
import random
#from itertools import izip
import seaborn as sns
sns.reset_orig()

import pygame
from pygame.locals import *

class FlappyBirdEnviornment(object):    
    
    def __init__(self, agent, play_sounds = False):  
        self.agent = agent
        
        self.FPS = 60
        self.SCREENWIDTH  = 288
        self.SCREENHEIGHT = 512
        self.play_sounds = play_sounds
                
        self.action_space = spaces.Discrete(2)
                
        #self.low = np.array([self.min_position, self.min_posiition])
        #self.high = np.array([self.SCREENWIDTH, self.SCREENHEIGHT])       
        #self.min_position = 0
        
        #self.observation_space = spaces.Box(self.low, self.high)     
        
        # amount by which base can maximum shift to left
        self.PIPEGAPSIZE  = 100 # gap between upper and lower part of pipe
        self.BASEY        = self.SCREENHEIGHT * 0.79
        # image, sound and hitmask  dicts
        self.IMAGES, self.SOUNDS, self.HITMASKS = {}, {}, {}

        # list of all possible players (tuple of 3 positions of flap)
        self.PLAYERS_LIST = (
            # red bird
            (
                'assets/sprites/redbird-upflap.png',
                'assets/sprites/redbird-midflap.png',
                'assets/sprites/redbird-downflap.png',
            ),
            # blue bird
            (
                # amount by which base can maximum shift to left
                'assets/sprites/bluebird-upflap.png',
                'assets/sprites/bluebird-midflap.png',
                'assets/sprites/bluebird-downflap.png',
            ),
            # yellow bird
            (
                'assets/sprites/yellowbird-upflap.png',
                'assets/sprites/yellowbird-midflap.png',
                'assets/sprites/yellowbird-downflap.png',
            ),
        )

        # list of backgrounds
        self.BACKGROUNDS_LIST = (
            'assets/sprites/background-day.png',
            'assets/sprites/background-night.png',
        )

        # list of pipes
        self.PIPES_LIST = (
            'assets/sprites/pipe-green.png',
            'assets/sprites/pipe-red.png',
        )

        self.episode = 0
        self.history = pd.DataFrame(columns=["Episode", "Score"])
        self.start = datetime.datetime.now()
        self.data  = []
        
    #end def __int__
    
    def seed(self, seed=None):
        self.np_random, seed = seeding.np_random(seed)
        return [seed]
    
    def sample(self):
        return random.randomint(0,1)
        return random.uniform(low=self.low, high=self.high + 
                                            (0 if self.dtype.kind == 'f' else 1), size=self.low.shape).astype(self.dtype)

    def save_stats(self, episode, reward, score):
        
        algorithm = "tabular_q_learning"
        duration = datetime.datetime.now() - self.start 
        
        if (score >= 50):
            print("Duration: {} Episode {} Score: {}".format(duration, 
                                                                episode, 
                                                                score))
        
        self.data.append(json.dumps({ "algorithm": algorithm, 
                    "duration":  "{}".format(duration), 
                    "episode":   episode, 
                    "reward":    reward, 
                    "score":     score}))
        
        if (len(self.data) == 10):
            file_name = 'data/stats_flappy_bird_{}.json'.format(algorithm)
            
            # delete the old file before saving data for this session
            if episode == 1 and os.path.exists(file_name): os.remove(file_name)
                
            # open the file in append mode to add more json data
            file = open(file_name, 'a+')  
            for item in self.data:
                file.write(item)  
                file.write(",")
            #end for
            file.close()
            
            self.data = []
            
    def simulate(self, max_score):
        
        #pygame.event.set_grab(False)
        
        pygame.init()
        self.FPSCLOCK = pygame.time.Clock()
        self.SCREEN = pygame.display.set_mode((self.SCREENWIDTH, self.SCREENHEIGHT))
        pygame.display.set_caption('Flappy Bird')

        # numbers sprites for score display
        self.IMAGES['numbers'] = (
            pygame.image.load('assets/sprites/0.png').convert_alpha(),
            pygame.image.load('assets/sprites/1.png').convert_alpha(),
            pygame.image.load('assets/sprites/2.png').convert_alpha(),
            pygame.image.load('assets/sprites/3.png').convert_alpha(),
            pygame.image.load('assets/sprites/4.png').convert_alpha(),
            pygame.image.load('assets/sprites/5.png').convert_alpha(),
            pygame.image.load('assets/sprites/6.png').convert_alpha(),
            pygame.image.load('assets/sprites/7.png').convert_alpha(),
            pygame.image.load('assets/sprites/8.png').convert_alpha(),
            pygame.image.load('assets/sprites/9.png').convert_alpha()
        )

        # game over sprite
        self.IMAGES['gameover'] = pygame.image.load('assets/sprites/gameover.png').convert_alpha()
        # message sprite for welcome screen
        self.IMAGES['message'] = pygame.image.load('assets/sprites/message.png').convert_alpha()
        # base (ground) sprite
        self.IMAGES['base'] = pygame.image.load('assets/sprites/base.png').convert_alpha()

        # sounds
        if 'win' in sys.platform:
            soundExt = '.wav'
        else:
            soundExt = '.ogg'

        self.SOUNDS['die']    = pygame.mixer.Sound('assets/audio/die' + soundExt)
        self.SOUNDS['hit']    = pygame.mixer.Sound('assets/audio/hit' + soundExt)
        self.SOUNDS['point']  = pygame.mixer.Sound('assets/audio/point' + soundExt)
        self.SOUNDS['swoosh'] = pygame.mixer.Sound('assets/audio/swoosh' + soundExt)
        self.SOUNDS['wing']   = pygame.mixer.Sound('assets/audio/wing' + soundExt)

        while True:
            # select random background sprites
            randBg = random.randint(0, len(self.BACKGROUNDS_LIST) - 1)
            self.IMAGES['background'] = pygame.image.load(self.BACKGROUNDS_LIST[randBg]).convert()

            # select random player sprites
            randPlayer = random.randint(0, len(self.PLAYERS_LIST) - 1)
            self.IMAGES['player'] = (
                pygame.image.load(self.PLAYERS_LIST[randPlayer][0]).convert_alpha(),
                pygame.image.load(self.PLAYERS_LIST[randPlayer][1]).convert_alpha(),
                pygame.image.load(self.PLAYERS_LIST[randPlayer][2]).convert_alpha(),
            )

            # select random pipe sprites
            pipeindex = random.randint(0, len(self.PIPES_LIST) - 1)
            self.IMAGES['pipe'] = (
                pygame.transform.rotate(
                    pygame.image.load(self.PIPES_LIST[pipeindex]).convert_alpha(), 180),
                pygame.image.load(self.PIPES_LIST[pipeindex]).convert_alpha(),
            )

            # hismask for pipes
            self.HITMASKS['pipe'] = (
                self.getHitmask(self.IMAGES['pipe'][0]),
                self.getHitmask(self.IMAGES['pipe'][1]),
            )

            # hitmask for player
            self.HITMASKS['player'] = (
                self.getHitmask(self.IMAGES['player'][0]),
                self.getHitmask(self.IMAGES['player'][1]),
                self.getHitmask(self.IMAGES['player'][2]),
            )

            movementInfo = self.showWelcomeAnimation()
            crashInfo =  self.play(movementInfo, max_score)
            self.showGameOverScreen(crashInfo)


    def showWelcomeAnimation(self):
        """Shows welcome screen animation of flappy bird"""
        # index of player to blit on screen
        playerIndex = 0
        playerIndexGen = cycle([0, 1, 2, 1])
        # iterator used to change playerIndex after every 5th iteration
        loopIter = 0

        playerx = int(self.SCREENWIDTH * 0.2)
        playery = int((self.SCREENHEIGHT - self.IMAGES['player'][0].get_height()) / 2)

        messagex = int((self.SCREENWIDTH - self.IMAGES['message'].get_width()) / 2)
        messagey = int(self.SCREENHEIGHT * 0.12)

        basex = 0
        # amount by which base can maximum shift to left
        baseShift = self.IMAGES['base'].get_width() - self.IMAGES['background'].get_width()

        # player shm for up-down motion on welcome screen
        playerShmVals = {'val': 0, 'dir': 1}


        while True:
            ''' De-activated the press key functionality

            for event in pygame.event.get():
                if event.type == QUIT or (event.type == KEYDOWN and event.key == K_ESCAPE):
                    pygame.quit()
                    sys.exit()
                if event.type == KEYDOWN and (event.key == K_SPACE or event.key == K_UP):
                    # make first flap sound and return values for mainGame
                    SOUNDS['wing'].play()
                    return {
                        'playery': playery + playerShmVals['val'],
                        'basex': basex,
                        'playerIndexGen': playerIndexGen,
                    }
            '''
            if self.play_sounds == True: self.SOUNDS['wing'].play()

            return {
                'playery': playery + playerShmVals['val'],
                'basex': basex,
                'playerIndexGen': playerIndexGen,
            }

            # adjust playery, playerIndex, basex
            if (loopIter + 1) % 5 == 0:
                playerIndex = next(playerIndexGen)

            loopIter = (loopIter + 1) % 30
            basex = -((-basex + 4) % baseShift)
            playerShm(playerShmVals)

            # draw sprites
            self.SCREEN.blit(self.IMAGES['background'], (0,0))
            self.SCREEN.blit(self.IMAGES['player'][playerIndex],
                        (playerx, playery + playerShmVals['val']))
            self.SCREEN.blit(self.IMAGES['message'], (messagex, messagey))
            self.SCREEN.blit(self.IMAGES['base'], (basex, self.BASEY))

            pygame.display.update()
            self.FPSCLOCK.tick(FPS)


    def play(self,movementInfo, max_iterations):

        score = playerIndex = loopIter = 0
        playerIndexGen = movementInfo['playerIndexGen']

        playerx, playery = int(self.SCREENWIDTH * 0.2), movementInfo['playery']

        basex = movementInfo['basex']
        baseShift = self.IMAGES['base'].get_width() - self.IMAGES['background'].get_width()

        # get 2 new pipes to add to upperPipes lowerPipes list
        newPipe1 = self.getRandomPipe()
        newPipe2 = self.getRandomPipe()

        # list of upper pipes
        upperPipes = [
            {'x': self.SCREENWIDTH + 200, 'y': newPipe1[0]['y']},
            {'x': self.SCREENWIDTH + 200 + (self.SCREENWIDTH / 2), 'y': newPipe2[0]['y']},
        ]

        # list of lowerpipe
        lowerPipes = [
            {'x': self.SCREENWIDTH + 200, 'y': newPipe1[1]['y']},
            {'x': self.SCREENWIDTH + 200 + (self.SCREENWIDTH / 2), 'y': newPipe2[1]['y']},
        ]

        pipeVelX = -4

        # player velocity, max velocity, downward accleration, accleration on flap
        playerVelY    =  -9   # player's velocity along Y, default same as playerFlapped
        playerMaxVelY =  10   # max vel along Y, max descend speed
        playerMinVelY =  -8   # min vel along Y, max ascend speed
        playerAccY    =   1   # players downward accleration
        playerFlapAcc =  -9   # players speed on flapping
        playerFlapped = False # True when player flaps

        while True:
                       
            if max_iterations < self.episode:
                end = datetime.datetime.now()
    
                #print('duration: {} to run episodes: {}'.format(end- self.start, max_iterations))  
                    
                pygame.quit()
                sys.exit()
                
            if -playerx + lowerPipes[0]['x'] > -30:
                myPipe = lowerPipes[0]
            else:
                myPipe = lowerPipes[1]

            for event in pygame.event.get():
                if event.type == QUIT or (event.type == KEYDOWN and event.key == K_ESCAPE):
                    pygame.quit()
                    sys.exit()
                    
                if (event.type == KEYDOWN and (event.key == K_SPACE or event.key == K_UP)):
                    if playery > -2 * self.IMAGES['player'][0].get_height():
                        playerVelY = playerFlapAcc
                        playerFlapped = True
                        if self.play_sounds == True: self.SOUNDS['wing'].play()

            if self.agent.act(-playerx + myPipe['x'], - playery + myPipe['y'], playerVelY):
                if playery > -2 * self.IMAGES['player'][0].get_height():
                    playerVelY = playerFlapAcc
                    playerFlapped = True
                    if self.play_sounds == True: self.SOUNDS['wing'].play()

            # check for crash here
            crashTest = self.checkCrash({'x': playerx, 'y': playery, 'index': playerIndex},
                                   upperPipes, lowerPipes)
            if crashTest[0]:
                
                self.episode += 1
                
                # Update the q scores
                self.agent.learn()
                
                self.history.loc[len(self.history)] = [self.episode, score]
                print("episode: {} score: {}".format(self.episode, score))
                
                self.save_stats(self.episode, score, score)
                
                plt.scatter(self.history.Episode, self.history.Score)
                plt.xlabel('Iterations')
                plt.ylabel('Score')
                plt.title(self.agent.name)
                #plt.show()
                
                display.clear_output(wait=True)
                display.display(plt.show())

                return {
                    'y': playery,
                    'groundCrash': crashTest[1],
                    'basex': basex,
                    'upperPipes': upperPipes,
                    'lowerPipes': lowerPipes,
                    'score': score,
                    'playerVelY': playerVelY,
                }

            # check for score
            playerMidPos = playerx + self.IMAGES['player'][0].get_width() / 2
            for pipe in upperPipes:
                pipeMidPos = pipe['x'] + self.IMAGES['pipe'][0].get_width() / 2
                if pipeMidPos <= playerMidPos < pipeMidPos + 4:
                    score += 1
                    if self.play_sounds == True: self.SOUNDS['point'].play()

            # playerIndex basex change
            if (loopIter + 1) % 3 == 0:
                playerIndex = next(playerIndexGen)
            loopIter = (loopIter + 1) % 30
            basex = -((-basex + 100) % baseShift)

            # player's movement
            if playerVelY < playerMaxVelY and not playerFlapped:
                playerVelY += playerAccY
            if playerFlapped:
                playerFlapped = False
            playerHeight = self.IMAGES['player'][playerIndex].get_height()
            playery += min(playerVelY, self.BASEY - playery - playerHeight)


            # move pipes to left
            for uPipe, lPipe in zip(upperPipes, lowerPipes):
                uPipe['x'] += pipeVelX
                lPipe['x'] += pipeVelX


            # add new pipe when first pipe is about to touch left of screen
            if 0 < upperPipes[0]['x'] < 5:
                newPipe = self.getRandomPipe()
                upperPipes.append(newPipe[0])
                lowerPipes.append(newPipe[1])

            # remove first pipe if its out of the screen
            if upperPipes[0]['x'] < - self.IMAGES['pipe'][0].get_width():
                upperPipes.pop(0)
                lowerPipes.pop(0)

            # draw sprites
            self.SCREEN.blit(self.IMAGES['background'], (0,0))

            for uPipe, lPipe in zip(upperPipes, lowerPipes):
                self.SCREEN.blit(self.IMAGES['pipe'][0], (uPipe['x'], uPipe['y']))
                self.SCREEN.blit(self.IMAGES['pipe'][1], (lPipe['x'], lPipe['y']))



            self.SCREEN.blit(self.IMAGES['base'], (basex, self.BASEY))
            # print score so player overlaps the score
            self.showScore(score)
            self.SCREEN.blit(self.IMAGES['player'][playerIndex], (playerx, playery))

            pygame.display.update()
            self.FPSCLOCK.tick(self.FPS)


    def showGameOverScreen(self,crashInfo):
        """crashes the player down and shows gameover image"""
        score = crashInfo['score']
        playerx = self.SCREENWIDTH * 0.2
        playery = crashInfo['y']
        playerHeight = self.IMAGES['player'][0].get_height()
        playerVelY = crashInfo['playerVelY']
        playerAccY = 2

        basex = crashInfo['basex']

        upperPipes, lowerPipes = crashInfo['upperPipes'], crashInfo['lowerPipes']

        # play hit and die sounds
        if self.play_sounds == True: self.SOUNDS['hit'].play()
        if not crashInfo['groundCrash']:
            if self.play_sounds == True: self.SOUNDS['die'].play()

        while True:
            ''' De-activated press key functionality
            for event in pygame.event.get():
                if event.type == QUIT or (event.type == KEYDOWN and event.key == K_ESCAPE):
                    pygame.quit()
                    sys.exit()
                if event.type == KEYDOWN and (event.key == K_SPACE or event.key == K_UP):
                    if playery + playerHeight >= BASEY - 1:
                        return
            '''
            return ### Must remove to activate press-key functionality

            # player y shift
            if playery + playerHeight < self.BASEY - 1:
                playery += min(playerVelY, self.BASEY - playery - playerHeight)

            # player velocity change
            if playerVelY < 15:
                playerVelY += playerAccY

            # draw sprites
            self.SCREEN.blit(self.IMAGES['background'], (0,0))

            for uPipe, lPipe in zip(upperPipes, lowerPipes):
                SCREEN.blit(self.IMAGES['pipe'][0], (uPipe['x'], uPipe['y']))
                SCREEN.blit(self.IMAGES['pipe'][1], (lPipe['x'], lPipe['y']))

            self.SCREEN.blit(self.IMAGES['base'], (basex, BASEY))
            self.showScore(score)
            self.SCREEN.blit(self.IMAGES['player'][1], (playerx,playery))

            self.FPSCLOCK.tick(FPS)
            pygame.display.update()


    def playerShm(playerShm):
        """oscillates the value of playerShm['val'] between 8 and -8"""
        if abs(playerShm['val']) == 8:
            playerShm['dir'] *= -1

        if playerShm['dir'] == 1:
             playerShm['val'] += 1
        else:
            playerShm['val'] -= 1


    def getRandomPipe(self):
        """returns a randomly generated pipe"""
        # y of gap between upper and lower pipe
        gapY = random.randrange(0, int(self.BASEY * 0.6 - self.PIPEGAPSIZE))
        gapY += int(self.BASEY * 0.2)
        pipeHeight = self.IMAGES['pipe'][0].get_height()
        pipeX = self.SCREENWIDTH + 10

        return [
            {'x': pipeX, 'y': gapY - pipeHeight},  # upper pipe
            {'x': pipeX, 'y': gapY + self.PIPEGAPSIZE}, # lower pipe
        ]


    def showScore(self, score):
        """displays score in center of screen"""
        scoreDigits = [int(x) for x in list(str(score))]
        totalWidth = 0 # total width of all numbers to be printed

        for digit in scoreDigits:
            totalWidth += self.IMAGES['numbers'][digit].get_width()

        Xoffset = (self.SCREENWIDTH - totalWidth) / 2

        for digit in scoreDigits:
            self.SCREEN.blit(self.IMAGES['numbers'][digit], (Xoffset, self.SCREENHEIGHT * 0.1))
            Xoffset += self.IMAGES['numbers'][digit].get_width()


    def checkCrash(self, player, upperPipes, lowerPipes):
        """returns True if player collders with base or pipes."""
        pi = player['index']
        player['w'] = self.IMAGES['player'][0].get_width()
        player['h'] = self.IMAGES['player'][0].get_height()

        # if player crashes into ground
        if (player['y'] + player['h'] >= self.BASEY - 1 ) or (player['y'] + player['h'] <= 0):
            return [True, True]
        else:

            playerRect = pygame.Rect(player['x'], player['y'],
                          player['w'], player['h'])
            pipeW = self.IMAGES['pipe'][0].get_width()
            pipeH = self.IMAGES['pipe'][0].get_height()

            for uPipe, lPipe in zip(upperPipes, lowerPipes):
                # upper and lower pipe rects
                uPipeRect = pygame.Rect(uPipe['x'], uPipe['y'], pipeW, pipeH)
                lPipeRect = pygame.Rect(lPipe['x'], lPipe['y'], pipeW, pipeH)

                # player and upper/lower pipe hitmasks
                pHitMask = self.HITMASKS['player'][pi]
                uHitmask = self.HITMASKS['pipe'][0]
                lHitmask = self.HITMASKS['pipe'][1]

                # if bird collided with upipe or lpipe
                uCollide = self.pixelCollision(playerRect, uPipeRect, pHitMask, uHitmask)
                lCollide = self.pixelCollision(playerRect, lPipeRect, pHitMask, lHitmask)

                if uCollide or lCollide:
                    return [True, False]

        return [False, False]

    def pixelCollision(self, rect1, rect2, hitmask1, hitmask2):
        """Checks if two objects collide and not just their rects"""
        rect = rect1.clip(rect2)

        if rect.width == 0 or rect.height == 0:
            return False

        x1, y1 = rect.x - rect1.x, rect.y - rect1.y
        x2, y2 = rect.x - rect2.x, rect.y - rect2.y

        for x in range(rect.width):
            for y in range(rect.height):
                if hitmask1[x1+x][y1+y] and hitmask2[x2+x][y2+y]:
                    return True
        return False

    def getHitmask(self, image):
        """returns a hitmask using an image's alpha."""
        mask = []
        for x in range(image.get_width()):
            mask.append([])
            for y in range(image.get_height()):
                mask[x].append(bool(image.get_at((x,y))[3]))
        return mask