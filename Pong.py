import pygame as pg
from Enums import *
from ball import *
from cards import *
from colorsys import *

# Class to work the paddles
class PongPaddle:
    paddleSurface: pg.Surface
    hitbox: pg.Rect
    position: tuple[float, float]
    bounds: tuple[float, float, float, float]
    speed: float
    currentSpeed: float
    velocity: tuple[float, float]

    color: tuple[int, int, int]
    font = None
    viewDebug: bool = False
    sprites: list[pg.Surface] = None

    can_swing: bool = True
    swinging: bool = False
    can_hit_ball: bool = False
    has_hit_ball: bool = False
    swingTimer: int = 0
    swingBackTime: int = 200
    swingForwardTime: int = 800
    swingAngle: float = 0

    smash_charging: bool = False
    smash_swinging: bool = False
    smashTimer: int = 0
    smashHoldTime: int = 3000
    cooldownTime: int = 2000
    cooldownTimer: int = 0
    smashPower: float = 0

    upKey: int = -1
    downKey: int = -1
    leftKey: int = -1
    rightKey: int = -1
    swingKey: int = -1
    smashKey: int = -1

    def __init__(self, width: int, height: int, color: tuple[int, int, int],
             initialPos: tuple[float, float] = (0, 0), speed: float = 1, images: list[pg.Surface] = None):
        self.sprites = images
        self.paddleSurface = images[0]
        self.hitbox = pg.Rect(initialPos[0], initialPos[1], width, height)
        self.color = rgb_to_hsv(*color)
        # self.fillSurface(color)
        self.font = pg.font.Font(None, 24)
        self.position = initialPos
        self.speed = speed
        self.currentSpeed = speed
        self.velocity = (0, 0)
    def brighten(self, amount: float) -> tuple[int, int, int]:
        '''Brightens the paddle's color by the specified amount (between 0 and 255) and returns the new color.'''
        h, s, v = self.color
        s = min(1, s - amount / 255)
        v = min(255, v + amount)
        # print(f"Brightening color from {self.color} to {(h, s, v)}")
        new_color = hsv_to_rgb(h, s, v)
        new_color = (int(new_color[0]), int(new_color[1]), int(new_color[2]))
        # print(f"New RGB color: {new_color}")
        return (new_color)

    def get_hitbox(self):
        return self.hitbox
    def set_hitbox_pos(self, x_offset: float = 0, y_offset: float = 0):
        x = self.position[X] + x_offset
        y = self.position[Y] + y_offset
        self.hitbox = pg.Rect(x, y, self.hitbox.width, self.hitbox.height)

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
    def setSwingConfig(self, swingBackTime: int, swingForwardTime: int, smashHoldTime: int, cooldownTime: int):
        self.swingBackTime = swingBackTime
        self.swingForwardTime = swingForwardTime
        self.smashHoldTime = smashHoldTime
        self.cooldownTime = cooldownTime
    def viewDebugInfo(self, view: bool):
        self.viewDebug = view

    def process_keys(self, keyList, dt: int):
        move_x = 0
        move_y = 0
        if self.upKey >= 0:
            if keyList[self.upKey] and self.position[Y] > self.bounds[TOP]:
                move_y -= 1
        if self.downKey >= 0:
            if keyList[self.downKey] and self.position[Y] + self.hitbox.height < self.bounds[BOTTOM]:
                move_y += 1
        if self.leftKey >= 0:
            if keyList[self.leftKey] and self.position[X] > self.bounds[LEFT]:
                move_x -= 1
        if self.rightKey >= 0:
            if keyList[self.rightKey] and self.position[X] + self.hitbox.width < self.bounds[RIGHT]:
                move_x += 1
        if self.cooldownTimer > 0:
            self.cooldownTimer -= dt
        else:
            self.can_swing = True
            self.cooldownTimer = 0
        if self.swingKey >= 0 and keyList[self.swingKey] and self.can_swing:
            self.swinging = True
            self.can_swing = False
        if self.smashKey >= 0 and keyList[self.smashKey] and self.can_swing:
            self.smash_charging = True
            self.can_swing = False
        if self.smashKey >= 0 and self.smash_charging and not keyList[self.smashKey]:
            self.smash_charging = False


        self.velocity = (
            move_x * self.currentSpeed,
            move_y * self.currentSpeed
        )
        new_x = self.position[X] + self.velocity[X] * dt / 1000
        new_y = self.position[Y] + self.velocity[Y] * dt / 1000

        new_x = max(self.bounds[LEFT], min(new_x, self.bounds[RIGHT] - self.hitbox.width))
        new_y = max(self.bounds[TOP], min(new_y, self.bounds[BOTTOM] - self.hitbox.height))

        self.position = (new_x, new_y)
        #self.position = (
            #self.position[X] + self.velocity[X] * dt / 1000,
            #self.position[Y] + self.velocity[Y] * dt / 1000
        #)
        self.set_hitbox_pos(self.paddleSurface.get_width() - self.hitbox.width, 0)
        #self.set_hitbox_pos(30)
    def process_swing(self, dt: int):
        if not self.swinging:
            return
        self.swingTimer += dt
        if self.swingTimer <= self.swingBackTime // 2:
            self.paddleSurface = self.sprites[1] # Advance to frame 2
        elif self.swingTimer > self.swingBackTime // 2 and self.swingTimer <= self.swingBackTime:
            self.paddleSurface = self.sprites[2] # Advance to frame 3
        else:
            self.swing_forward(self.swingTimer - self.swingBackTime)
        
    def swing_forward(self, timer: int):
        if timer <= self.swingForwardTime / 4:
            self.can_hit_ball = not self.has_hit_ball
            self.paddleSurface = self.sprites[3] # Advance to frame 4
        elif timer > self.swingForwardTime / 4 and timer <= self.swingForwardTime / 2:
            self.paddleSurface = self.sprites[4] # Advance to frame 5
        elif timer > self.swingForwardTime / 2 and timer <= self.swingForwardTime * 3 / 4:
            self.can_hit_ball = False 
            self.paddleSurface = self.sprites[5] # Advance to frame 6 and deactivate the hitbox
        elif timer > self.swingForwardTime * 3 / 4 and timer <= self.swingForwardTime:
            self.paddleSurface = self.sprites[6] # Advance to frame 7
        elif timer > self.swingForwardTime:
            self.swinging = False
            self.smash_swinging = False
            self.cooldownTimer = self.cooldownTime
            self.swingTimer = 0
            self.smashTimer = 0
            self.smashPower = 0
            self.currentSpeed = self.speed
            self.has_hit_ball = False
            self.paddleSurface = self.sprites[0] # Reset to frame 1

    #def process_smash(self, dt: int):
        #if not self.smash_charging:
            #if self.smash_swinging:
                #self.smashTimer += dt
                #self.swing_forward(self.smashTimer)
                #return
            #elif self.smashTimer > 0:
                #self.smashPower = min(self.smashTimer / self.smashHoldTime, 1)
                #self.smashTimer = 0
                #self.smash_swinging = True
                #self.swing_forward(self.smashTimer)
                #return
            #else:
                #return
        #self.smashTimer += dt
    def process_smash(self, dt: int):
        if not self.smash_charging:
            if self.smash_swinging:
                self.smashTimer += dt
                self.swing_forward(self.smashTimer)
                return
            elif self.smashTimer > 0:
                if self.smashTimer >= self.smashHoldTime:
                    self.smashPower = min(self.smashTimer / self.smashHoldTime, 1)
                    self.smash_swinging = True
                    self.swing_forward(0)
                else:
                    self.currentSpeed = self.speed
                    self.can_swing = True
                    self.cooldownTimer = 0
                    self.paddleSurface = self.sprites[0]  
                self.smashTimer = 0
                return  
            else:
                return

        # Still charging
        self.smashTimer += dt
        charge_progress = self.smashTimer / self.smashHoldTime  

        if charge_progress < 1.0:
            sprite_index = int(charge_progress * 3) + 1  
            self.currentSpeed = self.speed * 0.5
            self.paddleSurface = self.sprites[sprite_index]
        else:
            self.currentSpeed = self.speed * 0.2
            self.paddleSurface = self.sprites[3]

    def draw(self, screen: pg.Surface):
        screen.blit(self.paddleSurface, self.position)
        if self.viewDebug:
            pg.draw.rect(screen, WHITE, self.hitbox, 2)
            text = self.font.render(f"smashTimer: {int(self.smashTimer)}ms", True, WHITE)
            screen.blit(text, (self.position[X], self.position[Y] + 30))
            text = self.font.render(f"swingTimer: {int(self.swingTimer)}ms", True, WHITE)
            screen.blit(text, (self.position[X], self.position[Y] + 50))
            text = self.font.render(f"cooldown: {self.cooldownTimer}", True, WHITE)
            screen.blit(text, (self.position[X], self.position[Y] + 70))

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