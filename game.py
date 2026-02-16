import pygame
import sys
from Pong import *

pygame.init()

# random constants

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

# Ball Constants
Ball_Radius = 10
Ball_Max_Height = 25

# Ball Physics Constants
ball_init_vel_x = 3
ball_init_vel_y = 1.5
ball_init_vel_z = 8
Gravity = 0.35
BounceSpeedLost = 0.85
Max_Speed = 8
Bounce_MinZ = 8
paddle_hit_boost = 1

ball_x = Width // 2
ball_y = Height // 2
ball_vel_x = 1
ball_vel_y = 0.8
ball_height = 0
ball_vel_z = 0



# colors constants
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED_TABLE = (170, 40, 40)
LIGHT_BROWN = (200, 170, 130)
ORANGE = (255, 165, 0)
SHADOW = (0, 50, 0, 100)
PADDLE1_COLOR = (255, 100, 100)
PADDLE2_COLOR = (100, 100, 255)


#sample paddles
paddle1_surface = pygame.Surface((Paddle_Width, Paddle_Height))
paddle1_surface.fill((PADDLE1_COLOR))
pygame.draw.rect(paddle1_surface, WHITE, (0, 0, Paddle_Width, Paddle_Height), 2)

paddle2_surface = pygame.Surface((Paddle_Width, Paddle_Height))
paddle2_surface.fill((PADDLE2_COLOR))
pygame.draw.rect(paddle2_surface, WHITE, (0, 0, Paddle_Width, Paddle_Height), 2)

paddle1_x = Left_Boundary + 50
paddle1_y = Center_y - Paddle_Height // 2

paddle2_x = Right_Boundary - 50 - Paddle_Width
paddle2_y = Center_y - Paddle_Height // 2

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

    # paddle 1 movement (WASD)
    if keys[pygame.K_w] and paddle1_y > Top_Boundary:
        paddle1_y -= Paddle_Speed
    if keys[pygame.K_s] and paddle1_y + 80 < Bot_Boundary:
        paddle1_y += Paddle_Speed
    if keys[pygame.K_a] and paddle1_x > Left_Boundary:
        paddle1_x -= Paddle_Speed
    if keys[pygame.K_d] and paddle1_x + 20 < Center_x:
        paddle1_x += Paddle_Speed

    # paddle 2 movement (arrow keys)
    if keys[pygame.K_UP] and paddle2_y > Top_Boundary:
        paddle2_y -= Paddle_Speed
    if keys[pygame.K_DOWN] and paddle2_y + 80 < Bot_Boundary:
        paddle2_y += Paddle_Speed
    if keys[pygame.K_LEFT] and paddle2_x > Center_x:
        paddle2_x -= Paddle_Speed
    if keys[pygame.K_RIGHT] and paddle2_x + 20 < Right_Boundary:
        paddle2_x += Paddle_Speed

    if ball.height() < 15 and ball.within_rect(paddle1_surface.get_rect(), paddle1_x, paddle1_y):
        ball.bounce(1, 0)
    if ball.height() < 15 and ball.within_rect(paddle2_surface.get_rect(), paddle2_x, paddle2_y):
        ball.bounce(-1, 0)

    draw_table()

    screen.blit(paddle1_surface, (paddle1_x, paddle1_y))
    screen.blit(paddle2_surface, (paddle2_x, paddle2_y))

    ball.draw(screen=screen)
    pygame.display.flip()
    clock.tick(FPS)

pygame.quit()
sys.exit()
