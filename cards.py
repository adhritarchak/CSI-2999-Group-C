
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
    owner: int          # 1 for player 1, 2 for player 2, None for unowned (e.g. in a deck or something)
    used_this_round: bool  # Whether the card has been used this round, to prevent multiple uses of the same card in one round
    cooldown_rounds: int  # Number of rounds before the card can be used again after being used

    def __init__(self, name = "Card", effect_fn = None, cardType = CardTypes.Typeless, is_Passive=False, owner = None, cooldown_rounds = 1):
        self.name = name
        self.type = cardType
        self.effect_fn = effect_fn
        self.effects = []
        self.is_Passive = is_Passive
        self.owner = owner
        self.used_this_round = False
        self.cooldown_rounds = cooldown_rounds
        self.rounds_left_on_cooldown = 0

    def activate(self, activator = None, **kwargs):
        '''The function to call when the card is used, which activates all of its effects. The caller parameter 
        is the object that will call the effects.'''
        if self.effect_fn:
            kwargs['activator'] = activator
            self.effect_fn(**kwargs)

    def can_use(self, current_round):
        #if card can be used 
        if self.is_Passive:
            return True  
        return self.rounds_left_on_cooldown <= 0
    
    def use_card(self):
        #Mark as cooldownn till next round
        if not self.is_Passive:
            self.rounds_left_on_cooldown = self.cooldown_rounds
    
    def update_cooldown(self):
        #Back to normal after cooldown
        if self.rounds_left_on_cooldown > 0:
            self.rounds_left_on_cooldown -= 1

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
        if vel[X] > 0:  
            ball.spin = 0.15  # curve right
        else: 
            ball.spin = -0.15  # curve left
    elif activator == 2:  # paddle2 activated it
        print("Player 2 used Arc Strike!")
        vel = ball.get_velocity()
        if vel[X] < 0:  
            ball.spin = -0.15  # curve left
        else:  
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
    
    if activator == 1:  
        if vel[0] > 0 and pos[0] > paddle1.hitbox.right:
            ball.set_velocity(vel[0] * 0.5, vel[1], vel[2])
            ball.spin = -0.3
    else:  
        if vel[0] < 0 and pos[0] < paddle2.hitbox.left:
            ball.set_velocity(vel[0] * 0.5, vel[1], vel[2])
            ball.spin = 0.3


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
    Card("Arc Strike", arc_strike_effect, cooldown_rounds=1),
    Card("Bigger is better", bigger_is_better_effect, cooldown_rounds=2),
    Card("Bring it back", bring_it_back_effect, cooldown_rounds=1),
    Card("Shadow Clone", shadow_clone_effect, cooldown_rounds=2),
    Card("Low impact", low_impact_effect, is_Passive=True),  
    Card("High impact", high_impact_effect, is_Passive=True),
    Card("Shrink", shrink_effect, cooldown_rounds=1),
    Card("Rally", rally_effect, is_Passive=True),
    Card("Gravitational Pull", gravitational_pull_effect, cooldown_rounds=2),
    Card("Smaller Paddle", smaller_paddle_effect, cooldown_rounds=2),
    Card("Extra Weight", extra_weight_effect, cooldown_rounds=2),
    Card("AntiGravity", anti_gravity_effect, cooldown_rounds=2),
    Card("No Strength", no_strength_effect, cooldown_rounds=2),
    Card("Disruption", disruption_effect, cooldown_rounds=2),
    Card("Delay", delay_effect, cooldown_rounds=2),
    Card("Weakened", weakened_effect, cooldown_rounds=2),
    Card("Exhaustion", exhaustion_effect, cooldown_rounds=2),
]
card_count = 0

