import pygame
import sys
import json
from Pong import *
from cards import draw_random_card
from scoreboard import Scoreboard
from game_scoring import GameScoring

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

def draw_table():
    # Background
    screen.fill(colorConfig['Light Brown'])
    shadow_rect = Table_Rect.move(6, 6)
    pygame.draw.rect(screen, colorConfig['Black'], shadow_rect, border_radius=6)
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
# ===== END SCORING SYSTEM =====

# actual game
running = True
while running: 
    dt = clock.tick(screenConfig['FPS'])
    
    # ===== HANDLE EVENTS =====
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
                    chosen_card = draw_random_card(screen, font)
                    if chosen_card:
                        print("You picked: ", chosen_card.name)
            if event.key == pygame.K_z and chosen_card is not None:
                if not scoreboard.match_over and scoreboard.round_active and not scoreboard.showing_round_end:
                    chosen_card.activate(ball=ball, paddle1=paddle1, paddle2=paddle2, shadow_balls=shadow_balls)
                    print("Activated card effect:", chosen_card.name)
                    chosen_card = None
            if event.key == pygame.K_SPACE:
                if scoreboard.showing_round_end:
                    # Start next round
                    scoreboard.start_next_round()
                    scoring.reset_for_new_round(paddleConfig, ballConfig, Center_y, Left_Boundary, Right_Boundary)
                    
                    # Reset ball to player 1's side for new round
                    ball.set_position(
                        paddle1.hitbox.right + ballConfig['Radius'] + 5,
                        paddle1.hitbox.centery,
                        ballConfig['init_height']
                    )
                    ball.set_velocity(0, 0, 0)
                    ball.served = False
                    
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
                    chosen_card = None
                    shadow_balls.clear()
                    ball.set_velocity(0, 0, 0)
                    ball.served = False
                    scoreboard.showing_match_end = False
                    last_scorer = None
    
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
        scoreboard.draw_match_end()
        pygame.display.flip()
        continue
    
    keys = pygame.key.get_pressed()
    
    # ===== CHECK FOR SCORING =====
    scored, winner = scoring.check_score()
    if scored:
        print(f"SCORING EVENT - Winner: Player {winner}")
        last_scorer = winner  # Track who scored
        round_continues = scoreboard.add_point(winner)
        if round_continues:
            # Reset ball for next point - ball appears on the LOSER's side
            scoring.reset_ball_for_serve(ballConfig, last_scorer)  # Pass the scorer
            scoring.reset_paddle_states()
            waiting_for_serve = True
            serve_timer = 30
        continue
    
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
            if ball.get_velocity()[0] <= 0:
                ball.bounce(1, paddle1.swingAngle)
                ball.impulse((paddle1.velocity[0] * 0.01 * dt / 1000, paddle1.velocity[1] * 0.1 * dt / 1000, 0))
                ball.multiplyVelocity(1 + (ballConfig['paddle_hit_boost'] * paddle1.smashPower))
                paddle1.has_hit_ball = True
                if chosen_card and chosen_card.is_Passive:
                    chosen_card.activate(ball=ball, paddle1=paddle1, paddle2=paddle2, shadow_balls=shadow_balls)
                if abs(ball.get_velocity()[0]) >= ballConfig['Max_Speed'] * 0.7:
                    paddle1.position = (paddle1.position[0] - 30, paddle1.position[1])
                    
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
                    
        ball.clamp_velocity()
        
        # Update ball physics - ONLY when game is active (not waiting for serve)
        ball.update_position()
    
    draw_table()

    paddle1.draw(screen=screen)
    paddle2.draw(screen=screen)

    ball.draw(screen=screen)

    for shadow in shadow_balls[:]:
        shadow.draw(screen=screen)
        if shadow.get_height() <= 0:
            shadow_balls.remove(shadow)
    
    # Draw scoreboard
    scoreboard.draw()

    pygame.display.flip()

pygame.quit()
sys.exit()