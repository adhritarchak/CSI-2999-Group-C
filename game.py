import pygame
import sys
import json
from Pong import *
from cards import cards
from scoreboard import Scoreboard
from game_scoring import GameScoring
from cards import cards, PlayerCardInventory, draw_random_card, handle_inventory_selection, show_all_cards

pygame.init()

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


# Player inventories
player1_inventory = PlayerCardInventory(max_slots=5, player_id=1)
player2_inventory = PlayerCardInventory(max_slots=5, player_id=2)


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

ball = Ball(x=paddle1.hitbox.right + ballConfig['Radius'] + 5, 
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

ball.repulsion_active = False
ball.repulsion_activator = None
ball.repulsion_timer = 0
ball.repulsion_has_hit = False
ball.repulsion_printed = False  

paddle1_debuff_printed = False
paddle2_debuff_printed = False
paddle1_debuff_expired = False
paddle2_debuff_expired = False

shadow_balls = []
chosen_card = None

# ===== SCORING SYSTEM =====
scoreboard = Scoreboard(screen, font)

scoring = GameScoring(
    scoreboard, ball, paddle1, paddle2, 
    {'left': Left_Boundary, 'right': Right_Boundary, 'top': Top_Boundary, 'bottom': Bot_Boundary}
)

waiting_for_serve = True
serve_timer = 30
last_scorer = None  # Track who scored last to determine server
waiting_for_card = False
current_player_selecting = None
last_round_winner = None
# ===== END SCORING SYSTEM =====

# actual game
running = True
while running:
    dt = clock.tick(screenConfig['FPS'])
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
            continue
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                running = False
                continue
            if event.key == pygame.K_c:
                if not scoreboard.match_over and scoreboard.round_active and not scoreboard.showing_round_end:
                    chosen_card = show_all_cards(screen, font,1, player1_inventory)
                    if chosen_card:
                        print("You picked: ", chosen_card.name)
            #Player 1 uses 1,2,3,4,5 keys (left side of keyboard)
            if event.key == pygame.K_1 and len(player1_inventory.cards) > 0:
                if not scoreboard.match_over and scoreboard.round_active and not scoreboard.showing_round_end:
                    card = player1_inventory.get_card(0)
                    if card.can_use(scoreboard.round):
                        card.activate(ball=ball, paddle1=paddle1, paddle2=paddle2, shadow_balls=shadow_balls, activator=1)
                        player1_inventory.use_card(0, scoreboard.round)
                        print(f"Player 1 used: {card.name}")

            elif event.key == pygame.K_2 and len(player1_inventory.cards) > 1:
                if not scoreboard.match_over and scoreboard.round_active and not scoreboard.showing_round_end:
                    card = player1_inventory.get_card(1)
                    if card.can_use(scoreboard.round):
                        card.activate(ball=ball, paddle1=paddle1, paddle2=paddle2, shadow_balls=shadow_balls, activator=1)
                        player1_inventory.use_card(1, scoreboard.round)
                        print(f"Player 1 used: {card.name}")
                    print(f"Player 1 used: {card.name}")
            elif event.key == pygame.K_3 and len(player1_inventory.cards) > 2:
                if not scoreboard.match_over and scoreboard.round_active and not scoreboard.showing_round_end:
                    card = player1_inventory.get_card(2)
                    if card.can_use(scoreboard.round):
                        card.activate(ball=ball, paddle1=paddle1, paddle2=paddle2, shadow_balls=shadow_balls, activator=1)
                        player1_inventory.use_card(2, scoreboard.round)
                        print(f"Player 1 used: {card.name}")
                    print(f"Player 1 used: {card.name}")
            elif event.key == pygame.K_4 and len(player1_inventory.cards) > 3:
                if not scoreboard.match_over and scoreboard.round_active and not scoreboard.showing_round_end:
                    card = player1_inventory.get_card(3)
                    if card.can_use(scoreboard.round):
                        card.activate(ball=ball, paddle1=paddle1, paddle2=paddle2, shadow_balls=shadow_balls, activator=1)
                        player1_inventory.use_card(3, scoreboard.round)
                        print(f"Player 1 used: {card.name}")
                    print(f"Player 1 used: {card.name}")
            elif event.key == pygame.K_5 and len(player1_inventory.cards) > 4:
                if not scoreboard.match_over and scoreboard.round_active and not scoreboard.showing_round_end:
                    card = player1_inventory.get_card(4)
                    if card.can_use(scoreboard.round):
                        card.activate(ball=ball, paddle1=paddle1, paddle2=paddle2, shadow_balls=shadow_balls, activator=1)
                        player1_inventory.use_card(4, scoreboard.round)
                        print(f"Player 1 used: {card.name}")
                    print(f"Player 1 used: {card.name}")
            # Player 2 uses I, O, P, K, L keys (right side of keyboard)
            elif event.key == pygame.K_i and len(player2_inventory.cards) > 0:
                if not scoreboard.match_over and scoreboard.round_active and not scoreboard.showing_round_end:
                    card = player2_inventory.get_card(0)
                    if card.can_use(scoreboard.round):
                        card.activate(ball=ball, paddle1=paddle1, paddle2=paddle2, shadow_balls=shadow_balls, activator=2)
                        player2_inventory.use_card(0, scoreboard.round)
                        print(f"Player 2 used: {card.name}")
                    else:
                        print(f"Card {card.name} is on cooldown")

            elif event.key == pygame.K_o and len(player2_inventory.cards) > 1:
                if not scoreboard.match_over and scoreboard.round_active and not scoreboard.showing_round_end:
                    card = player2_inventory.get_card(1)
                    if card.can_use(scoreboard.round):
                        card.activate(ball=ball, paddle1=paddle1, paddle2=paddle2, shadow_balls=shadow_balls, activator=2)
                        player2_inventory.use_card(1, scoreboard.round)
                        print(f"Player 2 used: {card.name}")
                    else:
                        print(f"Card {card.name} is on cooldown")

            elif event.key == pygame.K_p and len(player2_inventory.cards) > 2:
                if not scoreboard.match_over and scoreboard.round_active and not scoreboard.showing_round_end:
                    card = player2_inventory.get_card(2)
                    if card.can_use(scoreboard.round):
                        card.activate(ball=ball, paddle1=paddle1, paddle2=paddle2, shadow_balls=shadow_balls, activator=2)
                        player2_inventory.use_card(2, scoreboard.round)
                        print(f"Player 2 used: {card.name}")
                    else:
                        print(f"Card {card.name} is on cooldown")

            elif event.key == pygame.K_k and len(player2_inventory.cards) > 3:
                if not scoreboard.match_over and scoreboard.round_active and not scoreboard.showing_round_end:
                    card = player2_inventory.get_card(3)
                    if card.can_use(scoreboard.round):
                        card.activate(ball=ball, paddle1=paddle1, paddle2=paddle2, shadow_balls=shadow_balls, activator=2)
                        player2_inventory.use_card(3, scoreboard.round)
                        print(f"Player 2 used: {card.name}")
                    else:
                        print(f"Card {card.name} is on cooldown")

            elif event.key == pygame.K_l and len(player2_inventory.cards) > 4:
                if not scoreboard.match_over and scoreboard.round_active and not scoreboard.showing_round_end:
                    card = player2_inventory.get_card(4)
                    if card.can_use(scoreboard.round):
                        card.activate(ball=ball, paddle1=paddle1, paddle2=paddle2, shadow_balls=shadow_balls, activator=2)
                        player2_inventory.use_card(4, scoreboard.round)
                        print(f"Player 2 used: {card.name}")
                    else:
                        print(f"Card {card.name} is on cooldown")

            if event.key == pygame.K_SPACE:
                if scoreboard.showing_round_end:
                    print(f"DEBUG: last_round_winner = {last_round_winner}")  # Add this
                    winner_for_next = scoreboard.rnd_winner
                    # Start next round
                    scoreboard.start_next_round()
                    scoring.reset_for_new_round(paddleConfig, ballConfig, Center_y, Left_Boundary, Right_Boundary, last_round_winner)
                
                    
                    waiting_for_serve = True
                    serve_timer = 30
                    chosen_card = None
                    shadow_balls.clear()
                    scoreboard.showing_round_end = False
                    last_scorer = None
                    
                elif scoreboard.showing_match_end:
                    # Restart entire match
                    scoreboard.reset_match()
                    scoring.reset_for_new_round(paddleConfig, ballConfig, Center_y, Left_Boundary, Right_Boundary)
                    waiting_for_serve = True
                    serve_timer = 30
                    shadow_balls.clear()
                    ball.set_velocity(0, 0, 0)
                    ball.served = False
                    scoreboard.showing_match_end = False
                    last_scorer = None
                    last_round_winner = None
    
    # ===== SHOW ROUND END SCREEN =====
    if scoreboard.showing_round_end:
        draw_table()
        paddle1.draw(screen=screen)
        paddle2.draw(screen=screen)
        ball.draw(screen=screen)
        for shadow in shadow_balls[:]:
            shadow.draw(screen=screen)
            if shadow.get_height() <= 0:
                shadow_balls.remove(shadow)
        scoreboard.draw_round_end()
        pygame.display.flip()
        continue
    
    # ===== SHOW MATCH END SCREEN =====
    if scoreboard.match_over or scoreboard.showing_match_end:
        draw_table()
        paddle1.draw(screen=screen)
        paddle2.draw(screen=screen)
        ball.draw(screen=screen)
        for shadow in shadow_balls[:]:
            shadow.draw(screen=screen)
            if shadow.get_height() <= 0:
                shadow_balls.remove(shadow)
        chosen_card = None
        scoreboard.draw_match_end()
        pygame.display.flip()
        continue
    
    keys = pygame.key.get_pressed()
    
    # ===== CHECK FOR SCORING =====
    scored, winner = scoring.check_score()
    if scored:
        print(f"SCORING EVENT - Winner: Player {winner}")
        last_scorer = winner
        losing_player = 2 if winner == 1 else 1

        player1_inventory.update_all_cooldowns()
        player2_inventory.update_all_cooldowns()

        round_continues = scoreboard.add_point(winner)

        selected_card = draw_random_card(screen, font, losing_player, player1_inventory, player2_inventory)
        if selected_card:
            print(f"Player {losing_player} selected: {selected_card.name}")
        
        if round_continues:
            # Reset ball for next point
            scoring.reset_ball_for_serve(ballConfig, last_scorer)
            scoring.reset_paddle_states()
            waiting_for_serve = True
            serve_timer = 30
        else:
            # Round ended - no need to update cooldowns again here
            last_round_winner = winner
            
            #scoring.reset_for_new_round(paddleConfig, ballConfig, Center_y, Left_Boundary, Right_Boundary, winner)
            waiting_for_serve = True    
            serve_timer = 30
            chosen_card = None
            shadow_balls.clear()
            #continue
    
    # ===== HANDLE SERVE WAITING STATE =====
    if waiting_for_serve:
        if serve_timer > 0:
            serve_timer -= 1
        
        # Process paddle inputs while waiting
        paddle1.process_keys(keys, dt)
        paddle2.process_keys(keys, dt)
        paddle1.process_swing(dt)
        paddle2.process_swing(dt)
        paddle1.process_smash(dt)
        paddle2.process_smash(dt)
        
        # Check if a player hits the ball while waiting for serve
        if ball.within_rect(paddle1.get_hitbox(), (0, 0)) and paddle1.can_hit_ball:
            ball.bounce(1, paddle1.swingAngle)
            ball.impulse((paddle1.velocity[0] * 0.01 * dt / 1000, paddle1.velocity[1] * 0.1 * dt / 1000, 0))
            ball.multiplyVelocity(1 + (ballConfig['paddle_hit_boost'] * paddle1.smashPower))
            paddle1.has_hit_ball = True
            ball.served = True
            waiting_for_serve = False
            if chosen_card and chosen_card.is_Passive:
                chosen_card.activate(ball=ball, paddle1=paddle1, paddle2=paddle2, shadow_balls=shadow_balls)
                
        if ball.within_rect(paddle2.get_hitbox(), (0, 0)) and paddle2.can_hit_ball:
            ball.bounce(-1, paddle2.swingAngle)
            ball.impulse((paddle2.velocity[0] * 0.01 * dt / 1000, paddle2.velocity[1] * 0.1 * dt / 1000, 0))
            ball.multiplyVelocity(1 + (ballConfig['paddle_hit_boost'] * paddle2.smashPower))
            paddle2.has_hit_ball = True
            ball.served = True
            waiting_for_serve = False
            if chosen_card and chosen_card.is_Passive:
                chosen_card.activate(ball=ball, paddle1=paddle1, paddle2=paddle2, shadow_balls=shadow_balls)
    else:
        # ===== NORMAL GAME LOGIC =====
        paddle1.process_keys(keys, dt)
        paddle2.process_keys(keys, dt)
        
        paddle1.process_swing(dt)
        paddle2.process_swing(dt)

        paddle1.process_smash(dt)
        paddle2.process_smash(dt)


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
            if paddle1.hitbox.width < paddleConfig['Paddle_Width'] or paddle1.hitbox.height < paddleConfig['Paddle_Height']:
                old_width = paddle1.hitbox.width
                old_height = paddle1.hitbox.height
                new_width = paddleConfig['Paddle_Width']
                new_height = paddleConfig['Paddle_Height']
                
                # Center the restored paddle
                new_x = paddle1.position[0] + (old_width - new_width) // 2
                new_y = paddle1.position[1] + (old_height - new_height) // 2
                
                paddle1.hitbox.width = new_width
                paddle1.hitbox.height = new_height
                paddle1.position = (new_x, new_y)
                paddle1.set_hitbox_pos(0, 0)
        
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
                if paddle2.hitbox.width < paddleConfig['Paddle_Width'] or paddle2.hitbox.height < paddleConfig['Paddle_Height']:
                    old_width = paddle2.hitbox.width
                    old_height = paddle2.hitbox.height
                    new_width = paddleConfig['Paddle_Width']
                    new_height = paddleConfig['Paddle_Height']
                    
                    # Center the restored paddle
                    new_x = paddle2.position[0] + (old_width - new_width) // 2
                    new_y = paddle2.position[1] + (old_height - new_height) // 2
                    
                    paddle2.hitbox.width = new_width
                    paddle2.hitbox.height = new_height
                    paddle2.position = (new_x, new_y)
                    paddle2.set_hitbox_pos(0, 0)
        
                if paddle2_debuff_expired == True:
                    print("Paddle2 debuffs expired")
                    paddle2_debuff_printed = True
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

    if hasattr(ball, 'repulsion_active') and ball.repulsion_active:
        ball.repulsion_timer -= dt
        
        if ball.repulsion_activator == 1:
            enemy_paddle = paddle2
            direction = 1  
        else:
            enemy_paddle = paddle1
            direction = -1  
        
        ball_x, ball_y = ball.get_position()
        ball_vel_x, ball_vel_y, ball_vel_z = ball.get_velocity()
        
        paddle_rect = enemy_paddle.get_hitbox()
        
        if direction == 1:
            distance = paddle_rect.left - ball_x
            if 0 < distance < 100:
                ball.set_velocity(-abs(ball_vel_x) * 0.8 if ball_vel_x > 0 else ball_vel_x * 1.2, 
                                ball_vel_y + random.uniform(-4, 4), ball_vel_z)
                ball.spin = -0.5
                print(f"Repulsion pushed ball left! Distance: {distance:.0f}")
        else:
            distance = ball_x - paddle_rect.right
            if 0 < distance < 100:
                ball.set_velocity(abs(ball_vel_x) * 0.8 if ball_vel_x < 0 else ball_vel_x * 1.2,
                                ball_vel_y + random.uniform(-4, 4), ball_vel_z)
                ball.spin = 0.5
                print(f"Repulsion pushed ball right! Distance: {distance:.0f}")
        
        # End effect after first hit
        if ball.repulsion_has_hit:
            ball.repulsion_active = False
            print("Repulsion effect ended after hit!")
        
        if ball.repulsion_timer <= 0:
            ball.repulsion_active = False
            print("Repulsion effect expired!")
   
    if ball.within_rect(paddle1.get_hitbox(), (0, 0)) and paddle1.can_hit_ball:
            if ball.get_velocity()[0] <= 0:
                ball.bounce(1, paddle1.swingAngle)
                ball.impulse((paddle1.velocity[0] * 0.01 * dt / 1000, paddle1.velocity[1] * 0.1 * dt / 1000, 0))
                ball.multiplyVelocity(1 + (ballConfig['paddle_hit_boost'] * paddle1.smashPower))
                paddle1.has_hit_ball = True
                if chosen_card and chosen_card.is_Passive:
                    chosen_card.activate(ball=ball, paddle1=paddle1, paddle2=paddle2, shadow_balls=shadow_balls)
                if abs(ball.get_velocity()[0]) >= ballConfig['Max_Speed'] * 0.7:
                    paddle1.position = (paddle1.position[0] - 30, paddle1.position[1])
                if hasattr(ball, 'repulsion_active') and ball.repulsion_active:
                    ball.repulsion_has_hit = True
                    
    if ball.within_rect(paddle2.get_hitbox(), (0, 0)) and paddle2.can_hit_ball:
            if ball.get_velocity()[0] >= 0:
                ball.bounce(-1, paddle2.swingAngle)
                ball.impulse((paddle2.velocity[0] * 0.01 * dt / 1000, paddle2.velocity[1] * 0.1 * dt / 1000, 0))
                ball.multiplyVelocity(1 + (ballConfig['paddle_hit_boost'] * paddle2.smashPower))
                paddle2.has_hit_ball = True
                if chosen_card and chosen_card.is_Passive:
                    chosen_card.activate(ball=ball, paddle1=paddle1, paddle2=paddle2, shadow_balls=shadow_balls)
                if abs(ball.get_velocity()[0]) >= ballConfig['Max_Speed'] * 0.7:
                    paddle2.position = (paddle2.position[0] + 30, paddle2.position[1])
                if hasattr(ball, 'repulsion_active') and ball.repulsion_active:
                    ball.repulsion_has_hit = True
                    
    ball.clamp_velocity()
        
    ball.update_position()
    
    draw_table()

    paddle1.draw(screen=screen)
    paddle2.draw(screen=screen)

    ball.draw(screen=screen)

    for shadow in shadow_balls[:]:
        shadow.draw(screen=screen)
        if shadow.get_height() <= 0:
            shadow_balls.remove(shadow)
   
    scoreboard.draw()

    pygame.display.flip()

pygame.quit()
sys.exit()