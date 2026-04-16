import pygame
import sys
from Pong import *
pygame.init()
from cards import cards

# Load config from JSON file
with open('config.json') as f:
    config = json.load(f)
    screenConfig = config['Window']
    tableConfig = config['Table Layout']
    paddleConfig = config['Paddle Physics']
    ballConfig = config['Ball Physics']
    colorConfig = config['colors']

paddle1Images = [pygame.image.load(f"assets/Red Paddle {i}.png") for i in range(1, 8)]
paddle2Images = [pygame.image.load(f"assets/Blue Paddle {i}.png") for i in range(1, 8)]

# Window Setup
screen = pygame.display.set_mode((screenConfig['Width'], screenConfig['Height']))
pygame.display.set_caption(screenConfig['Caption'])
clock = pygame.time.Clock()
font = pygame.font.SysFont(*screenConfig['font'])

# Table Setup
Table_Rect = pygame.Rect(tableConfig['Table_Margin'], tableConfig['Table_Margin'],
                         screenConfig['Width'] - tableConfig['Table_Margin'] * 2,
                         screenConfig['Height'] - tableConfig['Table_Margin'] * 2,)

Left_Boundary = Table_Rect.left
Right_Boundary = Table_Rect.right
Top_Boundary = Table_Rect.top
Bot_Boundary = Table_Rect.bottom
Center_x = Table_Rect.centerx
Center_y = Table_Rect.centery


Smash1_hold_time = 0
Smash1_hit = False
Smash1_hit_time = 0
Smash1_active = False
Smash2_hold_time = 0
Smash2_active = False
Smash_duration = 3000
Smash2_hit = False
Smash2_hit_time = 0


#paddles setup
paddle1_x = Left_Boundary + 50
paddle1_y = Center_y - paddleConfig['Paddle_Height'] // 2

paddle2_x = Right_Boundary - 50 - paddleConfig['Paddle_Width']
paddle2_y = Center_y - paddleConfig['Paddle_Height'] // 2

paddle1 = PongPaddle(width=paddleConfig['Paddle_Width'], height=paddleConfig['Paddle_Height'], color = colorConfig['Paddle 1'], 
                     initialPos=(paddle1_x, paddle1_y), speed=paddleConfig['BasePaddleSpeed'], images=paddle1Images)
paddle2 = PongPaddle(width=paddleConfig['Paddle_Width'], height=paddleConfig['Paddle_Height'], color=colorConfig['Paddle 2'], 
                     initialPos=(paddle2_x, paddle2_y), speed=paddleConfig['BasePaddleSpeed'], images=paddle2Images)

paddle1.setBounds(Top_Boundary, Bot_Boundary, Left_Boundary, Center_x)
paddle2.setBounds(Top_Boundary, Bot_Boundary, Center_x, Right_Boundary)

paddle1.setKeys(pygame.K_w, pygame.K_s, pygame.K_a, pygame.K_d, pygame.K_q, pygame.K_e)
paddle2.setKeys(pygame.K_UP, pygame.K_DOWN, pygame.K_LEFT, pygame.K_RIGHT, pygame.K_COMMA, pygame.K_PERIOD)

paddle1.setSwingConfig(paddleConfig['SwingBackTime'], paddleConfig['SwingForwardTime'], paddleConfig['SmashHoldtime'], paddleConfig['CooldownTime'])
paddle2.setSwingConfig(paddleConfig['SwingBackTime'], paddleConfig['SwingForwardTime'], paddleConfig['SmashHoldtime'], paddleConfig['CooldownTime'])

class PlayerCardInventory:
    def __init__(self, max_slots=5):
        self.cards = []  # List of Card objects
        self.max_slots = max_slots
    
    def add_card(self, card):
        if len(self.cards) < self.max_slots:
            self.cards.append(card)
            card.owner = self.player_id
            return True
        return False
    
    def remove_card(self, index):
        if 0 <= index < len(self.cards):
            return self.cards.pop(index)
        return None
    
    def swap_card(self, index, new_card):
        if 0 <= index < len(self.cards):
            old_card = self.cards[index]
            self.cards[index] = new_card
            new_card.owner = self.player_id
            return old_card
        return None
    def get_card(self, index):
        if 0 <= index < len(self.cards):
            return self.cards[index]
        return None
    
    def is_full(self):
        return len(self.cards) >= self.max_slots
    

