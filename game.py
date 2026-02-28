import pygame
import sys
from Pong import *
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

# Paddle Constants
# Old HEAD code (commented out):
# Paddle_Boost = 1.4
# Paddle_Width = 20
# Paddle_Height = 80
# BasePaddleSpeed = 5
# CurrentPaddle1Speed = BasePaddleSpeed
# CurrentPaddle2Speed = BasePaddleSpeed
# SmashChargeSpeed = 1.5
# Smash_start_time = 0

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

paddle1.setBounds(Top_Boundary, Bot_Boundary, Left_Boundary, Right_Boundary)
paddle2.setBounds(Top_Boundary, Bot_Boundary, Left_Boundary, Right_Boundary)

paddle1.setKeys(pygame.K_w, pygame.K_s, pygame.K_a, pygame.K_d, pygame.K_q, pygame.K_e)
paddle2.setKeys(pygame.K_UP, pygame.K_DOWN, pygame.K_LEFT, pygame.K_RIGHT, pygame.K_COMMA, pygame.K_PERIOD)

paddle1.setSwingConfig(paddleConfig['SwingBackTime'], paddleConfig['SwingForwardTime'], paddleConfig['SmashHoldtime'], paddleConfig['CooldownTime'])
paddle2.setSwingConfig(paddleConfig['SwingBackTime'], paddleConfig['SwingForwardTime'], paddleConfig['SmashHoldtime'], paddleConfig['CooldownTime'])

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

ball = Ball(x=ballConfig['init_x'], y=ballConfig['init_y'], height=ballConfig['init_height'],
             speed_x=ballConfig['init_vel_x'], speed_y=ballConfig['init_vel_y'], 
             radius=ballConfig['Radius'], max_velocity=ballConfig['Max_Speed'])
ball.set_bounds(top=Top_Boundary, bottom=Bot_Boundary, left=Left_Boundary, right=Right_Boundary)

ball.do_draw_prediction(screenConfig['View_Debug'])
paddle1.viewDebugInfo(screenConfig['View_Debug'])
paddle2.viewDebugInfo(screenConfig['View_Debug'])

