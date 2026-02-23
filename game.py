import pygame
import sys
from Pong import *

pygame.init()

# Window Constants
Width = 1000
Height = 600
FPS = 60
screen = pygame.display.set_mode((Width, Height))
pygame.display.set_caption("Supreme Pong")
clock = pygame.time.Clock()

# Table Layout/Dimensions
Table_Margin = 80
Table_Border = 5
Net_Thickness = 4
Midline_Thickness = 3

Table_Rect = pygame.Rect(Table_Margin, Table_Margin,
                         Width - Table_Margin * 2,
                         Height - Table_Margin * 2,)

Left_Boundary = Table_Rect.left
Right_Boundary = Table_Rect.right
Top_Boundary = Table_Rect.top
Bot_Boundary = Table_Rect.bottom
Center_x = Table_Rect.centerx
Center_y = Table_Rect.centery

# Paddle Constants
Paddle_Speed = 5
Paddle_Boost = 1.4
Paddle_Width = 20
Paddle_Height = 80


#sample paddles
paddle1_x = Left_Boundary + 50
paddle1_y = Center_y - Paddle_Height // 2

paddle2_x = Right_Boundary - 50 - Paddle_Width
paddle2_y = Center_y - Paddle_Height // 2

paddle1 = PongPaddle(width=Paddle_Width, height=Paddle_Height, color = PADDLE1_COLOR, 
                     initialPos=(paddle1_x, paddle1_y), speed=Paddle_Speed)
paddle2 = PongPaddle(width=Paddle_Width, height=Paddle_Height, color=PADDLE2_COLOR, 
                     initialPos=(paddle2_x, paddle2_y), speed=Paddle_Speed)

paddle1.setBounds(Top_Boundary, Bot_Boundary, Left_Boundary, Right_Boundary)
paddle2.setBounds(Top_Boundary, Bot_Boundary, Left_Boundary, Right_Boundary)

paddle1.setKeys(pygame.K_w, pygame.K_s, pygame.K_a, pygame.K_d)
paddle2.setKeys(pygame.K_UP, pygame.K_DOWN, pygame.K_LEFT, pygame.K_RIGHT)

def draw_table():
    # Background
    screen.fill(LIGHT_BROWN)
    shadow = Table_Rect.move(6, 6)
    pygame.draw.rect(screen, BLACK, shadow, border_radius=6)
    pygame.draw.rect(screen, RED_TABLE, Table_Rect)

    # Table border
    pygame.draw.rect(screen, WHITE, Table_Rect, Table_Border)

    # PingPong Net
    pygame.draw.line(
        screen, WHITE,
        (Table_Rect.centerx, Table_Rect.top),
        (Table_Rect.centerx, Table_Rect.bottom),
        Net_Thickness
    )

    # Center horizontal line
    pygame.draw.line(
        screen, WHITE,
        (Table_Rect.left, Table_Rect.centery),
        (Table_Rect.right, Table_Rect.centery),
        Midline_Thickness
    )

ball = Ball(x=100, y=300, height=50, speed_x=2, speed_y=1.2, radius=8)
ball.set_bounds(top=Top_Boundary, bottom=Bot_Boundary, left=Left_Boundary, right=Right_Boundary)

# actual game
running = True
while running: 
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    keys = pygame.key.get_pressed()

    paddle1.process_keys(keys)
    paddle2.process_keys(keys)

    if ball.height() < 15 and ball.within_rect(paddle1.get_rect(), paddle1.position) and ball.heightVelo() < 0:
        ball.bounce(1, 0)
        ball.impulse((paddle1.velocity[X] * 0.5, paddle1.velocity[Y] * 0.5))
    if ball.height() < 15 and ball.within_rect(paddle2.get_rect(), paddle2.position) and ball.heightVelo() < 0:
        ball.bounce(-1, 0)
        ball.impulse((paddle2.velocity[X] * 0.5, paddle2.velocity[Y] * 0.5))

    draw_table()

    paddle1.draw(screen)
    paddle2.draw(screen)

    ball.draw(screen=screen)
    pygame.display.flip()
    clock.tick(FPS)

pygame.quit()
sys.exit()