def draw_random_card(screen, font, player_id, num=3,is_swap=False, swap_index=None,):
    selected_cards = random.sample(cards, num)

    card_width = 200
    card_height = 120
    spacing = 50
    transparency = 180

    screen_width = screen.get_width()
    screen_height = screen.get_height()

    start_x = (screen_width - ((card_width * num) + spacing * (num - 1))) // 2
    y_pos = screen_height // 2 - card_height // 2

    inventory = player1_inventory if player_id == 1 else player2_inventory

    card_rects = []
    current_screen = screen.copy()

    running = True
    while running:
        #screen.fill((30, 30, 30))
        screen.blit(current_screen, (0, 0))

        overlay = pg.Surface((screen_width, screen_height), pg.SRCALPHA)
        overlay.fill((0, 0, 0, 180))  # Semi-transparent overlay
        screen.blit(overlay, (0, 0))

        title_text = font.render(f"Player {player_id} - Choose a Card", True, (255, 255, 255))
        title_rect = title_text.get_rect(center=(screen_width // 2, y_pos - 50))
        screen.blit(title_text, title_rect)
        
        # Draw inventory info
        inv_text = font.render(f"Your Cards: {len(inventory.cards)}/{inventory.max_slots}", True, (200, 200, 200))
        inv_rect = inv_text.get_rect(topleft=(20, 20))
        screen.blit(inv_text, inv_rect)
        
        # Draw inventory list
        inv_y = 60
        for i, card in enumerate(inventory.cards):
            card_num_text = font.render(f"{i+1}. {card.name}", True, (200, 200, 200))
            screen.blit(card_num_text, (30, inv_y + i * 25))

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

        if is_swap:
            inst_text = font.render("Click a card to swap it with your selected slot", True, (200, 200, 200))
        elif inventory.is_full():
            inst_text = font.render("Inventory full! Click a card to replace one of your existing cards", True, (200, 200, 200))
        else:
            inst_text = font.render("Click a card to add it to your inventory", True, (200, 200, 200))
            inst_rect = inst_text.get_rect(center=(screen_width // 2, screen_height - 30))
            screen.blit(inst_text, inst_rect)

        pg.display.flip()

        for event in pg.event.get():
            if event.type == pg.QUIT:
                pg.quit()
                return None

            if event.type == pg.MOUSEBUTTONDOWN:
                mouse_pos = pg.mouse.get_pos()

                for i, rect in enumerate(card_rects):
                    if rect.collidepoint(mouse_pos):
                        if is_swap and swap_index is not None:
                            # Swap cards
                            inventory.swap_card(swap_index, selected_cards[i])
                            print(f"Player {player_id} swapped card with {selected_cards[i].name}")
                            return selected_cards[i]
                        elif inventory.is_full():
                            # Show inventory selection to replace a card
                            return handle_inventory_selection(screen, font, player_id, selected_cards[i])
                        else:
                            # Just add the card
                            inventory.add_card(selected_cards[i])
                            print(f"Player {player_id} added {selected_cards[i].name} to inventory")
                            return selected_cards[i]
    
    return None
def handle_inventory_selection(screen, font, player_id, new_card):
    '''Helper function to let player choose which card to replace when inventory is full'''
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
                
                # Check inventory card clicks
                for i, rect in enumerate(card_rects):
                    if rect.collidepoint(mouse_pos):
                        # Replace the clicked card with the new card
                        old_card = inventory.swap_card(i, new_card)
                        print(f"Player {player_id} replaced {old_card.name} with {new_card.name}")
                        return new_card
                if cancel_rect.collidepoint(mouse_pos):
                    print(f"Player {player_id} cancelled card selection")
                    return None
    
    return None


# Player inventories
player1_inventory = PlayerCardInventory(max_slots=5)
player2_inventory = PlayerCardInventory(max_slots=5)

# Scoring system
score_timer = 0
score_display_time = 2000  # Show score for 2 seconds
show_score = False
last_scorer = None
waiting_for_card = False
current_player_selecting = None


def draw_table():
    # Background
    screen.fill(colorConfig['Light Brown'])
    colorConfig['Shadow'] = Table_Rect.move(6, 6)
    pygame.draw.rect(screen, colorConfig['Black'], colorConfig['Shadow'], border_radius=6)
    pygame.draw.rect(screen, colorConfig['Red Table'], Table_Rect)

    # Table border
    pygame.draw.rect(screen, colorConfig['White'], Table_Rect, tableConfig['Table_Border'])

    # PingPong Net
    pygame.draw.line(
        screen, colorConfig['White'],
        (Table_Rect.centerx, Table_Rect.top),
        (Table_Rect.centerx, Table_Rect.bottom),
        tableConfig['Net_Thickness']
    )

    # Center horizontal line
    pygame.draw.line(
        screen, colorConfig['White'],
        (Table_Rect.left, Table_Rect.centery),
        (Table_Rect.right, Table_Rect.centery),
        tableConfig['Midline_Thickness']
    )

ball = Ball(x=paddle1.hitbox.right + ballConfig['Radius'] + 5, #Ball will start just to the right of paddle 1
            y=paddle1.hitbox.centery,
            height=ballConfig['init_height'],
            vel_z=0,
            speed_x=0,
            speed_y=0,
            radius=ballConfig['Radius'],
            spin=0,
            chosen_card=None,
            max_speed=ballConfig['Max_Speed'])
ball.set_bounds(top=Top_Boundary, bottom=Bot_Boundary, left=Left_Boundary, right=Right_Boundary)

ball.do_draw_prediction(screenConfig['View_Debug'])
paddle1.viewDebugInfo(screenConfig['View_Debug'])
paddle2.viewDebugInfo(screenConfig['View_Debug'])

ball.rally_active = False
ball.rally_timer = 0
ball.rally_activator = None
ball.rally_slow_factor = 0.6
ball.rally_speed_threshold = 7.0
ball.original_max_speed = ball.max_speed

paddle1_debuff_printed = False
paddle2_debuff_printed = False
paddle1_debuff_expired = False
paddle2_debuff_expired = False

shadow_balls = []
chosen_card = None
# actual game
running = True
while running: 
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
            continue
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_c:  # Press C to open cards
                chosen_card = draw_random_card(screen, font, 1)
                if chosen_card:
                    print("You picked: ", chosen_card.name)
            if event.key == pygame.K_z and chosen_card is not None: # Press Z to activate the chosen card effect
                   chosen_card.activate(ball=ball, paddle1=paddle1, paddle2=paddle2, shadow_balls=shadow_balls)
                   print("Activated card effect:", chosen_card.name)
                   chosen_card = None  # Clear the chosen card after activation

    dt = clock.tick(screenConfig['FPS'])
    keys = pygame.key.get_pressed()
    

    paddle1.process_keys(keys, dt)
    paddle2.process_keys(keys, dt)

    
    paddle1.process_swing(dt)
    paddle2.process_swing(dt)

    paddle1.process_smash(dt)
    paddle2.process_smash(dt)

   
    if paddle1.debuff_timer > 0:
        paddle1.debuff_timer -= dt
        paddle1_debuff_printed = False
        paddle1_debuff_expired = True

    if paddle1.debuff_timer <= 0:   # debuff expired, reset all multipliers
        if not paddle1_debuff_printed:
            paddle1.speed_multiplier = 1.0
            paddle1.smash_hold_multiplier = 1.0
            paddle1.smash_power_debuff = 0.0
            paddle1.hit_strength_multiplier = 1.0
            paddle1.swing_time_multiplier = 1.0
            paddle1.keys_swapped = False
            if paddle1_debuff_expired == True:
                print("Paddle1 debuffs expired")
                paddle1_debuff_printed = True

        
    if paddle2.debuff_timer > 0:
        paddle2.debuff_timer -= dt
        paddle2_debuff_printed = False
        paddle2_debuff_expired = True

    if paddle2.debuff_timer <= 0:
        if not paddle2_debuff_printed:
                paddle2.speed_multiplier = 1.0
                paddle2.smash_hold_multiplier = 1.0
                paddle2.smash_power_debuff = 0.0
                paddle2.hit_strength_multiplier = 1.0
                paddle2.swing_time_multiplier = 1.0
                paddle2.keys_swapped = False
                if paddle2_debuff_expired == True:
                    print("Paddle2 debuffs expired")
                    paddle2_debuff_printed = True


    if ball.within_rect(paddle1.get_hitbox(), (0, 0)) and paddle1.can_hit_ball:
        if ball.get_velocity()[X] <= 0:
            ball.bounce(1, paddle1.swingAngle)
            ball.impulse((paddle1.velocity[X] * 0.01 * dt / 1000, paddle1.velocity[Y] * 0.1 * dt / 1000, 0))
            ball.multiplyVelocity(1 + (ballConfig['paddle_hit_boost'] * paddle1.smashPower))
            paddle1.has_hit_ball = True # Prevent multiple hits in one swing
            if chosen_card and chosen_card.is_Passive:  # passive triggers on hit
                chosen_card.activate(ball=ball, paddle1=paddle1, paddle2=paddle2, shadow_balls=shadow_balls)
            if abs(ball.get_velocity()[X]) >= ballConfig['Max_Speed'] * 0.7:
                paddle1.position = (paddle1.position[X] - 30, paddle1.position[Y]) #Should push paddle when returning a smash
    if ball.within_rect(paddle2.get_hitbox(), (0, 0)) and paddle2.can_hit_ball:
        if ball.get_velocity()[X] >= 0:
            ball.bounce(-1, paddle2.swingAngle)
            ball.impulse((paddle2.velocity[X] * 0.01 * dt / 1000, paddle2.velocity[Y] * 0.1 * dt / 1000, 0))
            ball.multiplyVelocity(1 + (ballConfig['paddle_hit_boost'] * paddle2.smashPower))
            paddle2.has_hit_ball = True # Prevent multiple hits in one swing
            if chosen_card and chosen_card.is_Passive:  # passive triggers on hit
                chosen_card.activate(ball=ball, paddle1=paddle1, paddle2=paddle2, shadow_balls=shadow_balls)
            if abs(ball.get_velocity()[X]) >= ballConfig['Max_Speed'] * 0.7: #Should push paddle when returning a smash
                paddle2.position = (paddle2.position[X] + 30, paddle2.position[Y])
    ball.clamp_velocity()

    if ball.get_position()[0] < Left_Boundary:
    # Player 2 scores
        if not waiting_for_card and not show_score:
            show_score = True
            last_scorer = 2
            score_timer = pg.time.get_ticks()
            waiting_for_card = True
            current_player_selecting = 2
            # Reset ball position
            ball.set_position(paddle1.hitbox.right + 20, Center_y, 50)
            ball.set_velocity(0, 0, 0)
            ball.served = False
        
    elif ball.get_position()[0] > Right_Boundary:
    # Player 1 scores
        if not waiting_for_card and not show_score:
            show_score = True
            last_scorer = 1
            score_timer = pg.time.get_ticks()
            waiting_for_card = True
            current_player_selecting = 1
            # Reset ball position
            ball.set_position(paddle1.hitbox.right + 20, Center_y, 50)
            ball.set_velocity(0, 0, 0)
            ball.served = False

# Handle score display and card selection
    if show_score:
        current_time = pg.time.get_ticks()
        if current_time - score_timer >= score_display_time:
            show_score = False
        # Show card selection for the player who lost the point
        if waiting_for_card and current_player_selecting:
            selected_card = draw_random_card(screen, font, current_player_selecting)
            if selected_card:
                print(f"Player {current_player_selecting} selected: {selected_card.name}")
                waiting_for_card = False
                current_player_selecting = None
                # Reset ball for next point
                ball.set_position(paddle1.hitbox.right + 20, Center_y, 50)
                ball.set_velocity(0, 0, 0)
                ball.served = False
        score_surface = font.render(f"Player {last_scorer} Scores!", True, (255, 255, 255))
        score_rect = score_surface.get_rect(center=(screen.get_width() // 2, screen.get_height() // 2))
        screen.blit(score_surface, score_rect)
    
    if ball.rally_active:
        ball.rally_timer -= dt
        if ball.rally_timer <= 0:
            # Rally effect expires
            ball.rally_active = False
            ball.max_speed = ball.original_max_speed
            print("Rally effect expired!")
        else:
            # Check current ball speed and apply slowing if needed
            current_speed = abs(ball.get_velocity()[0])  # Horizontal speed
            if current_speed > ball.rally_speed_threshold:
                # Apply slowing effect by temporarily reducing max speed
                slowed_max_speed = ball.original_max_speed * ball.rally_slow_factor
                ball.max_speed = max(slowed_max_speed, ball.rally_speed_threshold)
                
                # Optional: Visual indicator that rally is active
                if int(ball.rally_timer / 1000) != int((ball.rally_timer + dt) / 1000):
                    seconds_left = int(ball.rally_timer / 1000) + 1
                    print(f"Rally active: {seconds_left} seconds remaining")
            else:
                # Restore original max speed when ball is not going fast
                ball.max_speed = ball.original_max_speed
    draw_table()

    paddle1.draw(screen=screen)
    paddle2.draw(screen=screen)

    ball.draw(screen=screen)

    for shadow in shadow_balls[:]:
        shadow.draw(screen=screen)
        if shadow.get_height() <= 0:
            shadow_balls.remove(shadow)

    pygame.display.flip()

pygame.quit()
sys.exit()