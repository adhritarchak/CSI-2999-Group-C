
import json
import pygame as pg
import random
from Enums import *
from ball import Ball
import ball

#Call cardeffect.json file
class Card:
    '''The class containing card data.'''
    name: str
    type: CardTypes     # Specifies card type. I dunno if we need it yet, but it's probably not bad to have.
    effect_fn: callable
    effects: list[str]  # A list of effects to activate when the card is used, activated by getattr(). 
    is_Passive: bool     # Whether the card's effect is passive (always on) or active (activated by player)

    def __init__(self, name = "Card", effect_fn = None, cardType = CardTypes.Typeless, is_Passive=False, owner = None):
        self.name = name
        self.type = cardType
        self.effect_fn = effect_fn
        self.effects = []
        self.is_Passive = is_Passive
        self.owner = owner

    def activate(self, activator = None, **kwargs):
        '''The function to call when the card is used, which activates all of its effects. The caller parameter 
        is the object that will call the effects.'''
        if self.effect_fn:
            kwargs['activator'] = activator
            self.effect_fn(**kwargs)

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
        


def arc_strike_effect(ball, activator=None, **kwargs):
    if activator == 1:  # paddle1 activated it
        print("Player 1 used Arc Strike!")
        vel = ball.get_velocity()
        if vel[X] > 0:  # ball moving right, paddle1 last hit it
            ball.spin = 0.15  # curve right
        else:  # ball moving left, paddle2 last hit it
            ball.spin = -0.15  # curve left
    elif activator == 2:  # paddle2 activated it
        print("Player 2 used Arc Strike!")
        vel = ball.get_velocity()
        if vel[X] < 0:  # ball moving left, paddle2 last hit it
            ball.spin = -0.15  # curve left
        else:  # ball moving right, paddle1 last hit it
            ball.spin = 0.15  # curve right

def bigger_is_better_effect(paddle1, paddle2, activator=None, **kwargs):
    print(f"Player {activator} used Bigger is Better!")
    if activator == 1:
        paddle1.hitbox.width = int(paddle1.hitbox.width * 1.5)
        paddle1.hitbox.height = int(paddle1.hitbox.height * 1.5)
    else:
        paddle2.hitbox.width = int(paddle2.hitbox.width * 1.5)
        paddle2.hitbox.height = int(paddle2.hitbox.height * 1.5)

def bring_it_back_effect(ball, activator=None, **kwargs):
    print(f"Player {activator} used Bring it Back!")
    vel = ball.get_velocity()
    ball.set_velocity(-vel[0], vel[1], vel[2])

def shadow_clone_effect(ball, shadow_balls, activator=None, **kwargs):
    print(f"Player {activator} used Shadow Clone!")
    vel = ball.get_velocity()
    pos = ball.get_position()
    bounds = ball.get_bounds()
    
    shadow = Ball(
        x=pos[0], y=pos[1],
        height=ball.get_height(),
        vel_z=vel[2],
        speed_x=vel[0],
        speed_y=vel[1] + (3 if activator == 1 else -3),  # slight drift based on activator
        radius=ball.radius,
        spin=ball.spin,
        chosen_card=None,
        max_speed=ball.max_speed
    )
    shadow.set_bounds(top=bounds[0], bottom=bounds[1], left=bounds[2], right=bounds[3])
    shadow.is_shadow = True
    shadow_balls.append(shadow)

def low_impact_effect(ball, activator=None, **kwargs):
    print(f"Player {activator} used Low Impact!")
    vel = ball.get_velocity()
    if abs(vel[0]) >= ball.max_speed * 0.7:
        ball.set_velocity(vel[0] * 2.0, vel[1], vel[2])

def high_impact_effect(paddle1, paddle2, activator=None, **kwargs):
    print(f"Player {activator} used High Impact!")
    if activator == 1:
        paddle1.smashPower = min(paddle1.smashPower * 1.5, 1.0)
    else:
        paddle2.smashPower = min(paddle2.smashPower * 1.5, 1.0)

def shrink_effect(ball, activator=None, **kwargs):
    print(f"Player {activator} used Shrink!")
    ball.radius = max(4, ball.radius - 3)

def rally_effect(ball, activator=None, **kwargs):
    print(f"Player {activator} used Rally!")
    ball.rally_active = True
    ball.rally_timer = 10000  # 10 seconds in milliseconds
    ball.rally_activator = activator
    ball.rally_slow_factor = 0.6  # Slow to 60% of speed
    ball.rally_speed_threshold = 7.0  