# actual game
running = True
while running: 
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
            continue
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_c:  # Press C to open cards
                chosen_card = draw_random_card(screen, font)
                if chosen_card:
                    print("You picked: ", chosen_card.name)
            if event.key == pygame.K_z and chosen_card is not None: # Press Z to activate the chosen card effect
                    ball_data = { ##place holder
                    'x': ballConfig['init_x'],
                    'y': ballConfig['init_y'],
                    'vel_x': ballConfig['init_vel_x'],
                    'vel_y': ballConfig['init_vel_y'],
                    'vel_z': ballConfig['init_vel_z'],
                    'height': ballConfig['init_height'],
                    'radius': ballConfig['Radius']
                         }
                    chosen_card.activate(data=ball_data) # place holder for data, once we figure out which actual ball data we need I'll make it
                    print("Activated card effect:", chosen_card.name)
                    chosen_card = None  # Clear the chosen card after activation

    dt = clock.tick(screenConfig['FPS'])
    keys = pygame.key.get_pressed()
    
    # Old HEAD code (commented out):
    # #CurrentPaddle1Speed = SmashPaddle1Speed if Smash1_active else BasePaddleSpeed
    # #CurrentPaddle2Speed = SmashPaddle2Speed if Smash2_active else BasePaddleSpeed       
    # # paddle 1 movement (WASD)
    # if keys[pygame.K_w] and paddle1_y > Top_Boundary:
    #     paddle1_y -= CurrentPaddle1Speed * (dt / 16.67)
    # if keys[pygame.K_s] and paddle1_y + 80 < Bot_Boundary:
    #     paddle1_y += CurrentPaddle1Speed * (dt / 16.67)
    # if keys[pygame.K_a] and paddle1_x > Left_Boundary:
    #     paddle1_x -= CurrentPaddle1Speed * (dt / 16.67)
    # if keys[pygame.K_d] and paddle1_x + 20 < Center_x:
    #     paddle1_x += CurrentPaddle1Speed * (dt / 16.67)
    # if keys[pygame.K_SPACE]: # regular
    #     if paddle1_x < ball_x < paddle1_x + 20 and paddle1_y < ball_y < paddle1_y + 80:
    #         ball_vel_x += 3 
    # if keys[pygame.K_LSHIFT]: #smash
    #     Smash1_hold_time += dt
    #     CurrentPaddle1Speed = BasePaddleSpeed * 0.5
    #     if Smash1_hold_time >= 3000 and not Smash1_active:
    #         Smash1_active = True
    #         Smash1_start_time = pygame.time.get_ticks()
    #         CurrentPaddle1Speed = BasePaddleSpeed * 0.3
    #         Smash1_hit = False
    # if keys[pygame.K_LSHIFT] == False and Smash1_active:
    #         if not Smash1_hit:
    #             Smash1_active = False
    #             Smash1_hold_time = 0
    #             CurrentPaddle1Speed = BasePaddleSpeed
    # if Smash1_active == True and paddle1_x < ball_x < paddle1_x + 20 and paddle1_y < ball_y < paddle1_y + 80:
    #     ball_vel_x = min(abs(ball_vel_x) + 10, Max_Speed)
    #     Smash1_hit = True
    #     CurrentPaddle1Speed = BasePaddleSpeed * 0.2
    #     Smash1_hold_time = 0
    #     Smash1_hit_time = pygame.time.get_ticks()
    #         
    # if Smash1_hit:
    #     if pygame.time.get_ticks() - Smash1_hit_time >= 3000:  # 3 seconds recovery time
    #         CurrentPaddle1Speed = BasePaddleSpeed
    #         Smash1_hit = False

    paddle1.process_keys(keys, dt)
    paddle2.process_keys(keys, dt)

    # Old HEAD code (commented out):
    # # paddle 2 movement (arrow keys)
    # if keys[pygame.K_UP] and paddle2_y > Top_Boundary:
    #     paddle2_y -= CurrentPaddle2Speed * (dt / 16.67)
    # if keys[pygame.K_DOWN] and paddle2_y + 80 < Bot_Boundary:
    #     paddle2_y += CurrentPaddle2Speed * (dt / 16.67)
    # if keys[pygame.K_LEFT] and paddle2_x > Center_x:
    #     paddle2_x -= CurrentPaddle2Speed * (dt / 16.67)
    # if keys[pygame.K_RIGHT] and paddle2_x + 20 < Right_Boundary:
    #     paddle2_x += CurrentPaddle2Speed * (dt / 16.67)
    # if keys[pygame.K_RETURN]: # regular
    #     if paddle2_x < ball_x < paddle2_x + 20 and paddle2_y < ball_y < paddle2_y + 80:
    #         ball_vel_x -= 3 
    # if keys[pygame.K_RSHIFT]: #smash
    #      Smash2_hold_time += dt
    #      CurrentPaddle2Speed = BasePaddleSpeed * 0.5
    #      if Smash2_hold_time >= 3000 and not Smash2_active:
    #         Smash2_active = True
    #         Smash2_start_time = pygame.time.get_ticks()
    #         CurrentPaddle2Speed = BasePaddleSpeed * 0.3
    #         Smash2_hit = False
    # if keys[pygame.K_RSHIFT] == False and Smash2_active:
    #         if not Smash2_hit:
    #             Smash2_active = False
    #             Smash2_hold_time = 0
    #             CurrentPaddle2Speed = BasePaddleSpeed
    # if Smash2_active == True and paddle2_x < ball_x < paddle2_x + 20 and paddle2_y < ball_y < paddle2_y + 80:
    #     ball_vel_x = max(-(abs(ball_vel_x) + 10), -Max_Speed)
    #     Smash2_hit = True
    #     CurrentPaddle2Speed = BasePaddleSpeed * 0.2
    #     Smash2_hold_time = 0
    #     Smash2_hit_time = pygame.time.get_ticks()
    #         
    # if Smash2_hit:
    #     if pygame.time.get_ticks() - Smash2_hit_time >= 2000:  # 2 seconds recovery time
    #         CurrentPaddle2Speed = BasePaddleSpeed
    #         Smash1_hit = False
    # # Trying to make a ball
    # ball_vel_z -= Gravity
    # ball_height += ball_vel_z
    
    paddle1.process_swing(dt)
    paddle2.process_swing(dt)

    paddle1.process_smash(dt)
    paddle2.process_smash(dt)

    if ball.within_rect(paddle1.get_hitbox(), (0, 0)) and paddle1.can_hit_ball:
        ball.bounce(1, paddle1.swingAngle)
        ball.impulse((paddle1.velocity[X] * 0.01 * dt / 1000, paddle1.velocity[Y] * 0.1 * dt / 1000))
        ball.multiplyVelocity(1 + (ballConfig['paddle_hit_boost'] * paddle1.smashPower))
        paddle1.has_hit_ball = True # Prevent multiple hits in one swing
    if ball.within_rect(paddle2.get_hitbox(), (0, 0)) and paddle2.can_hit_ball:
        ball.bounce(-1, paddle2.swingAngle)
        ball.impulse((paddle2.velocity[X] * 0.01 * dt / 1000, paddle2.velocity[Y] * 0.1 * dt / 1000))
        ball.multiplyVelocity(1 + (ballConfig['paddle_hit_boost'] * paddle2.smashPower))
        paddle2.has_hit_ball = True # Prevent multiple hits in one swing
    ball.clamp_velocity()

    draw_table()

    paddle1.draw(screen=screen)
    paddle2.draw(screen=screen)

    ball.draw(screen=screen)
    pygame.display.flip()

pygame.quit()
sys.exit()