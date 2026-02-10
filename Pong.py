import pygame as pg
import random, json
from Enums import *

# Base class for managing the game
class PongGame:
    roundsAmount: int           # total # of rounds, best of X
    winThreshold: int           # how many rounds needed to win
    p1Rounds: int               # how many rounds player 1 has won
    p2Rounds: int               # how mant rounds player 2 has won
    lastRoundWinner: int        # who the winner of the last round is, 1 for player 1, 2 for player 2, 0 for none (the first round)

    postRoundFunction: callable # the method to call when a round is won (for things like card selection)
    postMatchFunction: callable # the method to call when someone wins (for exiting the match)

    def __init__(self, postRoundLogic: callable = None, postMatchLogic: callable = None, bestOfRounds = 5):
        '''The Object that handles the game state. In the constructor, the functions to call when a round 
        is won or the match is won can be specified, but by default they will not do anything.'''
        self.roundsAmount = bestOfRounds
        self.winThreshold = bestOfRounds / 2
        self.p1Rounds = 0
        self.p2Rounds = 0
        lastRoundWinner = 0

        self.postRoundFunction = postRoundLogic
        self.postMatchFunction = postMatchLogic

    def p1WinRound(self):
        '''The function to be called when player 1 wins a round.'''
        self.p1Rounds += 1
        lastRoundWinner = 1

        # If P1 has won enough rounds to win the match, call the match win function but not the round win function.
        if self.p1Rounds == self.winThreshold:
            self.postMatchFunction
            return
        self.postRoundFunction
    def p2WinRound(self):
        '''The function to be called when player 2 wins a round.'''
        self.p2Rounds += 1
        lastRoundWinner = 2

        # If P2 has won enough rounds to win the match, call the match win function but not the round win function.
        if self.p2Rounds == self.winThreshold:
            self.postMatchFunction
            return
        self.postRoundFunction

    def getRoundNumber(self):
        return self.p1Rounds + self.p2Rounds + 1

class Card:
    name: str
    type: CardTypes

    def __init__(self, name = "", cardType = CardTypes.Typeless):
        self.name = name
        self.type = cardType

class Deck:
    name: str
    drawPile: list[Card]
    discardPile: list[Card]
    deckSize: int

    def __init__(self, name = ""):
        self.name = name
        self.drawPile = []
        self.discardPile = []
        self.deckSize = 0
    
    def add(self, card: Card):
        self.drawPile.append(card)
        self.deckSize += 1
    def add(self, cards: list[Card]):
        self.drawPile.extend(cards)
        self.deckSize += len(cards)
    
    def draw(self, shuffleIfEmpty = True) -> Card:
        if len(self.drawPile) == 0:
            if shuffleIfEmpty: self.shuffle()
            else: return None
        card = self.drawPile.pop()
        self.discardPile.append(card)
        return card

    def shuffle(self):
        for c in self.discardPile:
            self.drawPile.append(c)
            self.discardPile.remove(c)
        random.shuffle(self.drawPile)

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

# --- Functions ---
def loadCardFile(pathname: str) -> Card:
    card: Card = None
    try:
        with open(pathname, 'r') as file:
            card = json.load(file)
    except FileNotFoundError:
        print("Error: could not find file at {}".format(pathname))
    return card