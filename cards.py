
import json
import pygame as pg
import random
from Enums import *
from ball import Ball

class Card:
    '''The class containing card data.'''
    name: str
    type: CardTypes     # Specifies card type. I dunno if we need it yet, but it's probably not bad to have.
    effects: list[str]  # A list of effects to activate when the card is used, activated by getattr(). 

    def __init__(self, name = "Card", cardType = CardTypes.Typeless):
        self.name = name
        self.type = cardType
        self.effects = []

    def activate(self, caller: object = None, data: dict = None):
        '''The function to call when the card is used, which activates all of its effects. The caller parameter 
        is the object that will call the effects.'''
        if caller is None: caller = self
        for effect in self.effects:
            getattr(caller, effect)(data[effect])  # Pass data to each effect function

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
def set_velocity(self, vx, vy, vz):
    Ball.set_velocity((vx, vy, vz))
        
def arc_strike_effect(ball):
        print("Arc Strike activated!")
        ball.impulse((4,0,6))


def bigger_is_better_effect(ball, game):
        print("Bigger is better activated!")
        game.paddle1.radius += 5
        game.paddle2.radius += 5
        

def bring_it_back_effect(ball):
        print("Bring it back activated!")
        vx, vy, vz = ball.get_velocity()
        ball.set_velocity(-vx, -vy, vz)

def shadow_clone_effect(ball):
        print("Shadow Clone activated!")
        # Implement the effect of Shadow Clone here

def low_impact_effect(ball):
        print("Low impact activated!")
        #Returning smash
    

def high_impact_effect(ball):
        print("High impact activated!")
        #if Smash1_active or Smash2_active:
            #pass #Ball smash speed goes up by 1.5

def shrink_effect(ball):
        import ball
        print("Shrink activated!")
        ball.radius = max(4, ball.radius - 4)
        ball.impulse((2,0,2))


chosen_card = None

cards = [
          Card("Arc Strike", arc_strike_effect), #cards[0]
          Card("Bigger is better", bigger_is_better_effect), #cards[1]
          Card("Bring it back", bring_it_back_effect), #cards[2]
          #Card("Shadow Clone", shadow_clone_effect), #cards[3]
          Card("Low impact", low_impact_effect), #cards[4]
          Card("High impact", high_impact_effect), #cards[5]
          Card("Shrink", shrink_effect) #cards[6]
]
card_count = 0


def draw_random_card(screen, font, num=3):
    selected_cards = random.sample(cards, num)

    card_width = 200
    card_height = 120
    spacing = 50
    transparency = 180

    screen_width = screen.get_width()
    screen_height = screen.get_height()

    start_x = (screen_width - ((card_width * num) + spacing * (num - 1))) // 2
    y_pos = screen_height // 2 - card_height // 2

    card_rects = []
    current_screen = screen.copy()

    running = True
    while running:
        #screen.fill((30, 30, 30))
        screen.blit(current_screen, (0, 0))

        overlay = pg.Surface((screen_width, screen_height), pg.SRCALPHA)
        overlay.fill((0, 0, 0, 180))  # Semi-transparent overlay
        screen.blit(overlay, (0, 0))

        # Draw cards
        for i, card in enumerate(selected_cards):
            rect = pg.Rect(start_x + i * (card_width + spacing), y_pos, card_width, card_height)
            card_rects.append(rect)
            card_surface = pg.Surface((card_width, card_height), pg.SRCALPHA)

            card_surface.fill((0,0,0,0))

            pg.draw.rect(card_surface, (200, 200, 200, transparency), card_surface.get_rect(), border_radius= 10)
            pg.draw.rect(card_surface, (0, 0, 0, transparency), card_surface.get_rect(), 3, border_radius=10)

            text_surface = font.render(card.name, True, (0, 0, 0))
            text_rect = text_surface.get_rect(center=card_surface.get_rect().center)
            card_surface.blit(text_surface, text_rect)
            screen.blit(card_surface, rect)

        pg.display.flip()

        for event in pg.event.get():
            if event.type == pg.QUIT:
                pg.quit()
                return None

            if event.type == pg.MOUSEBUTTONDOWN:
                mouse_pos = pg.mouse.get_pos()

                for i, rect in enumerate(card_rects):
                    if rect.collidepoint(mouse_pos):
                        return selected_cards[i]
