import pygame
import sys
from Pong import *
pygame.init()

with open('config.json') as f:
    config = json.load(f)
    screenConfig = config['Window']
    tableConfig = config['Table Layout']
    paddleConfig = config['Paddle Physics']
    ballConfig = config['Ball Physics']
    colorConfig = config['colors']

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

#sample paddles
paddle1_x = Left_Boundary + 50
paddle1_y = Center_y - paddleConfig['Paddle_Height'] // 2

paddle2_x = Right_Boundary - 50 - paddleConfig['Paddle_Width']
paddle2_y = Center_y - paddleConfig['Paddle_Height'] // 2

paddle1 = PongPaddle(width=paddleConfig['Paddle_Width'], height=paddleConfig['Paddle_Height'], color = colorConfig['Paddle 1'], 
                     initialPos=(paddle1_x, paddle1_y), speed=paddleConfig['BasePaddleSpeed'])
paddle2 = PongPaddle(width=paddleConfig['Paddle_Width'], height=paddleConfig['Paddle_Height'], color=colorConfig['Paddle 2'], 
                     initialPos=(paddle2_x, paddle2_y), speed=paddleConfig['BasePaddleSpeed'])

paddle1.setBounds(Top_Boundary, Bot_Boundary, Left_Boundary, Right_Boundary)
paddle2.setBounds(Top_Boundary, Bot_Boundary, Left_Boundary, Right_Boundary)

paddle1.setKeys(pygame.K_w, pygame.K_s, pygame.K_a, pygame.K_d)
paddle2.setKeys(pygame.K_UP, pygame.K_DOWN, pygame.K_LEFT, pygame.K_RIGHT)

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
             speed_x=ballConfig['init_vel_x'], speed_y=ballConfig['init_vel_y'], radius=ballConfig['Radius'])
ball.set_bounds(top=Top_Boundary, bottom=Bot_Boundary, left=Left_Boundary, right=Right_Boundary)

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

    paddle1.process_keys(keys)
    paddle2.process_keys(keys)

    if ball.height() < 15 and ball.within_rect(paddle1.get_rect(), paddle1.position) and ball.heightVelo() < 0:
        ball.bounce(1, 0)
        ball.impulse((paddle1.velocity[X] * 0.5, paddle1.velocity[Y] * 0.5))
    if ball.height() < 15 and ball.within_rect(paddle2.get_rect(), paddle2.position) and ball.heightVelo() < 0:
        ball.bounce(-1, 0)
        ball.impulse((paddle2.velocity[X] * 0.5, paddle2.velocity[Y] * 0.5))
    CurrentPaddle1Speed = paddleConfig['SmashPaddle1Speed'] if Smash1_active else paddleConfig['BasePaddleSpeed']
    CurrentPaddle2Speed = paddleConfig['SmashPaddle2Speed'] if Smash2_active else paddleConfig['BasePaddleSpeed']       
    
    
    #elif Smash1_active and not (paddle1_x < ballConfig['init_x'] < paddle1_x + 20 and paddle1_y < ballConfig['init_y'] < paddle1_y + 80):
       #Smash1_hit = False

    # paddle 2 movement (arrow keys)
    if keys[pygame.K_RETURN]: # regular
        if paddle2_x < ballConfig['init_x'] < paddle2_x + 20 and paddle2_y < ballConfig['init_y'] < paddle2_y + 80:
            ballConfig['init_vel_x'] -= 3 
    if keys[pygame.K_RSHIFT]: #smash
        Smash2_hold_time += dt
    if Smash2_hold_time >= 3000 and not Smash2_active:
            Smash2_active = True
            Smash2_start_time = pygame.time.get_ticks()
            CurrentPaddle2Speed = paddleConfig['SmashPaddle2Speed']
            Smash2_hit = False
    if Smash2_active == True:
            if paddle2_x < ballConfig['init_x'] < paddle2_x + 20 and paddle2_y < ballConfig['init_y'] < paddle2_y + 80:
                ballConfig['init_vel_x'] += 5
                Smash2_hit = True
    if Smash2_active and pygame.time.get_ticks() - Smash2_start_time >= Smash_duration:
            Smash2_active = False
            Smash2_hold_time = 0
            CurrentPaddle2Speed = paddleConfig['BasePaddleSpeed'] 
            Smash2_hit = False

    draw_table()

    ball.draw(screen=screen)
    pygame.display.flip()

pygame.quit()
sys.exit()