def gravitational_pull_effect(ball, paddle1, paddle2, activator=None, **kwargs):
    print(f"Player {activator} used Gravitational Pull!")
    vel = ball.get_velocity()
    pos = ball.get_position()
    
    if activator == 1:  # Paddle1 activated - pull ball toward left
        if vel[0] > 0 and pos[0] > paddle1.hitbox.right:
            ball.set_velocity(vel[0] * 0.5, vel[1], vel[2])
            ball.spin = -0.3
    else:  # Paddle2 activated - pull ball toward right
        if vel[0] < 0 and pos[0] < paddle2.hitbox.left:
            ball.set_velocity(vel[0] * 0.5, vel[1], vel[2])
            ball.spin = 0.3

# Nerf effects (target opponent)
def smaller_paddle_effect(paddle1, paddle2, activator=None, **kwargs):
    print(f"Player {activator} used Smaller Paddle on opponent!")
    if activator == 1:
        paddle2.hitbox.width = max(20, paddle2.hitbox.width // 2)
        paddle2.hitbox.height = max(20, paddle2.hitbox.height // 2)
    else:
        paddle1.hitbox.width = max(20, paddle1.hitbox.width // 2)
        paddle1.hitbox.height = max(20, paddle1.hitbox.height // 2)

def extra_weight_effect(paddle1, paddle2, activator=None, **kwargs):
    print(f"Player {activator} used Extra Weight on opponent!")
    target = paddle2 if activator == 1 else paddle1
    target.speed_multiplier = 0.5
    target.debuff_timer = 10000

def anti_gravity_effect(ball, activator=None, **kwargs):
    print(f"Player {activator} used AntiGravity!")
    ball.gravity = -abs(ball.gravity)
    ball.served = False

def no_strength_effect(paddle1, paddle2, activator=None, **kwargs):
    print(f"Player {activator} used No Strength on opponent!")
    target = paddle2 if activator == 1 else paddle1
    target.smash_hold_multiplier = 1.5
    target.smash_power_debuff = 0.05
    target.debuff_timer = 5000

def disruption_effect(paddle1, paddle2, activator=None, **kwargs):
    print(f"Player {activator} used Disruption on opponent!")
    target = paddle2 if activator == 1 else paddle1
    target.keys_swapped = True
    target.debuff_timer = 10000

def delay_effect(paddle1, paddle2, activator=None, **kwargs):
    print(f"Player {activator} used Delay on opponent!")
    target = paddle2 if activator == 1 else paddle1
    target.swing_time_multiplier = 2.0
    target.debuff_timer = 10000

def weakened_effect(paddle1, paddle2, activator=None, **kwargs):
    print(f"Player {activator} used Weakened on opponent!")
    target = paddle2 if activator == 1 else paddle1
    target.pushback_multiplier = 3.0
    target.debuff_timer = 10000

def exhaustion_effect(paddle1, paddle2, activator=None, **kwargs):
    print(f"Player {activator} used Exhaustion on opponent!")
    target = paddle2 if activator == 1 else paddle1
    target.hit_strength_multiplier = 0.5
    target.debuff_timer = 10000


chosen_card = None

cards = [
          Card("Arc Strike", arc_strike_effect), #cards[0]
          Card("Bigger is better", bigger_is_better_effect), #cards[1]
          Card("Bring it back", bring_it_back_effect), #cards[2]
          Card("Shadow Clone", shadow_clone_effect), #cards[3]
          Card("Low impact", low_impact_effect, is_Passive=True), #cards[4]
          Card("High impact", high_impact_effect, is_Passive=True), #cards[5]
          Card("Shrink", shrink_effect), #cards[6]
          Card("Rally", rally_effect,  is_Passive=True),
          Card("Gravitational Pull",gravitational_pull_effect),
          Card("Smaller Paddle", smaller_paddle_effect),
          Card("Extra Weight", extra_weight_effect),
          Card("AntiGravity", anti_gravity_effect),
          Card("No Strength", no_strength_effect),
          Card("Disruption", disruption_effect),
          Card("Delay", delay_effect),
          Card("Weakened", weakened_effect),
          Card("Exhaustion", exhaustion_effect),
]
card_count = 0