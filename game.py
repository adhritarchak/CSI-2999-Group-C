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

    paddle1.process_keys(keys, dt)
    paddle2.process_keys(keys, dt)

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