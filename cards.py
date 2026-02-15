
import json
import pygame as pg
import random
from Enums import *

class Card:
    '''The class containing card data.'''
    name: str
    type: CardTypes     # Specifies card type. I dunno if we need it yet, but it's probably not bad to have.
    effects: list[str]  # A list of effects to activate when the card is used, activated by getattr(). 

    def __init__(self, name = "Card", cardType = CardTypes.Typeless):
        self.name = name
        self.type = cardType
        self.effects = []

    def activate(self, caller: object):
        '''The function to call when the card is used, which activates all of its effects. The caller parameter 
        is the object that will call the effects.'''
        for effect in self.effects:
            getattr(caller, effect)()

class Deck:
    '''Stack for cards, has both a draw and discard pile for the cards.'''
    name: str
    drawPile: list[Card]        # Undrawn cards go here, and it's refilled on shuffle
    discardPile: list[Card]     # Where cards that have been drawn go
    deckSize: int               # Stores the total size of both decks

    def __init__(self, name = "Deck"):
        self.name = name
        self.drawPile = []
        self.discardPile = []
        self.deckSize = 0
    
    def add(self, card: Card):
        '''Can add cards one by one or all at once in a list. Note that cards are placed on top of the deck.'''
        self.drawPile.append(card)
        self.deckSize += 1
    def add(self, cards: list[Card]):
        '''Adds a list of cards. Note that cards are placed in order of the list on the top of the deck.'''
        for c in cards:
            self.drawPile.append(c)
        self.deckSize += len(cards)
    
    def draw(self, shuffleIfEmpty = True) -> Card:
        '''Removes a card from the draw pile, puts it in the discard pile, and returns the drawn card. The
        shuffleIfEmpty argument specifies if the deck should be shuffled if the draw pile is empty. If false,
        the function returns None if the draw pile is empty.'''
        if len(self.drawPile) == 0:
            if shuffleIfEmpty: self.shuffle()
            else: return None
        card = self.drawPile.pop()
        self.discardPile.append(card)
        return card
    def drawNumber(self, num: int, shuffleIfEmpty = True) -> list[Card]:
        '''Draws a number of cards from the deck, and returns them in a list. If there are not enough cards 
        in the draw pile, it will shuffle if shuffleIfEmpty is True, otherwise it will return as many cards as possible.'''
        drawnCards = []
        for i in range(num):
            card = self.draw(shuffleIfEmpty)
            if card is None: break
            drawnCards.append(card)
        return drawnCards

    def shuffle(self):
        '''Shuffles the deck after putting all cards from the discard pile into the draw pile. To shuffle without
        reloading the draw pile, use shuffleDrawPile().'''
        for c in self.discardPile:
            self.drawPile.append(c)
            self.discardPile.remove(c)
        random.shuffle(self.drawPile)
    def shuffleDrawPile(self):
        '''Shuffles the remaining cards in the draw pile without reloading it.'''
        random.shuffle(self.drawPile)

# --- Functions ---
def loadCardFile(pathname: str) -> Card:
    card: Card = None
    try:
        with open(pathname, 'r') as file:
            card = json.load(file)
    except FileNotFoundError:
        print("Error: could not find file at {}".format(pathname))
    except json.JSONDecodeError:
        print("Error: problem decoding json file at {}".format(pathname))
    return card
def loadDeck(pathname: str) -> Deck:
    deck: Deck = None
    try:
        with open(pathname, 'r') as file:
            deck = json.load(file)
    except FileNotFoundError:
        print("Error: could not find file at {}".format(pathname))
    except json.JSONDecodeError:
        print("Error: problem decoding json file at {}".format(pathname))
    return deck
        
def arc_strike_effect():
        print("Arc Strike activated!")
        #if player.has_card("arc_strike"):
            #ball.speed_x *= 1.5
            #ball.speed_y *= 1.5
            #player.has_card("arc_strike") = False
        # Implement the effect of Arc Strike here


def bigger_is_better_effect():
        print("Bigger is better activated!")
        #if player.has_card("bigger_is_better"):
            #ball.radius *= 1.5
            #player.has_card("bigger_is_better") = False
        # Implement the effect of Bigger is better here

def bring_it_back_effect():
        print("Bring it back activated!")
        #if player.has_card("bring_it_back"):
            #ball.x, ball.y = player.initial_position()
            #player.has_card("bring_it_back") = False
        # Implement the effect of Bring it back here

def shadow_clone_effect():
        print("Shadow Clone activated!")
        # Implement the effect of Shadow Clone here

def low_impact_effect():
        print("Low impact activated!")
        # Implement the effect of Low impact here

def high_impact_effect():
        print("High impact activated!")
        # Implement the effect of High impact here
def shrink_effect():
        print("Shrink activated!")
        # Implement the effect of Shrink here

# cards = [
#         Card("Arc Strike", arc_strike_effect), #cards[0]
#         Card("Bigger is better", bigger_is_better_effect), #cards[1]
#         Card("Bring it back", bring_it_back_effect), #cards[2]
#         Card("Shadow Clone", shadow_clone_effect), #cards[3]
#         Card("Low impact", low_impact_effect), #cards[4]
#         Card("High impact", high_impact_effect), #cards[5]
#         Card("Shrink", shrink_effect) #cards[6]
#         ]

# card_count = 0


# def draw_random_card(num = 3):
#    selected_cards = random.sample(cards, num)
#    global card_count
#    print("These are your available cards!")
#    for card in selected_cards:
#         print(f"Drawn card: {card.name}")
#    while card_count == 0:
#         card_name_choice = input("Which card would you like: ")
#         for card in selected_cards:
#             if card.name.lower() == card_name_choice.lower():
#                 print(f"Selected card: {card.name}")
#                 card_count += 1
#                 return card
#                 break
#         else:
#             print("That card is not in the deck, please enter another one: ")
    
# hand = draw_random_card()
