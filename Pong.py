import pygame as pg
from Enums import *
from ball import *
from cards import *

# Class to work the paddles
class PongPaddle:
    paddleSurface: pg.Surface
    position: tuple[float, float]
    bounds: tuple[float, float, float, float]
    speed: float
    currentSpeed: float
    velocity: tuple[float, float]

    swinging: bool = False
    can_hit_ball: bool = False
    swingTimer: int = 0
    swingBackTime: int = 200
    swingForwardTime: int = 400
    swingAngle: float = 0

    smash_active: bool = False
    smashTimer: int = 0
    smashHoldTime: int = 3000
    cooldownTime: int = 2000
    smashAngle: float = 0

    upKey: int = -1
    downKey: int = -1
    leftKey: int = -1
    rightKey: int = -1
    swingKey: int = -1
    smashKey: int = -1

    def __init__(self, width: int, height: int, color: tuple[int, int, int],
             initialPos: tuple[float, float] = (0, 0), speed: float = 1):
        self.paddleSurface = pg.Surface((width, height))
        self.paddleSurface.fill(color)
        pg.draw.rect(surface=self.paddleSurface, color=WHITE, rect=(0, 0, width, height), width=2)
        self.position = initialPos
        self.speed = speed
        self.velocity = (0, 0)

    def get_rect(self):
        return self.paddleSurface.get_rect()

    def setPosition(self, x: float, y: float):
        self.position = (x, y)

    def setBounds(self, topBound: float, botBound: float, leftBound: float, rightBound: float):
        self.bounds = (
            topBound,
            botBound,
            leftBound,
            rightBound
        )

    def setKeys(self, upKey: int = -1, downKey: int = -1, leftKey: int = -1, rightKey: int = -1, swingKey: int = -1, smashKey: int = -1):
        self.upKey = upKey
        self.downKey = downKey
        self.leftKey = leftKey
        self.rightKey = rightKey
        self.swingKey = swingKey
        self.smashKey = smashKey

    def process_keys(self, keyList, dt: int):
        move_x = 0
        move_y = 0
        if self.upKey >= 0:
            if keyList[self.upKey] and self.position[Y] > self.bounds[TOP]:
                move_y -= 1
        if self.downKey >= 0:
            if keyList[self.downKey] and self.position[Y] < self.bounds[BOTTOM]:
                move_y += 1
        if self.leftKey >= 0:
            if keyList[self.leftKey] and self.position[X] > self.bounds[LEFT]:
                move_x -= 1
        if self.rightKey >= 0:
            if keyList[self.rightKey] and self.position[X] < self.bounds[RIGHT]:
                move_x += 1
        if keyList[self.swingKey]: # regular
            self.swinging = True
        if keyList[self.smashKey] and not self.smash_active: #smash
            self.smash_active = True
        if self.smash_active and not keyList[self.smashKey]: #end smash
            self.smash_active = False
            self.smashTimer = 0
            
        # if smash_active and self.position[X] < ballConfig['init_x'] < self.position[X] + 20 and self.position[Y] < ballConfig['init_y'] < self.position[Y] + 80:
        #     ballConfig['init_vel_x'] = min(abs(ballConfig['init_vel_x']) + 5, ballConfig['Max_Speed'])
        #     Smash1_hit = True
        #     self.currentSpeed = self.speed * 0.2
        #     Smash1_hold_time = 0
        #     Smash1_hit_time = pygame.time.get_ticks()
        
        # if Smash1_hit:
        #     if pygame.time.get_ticks() - Smash1_hit_time >= 2000:  # 2 seconds recovery time
        #         self.currentSpeed = self.speed
        #         Smash1_hit = False

        self.velocity = (
            move_x * self.currentSpeed,
            move_y * self.currentSpeed
        )
        self.position = (
            self.position[X] + move_x,
            self.position[Y] + move_y
        )
    def process_swing(self, dt: int):
        if not self.swinging:
            return
        self.swingTimer += dt
        if self.swingTimer <= self.swingBackTime // 2:
            pass # Stay on frame 2
        elif self.swingTimer > self.swingBackTime // 2 and self.swingTimer <= self.swingBackTime:
            pass # Advance to frame 3
        elif self.swingTimer > self.swingBackTime and self.swingTimer <= self.swingForwardTime / 4:
            self.can_hit_ball = True # Advance to frame 4 and activate the hitbox
        elif self.swingTimer > self.swingForwardTime / 4 and self.swingTimer <= self.swingForwardTime / 2:
            pass # Advance to frame 5
        elif self.swingTimer > self.swingForwardTime / 2 and self.swingTimer <= self.swingForwardTime * 3 / 4:
            self.can_hit_ball = False # Advance to frame 6 and deactivate the hitbox
        elif self.swingTimer > self.swingForwardTime * 3 / 4 and self.swingTimer <= self.swingForwardTime:
            pass # Advance to frame 7
        elif self.swingTimer > self.swingForwardTime:
            self.swinging = False
            self.swingTimer = 0
                # Return to frame 1
    def process_smash(self, dt: int):
        if not self.smash_active:
            self.currentSpeed = self.speed
            return
        self.smashTimer += dt
        if self.smashTimer < self.smashHoldTime:
            self.currentSpeed = self.speed * 0.2

    def draw(self, screen: pg.Surface):
        screen.blit(self.paddleSurface, self.position)

# Class to handle the players in the game
class PongPlayer:
    paddle: PongPaddle
    deck: Deck

# Base class for managing the game
class PongGame:
    gameStage: GameStages       # The current stage of the game, used to determine what logic to run and what to draw
    player1: PongPlayer
    player2: PongPlayer
    ball: Ball

    roundsAmount: int           # total # of rounds, best of X
    winThreshold: int           # how many rounds needed to win
    p1Rounds: int               # how many rounds player 1 has won
    p2Rounds: int               # how many rounds player 2 has won
    lastRoundWinner: int        # who the winner of the last round is, 1 for player 1, 2 for player 2, 0 for none (the first round)

    postRoundFunction: callable # the method to call when a round is won (for things like card selection)
    postMatchFunction: callable # the method to call when someone wins (for exiting the match)

    screen: pg.Surface          # The Pygame screen to draw on

    def __init__(self, screen: pg.Surface, postRoundLogic: callable = None, postMatchLogic: callable = None, bestOfRounds = 5):
        '''The Object that handles the game state. In the constructor, the functions to call when a round 
        is won or the match is won can be specified, but by default they will not do anything.'''
        self.gameStage = GameStages.StartScreen
        self.screen = screen
        self.roundsAmount = bestOfRounds
        self.winThreshold = bestOfRounds / 2
        self.p1Rounds = 0
        self.p2Rounds = 0
        self.lastRoundWinner = 0

        self.postRoundFunction = postRoundLogic
        self.postMatchFunction = postMatchLogic

    def p1WinRound(self):
        '''The function to be called when player 1 wins a round.'''
        self.p1Rounds += 1
        self.lastRoundWinner = 1

        # If P1 has won enough rounds to win the match, call the match win function but not the round win function.
        if self.p1Rounds == self.winThreshold:
            self.postMatchFunction()
            return
        self.postRoundFunction()
    def p2WinRound(self):
        '''The function to be called when player 2 wins a round.'''
        self.p2Rounds += 1
        self.lastRoundWinner = 2

        # If P2 has won enough rounds to win the match, call the match win function but not the round win function.
        if self.p2Rounds == self.winThreshold:
            self.postMatchFunction()
            return
        self.postRoundFunction()

    def getRoundNumber(self):
        return self.p1Rounds + self.p2Rounds + 1

# Class to manage the pong board
class PongTable:
    pass