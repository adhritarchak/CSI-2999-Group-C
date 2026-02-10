import pygame as pg

# Base class for managing the game
class PongGame:
    roundsAmount: int
    winThreshold: int
    p1Rounds: int
    p2Rounds: int
    lastRoundWinner: int

    postRoundFunction: callable
    postMatchFunction: callable

    def __init__(self, postRoundLogic: callable = None, postMatchLogic: callable = None, bestOfRounds = 5):
        self.roundsAmount = bestOfRounds
        self.winThreshold = bestOfRounds / 2
        self.p1Rounds = 0
        self.p2Rounds = 0
        lastRoundWinner = 0

        self.postRoundFunction = postRoundLogic
        self.postMatchFunction = postMatchLogic

    def p1WinRound(self):
        self.p1Rounds += 1
        lastRoundWinner = 1
        if self.p1Rounds == self.winThreshold:
            self.postMatchFunction
            return
        self.postRoundFunction
    def p2WinRound(self):
        self.p2Rounds += 1
        lastRoundWinner = 2
        if self.p2Rounds == self.winThreshold:
            self.postMatchFunction
            return
        self.postRoundFunction

# Class to handle the players in the game
class PongPlayer:
    pass

# Class to manage the pong board
class PongTable:
    pass

# Class to work the paddles
class PongPaddle:
    pass

# Class for the ball
class PongBall:
    pass