class PlayerCardInventory:
    def __init__(self, max_slots=5, player_id=None):
        self.cards = []
        self.max_slots = max_slots
        self.player_id = player_id
        self.card_names = set()

    def add_card(self, card):
        if card.name in self.card_names:
            print(f"Player {self.player_id} already has {card.name} in inventory. Cannot add duplicate cards.")
            return False
        
        if len(self.cards) < self.max_slots:
            self.cards.append(card)
            self.card_names.add(card.name)
            card.owner = self.player_id
            return True
        return False
    
    def remove_card(self, index):
        if 0 <= index < len(self.cards):
            removed_card = self.cards.pop(index)
            self.card_names.discard(removed_card.name)  
            return removed_card
        return None
    
    def swap_card(self, index, new_card):
        if 0 <= index < len(self.cards):
            if new_card.name in self.card_names:
                print(f"Player {self.player_id} already has {new_card.name}! Cannot swap with duplicate.")
                return None
            old_card = self.cards[index]
            self.cards[index] = new_card
            self.card_names.discard(old_card.name)
            self.card_names.add(new_card.name)
            new_card.owner = self.player_id
            return old_card
        return None
    
    def get_card(self, index):
        if 0 <= index < len(self.cards):
            return self.cards[index]
        return None
    def has_card(self, card_name):
        return card_name in self.card_names
    
    def is_full(self):
        return len(self.cards) >= self.max_slots
    def use_card(self, index, current_round):
        card = self.get_card(index)
        if card and card.can_use(current_round):
            card.use_card()
            return True
        return False
    
    def update_all_cooldowns(self):
        for card in self.cards:
            card.update_cooldown()
    

