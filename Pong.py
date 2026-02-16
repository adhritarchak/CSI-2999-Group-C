import pygame as pg
from Enums import *
from ball import *
from cards import *

# Class to work the paddles
class PongPaddle:
    pass

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