def handle_inventory_selection(screen, font, player_id, player1_inventory, player2_inventory, new_card):
    inventory = player1_inventory if player_id == 1 else player2_inventory
    
    card_width = 300
    card_height = 60
    spacing = 15
    
    screen_width = screen.get_width()
    screen_height = screen.get_height()
    
    start_x = (screen_width - card_width) // 2
    total_height = len(inventory.cards) * (card_height + spacing)
    y_pos = screen_height // 2 - total_height // 2
    
    title_text = font.render(f"Inventory Full - Choose a card to replace", True, (255, 255, 255))
    title_rect = title_text.get_rect(center=(screen_width // 2, y_pos - 50))
    
    new_card_text = font.render(f"New Card: {new_card.name}", True, (255, 255, 0))
    new_card_rect = new_card_text.get_rect(center=(screen_width // 2, y_pos + total_height + 30))
    
    card_rects = []
    current_screen = screen.copy()
    running = True
    while running:
        screen.blit(current_screen, (0, 0))
        overlay = pg.Surface((screen_width, screen_height), pg.SRCALPHA)
        overlay.fill((0, 0, 0, 180))
        screen.blit(overlay, (0, 0))
        screen.blit(title_text, title_rect)
        screen.blit(new_card_text, new_card_rect)
        
        for i, card in enumerate(inventory.cards):
            rect = pg.Rect(start_x, y_pos + i * (card_height + spacing), card_width, card_height)
            card_rects.append(rect)
            card_surface = pg.Surface((card_width, card_height), pg.SRCALPHA)
            pg.draw.rect(card_surface, (200, 200, 200, 180), card_surface.get_rect(), border_radius=8)
            pg.draw.rect(card_surface, (0, 0, 0, 180), card_surface.get_rect(), 3, border_radius=8)
            text_surface = font.render(f"{i+1}. {card.name}", True, (0, 0, 0))
            text_rect = text_surface.get_rect(center=card_surface.get_rect().center)
            card_surface.blit(text_surface, text_rect)
            screen.blit(card_surface, rect)
        
        cancel_rect = pg.Rect(start_x, y_pos + total_height + 60, card_width, 40)
        pg.draw.rect(screen, (100, 100, 100, 180), cancel_rect, border_radius=8)
        cancel_text = font.render("Cancel - Keep existing cards", True, (255, 255, 255))
        cancel_text_rect = cancel_text.get_rect(center=cancel_rect.center)
        screen.blit(cancel_text, cancel_text_rect)
        pg.display.flip()
        
        for event in pg.event.get():
            if event.type == pg.QUIT:
                pg.quit()
                return None
            if event.type == pg.MOUSEBUTTONDOWN:
                mouse_pos = pg.mouse.get_pos()
                for i, rect in enumerate(card_rects):
                    if rect.collidepoint(mouse_pos):
                        if new_card.name in inventory.card_names:
                            print(f"Player {player_id} already has {new_card.name}. Cannot add duplicate.")
                            temp_surface = screen.copy()
                            screen.blit(temp_surface, (0, 0))
                            overlay = pg.Surface((screen.get_width(), screen.get_height()), pg.SRCALPHA)
                            overlay.fill((0, 0, 0, 180))
                            screen.blit(overlay, (0, 0))
                            msg_text = font.render(f"You already have {new_card.name}", True, (255, 200, 100))
                            msg_rect = msg_text.get_rect(center=(screen.get_width() // 2, screen.get_height() // 2))
                            screen.blit(msg_text, msg_rect)
                            pg.display.flip()
                            pg.time.wait(1000)
                            return None
                        old_card = inventory.swap_card(i, new_card)
                        print(f"Player {player_id} replaced {old_card.name} with {new_card.name}")
                        return new_card
                for i, rect in enumerate(card_rects):
                    if rect.collidepoint(mouse_pos):
                        old_card = inventory.swap_card(i, new_card)
                        print(f"Player {player_id} replaced {old_card.name} with {new_card.name}")
                        return new_card
                if cancel_rect.collidepoint(mouse_pos):
                    print(f"Player {player_id} cancelled card selection")
                    return None
    return None

def handle_inventory_selection_for_all_cards(screen, font, player_id, inventory, new_card):
    card_width = 300
    card_height = 60
    spacing = 15
    
    screen_width = screen.get_width()
    screen_height = screen.get_height()
    
    start_x = (screen_width - card_width) // 2
    total_height = len(inventory.cards) * (card_height + spacing)
    y_pos = screen_height // 2 - total_height // 2
    
    title_text = font.render(f"Inventory Full - Choose a card to replace", True, (255, 255, 255))
    title_rect = title_text.get_rect(center=(screen_width // 2, y_pos - 50))
    
    new_card_text = font.render(f"New Card: {new_card.name}", True, (255, 255, 0))
    new_card_rect = new_card_text.get_rect(center=(screen_width // 2, y_pos + total_height + 30))
    
    card_rects = []
    current_screen = screen.copy()
    running = True
    while running:
        screen.blit(current_screen, (0, 0))
        overlay = pg.Surface((screen_width, screen_height), pg.SRCALPHA)
        overlay.fill((0, 0, 0, 180))
        screen.blit(overlay, (0, 0))
        screen.blit(title_text, title_rect)
        screen.blit(new_card_text, new_card_rect)
        
        for i, card in enumerate(inventory.cards):
            rect = pg.Rect(start_x, y_pos + i * (card_height + spacing), card_width, card_height)
            card_rects.append(rect)
            card_surface = pg.Surface((card_width, card_height), pg.SRCALPHA)
            pg.draw.rect(card_surface, (200, 200, 200, 180), card_surface.get_rect(), border_radius=8)
            pg.draw.rect(card_surface, (0, 0, 0, 180), card_surface.get_rect(), 3, border_radius=8)
            text_surface = font.render(f"{i+1}. {card.name}", True, (0, 0, 0))
            text_rect = text_surface.get_rect(center=card_surface.get_rect().center)
            card_surface.blit(text_surface, text_rect)
            screen.blit(card_surface, rect)
        
        cancel_rect = pg.Rect(start_x, y_pos + total_height + 60, card_width, 40)
        pg.draw.rect(screen, (100, 100, 100, 180), cancel_rect, border_radius=8)
        cancel_text = font.render("Cancel - Keep existing cards", True, (255, 255, 255))
        cancel_text_rect = cancel_text.get_rect(center=cancel_rect.center)
        screen.blit(cancel_text, cancel_text_rect)
        pg.display.flip()
        
        for event in pg.event.get():
            if event.type == pg.QUIT:
                pg.quit()
                return None
            if event.type == pg.MOUSEBUTTONDOWN:
                mouse_pos = pg.mouse.get_pos()
                for i, rect in enumerate(card_rects):
                    if rect.collidepoint(mouse_pos):
                        if new_card.name in inventory.card_names:
                            print(f"Player {player_id} already has {new_card.name}! Cannot add duplicate.")
                            # Show message on screen
                            temp_surface = screen.copy()
                            screen.blit(temp_surface, (0, 0))
                            overlay = pg.Surface((screen.get_width(), screen.get_height()), pg.SRCALPHA)
                            overlay.fill((0, 0, 0, 180))
                            screen.blit(overlay, (0, 0))
                            msg_text = font.render(f"You already have {new_card.name}!", True, (255, 200, 100))
                            msg_rect = msg_text.get_rect(center=(screen.get_width() // 2, screen.get_height() // 2))
                            screen.blit(msg_text, msg_rect)
                            pg.display.flip()
                            pg.time.wait(1000)
                            return None
                        old_card = inventory.swap_card(i, new_card)
                        print(f"Player {player_id} replaced {old_card.name} with {new_card.name}")
                        return new_card
                if cancel_rect.collidepoint(mouse_pos):
                    print(f"Player {player_id} cancelled card selection")
                    return None
    return None

def draw_random_card(screen, font, player_id, player1_inventory, player2_inventory, num=3, is_swap=False, swap_index=None):
    from cards import cards
    
    inventory = player1_inventory if player_id == 1 else player2_inventory

    available_cards = [card for card in cards if card.name not in inventory.card_names]
    
    if len(available_cards) == 0:
        return None
    
    if len(available_cards) < num:
        selected_cards = available_cards
    else:
        selected_cards = random.sample(available_cards, num)
    
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
        screen.blit(current_screen, (0, 0))
        
        overlay = pg.Surface((screen_width, screen_height), pg.SRCALPHA)
        overlay.fill((0, 0, 0, 180))
        screen.blit(overlay, (0, 0))
        
        title_text = font.render(f"Player {player_id} - Choose a Card", True, (255, 255, 255))
        title_rect = title_text.get_rect(center=(screen_width // 2, y_pos - 50))
        screen.blit(title_text, title_rect)
        
        inv_text = font.render(f"Your Cards: {len(inventory.cards)}/{inventory.max_slots}", True, (200, 200, 200))
        inv_rect = inv_text.get_rect(topleft=(20, 20))
        screen.blit(inv_text, inv_rect)
        
        inv_y = 60
        for i, card in enumerate(inventory.cards):
            card_num_text = font.render(f"{i+1}. {card.name}", True, (200, 200, 200))
            screen.blit(card_num_text, (30, inv_y + i * 25))
        
        for i, card in enumerate(selected_cards):
            rect = pg.Rect(start_x + i * (card_width + spacing), y_pos, card_width, card_height)
            card_rects.append(rect)
            card_surface = pg.Surface((card_width, card_height), pg.SRCALPHA)
            card_surface.fill((0,0,0,0))
            pg.draw.rect(card_surface, (200, 200, 200, transparency), card_surface.get_rect(), border_radius=10)
            pg.draw.rect(card_surface, (0, 0, 0, transparency), card_surface.get_rect(), 3, border_radius=10)
            text_surface = font.render(card.name, True, (0, 0, 0))
            text_rect = text_surface.get_rect(center=card_surface.get_rect().center)
            card_surface.blit(text_surface, text_rect)
            screen.blit(card_surface, rect)
        
        if is_swap:
            inst_text = font.render("Click a card to swap it with your selected slot", True, (200, 200, 200))
        elif inventory.is_full():
            inst_text = font.render("Inventory full. Click a card to replace one of your existing cards", True, (200, 200, 200))
        else:
            inst_text = font.render("Click a card to add it to your inventory", True, (200, 200, 200))
        inst_rect = inst_text.get_rect(center=(screen_width // 2, screen_height - 30))
        screen.blit(inst_text, inst_rect)
        
        pg.display.flip()
        
        # Process events inside this loop
        for event in pg.event.get():
            if event.type == pg.QUIT:
                pg.quit()
                return None
            
            if event.type == pg.MOUSEBUTTONDOWN:
                mouse_pos = pg.mouse.get_pos()
                for i, rect in enumerate(card_rects):
                    if rect.collidepoint(mouse_pos):
                        if is_swap and swap_index is not None:
                            inventory.swap_card(swap_index, selected_cards[i])
                            print(f"Player {player_id} swapped card with {selected_cards[i].name}")
                            return selected_cards[i]
                        elif inventory.is_full():
                            return handle_inventory_selection(screen, font, player_id, player1_inventory, player2_inventory, selected_cards[i])
                        else:
                            inventory.add_card(selected_cards[i])
                            print(f"Player {player_id} added {selected_cards[i].name} to inventory")
                            return selected_cards[i]
    return None

def show_all_cards(screen, font, player_id, player_inventory):
    from cards import cards
    
    available_cards = [card for card in cards if card.name not in player_inventory.card_names]

    if len(available_cards) == 0:
        print(f"Player {player_id} has all cards already!")
        screen_copy = screen.copy()
        screen.blit(screen_copy, (0, 0))
        overlay = pg.Surface((screen.get_width(), screen.get_height()), pg.SRCALPHA)
        overlay.fill((0, 0, 0, 180))
        screen.blit(overlay, (0, 0))
        msg_text = font.render("You already have all cards!", True, (255, 200, 100))
        msg_rect = msg_text.get_rect(center=(screen.get_width() // 2, screen.get_height() // 2))
        screen.blit(msg_text, msg_rect)
        pg.display.flip()
        pg.time.wait(1500)
        return None
    
    all_cards = available_cards
    
    card_width = 200
    card_height = 120
    cols = 5
    spacing = 5
    transparency = 180
    
    screen_width = screen.get_width()
    screen_height = screen.get_height()
    
    total_width = cols * card_width + (cols - 1) * spacing
    start_x = (screen_width - total_width) // 2
    start_y = 100
    
    current_screen = screen.copy()
    
    running = True
    while running:
        screen.blit(current_screen, (0, 0))
        overlay = pg.Surface((screen_width, screen_height), pg.SRCALPHA)
        overlay.fill((0, 0, 0, 180))
        screen.blit(overlay, (0, 0))
        
        title_text = font.render(f"Player {player_id} - ALL CARDS", True, (255, 255, 0))
        title_rect = title_text.get_rect(center=(screen_width // 2, 50))
        screen.blit(title_text, title_rect)
        
        card_rects = []
        for i, card in enumerate(all_cards):
            row = i // cols
            col = i % cols
            x = start_x + col * (card_width + spacing)
            y = start_y + row * (card_height + spacing)
            if y + card_height > screen_height:
                break
            rect = pg.Rect(x, y, card_width, card_height)
            card_rects.append((rect, card))
            card_surface = pg.Surface((card_width, card_height), pg.SRCALPHA)
            card_surface.fill((0, 0, 0, 0))
            pg.draw.rect(card_surface, (200, 200, 200, transparency), card_surface.get_rect(), border_radius=10)
            pg.draw.rect(card_surface, (0, 0, 0, transparency), card_surface.get_rect(), 3, border_radius=10)
            text_surface = font.render(card.name, True, (0, 0, 0))
            text_rect = text_surface.get_rect(center=card_surface.get_rect().center)
            card_surface.blit(text_surface, text_rect)
            screen.blit(card_surface, rect)
        
        if player_inventory.is_full():
            inst_text = font.render("Inventory Full. Click a card to REPLACE an existing card", True, (255, 200, 100))
        else:
            inst_text = font.render("Click a card to add it to your inventory", True, (200, 200, 200))
        inst_rect = inst_text.get_rect(center=(screen_width // 2, screen_height - 50))
        screen.blit(inst_text, inst_rect)
        
        inv_text = font.render(f"Inventory: {len(player_inventory.cards)}/{player_inventory.max_slots}", True, (255, 255, 255))
        inv_rect = inv_text.get_rect(topleft=(20, 20))
        screen.blit(inv_text, inv_rect)
        
        if player_inventory.is_full():
            inv_title = font.render("Your cards (click to replace):", True, (255, 200, 100))
            screen.blit(inv_title, (20, 50))
            for i, card in enumerate(player_inventory.cards):
                card_text = font.render(f"{i+1}. {card.name}", True, (200, 200, 200))
                screen.blit(card_text, (30, 80 + i * 25))
        
        pg.display.flip()
        
        for event in pg.event.get():
            if event.type == pg.QUIT:
                pg.quit()
                return None
            
            if event.type == pg.MOUSEBUTTONDOWN:
                mouse_pos = pg.mouse.get_pos()
                for rect, card in card_rects:
                    if rect.collidepoint(mouse_pos):
                        if player_inventory.is_full():
                            return handle_inventory_selection_for_all_cards(screen, font, player_id, player_inventory, card)
                        else:
                            if player_inventory.add_card(card):
                                print(f"Player {player_id} added {card.name} to inventory")
                            else:
                                print(f"Failed to add {card.name}")
                            return card
    return None
